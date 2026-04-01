# LinkedIn Claude Code Tips Scraper

## 프로젝트 개요
LinkedIn에서 Claude Code 관련 게시글을 매일 자동 수집하고, Claude Agent SDK로 팁을 추출해 JSON으로 저장하는 프로젝트.

## 디렉터리 구조
- `scraper/` — Playwright 기반 LinkedIn 크롤러 + Claude 분석
- `scheduler/` — 매일 09:00 자동 실행 스케줄러
- `mcp_server/` — 저장된 팁 조회용 MCP 서버
- `data/YYYY-MM-DD.json` — 날짜별 수집 결과
- `generated_skills/YYYY-MM-DD/` — 날짜별 생성된 Skill 파일

## 실행 방법
```bash
# 즉시 1회 실행
uv run python -c "import asyncio; from scheduler.daily_job import run_daily_scrape; asyncio.run(run_daily_scrape())"

# 스케줄러 데몬 실행 (매일 09:00)
uv run python -m scheduler.daily_job
```

## 코딩 규칙
- Python 3.11+, async/await 사용
- 모든 파일 입출력은 `encoding='utf-8'` 명시
- LinkedIn 크롤링 딜레이: 키워드 사이 5초, 스크롤 사이 2초 이상 유지
- 분석 실패 시 예외를 삼키지 말고 `analysis` 필드에 오류 기록

## 주의사항
- `.env` 파일에 LinkedIn 계정 정보 있음 — 절대 커밋 금지
- `.linkedin_cookies.json` — 세션 쿠키, 커밋 금지
- LinkedIn 셀렉터는 `data-testid="expandable-text-box"` 기반 (2026-04 기준)
- Claude Agent SDK `query()`는 반드시 키워드 인자 `prompt=` 사용

## MCP 서버
```bash
# Claude Code에 등록됨 (linkedin-tips)
# 사용 가능한 도구: get_latest_tips, get_tips_by_date, get_tips_by_category, search_tips, generate_skill, list_available_dates
```
