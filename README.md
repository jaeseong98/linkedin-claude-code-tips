# LinkedIn Claude Code Tips

> LinkedIn에서 매일 자동 수집한 Claude Code 팁을 Skills로 변환해 바로 사용할 수 있는 개인 플러그인 마켓플레이스.

## 빠른 설치

```bash
git clone https://github.com/jaeseong98/linkedin-claude-code-tips.git
cd linkedin-claude-code-tips
bash install.sh
```

설치 후 Claude Code에서 `/agent-`, `/config-`, `/skills-` 등으로 바로 사용 가능.

---

## Skills 카탈로그 (27개)

### 🤖 Agent (10개)

| 스킬 | 설명 |
|------|------|
| `/agent-Discord를-멀티-에이전트-협업-채널로-활용하기` | Discord 봇 계정을 에이전트에 부여해 봇끼리 협업 |
| `/agent-GitHub-Actions와-Claude-Code를-연동해-이슈-정리코드` | PR 자동 리뷰, 이슈 라벨링·요약 자동화 |
| `/agent-Ralph-Loop-Claude-Code를-무한-루프로-돌려-자율-개발` | PROMPT.md 기반 완전 자율 반복 실행 |
| `/agent-Ralph-Loop-Claude를-while-true-무한-루프로-자율` | `while true` 루프로 Claude를 자율 개발 에이전트로 |
| `/agent-멀티-에이전트-브레인스토밍으로-아키텍처-설계하기` | 3개 관점(사용자/비판/구현)으로 아키텍처 설계 |
| `/agent-에이전트는-맥락과-암묵지를-명시적으로-주입해야-제대로-작동한다` | 암묵지를 CLAUDE.md 규칙으로 명문화하는 인터뷰 |
| `/agent-검증구현은-리서치-스킬-에이전트에-위임하고-분리-실행` | 설계와 검증을 분리해 병렬 처리 |
| `/agent-구현-Agent와-테스트-Agent를-분리해-컨텍스트-격리하기` | 구현/테스트 에이전트 컨텍스트 격리 |
| `/agent-Figma-JSON-정규화-파이프라인을-Claude-Code-Agent로` | Figma → tokens.json 자동 추출 |

---

### ⚙️ Config (6개)

| 스킬 | 설명 |
|------|------|
| `/config-CLAUDEmd로-프로젝트-표준-및-제약-조건-정의하기` | CLAUDE.md에 코딩 컨벤션·금지 패턴·HIGH-RISK 함수 정의 |
| `/config-CLAUDEmd-설정으로-AI가-프로젝트-규칙을-기억하게-하기` | 세션 간 프로젝트 규칙 자동 기억 |
| `/config-Claude-Code를-Discord-봇으로-연결해-원격-제어하기` | Discord 봇으로 Claude Code 원격 제어 |
| `/config-alias-cclaude-설정으로-타이핑-시간-단축` | `alias c='claude'` 설정 자동화 |
| `/config-terminal-setup-한-번으로-터미널-환경-최적화` | iTerm2/Kitty/Warp 등 터미널 최적 설정 |

---

### 🛠️ Skills (6개)

| 스킬 | 설명 |
|------|------|
| `/skills-동일-프롬프트-흐름을-3회-이상-반복하면-즉시-Skill로-만들기` | 반복 프롬프트를 `/project:` 슬래시 커맨드로 저장 |
| `/skills-스킬에-반드시-Gotchas-섹션을-포함하라` | 에이전트 실수 방지를 위한 Gotchas 섹션 작성법 |
| `/skills-Progressive-Disclosure점진적-공개-패턴으로-스킬을-설계` | TL;DR → 기본 → 고급 순 점진적 스킬 설계 |
| `/skills-Claude-스킬-설계-가이드로-반복-워크플로우를-자동화-스킬로-전환하기` | 반복 워크플로우를 스킬로 변환하는 가이드 |
| `/skills-사내-Claude-Code-플러그인-마켓플레이스-구축으로-팀-전체-생산성` | 이 레포 자체를 만든 스킬 |
| `/skills-로컬-Skill-폴더를-별도로-만들고-설치-경로를-명확히-지정하라` | Skill 설치 경로 및 상태 점검 |

---

### 🔌 MCP (3개)

| 스킬 | 설명 |
|------|------|
| `/mcp-Zapier-MCP-서버-연결로-8000개-앱-워크플로우-자동화` | Zapier 8,000개 앱을 Claude에서 직접 트리거 |
| `/mcp-Stripe-MCP-서버로-인보이스-자동-발급-파이프라인-구성` | Stripe 고객 생성·인보이스 발급 자동화 |
| `/mcp-MCP-세션마다-재학습-오버헤드를-줄이려면-데이터-소스를-정규화된-JSO` | MCP 컨텍스트 파일을 경량 JSON으로 정규화 |

---

### 💬 Prompting (1개)

| 스킬 | 설명 |
|------|------|
| `/prompting-대화가-길어지면-compact로-압축-또는-새-세션-시작` | `/compact`로 컨텍스트 압축해 성능 유지 |

---

### 🪝 Hooks (1개)

| 스킬 | 설명 |
|------|------|
| `/hooks-pre-commit-hook에-8단계-정적-분석-체인-연결하기` | tsc→eslint→sonarjs→knip→jscpd→semgrep 체인 자동화 |

---

## 구조

```
linkedin-claude-code-tips/
├── scraper/          # Playwright LinkedIn 크롤러
├── scheduler/        # 매일 09:00 자동 실행
├── mcp_server/       # 저장된 팁 조회 MCP 서버 (6개 도구)
├── hooks/            # Claude Code PostToolUse 훅
├── generated_skills/ # 날짜별 생성된 Skills
│   └── 2026-04-01/  # 27개 스킬 파일
├── reports/          # 수집 결과 보고서
├── install.sh        # Skills 자동 설치
├── CLAUDE.md         # 프로젝트 규칙 (Claude Code 자동 인식)
└── .env.example      # 환경변수 설정 예시
```

## 직접 실행

```bash
# 환경 설정
cp .env.example .env
# .env 파일에 LinkedIn 계정 정보 입력

# 즉시 1회 수집
uv run python -c "import asyncio; from scheduler.daily_job import run_daily_scrape; asyncio.run(run_daily_scrape())"

# 스케줄러 데몬 (매일 09:00 자동 실행)
uv run python -m scheduler.daily_job
```

## 라이선스

MIT
