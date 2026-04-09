"""LinkedIn 게시글 크롤러 (Playwright 기반)"""

import asyncio
import json
import os
import urllib.parse
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
from playwright.async_api import Page, async_playwright

load_dotenv()

COOKIES_PATH = Path(__file__).parent.parent / ".linkedin_cookies.json"


class LinkedInScraper:
    def __init__(self):
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        self.max_posts = int(os.getenv("MAX_POSTS_PER_KEYWORD", "20"))

    async def _save_cookies(self, context) -> None:
        cookies = await context.cookies()
        COOKIES_PATH.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding='utf-8')

    async def _load_cookies(self, context) -> bool:
        if not COOKIES_PATH.exists():
            return False
        cookies = json.loads(COOKIES_PATH.read_text(encoding='utf-8'))
        await context.add_cookies(cookies)
        return True

    async def _is_logged_in(self, page: Page) -> bool:
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        return "feed" in page.url and "login" not in page.url

    async def _login(self, page: Page) -> None:
        """로그인 처리 - 브라우저 창에서 직접 로그인 (Google 포함 어떤 방식이든 OK)"""
        print("[*] LinkedIn 로그인 페이지 열기...")
        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        await asyncio.sleep(1)

        print("=" * 50)
        print("[!] 브라우저 창에서 직접 LinkedIn에 로그인하세요.")
        print("    (Google 계정, 이메일/비밀번호 어떤 방식이든 OK)")
        print("    로그인 완료되면 자동으로 진행됩니다. (최대 120초 대기)")
        print("=" * 50)

        # 로그인 완료 감지: feed 페이지로 이동할 때까지 폴링
        for _ in range(120):
            await asyncio.sleep(1)
            current_url = page.url
            if any(x in current_url for x in ["feed", "mynetwork", "jobs", "messaging", "notifications"]):
                break
        else:
            print("[!] 로그인 타임아웃 (120초). 현재 URL:", page.url)
            return

        print(f"[+] 로그인 완료!")

    async def _scroll_and_collect(self, page: Page, max_posts: int) -> list[dict]:
        """피드를 스크롤하며 게시글 데이터 수집"""
        posts = []
        seen_ids = set()
        seen_contents = set()  # content 기반 중복 제거 (post_id가 없을 때 대비)
        scroll_attempts = 0
        max_scrolls = max_posts // 2 + 10

        # 1회: 어떤 셀렉터가 현재 DOM에 존재하는지 진단
        debug = await page.evaluate("""
            () => {
                const selectors = [
                    'div[data-urn^="urn:li:activity"]',
                    'div[data-id^="urn:li:activity"]',
                    '.feed-shared-update-v2',
                    '.occludable-update',
                    '[data-entity-urn*="activity"]',
                    '.search-results__list li',
                    '[data-chameleon-result-urn]',
                    '.reusable-search__result-container',
                    '[data-testid*="post"]',
                    '[data-testid*="update"]',
                    '[data-testid*="feed"]',
                    'article',
                    'li.search-content__result',
                    '[class*="search-result"]'
                ];
                const result = {};
                for (const sel of selectors) {
                    result[sel] = document.querySelectorAll(sel).length;
                }
                // data-testid 목록도 수집
                const testIds = [...new Set(
                    Array.from(document.querySelectorAll('[data-testid]'))
                        .map(el => el.getAttribute('data-testid'))
                )].slice(0, 20);
                result['__testids__'] = testIds.join(', ');
                return result;
            }
        """)
        print("    [DOM 진단] 셀렉터별 요소 수:")
        working_selector = None
        for sel, count in debug.items():
            if sel == '__testids__':
                print(f"      data-testid 목록: {count}")
                continue
            print(f"      {count:3d}개  {sel}")
            if isinstance(count, int) and count > 0 and working_selector is None:
                working_selector = sel

        if not working_selector:
            print("    [!] 매칭되는 셀렉터 없음 - 페이지 소스 일부 출력:")
            snippet = await page.evaluate("() => document.body.innerHTML.substring(0, 2000)")
            print(snippet[:500])

        while len(posts) < max_posts and scroll_attempts < max_scrolls:
            new_posts = await page.evaluate("""
                () => {
                    const results = [];

                    // expandable-text-box가 게시글 본문 (data-testid 기반)
                    const textBoxes = document.querySelectorAll('[data-testid="expandable-text-box"]');

                    for (const textBox of textBoxes) {
                        const content = textBox.innerText?.trim();
                        if (!content || content.length < 30) continue;

                        // 부모 컨테이너 탐색 (최대 10단계)
                        let container = textBox;
                        for (let i = 0; i < 10; i++) {
                            container = container.parentElement;
                            if (!container) break;
                            if (container.querySelector('a[href*="/in/"]')) break;
                        }

                        // 작성자 링크
                        const authorLink = container?.querySelector('a[href*="/in/"]');
                        const authorName = authorLink?.innerText?.trim()
                            || authorLink?.getAttribute('aria-label')
                            || '알 수 없음';

                        // 게시글 링크
                        const postLink = container?.querySelector('a[href*="/posts/"], a[href*="/feed/update/"]');

                        // 고유 ID
                        const urn = container?.getAttribute('data-urn')
                            || container?.getAttribute('data-id')
                            || postLink?.href
                            || `noid_${Date.now()}_${Math.random()}`;

                        // 좋아요 수
                        const likesEl = container?.querySelector(
                            '[aria-label*="reaction"], [aria-label*="반응"]'
                        );

                        results.push({
                            post_id: urn,
                            author: {
                                name: authorName,
                                headline: '',
                                url: authorLink?.href || ''
                            },
                            content: content,
                            url: postLink?.href || '',
                            engagement: {
                                likes: parseInt(likesEl?.innerText?.replace(/[^0-9]/g, '') || '0'),
                                comments: 0
                            }
                        });
                    }
                    return results;
                }
            """)

            newly_added = 0
            for post in new_posts:
                content_key = post["content"][:100]  # 앞 100자로 중복 판단
                if post["post_id"] not in seen_ids and content_key not in seen_contents and post["content"]:
                    seen_ids.add(post["post_id"])
                    seen_contents.add(content_key)
                    posts.append(post)
                    newly_added += 1
                    author = post["author"]["name"].encode("ascii", "replace").decode()
                    preview = post["content"][:40].replace('\n', ' ').encode("ascii", "replace").decode()
                    print(f"    [collect {len(posts):2d}] {author} - {preview}...")

            await page.evaluate("window.scrollBy(0, 1500)")
            await asyncio.sleep(2)
            scroll_attempts += 1

            if newly_added == 0 and scroll_attempts > 3:
                print(f"    스크롤 {scroll_attempts}회째 새 게시글 없음, 종료")
                break

        return posts[:max_posts]

    @staticmethod
    async def _wait_for_network(timeout: int = 120) -> None:
        """절전 모드 복귀 후 네트워크 연결 대기 (최대 timeout초)"""
        import urllib.request
        for i in range(timeout // 5):
            try:
                urllib.request.urlopen("https://www.linkedin.com", timeout=10)
                return
            except Exception:
                if i == 0:
                    print("[*] 네트워크 연결 대기 중...")
                await asyncio.sleep(5)
        raise ConnectionError(f"네트워크 연결 실패 ({timeout}초 초과)")

    async def search_posts(self, keyword: str) -> list[dict]:
        """키워드로 LinkedIn 게시글 검색 및 수집"""
        await self._wait_for_network()
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            try:
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 800},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                # 쿠키 복원 시도
                cookie_loaded = await self._load_cookies(context)
                logged_in = cookie_loaded and await self._is_logged_in(page)

                if not logged_in:
                    await self._login(page)
                    await self._save_cookies(context)

                # 검색 실행
                print(f"[*] 검색 중: '{keyword}'")
                encoded = urllib.parse.quote(keyword)
                url = f"https://www.linkedin.com/search/results/content/?keywords={encoded}&sortBy=date_posted"
                await page.goto(url, wait_until="load", timeout=30000)
                # LinkedIn React SPA 렌더링 대기 - article 또는 li 등장할 때까지
                try:
                    await page.wait_for_selector(
                        "article, li[class], [data-testid]:not([data-testid='toasts-title'])",
                        timeout=15000
                    )
                except Exception:
                    pass
                await asyncio.sleep(3)

                # 스크린샷 (디버그용)
                screenshot_path = str(Path(__file__).parent.parent / f"debug_{keyword[:10]}.png")
                await page.screenshot(path=screenshot_path)
                print(f"    스크린샷 저장: {screenshot_path}")

                # 현재 URL 확인
                print(f"    현재 URL: {page.url[:80]}")

                posts = await self._scroll_and_collect(page, self.max_posts)
                print(f"[+] '{keyword}' 결과: {len(posts)}개 수집")

                await self._save_cookies(context)
                return posts
            finally:
                await browser.close()

    async def scrape_all_keywords(self, keywords: list[str]) -> list[dict]:
        """여러 키워드 순차 검색, 중복 제거"""
        all_posts: dict[str, dict] = {}
        for keyword in keywords:
            posts = await self.search_posts(keyword)
            for post in posts:
                all_posts[post["post_id"]] = post
            await asyncio.sleep(5)  # 키워드 사이 딜레이

        return list(all_posts.values())
