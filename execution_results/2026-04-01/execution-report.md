# 2026-04-01 Skill Execution Report

*Executed at: 2026-04-02T20:11:47.240600*

## 1. GitHub Actions와 Claude Code를 연동해 이슈 정리·코드 리뷰 자동화

**추천 이유:** 마켓플레이스 레포(claude-code-skills)에 자동 push하는 구조가 이미 있으므로, PR 코드 리뷰·이슈 라벨링을 GitHub Actions로 자동화하면 생성된 Skill 품질 게이트를 즉시 추가할 수 있다.

**실행 프롬프트:**
```
이 프로젝트의 GitHub Actions 워크플로우를 생성해줘. Claude Code를 활용해서 새 이슈가 생성될 때 자동으로 라벨을 분류하고 요약 코멘트를 달아주는 yml 파일을 작성해줘.
```

**실행 결과:**

파일 쓰기 권한 승인이 필요합니다. `.github/workflows/` 디렉터리에 파일을 만들어야 하는데, 승인 팝업에서 **"허용(Allow)"**을 눌러주세요.

권한이 승인되는 동안, 생성할 워크플로우 파일들의 전체 내용을 먼저 마크다운으로 정리해 드리겠습니다.

---

# 🏷️ GitHub Actions × Claude Code — 이슈 자동 분류 & 코드 리뷰 자동화

## 적용 개요

| 항목 | 내용 |
|------|------|
| **프로젝트** | LinkedIn Claude Code Tips Scraper |
| **생성 파일** | `.github/workflows/issue-triage.yml` (이슈 자동 분류) |
|  | `.github/workflows/pr-review.yml` (PR 코드 리뷰) |
| **트리거** | 이슈 생성 시 / PR 오픈 시 |
| **필요 시크릿** | `ANTHROPIC_API_KEY` (GitHub Repo → Settings → Secrets) |

---

## 파일 1: `.github/workflows/issue-triage.yml`

### 동작 흐름

```
새 이슈 생성 → Claude가 내용 분석 → 라벨 자동 부착 → 요약 코멘트 작성
```

### 프로젝트 맞춤 라벨 체계

| 라벨 | 대상 모듈 |
|------|-----------|
| `bug` | 버그 리포트 |
| `enhancement` | 기능 개선 |
| `scraper` | `scraper/linkedin_scraper.py`, `scraper/analyzer.py` |
| `mcp-server` | `mcp_server/` |
| `scheduler` | `scheduler/daily_job.py` |
| `skills` | `scraper/publisher.py`, `generated_skills/` |
| `ci-cd` | GitHub Actions 관련 |
| `docs` | 문서 |
| `question` | 질문 |

### 전체 소스

```yaml
name: "🏷️ Issue Auto-Triage with Claude"

on:
  issues:
    types: [opened]

permissions:
  contents: read
  issues: write

jobs:
  triage:
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Claude Code for issue triage
        id: claude
        uses: anthropics/claude-code-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          direct_prompt: |
            아래 GitHub 이슈를 분석해서 두 가지 작업을 수행해줘.

            ## 이슈 정보
            - 제목: ${{ github.event.issue.title }}
            - 본문:
            ${{ github.event.issue.body }}

            ## 작업 1 — 라벨 분류
            아래 라벨 중 해당되는 것을 모두 골라줘 (쉼표 구분):
            bug, enhancement, scraper, mcp-server, scheduler,
            skills, ci-cd, docs, question

            ## 작업 2 — 요약 코멘트
            이슈 내용을 1~3줄로 요약하고, 관련 파일/모듈이 있으면 언급해줘.

            ## 출력 형식
            LABELS: bug, scraper
            SUMMARY: LinkedIn 셀렉터 변경으로 크롤링 실패.

      - name: Parse Claude response
        id: parse
        uses: actions/github-script@v7
        with:
          script: |
            const response = `${{ steps.claude.outputs.response }}`;
            const labelsMatch = response.match(/LABELS:\s*(.+)/i);
            const labels = labelsMatch
              ? labelsMatch[1].split(',').map(l => l.trim().toLowerCase()).filter(Boolean)
              : ['needs-triage'];
            const summaryMatch = response.match(/SUMMARY:\s*(.+)/is);
            const summary = summaryMatch
              ? summaryMatch[1].trim()
              : '자동 분류에 실패했습니다.';
            core.setOutput('labels', JSON.stringify(labels));
            core.setOutput('summary', summary);

      - name: Apply labels
        uses: actions/github-script@v7
        with:
          script: |
            const labels = JSON.parse('${{ steps.parse.outputs.labels }}');
            const validLabels = [
              'bug','enhancement','scraper','mcp-server',
              'scheduler','skills','ci-cd','docs','question','needs-triage'
            ];
            const filtered = labels.filter(l => validLabels.includes(l));
            if (filtered.length === 0) filtered.push('needs-triage');
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: filtered,
            });

      - name: Post summary comment
        uses: actions/github-script@v7
        with:
          script: |
            const summary = `${{ steps.parse.outputs.summary }}`;
            const labels = JSON.parse('${{ steps.parse.outputs.labels }}');
            const body = [
              `## 🤖 Claude 자동 분류 결과`,
              ``,
              `**라벨:** ${labels.map(l => '`' + l + '`').join(' ')}`,
              ``,
              `**요약:** ${summary}`,
              ``,
              `---`,
              `> _이 코멘트는 Claude Code Action이 자동 생성했습니다._`,
            ].join('\n');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body,
            });
```

---

## 파일 2: `.github/workflows/pr-review.yml`

### 동작 흐름

```
PR 오픈/업데이트 → Claude가 diff 분석 → 리뷰 코멘트 작성
```

### 전체 소스

```yaml
name: "🔍 PR Auto-Review with Claude"

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Claude Code for PR review
        uses: anthropics/claude-code-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          direct_prompt: |
            이 PR의 변경사항을 리뷰해줘.

            ## 프로젝트 컨텍스트
            LinkedIn Claude Code Tips Scraper 프로젝트:
            - scraper/: Playwright 기반 LinkedIn 크롤러 + Claude 분석
            - scheduler/: 매일 자동 실행 스케줄러
            - mcp_server/: 팁 조회용 MCP 서버
            - generated_skills/: 자동 생성 Skill 파일

            ## 코딩 규칙
            - Python 3.11+, async/await 사용
            - 파일 입출력은 encoding='utf-8' 명시
            - LinkedIn 크롤링 딜레이: 키워드 5초, 스크롤 2초 이상
            - 분석 실패 시 analysis 필드에 오류 기록
            - .env, .linkedin_cookies.json 커밋 금지

            ## 리뷰 기준
            1. 🐛 버그 가능성 (예외 미처리, 타입 오류 등)
            2. 🔒 보안 이슈 (.env, 쿠키 파일 노출 여부)
            3. ⚡ 성능 (불필요한 API 호출, 크롤링 딜레이 위반)
            4. 📐 코드 스타일 (프로젝트 규칙 준수)
            5. ✅ 좋은 점도 언급

            ## 출력 형식
            ### 리뷰 요약
            (전체 변경 1-2줄 요약)

            ### 상세 리뷰
            (파일별 구체적 피드백)

            ### 승인 판단
            ✅ LGTM / ⚠️ 수정 요청 / 🚫 블로킹 이슈
```

---

## 셋업 체크리스트

### 1. GitHub Secrets 등록
```
GitHub Repo → Settings → Secrets and variables → Actions → New repository secret
  Name:  ANTHROPIC_API_KEY
  Value: sk-ant-api03-xxxxx
```

### 2. GitHub 라벨 생성 (한 번만)
```bash
# gh CLI로 프로젝트 전용 라벨 일괄 생성
gh label create scraper    --color "1d76db" --description "LinkedIn 크롤러 관련"
gh label create mcp-server --color "0e8a16" --description "MCP 서버 관련"
gh label create scheduler  --color "d93f0b" --description "스케줄러 관련"
gh label create skills     --color "5319e7" --description "Skill 생성/마켓플레이스"
gh label create ci-cd      --color "fbca04" --description "CI/CD 자동화"
gh label create needs-triage --color "ededed" --description "자동 분류 실패"
```

### 3. 파일 배치
```
.github/
└── workflows/
    ├── issue-triage.yml   ← 이슈 자동 분류 + 요약
    └── pr-review.yml      ← PR 자동 코드 리뷰
```

### 4. 동작 확인
- **이슈 테스트**: 새 이슈 생성 → Actions 탭에서 워크플로우 실행 확인 → 라벨 + 코멘트 확인
- **PR 테스트**: 브랜치에서 PR 오픈 → 리뷰 코멘트 자동 생성 확인

---

## 예상 결과 (이슈 생성 시)

> ### 🤖 Claude 자동 분류 결과
>
> **라벨:** `bug` `scraper`
>
> **요약:** LinkedIn 프로필 페이지 셀렉터(`data-testid="expandable-text-box"`)가 변경되어 크롤링이 실패함. `scraper/linkedin_scraper.py`의 셀렉터 업데이트 필요.
>
> ---
> _이 코멘트는 Claude Code Action이 자동 생성했습니다._

---

## 비용 참고

| 워크플로우 | 트리거 | 예상 토큰 | 예상 비용/회 |
|------------|--------|-----------|-------------|
| Issue Triage | 이슈 생성 시 | ~2K tokens | ~$0.01 |
| PR Review | PR 오픈 시 | ~5-15K tokens | ~$0.05-0.15 |

> ⚠️ 파일 쓰기 권한을 승인해 주시면 위 두 워크플로우 파일을 프로젝트에 직접 생성합니다. 터미널에서 **Allow** 버튼을 눌러주세요.

---

## 2. 스킬에 반드시 Gotchas 섹션을 포함하라

**추천 이유:** 이 프로젝트가 매일 자동 생성하는 Skill 파일에 Gotchas 섹션을 포함하도록 skill_generator 템플릿을 개선하면, 마켓플레이스에 배포되는 모든 스킬의 실행 안정성이 즉시 향상된다.

**실행 프롬프트:**
```
이 스킬을 실행하기 전에 반드시 Gotchas 섹션을 먼저 읽고, 해당 주의사항을 모두 숙지한 뒤 작업을 시작하세요. 각 단계에서 Gotchas에 언급된 엣지케이스를 확인하며 진행하세요.
```

**실행 결과:**

파일 쓰기 권한이 필요합니다. 권한을 허용해 주시면 다음 파일들을 수정하겠습니다. 우선 변경 내용을 마크다운으로 정리해서 보여드리겠습니다.

---

# 🔍 Skill 적용 결과: "스킬에 반드시 Gotchas 섹션을 포함하라"

## 📊 현황 분석

### Gotchas 섹션 포함 여부 (전체 37개 스킬 파일)

| 상태 | 파일 수 | 비율 |
|------|---------|------|
| ✅ Gotchas 포함 | 8개 | 21.6% |
| ❌ Gotchas 미포함 | **29개** | **78.4%** |

> 기존 스킬의 약 **80%가 Gotchas 섹션 없이** 배포되고 있어, 에이전트 실행 시 엣지케이스 사전 방지가 불가능한 상태입니다.

---

## 🛠️ 적용 대상: 4개 파일 수정 + 2개 대표 스킬에 Gotchas 추가

### 1. `scraper/analyzer.py` — 분석 프롬프트에 gotchas 필드 추가

**변경 내용:** Claude가 LinkedIn 게시글 분석 시 `gotchas` 배열을 함께 추출하도록 프롬프트 수정

```python
# 기존 (gotchas 없음)
"skill_template": "skill_worthy가 true일 때 Skill 프롬프트 내용, 아니면 빈 문자열"

# 변경 후 (gotchas 추가)
"skill_template": "skill_worthy가 true일 때 Skill 프롬프트 내용, 아니면 빈 문자열",
"gotchas": "skill_worthy가 true일 때 이 스킬 실행 시 주의사항·엣지케이스 목록(배열). 아니면 빈 배열"
```

**프롬프트 끝에 gotchas 작성 가이드 추가:**
```
gotchas 작성 가이드:
- 에이전트가 무시하기 쉬운 환경 전제조건 (예: API 키, 권한, OS 차이)
- 실행 순서 의존성 (예: A를 먼저 해야 B가 동작)
- 흔한 오류 패턴 (예: 비동기 호출 누락, 인코딩 문제)
- 보안 관련 주의 (예: 민감 정보 노출, 위험한 플래그)
```

---

### 2. `mcp_server/server.py` — `generate_skill` 도구 템플릿에 Gotchas 섹션 삽입

**변경 내용:** MCP `generate_skill` 도구가 스킬 파일 생성 시 자동으로 Gotchas 섹션 포함

```python
# 기존
skill_content = f"""---
name: {skill_name}
description: {target_tip.get('title', '')} (LinkedIn에서 수집된 Claude Code 팁)
---

{template}
"""

# 변경 후
gotchas = target_tip.get("gotchas", [])
gotchas_section = ""
if gotchas:
    gotchas_section = "\n## ⚠️ Gotchas\n\n"
    gotchas_section += "\n".join(f"- {g}" for g in gotchas)
    gotchas_section += "\n"

skill_content = f"""---
name: {skill_name}
description: {target_tip.get('title', '')} (LinkedIn에서 수집된 Claude Code 팁)
---

{template}
{gotchas_section}
"""
```

---

### 3. `scraper/reporter.py` — 리포트에 Gotchas 칼럼 추가

**변경 내용:** Skill 후보 리포트에 각 팁의 gotchas 표시

```python
# 기존 (template만 표시)
lines.extend([
    f"### {title}",
    "",
    desc,
    "",
    "**skill_template:**",
    "```",
    template,
    "```",
    "",
])

# 변경 후 (gotchas도 함께 표시)
gotchas = tip.get("gotchas", [])
gotchas_block = ""
if gotchas:
    gotchas_block = "\n**⚠️ Gotchas:**\n" + "\n".join(f"- {g}" for g in gotchas) + "\n"

lines.extend([
    f"### {title}",
    "",
    desc,
    "",
    "**skill_template:**",
    "```",
    template,
    "```",
    gotchas_block,
    "",
])
```

---

### 4. `CLAUDE.md` — Gotchas 컨벤션 규칙 추가

**추가 섹션:**
```markdown
## Gotchas 컨벤션
- 모든 Skill 파일(`.md`)에 `## ⚠️ Gotchas` 섹션을 반드시 포함
- 에이전트가 스킬 실행 전 Gotchas를 먼저 읽도록 사용법 섹션에 명시
- gotchas가 없으면 "특별한 주의사항 없음"이라도 명시적으로 기재
- analyzer.py 분석 시 gotchas 배열이 빈값이면 안 됨 — 최소 1개 이상 작성
```

---

### 5. 대표 스킬 파일 2개에 Gotchas 섹션 추가 (시범 적용)

#### 5-1. `agent-Ralph-Loop-Claude-Code를-무한-루프로-돌려-자율-개발.md`

```markdown
## ⚠️ Gotchas

- `--dangerously-skip-permissions` 플래그는 **모든 파일 쓰기/삭제를 무확인 실행**하므로, 프로덕션 환경에서는 절대 사용 금지
- PROMPT.md에 **완료 조건(exit condition)이 없으면 진짜 무한루프** — 반드시 "X 완료 시 DONE.md 생성" 같은 종료 조건 명시
- Windows에서는 `while true; do ... done`이 bash 전용 — PowerShell에서는 `while ($true) { ... }` 사용 필요
- Claude 세션 당 토큰 한도 초과 시 무한루프가 매 반복마다 실패 → 비용만 누적되는 함정
- `.env`, `.linkedin_cookies.json` 등 민감 파일이 있는 디렉터리에서 실행하면 에이전트가 해당 파일을 읽거나 커밋할 위험
```

#### 5-2. `mcp-Stripe-MCP-서버로-인보이스-자동-발급-파이프라인-구성.md`

```markdown
## ⚠️ Gotchas

- Stripe **live key**를 MCP 서버에 넣으면 Claude가 실제 결제를 실행할 수 있음 — 반드시 **test key**(`sk_test_`)로 먼저 검증
- `restricted key`는 읽기/쓰기 범위를 명확히 분리해야 함 (예: 인보이스 write만 허용, 고객 delete는 차단)
- MCP 서버 환경변수에 API 키를 직접 넣을 경우 `.env`나 `settings.json`이 커밋되지 않도록 `.gitignore` 확인 필수
- Stripe API rate limit (초당 25회)를 초과하면 429 에러 — 대량 인보이스 발급 시 배치 딜레이 필요
- 인보이스 `auto_advance: true` 설정 시 생성 즉시 고객에게 발송됨 — 테스트 중엔 반드시 `false`로 설정
```

---

## 📋 전체 변경 요약

| 파일 | 변경 유형 | 효과 |
|------|-----------|------|
| `scraper/analyzer.py` | 프롬프트 수정 | 앞으로 수집되는 **모든 팁에 gotchas 자동 추출** |
| `mcp_server/server.py` | 스킬 생성 함수 수정 | MCP로 생성하는 **모든 스킬에 Gotchas 섹션 자동 삽입** |
| `scraper/reporter.py` | 리포트 템플릿 수정 | 일별 리포트에서 **Gotchas 한눈에 확인** |
| `CLAUDE.md` | 규칙 추가 | 프로젝트 전체에 **Gotchas 컨벤션 강제** |
| 대표 스킬 2개 | Gotchas 섹션 추가 | 기존 스킬 **시범 적용 예시** |

## ⚠️ 이 작업 자체의 Gotchas

- **기존 29개 스킬 파일**에는 수동으로 Gotchas를 추가해야 함 — 한번에 일괄 수정하면 원본 의미가 훼손될 수 있으므로, 향후 재수집/재분석 시 자동 보강 권장
- `analyzer.py` 프롬프트 변경 후 **기존 JSON 데이터(`data/YYYY-MM-DD.json`)와 스키마 불일치** 가능 — MCP 서버의 `search_tips` 등은 `gotchas` 필드가 없어도 동작하므로 하위호환 OK
- `gotchas`가 빈 배열 `[]`로 오는 경우 리포트에 빈 섹션이 출력되지 않도록 조건 분기 처리 완료
- Claude Agent SDK의 `query()` 응답에서 gotchas가 누락될 수 있음 — `tip.get("gotchas", [])` 방어 코드 필수

---

파일 쓰기 권한을 허용해 주시면 위 변경사항을 실제 코드에 즉시 반영하겠습니다. 허용하시겠습니까?

---
