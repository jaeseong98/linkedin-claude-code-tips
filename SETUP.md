# 설치 및 실행 가이드

## 1. 환경 설정

```bash
# 의존성 설치
uv sync

# Playwright 브라우저 설치
uv run playwright install chromium
```

## 2. .env 파일 설정

`.env` 파일에 실제 값 입력:
- `LINKEDIN_EMAIL` / `LINKEDIN_PASSWORD`: LinkedIn 계정
- API 키 불필요: Claude Code 로그인 인증을 그대로 사용

## 3. 스케줄러 실행 (매일 자동 수집)

```bash
uv run python -m scheduler.daily_job
```

매일 09:00에 자동 실행됩니다.

즉시 한 번 실행하려면 `daily_job.py` 안에서 `# job()` 주석 해제 후 실행.

## 4. MCP 서버를 Claude Code에 등록

```bash
claude mcp add linkedin-tips -- uv run python -m mcp_server.server
```

등록 후 Claude Code에서 사용 가능한 명령:
- "오늘 팁 보여줘" → `get_latest_tips`
- "MCP 카테고리 팁 찾아줘" → `get_tips_by_category`
- "2026-04-01 데이터 보여줘" → `get_tips_by_date`
- "키워드로 검색" → `search_tips`
- "이 팁 Skill로 만들어줘" → `generate_skill`

## 5. 데이터 구조

```
data/
├── 2026-04-01.json
├── 2026-04-02.json
└── ...

generated_skills/
├── mcp-server-설정법.md
└── ...
```

## 주의사항

- LinkedIn은 자동화 크롤링을 ToS로 금지하고 있습니다. 개인 학습 목적으로만 사용하세요.
- 첫 실행 시 보안 인증(캡차 등)이 나올 수 있습니다. 브라우저 창에서 직접 완료하세요.
- 쿠키는 `.linkedin_cookies.json`에 저장됩니다 (git에 올리지 마세요).
