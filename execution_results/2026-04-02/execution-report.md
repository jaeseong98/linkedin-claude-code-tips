# 2026-04-02 Skill Execution Report

*Executed at: 2026-04-02T20:18:02.791646*

## 1. [Skills] 슬래시(/) 커맨드로 반복 프롬프트를 자동화하라

**추천 이유:** 매일 수집→분석→Skill 생성→publish 파이프라인이 반복되므로, /scrape /publish 같은 슬래시 커맨드로 즉시 자동화 가능

**실행 프롬프트:**
```
3회 이상 반복되는 프롬프트 흐름을 슬래시 커맨드로 등록하라. 예: /scrape → LinkedIn 크롤링 + Claude 분석 + data/ 저장, /publish → generated_skills/ 에서 마켓플레이스 레포로 복사 + git push. 각 커맨드는 .claude/commands/ 디렉터리에 .md 파일로 저장하고, 프론트매터에 description을 명시한다. 커맨드 내부에서 uv run python -m scheduler.daily_job_once 등 기존 스크립트를 호출하도록 연결한다.
```

**실행 결과:**

파일 쓰기 권한이 전혀 허용되지 않고 있습니다. **대화 상단의 권한 요청 팝업에서 "Allow" 를 클릭**해주셔야 파일을 생성할 수 있습니다.

대신, 수동으로 직접 생성하실 수 있도록 **완성된 슬래시 커맨드 파일 내용 전체**를 아래에 정리해 드리겠습니다.

---

# 📋 Skill 적용 결과: 슬래시(/) 커맨드로 반복 프롬프트 자동화

## 개요

프로젝트에서 3회 이상 반복되는 워크플로우 6개를 `.claude/commands/` 슬래시 커맨드로 등록합니다.

| 커맨드 | 설명 | 매핑 대상 |
|--------|------|-----------|
| `/scrape` | LinkedIn 크롤링 + 분석 + 저장 | `scheduler.daily_job_once` |
| `/publish` | 마켓플레이스 레포로 Skills push | `scraper.publisher` |
| `/report` | Skill 후보 리포트 생성 | `scraper.reporter` |
| `/status` | 수집 현황 대시보드 | data/ 파일 조회 |
| `/mcp-start` | MCP 서버 시작 | `mcp_server.server` |
| `/pipeline` | 전체 파이프라인 (위 전체) | `scheduler.daily_job_once` |

## 디렉터리 구조

```
.claude/
├── settings.local.json
└── commands/
    ├── scrape.md       ← /scrape
    ├── publish.md      ← /publish [날짜]
    ├── report.md       ← /report [날짜]
    ├── status.md       ← /status [날짜]
    ├── mcp-start.md    ← /mcp-start
    └── pipeline.md     ← /pipeline
```

## 파일 내용

### 1. `.claude/commands/scrape.md`

```markdown
---
description: LinkedIn 크롤링 + Claude 분석 + data/ 저장 (1회 즉시 실행)
---

LinkedIn에서 Claude Code 관련 게시글을 크롤링하고, Claude API로 분석한 후 data/ 디렉터리에 JSON으로 저장해줘.

다음 명령어를 실행해:

\```bash
uv run python -m scheduler.daily_job_once
\```

실행이 끝나면 결과 요약을 보여줘:
- 수집된 게시글 수
- 관련 게시글 수
- 추출된 팁 수
- Skill 후보 수
- 저장된 파일 경로
```

### 2. `.claude/commands/publish.md`

```markdown
---
description: generated_skills/ 에서 마켓플레이스 레포로 Skills 복사 + git push
---

오늘 날짜(또는 $ARGUMENTS로 지정된 날짜)의 generated_skills를 claude-code-skills 마켓플레이스 레포에 publish해줘.

날짜 인자: $ARGUMENTS (비어 있으면 오늘 날짜 사용)

다음 Python 코드를 실행해:

\```bash
uv run python -c "
from scraper.publisher import publish_skills
from datetime import datetime

date = '$ARGUMENTS'.strip() or datetime.now().strftime('%Y-%m-%d')
print(f'[*] Publishing skills for {date}...')
result = publish_skills(date)
print(f'결과: copied={result[\"copied\"]}, skipped={result[\"skipped\"]}, pushed={result[\"pushed\"]}')
if result['error']:
    print(f'오류: {result[\"error\"]}')
"
\```

실행 후 결과를 요약해줘:
- 복사된 Skill 수
- 스킵된 Skill 수
- push 성공 여부
- 오류 내용 (있다면)
```

### 3. `.claude/commands/report.md`

```markdown
---
description: 날짜별 Skill 후보 리포트 생성 및 요약 출력
---

오늘 날짜(또는 $ARGUMENTS로 지정된 날짜)의 수집 데이터에서 Skill 후보 리포트를 생성해줘.

날짜 인자: $ARGUMENTS (비어 있으면 오늘 날짜 사용)

다음 Python 코드를 실행해:

\```bash
uv run python -c "
import json
from pathlib import Path
from datetime import datetime
from scraper.reporter import generate_report

date = '$ARGUMENTS'.strip() or datetime.now().strftime('%Y-%m-%d')
data_path = Path('data') / f'{date}.json'

if not data_path.exists():
    print(f'[!] 데이터 없음: {data_path}')
    print('먼저 /scrape 를 실행하세요.')
else:
    data = json.loads(data_path.read_text(encoding='utf-8'))
    report_path = generate_report(date, data.get('posts', []))
    print(f'[OK] 리포트 생성: {report_path}')
    print()
    print(report_path.read_text(encoding='utf-8'))
"
\```

생성된 리포트 내용을 마크다운으로 요약해줘.
```

### 4. `.claude/commands/status.md`

```markdown
---
description: 오늘(또는 지정일)의 수집 현황 및 데이터 요약 확인
---

오늘 날짜(또는 $ARGUMENTS로 지정된 날짜)의 수집 현황을 확인해줘.

날짜 인자: $ARGUMENTS (비어 있으면 오늘 날짜 사용)

다음 Python 코드를 실행해:

\```bash
uv run python -c "
import json
from pathlib import Path
from datetime import datetime

date = '$ARGUMENTS'.strip() or datetime.now().strftime('%Y-%m-%d')
data_path = Path('data') / f'{date}.json'
skills_path = Path('generated_skills') / date
report_path = Path('reports') / f'{date}-skill-report.md'
exec_path = Path('execution_results') / date / 'execution-report.md'

print(f'=== {date} 수집 현황 ===')
print()

if data_path.exists():
    data = json.loads(data_path.read_text(encoding='utf-8'))
    summary = data.get('daily_summary', {})
    print(f'데이터: {data_path} [OK]')
    print(f'   수집: {summary.get(\"total_posts_scraped\", \"?\")}개')
    print(f'   관련: {summary.get(\"relevant_posts\", \"?\")}개')
    print(f'   팁:   {summary.get(\"tips_extracted\", \"?\")}개')
    print(f'   Skill 후보: {summary.get(\"skill_worthy_tips\", \"?\")}개')
    print(f'   카테고리: {summary.get(\"categories\", {})}')
else:
    print(f'데이터: {data_path} [없음] - /scrape 먼저 실행')

print()
if skills_path.exists():
    skills = list(skills_path.glob('*.md'))
    print(f'생성 Skills: {len(skills)}개')
    for s in skills:
        print(f'   - {s.name}')
else:
    print(f'생성 Skills: 없음')

print()
print(f'리포트: {\"OK\" if report_path.exists() else \"없음\"}')
print(f'실행결과: {\"OK\" if exec_path.exists() else \"없음\"}')

all_dates = sorted([f.stem for f in Path('data').glob('*.json')])
print(f'\\n수집 완료 날짜: {len(all_dates)}일')
for d in all_dates[-5:]:
    print(f'   {d}')
if len(all_dates) > 5:
    print(f'   ... 외 {len(all_dates)-5}일')
"
\```

출력 결과를 깔끔하게 정리해서 보여줘.
```

### 5. `.claude/commands/mcp-start.md`

```markdown
---
description: 팁 조회용 MCP 서버 시작 (linkedin-tips)
---

LinkedIn 팁 조회용 MCP 서버를 시작해줘.

다음 명령어를 실행해:

\```bash
uv run python -m mcp_server.server
\```

서버가 시작되면 사용 가능한 도구를 안내해줘:
- `get_latest_tips` — 최신 팁 조회
- `get_tips_by_date` — 날짜별 팁 조회
- `get_tips_by_category` — 카테고리별 팁 조회
- `search_tips` — 키워드 검색
- `generate_skill` — Skill 생성
- `list_available_dates` — 수집 가능 날짜 목록
```

### 6. `.claude/commands/pipeline.md`

```markdown
---
description: 전체 파이프라인 실행 (크롤링 → 분석 → 리포트 → Skill 생성 → publish)
---

전체 파이프라인을 한 번에 실행해줘. 순서:

1. **크롤링 + 분석 + 저장**: LinkedIn 게시글 수집 → Claude 분석 → data/ JSON 저장
2. **리포트 생성**: Skill 후보 리포트
3. **Skill 실행**: 추천 Skill 실행 및 결과 저장
4. **마켓플레이스 publish**: claude-code-skills 레포에 push

다음 명령어를 실행해:

\```bash
uv run python -m scheduler.daily_job_once
\```

이 명령 하나로 위 모든 단계가 순차적으로 실행돼.

실행 완료 후 결과를 요약해줘:
- 수집/분석 결과 (게시글 수, 팁 수, Skill 후보 수)
- 생성된 파일 목록
- 마켓플레이스 publish 결과
```

---

## 사용법

| 입력 | 동작 |
|------|------|
| `/scrape` | 오늘 LinkedIn 크롤링 즉시 실행 |
| `/publish` | 오늘 날짜 Skills를 마켓플레이스에 push |
| `/publish 2026-04-01` | 특정 날짜 Skills publish |
| `/report` | 오늘 Skill 후보 리포트 생성 |
| `/report 2026-03-31` | 특정 날짜 리포트 |
| `/status` | 오늘 수집 현황 대시보드 |
| `/status 2026-04-01` | 특정 날짜 현황 |
| `/mcp-start` | MCP 서버 시작 |
| `/pipeline` | 전체 파이프라인 한방 실행 |

## 적용 방법

`.claude/commands/` 디렉터리를 생성하고 위 6개 파일을 저장하면 즉시 사용 가능합니다:

```powershell
mkdir .claude\commands
# 각 .md 파일을 위 내용대로 생성
```

> **참고**: 파일 쓰기 권한이 현재 차단되어 있어 자동 생성이 안 되었습니다. 권한을 허용하시면 다시 실행해 드리거나, 위 내용을 수동으로 복사하여 파일을 생성해주세요.

---

## 2. [Prompting] 시니어 역할 프롬프트로 코드베이스 전체 리뷰·QA 수행

**추천 이유:** scraper/publisher/MCP 서버 등 모듈이 다수이므로, 1차 구현 후 셀렉터 깨짐·예외 누락·인코딩 이슈 등을 시니어 리뷰 패턴으로 일괄 점검 가능

**실행 프롬프트:**
```
시니어 Python 엔지니어 역할로 이 코드베이스를 전체 리뷰하라. 1단계: scraper/, scheduler/, mcp_server/, hooks/ 전체를 읽고 아키텍처·의존성·에러 핸들링을 점검한다. 2단계: LinkedIn 셀렉터 변경 대응력, async 예외 전파, encoding='utf-8' 누락, .env 노출 위험 등 실무 엣지케이스를 체크한다. 3단계: 발견된 이슈를 critical/warning/suggestion으로 분류해 표로 출력하고, 각 항목에 수정 코드 스니펫을 첨부한다.
```

**실행 결과:**

모든 소스 파일을 읽었습니다. 시니어 Python 엔지니어 관점에서 전체 리뷰 결과를 정리합니다.

---

# 🔍 시니어 Python 엔지니어 코드베이스 전체 리뷰

## 1단계: 아키텍처 개요

| 모듈 | 역할 | 핵심 의존성 |
|------|------|------------|
| `scraper/linkedin_scraper.py` | Playwright 기반 LinkedIn 크롤링 | playwright, dotenv |
| `scraper/analyzer.py` | Claude Agent SDK로 게시글 분석 | claude-agent-sdk |
| `scraper/publisher.py` | 마켓플레이스 레포에 Skill 자동 push | subprocess(git) |
| `scraper/reporter.py` | Skill 후보 리포트 생성 | (순수 Python) |
| `scraper/skill_executor.py` | 추천 Skill 실행 + 결과 저장 | claude-agent-sdk |
| `scheduler/daily_job.py` | 매일 09:00 자동 실행 오케스트레이터 | schedule |
| `mcp_server/server.py` | 저장된 팁 조회 MCP 서버 | FastMCP |
| `hooks/file_logger.py` | PostToolUse 파일 변경 로거 | (순수 Python) |

**아키텍처 평가:** 모듈 분리가 깔끔하고, 단방향 의존 흐름(`scheduler → scraper → data`, `mcp_server → data`)이 잘 유지됨. 다만 몇 가지 실무 레벨 이슈가 존재.

---

## 2단계: 엣지케이스 점검 결과

## 3단계: 이슈 분류표

### 🔴 Critical (즉시 수정 필요)

| # | 파일 | 라인 | 이슈 | 설명 |
|---|------|------|------|------|
| C1 | `linkedin_scraper.py` | 40-61 | **로그인 실패 시 조용히 진행** | `_login()`이 타임아웃되어도 예외 없이 return → 미인증 상태로 검색 시도 → 수집 0건 + 원인 파악 불가 |
| C2 | `linkedin_scraper.py` | 200-251 | **키워드마다 브라우저 재생성** | `search_posts()`가 매 호출마다 `async_playwright()` + `browser.close()` → 3개 키워드 = 3번 브라우저 시작/종료, 쿠키 복원 반복 |
| C3 | `linkedin_scraper.py` | 203 | **headless=False 하드코딩** | Task Scheduler에서 자동 실행 시 GUI 없는 세션이면 브라우저가 뜨지 않아 실패 |
| C4 | `mcp_server/server.py` | 193-194 | **Skill 저장 경로 불일치** | `SKILLS_DIR` 루트에 저장하지만, CLAUDE.md 규칙은 `generated_skills/YYYY-MM-DD/` 하위 디렉터리 |

### 🟡 Warning (가까운 시일 내 수정 권장)

| # | 파일 | 라인 | 이슈 | 설명 |
|---|------|------|------|------|
| W1 | `hooks/file_logger.py` | 29 | **bare except + pass** | 모든 예외를 삼킴 → 디스크 풀, 권한 오류 등 디버깅 불가 |
| W2 | `analyzer.py` | 55 | **greedy regex로 JSON 추출** | `r'\{[\s\S]*\}'` 는 마지막 `}`까지 매칭 → 복수 JSON 객체나 후행 텍스트에 취약 |
| W3 | `analyzer.py` | 72-84 | **순차 분석, 병렬화 부재** | `analyze_posts_batch`가 게시글을 하나씩 순차 처리 → 20개 × 3초 = 60초+ 소요 |
| W4 | `scheduler/daily_job.py` | 26-37 | **전체 히스토리 매번 로드** | `load_previous_contents()`가 모든 날짜 JSON을 매 실행마다 읽음 → 데이터 누적 시 성능 저하 |
| W5 | `publisher.py` | 30-34 | **git 미설치 시 무방비** | `subprocess.run(["git", ...])` 호출 시 `FileNotFoundError` 가능 |
| W6 | `linkedin_scraper.py` | 152 | **비결정적 fallback ID** | `noid_${Date.now()}_${Math.random()}` → 매번 다른 ID 생성 → 중복 제거 실패 |
| W7 | `skill_executor.py` | 43-51 | **`_query_claude` 중복 패턴** | `analyzer.py`와 거의 동일한 Claude 쿼리 패턴 → 공통 유틸로 추출 필요 |

### 🔵 Suggestion (개선 권장)

| # | 파일 | 이슈 | 설명 |
|---|------|------|------|
| S1 | 전체 | **print → logging 전환** | `print()` 산재 → `logging` 모듈로 전환 시 레벨 제어, 파일 로깅, 타임스탬프 자동화 |
| S2 | `pyproject.toml` | **dev 의존성 부재** | pytest, ruff, mypy 등 개발 도구 미선언 |
| S3 | `.gitignore` | **generated_skills/, reports/ 미포함** | 생성 파일이 커밋될 수 있음 (의도적이면 OK) |
| S4 | `mcp_server/server.py` | **날짜 포맷 미검증** | `get_tips_by_date("invalid")` → 에러 없이 None 반환, 사용자 혼란 |
| S5 | `scheduler/daily_job.py` | **graceful shutdown 부재** | `while True: time.sleep(30)` → KeyboardInterrupt 시 브라우저가 열린 채로 남을 수 있음 |
| S6 | `daily_job_once.py` | **에러 exit code 미반환** | Task Scheduler가 실패를 감지 못함 |

---

## 수정 코드 스니펫

### C1: 로그인 실패 시 예외 발생

```python
# scraper/linkedin_scraper.py — _login 메서드 끝부분
    async def _login(self, page: Page) -> None:
        """로그인 처리 - 브라우저 창에서 직접 로그인"""
        print("[*] LinkedIn 로그인 페이지 열기...")
        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        await asyncio.sleep(1)

        print("=" * 50)
        print("[!] 브라우저 창에서 직접 LinkedIn에 로그인하세요.")
        print("    로그인 완료되면 자동으로 진행됩니다. (최대 120초 대기)")
        print("=" * 50)

        for _ in range(120):
            await asyncio.sleep(1)
            current_url = page.url
            if any(x in current_url for x in ["feed", "mynetwork", "jobs", "messaging", "notifications"]):
                print("[+] 로그인 완료!")
                return  # ✅ 성공 시에만 정상 반환

        raise TimeoutError(f"LinkedIn 로그인 타임아웃 (120초). 현재 URL: {page.url}")
```

### C2: 브라우저 인스턴스 재사용

```python
# scraper/linkedin_scraper.py — scrape_all_keywords 리팩토링
    async def scrape_all_keywords(self, keywords: list[str]) -> list[dict]:
        """여러 키워드를 단일 브라우저 세션에서 순차 검색, 중복 제거"""
        all_posts: dict[str, dict] = {}

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=os.getenv("HEADLESS", "false").lower() == "true",
                args=["--disable-blink-features=AutomationControlled"],
            )
            try:
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 800},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                )
                page = await context.new_page()

                cookie_loaded = await self._load_cookies(context)
                logged_in = cookie_loaded and await self._is_logged_in(page)
                if not logged_in:
                    await self._login(page)
                    await self._save_cookies(context)

                for keyword in keywords:
                    posts = await self._search_keyword(page, keyword)
                    for post in posts:
                        all_posts[post["post_id"]] = post
                    await asyncio.sleep(5)

                await self._save_cookies(context)
            finally:
                await browser.close()

        return list(all_posts.values())
```

### C3: headless 모드 환경변수 제어

```python
# scraper/linkedin_scraper.py — launch 시
browser = await p.chromium.launch(
    headless=os.getenv("HEADLESS", "false").lower() == "true",
    args=["--disable-blink-features=AutomationControlled"],
)
```

`.env.example`에 추가:
```
# headless 모드 (Task Scheduler 자동 실행 시 true)
HEADLESS=false
```

### C4: MCP Skill 생성 경로를 날짜 기반으로

```python
# mcp_server/server.py — generate_skill 함수 내
    today = datetime.now().strftime("%Y-%m-%d")
    date_dir = SKILLS_DIR / today
    date_dir.mkdir(parents=True, exist_ok=True)
    skill_path = date_dir / f"{skill_name}.md"
```

### W1: Hook에서 예외를 stderr로 출력

```python
# hooks/file_logger.py
import sys

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "unknown")
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", tool_input.get("path", ""))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {tool_name}: {file_path}\n"

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

    except Exception as e:
        # hook 실패해도 Claude Code에 영향 없어야 하지만, 디버그는 가능하게
        print(f"[hook error] {e}", file=sys.stderr)
```

### W2: JSON 추출 regex를 non-greedy로

```python
# scraper/analyzer.py — line 55
match = re.search(r'\{[\s\S]*?\}(?=[^}]*$)', raw)  # 마지막 완전한 JSON 객체
# 또는 더 안전하게:
import json
def extract_json(raw: str) -> dict:
    """첫 번째 유효한 JSON 객체를 추출"""
    depth = 0
    start = None
    for i, ch in enumerate(raw):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    return json.loads(raw[start:i+1])
                except json.JSONDecodeError:
                    continue
    raise ValueError("유효한 JSON 객체를 찾을 수 없음")
```

### W3: 분석 배치 병렬화 (세마포어 제한)

```python
# scraper/analyzer.py — analyze_posts_batch
async def analyze_posts_batch(posts: list[dict], concurrency: int = 3) -> list[dict]:
    """게시글 목록 병렬 분석 (동시 실행 수 제한)"""
    semaphore = asyncio.Semaphore(concurrency)

    async def _analyze_one(i: int, post: dict) -> dict:
        async with semaphore:
            author = post.get("author", {}).get("name", "?")
            print(f"[*] 분석 중 ({i+1}/{len(posts)}): {author}", flush=True)
            analysis = await analyze_post(post)
            return {**post, "analysis": analysis}

    tasks = [_analyze_one(i, post) for i, post in enumerate(posts)]
    return await asyncio.gather(*tasks)
```

### W6: content 기반 결정적 fallback ID

```python
// JavaScript 내 (linkedin_scraper.py _scroll_and_collect)
const urn = container?.getAttribute('data-urn')
    || container?.getAttribute('data-id')
    || postLink?.href
    || `content_${btoa(content.substring(0, 50)).replace(/[^a-zA-Z0-9]/g, '')}`;
```

### S4: 날짜 포맷 검증

```python
# mcp_server/server.py
import re

@mcp.tool()
def get_tips_by_date(date: str) -> str:
    """특정 날짜(YYYY-MM-DD)의 팁과 요약을 반환합니다."""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return f"잘못된 날짜 형식: '{date}'. YYYY-MM-DD 형식을 사용하세요."
    # ... 기존 로직
```

### S6: daily_job_once에 exit code 반환

```python
# scheduler/daily_job_once.py
import asyncio
import sys
from scheduler.daily_job import run_daily_scrape

if __name__ == "__main__":
    try:
        asyncio.run(run_daily_scrape())
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)
```

---

## 요약 대시보드

| 등급 | 건수 | 핵심 키워드 |
|------|------|------------|
| 🔴 Critical | **4건** | 로그인 실패 무시, 브라우저 재생성, headless 하드코딩, Skill 경로 불일치 |
| 🟡 Warning | **7건** | 예외 삼킴, greedy regex, 순차 분석, 히스토리 전량 로드, git 미검증, 비결정적 ID, 코드 중복 |
| 🔵 Suggestion | **6건** | logging 전환, dev deps, gitignore, 입력 검증, graceful shutdown, exit code |

**우선 조치 권장 순서:**
1. **C1 + C3** → Task Scheduler 자동 실행이 현재 실패할 수 있는 가장 큰 원인
2. **C2** → 성능 2-3배 개선 (브라우저 1회만 기동)
3. **W3** → 분석 시간 60% 단축 가능 (병렬화)
4. **나머지** → 안정성·유지보수성 점진 개선

---
