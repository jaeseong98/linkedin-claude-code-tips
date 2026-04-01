"""매일 지정 시각에 LinkedIn 크롤링 + 분석 + 저장"""

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import schedule
import time

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def get_keywords() -> list[str]:
    raw = os.getenv("SEARCH_KEYWORDS", "Claude Code,MCP tips,Claude Code skills")
    return [k.strip() for k in raw.split(",") if k.strip()]


async def run_daily_scrape():
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = DATA_DIR / f"{today}.json"

    if output_path.exists():
        print(f"[!] {today} 데이터 이미 존재함. 덮어쓸게요.")

    print(f"\n{'='*50}")
    print(f"[시작] {datetime.now().isoformat()} 일별 스크랩")
    print(f"{'='*50}")

    keywords = get_keywords()
    print(f"[*] 검색 키워드: {keywords}")

    # 1. 크롤링
    from scraper.linkedin_scraper import LinkedInScraper
    scraper = LinkedInScraper()
    raw_posts = await scraper.scrape_all_keywords(keywords)
    print(f"[+] 총 {len(raw_posts)}개 게시글 수집 완료")

    # 2. Claude API 분석
    from scraper.analyzer import analyze_posts_batch, build_daily_summary
    print("[*] Claude API 분석 시작...")
    analyzed_posts = await analyze_posts_batch(raw_posts)

    # 3. 일별 요약
    daily_summary = build_daily_summary(analyzed_posts)

    # 4. JSON 저장
    output = {
        "date": today,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "query_keywords": keywords,
        "posts": analyzed_posts,
        "daily_summary": daily_summary
    }

    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\n[완료] {output_path}")
    print(f"  - 수집: {daily_summary['total_posts_scraped']}개")
    print(f"  - 관련: {daily_summary['relevant_posts']}개")
    print(f"  - 팁:   {daily_summary['tips_extracted']}개")
    print(f"  - Skill 후보: {daily_summary['skill_worthy_tips']}개")
    print(f"  - 카테고리: {daily_summary['categories']}")

    # 5. 마켓플레이스 레포에 자동 publish
    print("\n[*] 마켓플레이스 publish 중...")
    from scraper.publisher import publish_skills
    pub_result = publish_skills(today)
    if pub_result["error"]:
        print(f"  [!] publish 실패: {pub_result['error']}")
    elif pub_result["pushed"]:
        print(f"  [✓] {pub_result['copied']}개 Skills → claude-code-skills 레포 push 완료")


def job():
    asyncio.run(run_daily_scrape())


def main():
    run_time = os.getenv("DAILY_RUN_TIME", "09:00")
    print(f"[스케줄러 시작] 매일 {run_time}에 실행됩니다.")
    print("Ctrl+C로 종료")

    schedule.every().day.at(run_time).do(job)

    # 시작 시 즉시 한 번 실행하려면 아래 주석 해제
    # job()

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
