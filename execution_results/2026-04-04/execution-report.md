# 2026-04-04 Skill Execution Report

*Executed at: 2026-04-04T18:16:10.218631*

## 1. [MCP] Context7 MCP로 최신 라이브러리 문서를 컨텍스트에 주입해 환각 제거

**추천 이유:** Playwright 셀렉터 변경, Claude Agent SDK query() 키워드 인자 등 이 프로젝트가 의존하는 라이브러리의 최신 API를 컨텍스트에 자동 주입해 환각과 버그를 예방할 수 있음

**실행 프롬프트:**
```
# Context7 최신 문서 주입 Skill

TRIGGER: 사용자가 외부 라이브러리/프레임워크 코드를 작성하거나 API 사용법을 물을 때

## Instructions
1. 사용 중인 라이브러리를 식별한다 (Playwright, Claude Agent SDK, APScheduler 등)
2. Context7 MCP 서버의 resolve-library-id 도구로 라이브러리 ID를 조회한다
3. get-library-docs 도구로 해당 라이브러리의 최신 문서를 가져온다
4. 가져온 문서를 기반으로 코드를 작성하거나 답변한다
5. 문서에 명시된 API 시그니처와 실제 코드가 일치하는지 반드시 검증한다

## Gotchas
- Context7이 반환하는 문서가 너무 길면 topic 파라미터로 범위를 좁혀라
- 라이브러리 버전이 프로젝트의 pyproject.toml/requirements와 일치하는지 확인
```

**실행 결과:**

파일 쓰기 권한이 필요합니다. 승인해 주시면 계속 진행하겠습니다. 일단 결과를 마크다운으로 정리해 드리겠습니다.

---

# Context7 MCP 최신 문서 주입 Skill — 적용 결과

## 1. 적용 개요

| 항목 | 내용 |
|------|------|
| **Skill 이름** | Context7 최신 문서 주입 |
| **목적** | 외부 라이브러리 API 사용 시 최신 공식 문서를 컨텍스트에 주입하여 환각(hallucination) 제거 |
| **대상 라이브러리** | Playwright, Claude Agent SDK, FastMCP, schedule |
| **MCP 서버** | `@upstash/context7-mcp` (npx 기반) |

## 2. 필요한 설정 변경 (3개 파일)

### 2-1. `.mcp.json` (프로젝트 루트에 생성 — 수동 필요)

> ⚠️ 민감 파일이므로 자동 생성이 차단되었습니다. 아래 내용을 직접 생성해 주세요.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "description": "Context7 - 최신 라이브러리 문서를 컨텍스트에 주입하여 환각 제거"
    },
    "linkedin-tips": {
      "command": "uv",
      "args": ["run", "python", "-m", "mcp_server.server"],
      "description": "LinkedIn Claude Code 팁 조회 MCP 서버"
    }
  }
}
```

### 2-2. `CLAUDE.md` — MCP 서버 섹션 업데이트 (승인 대기)

기존 `## MCP 서버` 섹션을 아래로 교체:

```markdown
## MCP 서버

### linkedin-tips (프로젝트 전용)
# 사용 가능한 도구: get_latest_tips, get_tips_by_date, get_tips_by_category, search_tips, generate_skill, list_available_dates

### Context7 (최신 라이브러리 문서 주입)
- 외부 라이브러리 코드를 작성할 때 Context7 MCP로 최신 문서를 가져와 환각을 제거한다
- 사용 가능한 도구: `resolve-library-id` (라이브러리 검색), `get-library-docs` (문서 가져오기)
- 프로젝트 핵심 라이브러리 매핑:
  - Playwright → `/playwright/playwright-python`
  - FastMCP → `/jlowin/fastmcp`
  - schedule → `/dbader/schedule`
  - Claude Agent SDK → `resolve-library-id`로 조회 필요
- 문서가 너무 길면 `topic` 파라미터로 범위를 좁혀라
- 가져온 문서의 API 시그니처와 실제 코드가 일치하는지 반드시 검증한다
```

## 3. 프로젝트 라이브러리 ↔ Context7 ID 매핑

| pyproject.toml 의존성 | Context7 Library ID | topic 예시 |
|----------------------|---------------------|------------|
| `playwright` | `/playwright/playwright-python` | `page.goto`, `selectors`, `browser context` |
| `mcp[cli]` (FastMCP) | `/jlowin/fastmcp` | `@mcp.tool`, `FastMCP server` |
| `schedule` | `/dbader/schedule` | `every().day.at()`, `run_pending` |
| `claude-agent-sdk` | 조회 필요 (`resolve-library-id`) | `query`, `agent`, `prompt` |
| `python-dotenv` | `/theskumar/python-dotenv` | `load_dotenv`, `dotenv_values` |

## 4. 사용 워크플로우

```
사용자: "Playwright에서 새 탭으로 URL을 열려면?"

Claude Code 내부 동작:
  1️⃣ 라이브러리 식별 → Playwright
  2️⃣ resolve-library-id("playwright python") → /playwright/playwright-python
  3️⃣ get-library-docs(libraryId="/playwright/playwright-python", topic="new tab page")
  4️⃣ 반환된 공식 문서 기반으로 코드 작성
  5️⃣ API 시그니처 검증 (문서 vs 코드 일치 확인)
```

## 5. Gotchas (주의사항)

| 주의 | 설명 |
|------|------|
| **버전 불일치** | Context7가 반환하는 문서는 최신 버전 기준. `pyproject.toml`의 버전 고정 여부 확인 |
| **문서 과다** | `topic` 파라미터 없이 호출하면 토큰 초과 가능 → 반드시 topic으로 범위 한정 |
| **Claude Agent SDK** | 비공개/신규 라이브러리라 Context7에 없을 수 있음 → `CLAUDE.md`의 규칙 우선 적용 |
| **네트워크 필요** | Context7는 온라인 API → 오프라인 환경에서는 동작 불가 |

## 6. 남은 작업 (수동)

- [ ] `.mcp.json` 파일을 프로젝트 루트에 직접 생성 (위 2-1 내용)
- [ ] Claude Code 재시작하여 Context7 MCP 서버 로드 확인
- [ ] `CLAUDE.md` 편집 승인 (파일 쓰기 권한 허용 후 재시도)

---

## 2. [Agent] cmux·figaro·claude-squad로 Claude 에이전트 병렬 실행 및 오케스트레이션

**추천 이유:** 키워드별 LinkedIn 크롤링 + Claude 분석 + 마켓플레이스 publish를 독립 에이전트로 분리해 병렬 실행하면 daily_job 전체 소요 시간을 대폭 단축할 수 있음

**실행 프롬프트:**
```
# 멀티 에이전트 병렬 실행 Skill

TRIGGER: 사용자가 대규모 리팩토링, 다중 파일 동시 수정, 또는 독립적인 여러 태스크를 병렬로 처리하고 싶을 때

## Instructions
1. 태스크를 독립 단위로 분해한다 (예: 키워드별 크롤링, 분석, skill 생성, publish)
2. 각 단위를 별도 Agent(worktree 격리)로 위임한다
3. 의존성이 없는 태스크는 반드시 동시에 launch한다
4. 모든 에이전트 완료 후 결과를 병합하고 충돌을 해소한다

## Gotchas
- LinkedIn 크롤링 에이전트는 rate-limit 때문에 완전 병렬이 아닌 세마포어(동시 2~3개)로 제한
- 각 에이전트에 .env 경로와 쿠키 경로를 명시적으로 전달해야 함
- worktree 간 data/ 디렉터리 충돌 방지를 위해 파일명에 키워드 prefix 부여
```

**실행 결과:**

파일 쓰기 권한이 계속 차단되고 있습니다. 대신 전체 구현 코드와 적용 방법을 마크다운으로 정리해서 드리겠습니다.

---

# 멀티 에이전트 병렬 실행 Skill 적용 결과

## 1. 아키텍처 개요

현재 파이프라인은 **7단계 순차 실행** 구조입니다. 이를 **4-Phase 병렬 오케스트레이션**으로 전환합니다.

```
[현재] 순차 실행 (직렬)
─────────────────────────────────────────────────────────
KW1 크롤링 → KW2 → KW3 → 분석1 → 분석2 → ... → 리포트 → Skill → Publish

[변경 후] 병렬 오케스트레이션
─────────────────────────────────────────────────────────
Phase 1 (Sem=2)    Phase 2 (Sem=5)     Phase 3 (병렬)      Phase 4
┌─ KW1 크롤링 ─┐   ┌─ 분석1 ─┐          ┌─ 리포트 ──┐
├─ KW2 크롤링 ─┤   ├─ 분석2 ─┤          │           │
│  (KW3 대기)  │   ├─ 분석3 ─┤    →     ├─ Skill   ─┤  →  Publish
└──────────────┘   ├─ 분석4 ─┤          │  실행     │     (순차)
     병합+중복제거   ├─ 분석5 ─┤          └───────────┘
                   └─────────┘
```

## 2. 새 파일: `scraper/orchestrator.py`

```python
"""
멀티 태스크 병렬 오케스트레이터

파이프라인의 독립 단위를 세마포어 기반으로 병렬 실행한다.
- 크롤링: 키워드별 동시 2개 (LinkedIn rate-limit 대응)
- 분석: 게시글별 동시 5개 (Claude API 호출)
- 리포트 생성 + Skill 실행: 동시 진행
- Publish: 마지막 순차 실행 (git 충돌 방지)
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 세마포어 설정 (환경 변수로 오버라이드 가능)
SCRAPE_CONCURRENCY = int(os.getenv("SCRAPE_CONCURRENCY", "2"))
ANALYZE_CONCURRENCY = int(os.getenv("ANALYZE_CONCURRENCY", "5"))


class PipelineOrchestrator:
    """병렬 파이프라인 오케스트레이터"""

    def __init__(self, keywords: list[str], date: str | None = None):
        self.keywords = keywords
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self._scrape_sem = asyncio.Semaphore(SCRAPE_CONCURRENCY)
        self._analyze_sem = asyncio.Semaphore(ANALYZE_CONCURRENCY)
        self._results: dict[str, Any] = {}

    # ── Phase 1: 병렬 크롤링 ──

    async def _scrape_keyword(self, keyword: str) -> list[dict]:
        """세마포어로 제한된 단일 키워드 크롤링"""
        async with self._scrape_sem:
            from scraper.linkedin_scraper import LinkedInScraper
            print(f"  [크롤링 시작] '{keyword}' (동시 최대 {SCRAPE_CONCURRENCY}개)")
            scraper = LinkedInScraper()
            posts = await scraper.search_posts(keyword)
            print(f"  [크롤링 완료] '{keyword}' -> {len(posts)}개")
            await asyncio.sleep(3)  # rate-limit 딜레이
            return posts

    async def phase_scrape(self) -> list[dict]:
        """모든 키워드를 병렬 크롤링 (세마포어 제한)"""
        print(f"\n[Phase 1] 병렬 크롤링 (동시 {SCRAPE_CONCURRENCY}개)")
        tasks = [self._scrape_keyword(kw) for kw in self.keywords]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 결과 병합 + 중복 제거
        all_posts: dict[str, dict] = {}
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"  [!] '{self.keywords[i]}' 실패: {result}")
                continue
            for post in result:
                key = post.get("post_id", "") or post.get("content", "")[:100]
                if key and key not in all_posts:
                    all_posts[key] = post

        posts = list(all_posts.values())
        print(f"[Phase 1 완료] {len(posts)}개 고유 게시글")
        return posts

    # ── Phase 2: 병렬 분석 ──

    async def _analyze_single(self, index: int, post: dict) -> dict:
        async with self._analyze_sem:
            from scraper.analyzer import analyze_post
            author = post.get("author", {}).get("name", "?")
            print(f"    [분석 {index+1}] {author[:20]}...")
            analysis = await analyze_post(post)
            return {**post, "analysis": analysis}

    async def phase_analyze(self, posts: list[dict]) -> list[dict]:
        print(f"\n[Phase 2] 병렬 분석 (동시 {ANALYZE_CONCURRENCY}개, 총 {len(posts)}개)")
        if not posts:
            return []

        tasks = [self._analyze_single(i, p) for i, p in enumerate(posts)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        analyzed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"    [!] 분석 {i+1} 실패: {result}")
                analyzed.append({**posts[i], "analysis": {
                    "is_relevant": False, "categories": [],
                    "tips": [], "summary": f"분석 오류: {result}"
                }})
            else:
                analyzed.append(result)
        return analyzed

    # ── Phase 3: 리포트 + Skill 실행 (동시) ──

    async def _generate_report(self, posts):
        from scraper.reporter import generate_report
        return generate_report(self.date, posts)

    async def _execute_skills(self, posts):
        from scraper.skill_executor import recommend_and_execute
        return await recommend_and_execute(self.date, posts)

    async def phase_report_and_skills(self, posts):
        print(f"\n[Phase 3] 리포트 + Skill 실행 (병렬)")
        report_task = asyncio.create_task(self._generate_report(posts))
        skill_task = asyncio.create_task(self._execute_skills(posts))
        report_path, exec_path = await asyncio.gather(
            report_task, skill_task, return_exceptions=True
        )
        if isinstance(report_path, Exception):
            print(f"  [!] 리포트 실패: {report_path}"); report_path = None
        if isinstance(exec_path, Exception):
            print(f"  [!] Skill 실패: {exec_path}"); exec_path = None
        return report_path, exec_path

    # ── Phase 4: Publish (순차) ──

    async def phase_publish(self) -> dict:
        print(f"\n[Phase 4] 마켓플레이스 publish")
        from scraper.publisher import publish_skills
        return publish_skills(self.date)

    # ── 전체 실행 ──

    async def run(self, previous_contents: set[str] | None = None) -> dict:
        start = datetime.now()
        print(f"\n{'='*60}")
        print(f"[오케스트레이터] {self.date} | 크롤링x{SCRAPE_CONCURRENCY} 분석x{ANALYZE_CONCURRENCY}")
        print(f"{'='*60}")

        raw_posts = await self.phase_scrape()

        if previous_contents:
            before = len(raw_posts)
            raw_posts = [p for p in raw_posts if p.get("content","")[:100] not in previous_contents]
            if (d := before - len(raw_posts)):
                print(f"[중복 제거] {d}개 -> {len(raw_posts)}개 신규")

        analyzed = await self.phase_analyze(raw_posts)
        report_path, exec_path = await self.phase_report_and_skills(analyzed)
        pub = await self.phase_publish()

        from scraper.analyzer import build_daily_summary
        summary = build_daily_summary(analyzed)
        elapsed = (datetime.now() - start).total_seconds()

        print(f"\n[완료] {elapsed:.1f}초 | 수집:{summary['total_posts_scraped']} "
              f"관련:{summary['relevant_posts']} 팁:{summary['tips_extracted']}")

        return {
            "date": self.date, "elapsed_seconds": elapsed,
            "posts": analyzed, "daily_summary": summary,
            "report_path": str(report_path) if report_path else None,
            "exec_path": str(exec_path) if exec_path else None,
            "publish_result": pub,
        }
```

## 3. 변경 파일: `scheduler/daily_job.py`

`run_daily_scrape()` 함수를 오케스트레이터로 교체합니다:

```python
# === 변경 부분 (기존 순차 로직 대체) ===

async def run_daily_scrape():
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = DATA_DIR / f"{today}.json"

    if output_path.exists():
        print(f"[!] {today} 데이터 이미 존재함. 덮어쓸게요.")

    print(f"\n{'='*50}")
    print(f"[시작] {datetime.now().isoformat()} 일별 스크랩 (병렬 모드)")
    print(f"{'='*50}")

    keywords = get_keywords()

    # 오케스트레이터로 병렬 실행
    from scraper.orchestrator import PipelineOrchestrator

    orchestrator = PipelineOrchestrator(keywords=keywords, date=today)
    previous_contents = load_previous_contents()
    result = await orchestrator.run(previous_contents=previous_contents)

    # JSON 저장
    output = {
        "date": today,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "query_keywords": keywords,
        "posts": result["posts"],
        "daily_summary": result["daily_summary"],
    }

    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    summary = result["daily_summary"]
    print(f"\n[완료] {output_path}")
    print(f"  - 소요: {result['elapsed_seconds']:.1f}초")
    print(f"  - 수집: {summary['total_posts_scraped']}개")
    print(f"  - 관련: {summary['relevant_posts']}개")
    print(f"  - 팁:   {summary['tips_extracted']}개")
    print(f"  - Skill 후보: {summary['skill_worthy_tips']}개")
```

## 4. 환경 변수 추가 (`.env`)

```env
# 병렬 오케스트레이터 설정
SCRAPE_CONCURRENCY=2    # LinkedIn 크롤링 동시 수 (rate-limit 대응, 최대 3)
ANALYZE_CONCURRENCY=5   # Claude API 분석 동시 수
```

## 5. 변경 요약

| 구분 | 파일 | 변경 내용 |
|------|------|----------|
| **새 파일** | `scraper/orchestrator.py` | 4-Phase 병렬 오케스트레이터 |
| **수정** | `scheduler/daily_job.py` | `run_daily_scrape()`를 오케스트레이터 호출로 교체 |
| **수정** | `.env` | `SCRAPE_CONCURRENCY`, `ANALYZE_CONCURRENCY` 추가 |
| 미변경 | `scraper/linkedin_scraper.py` | 기존 코드 그대로 (오케스트레이터가 감싸서 호출) |
| 미변경 | `scraper/analyzer.py` | `analyze_post()` 그대로 (오케스트레이터가 병렬 호출) |

## 6. 성능 개선 예상치

| 단계 | 키워드 3개 기준 (현재) | 병렬 후 | 개선율 |
|------|----------------------|---------|--------|
| 크롤링 | ~180초 (60초 x 3) | ~120초 (2개씩 동시) | **33% 단축** |
| 분석 | ~30초 (20개 x 1.5초) | ~9초 (5개씩 동시) | **70% 단축** |
| 리포트+Skill | ~15초 (순차) | ~10초 (동시) | **33% 단축** |
| **전체** | **~225초** | **~140초** | **~38% 단축** |

## 7. Gotchas (주의사항)

- **LinkedIn rate-limit**: `SCRAPE_CONCURRENCY`를 3 이상으로 올리면 계정 제한 위험. **2를 권장**
- **Playwright 브라우저**: 각 키워드마다 별도 브라우저를 열기 때문에, 동시 3개 이상이면 메모리 2GB+ 필요
- **쿠키 공유**: 현재 구조에서는 각 `LinkedInScraper` 인스턴스가 같은 쿠키 파일을 읽으므로, 동시 쓰기 충돌 가능성 있음. 읽기 전용으로 사용하고 저장은 마지막에 1회만 수행 권장
- **`.env` 경로**: 오케스트레이터는 `load_dotenv()`를 자체 호출하므로 별도 경로 전달 불필요

---

파일 쓰기 권한을 허용해 주시면 위 코드를 바로 프로젝트에 적용하겠습니다. 또는 위 코드를 직접 복사해서 파일을 생성하셔도 됩니다.

---
