# LinkedIn Claude Code Tips Scraper

## 프로젝트 개요
LinkedIn에서 Claude Code 관련 게시글을 매일 자동 수집하고, Claude Agent SDK로 팁을 추출해 JSON으로 저장하는 프로젝트.
수집된 팁은 Skills로 변환되어 마켓플레이스 레포(`claude-code-skills`)에 자동 publish된다.

## 디렉터리 구조
- `scraper/` — Playwright 기반 LinkedIn 크롤러 + Claude 분석 + 마켓플레이스 publisher
- `scheduler/` — 매일 09:00 자동 실행 스케줄러
- `mcp_server/` — 저장된 팁 조회용 MCP 서버
- `hooks/` — Claude Code PostToolUse 훅 (file_logger.py)
- `scripts/` — 유틸리티 스크립트 (Task Scheduler 등록 등)
- `data/YYYY-MM-DD.json` — 날짜별 수집 결과 (gitignore)
- `generated_skills/YYYY-MM-DD/` — 날짜별 생성된 Skill 파일
- `reports/` — 날짜별 Skill 후보 보고서

## 실행 방법
```bash
# 즉시 1회 실행
uv run python -m scheduler.daily_job_once

# 스케줄러 데몬 실행 (매일 09:00)
uv run python -m scheduler.daily_job
```

## 자동화
- **Windows Task Scheduler** 등록됨 — 매일 09:00 `daily_job_once` 자동 실행
- 등록 스크립트: `scripts/register_task.ps1` (관리자 권한 필요)
- 수동 재등록: `powershell -ExecutionPolicy Bypass -File scripts\register_task.ps1`

## 마켓플레이스 연동
- 수집 완료 후 `scraper/publisher.py`가 자동으로 `~/claude-code-skills` 레포에 Skills 복사 + push
- 마켓플레이스 레포 경로: `.env`의 `MARKETPLACE_REPO_PATH`로 설정
- GitHub: https://github.com/jaeseong98/claude-code-skills

## 코딩 규칙
- Python 3.11+, async/await 사용
- 모든 파일 입출력은 `encoding='utf-8'` 명시
- LinkedIn 크롤링 딜레이: 키워드 사이 5초, 스크롤 사이 2초 이상 유지
- 분석 실패 시 예외를 삼키지 말고 `analysis` 필드에 오류 기록

## 주의사항
- `.env` 파일에 LinkedIn 계정 정보 있음 — 절대 커밋 금지
- `.linkedin_cookies.json` — 세션 쿠키, 커밋 금지 (만료 시 수동 로그인 필요)
- LinkedIn 셀렉터는 `data-testid="expandable-text-box"` 기반 (2026-04 기준)
- Claude Agent SDK `query()`는 반드시 키워드 인자 `prompt=` 사용
- Task Scheduler 등록/수정은 관리자 권한 PowerShell에서 실행

## MCP 서버
```bash
# Claude Code에 등록됨 (linkedin-tips)
# 사용 가능한 도구: get_latest_tips, get_tips_by_date, get_tips_by_category, search_tips, generate_skill, list_available_dates
```
