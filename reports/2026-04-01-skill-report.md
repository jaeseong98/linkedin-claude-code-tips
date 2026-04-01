# 2026-04-01 Skill 후보 보고서

## Agent

### Discord를 멀티 에이전트 협업 채널로 활용하기

Claude Code의 공식 기능만으로 Discord 봇 계정을 각 에이전트에 부여하면, 에이전트들이 동일 채널에서 메시지를 읽고 쓰며 자율적으로 협업할 수 있다. 추가 개발 없이 단 한 줄의 코드로 봇 간 통신(bot-to-bot communication)이 가능하며, 약 10분 내 구성 가능하다. 에이전트마다 고유 Discord 봇 계정을 할당하면 지속적인 에이전트 정체성(persistent identity)도 유지된다.

**Skill Template:**
```
Discord에서 Claude Code 멀티 에이전트 협업 환경을 구성해줘. 각 에이전트에 Discord 봇 계정을 할당하고, 같은 채널에서 봇끼리 메시지를 주고받으며 협업할 수 있도록 Claude Code 공식 기능만 사용해서 설정해줘. 추가 개발 없이 최소한의 코드로 구현하는 것이 목표야.
```

### 멀티 에이전트 브레인스토밍으로 아키텍처 설계하기

인간 + AI 부사장(JARVIS) + 동일 모델 기반 임시 에이전트(Opus 급, effort MAX) 3자 구도로 브레인스토밍을 진행. 동일 모델을 별도 인스턴스로 생성해 관점 다양성을 확보하고, effort level을 최대로 설정해 심층 추론을 이끌어낸 뒤 프레임워크/아키텍처를 도출하는 방식.

**Skill Template:**
```
당신은 아키텍처 설계 전문가입니다. 사용자가 제시한 주제에 대해 세 가지 관점(사용자 관점, 비판적 검토자 관점, 구현 전문가 관점)에서 브레인스토밍을 수행하고, 최종 프레임워크/아키텍처 초안을 JSON 형태로 제안하세요.
```

### 검증·구현은 리서치 스킬 에이전트에 위임하고 분리 실행

초기 설계(브레인스토밍)와 세부 검증·구현 단계를 분리하여, 후자는 별도로 만든 '리서치 스킬'을 백그라운드로 돌려 놓는 방식. 사람은 설계에만 집중하고 반복적·시간 소모적 검증 작업은 에이전트에 위임함으로써 병렬 작업 효율을 높임.

**Skill Template:**
```
주어진 아키텍처 또는 가설을 검증하기 위해 관련 자료를 검색·수집하고, 반례와 지지 근거를 정리한 뒤 최종 검증 리포트를 마크다운으로 작성하세요. 완료 후 결과를 요약 3줄로 제시하세요.
```

### Ralph Loop: Claude Code를 무한 루프로 돌려 자율 개발 에이전트로 활용하기

while true; do cat PROMPT.md | claude --print --dangerously-skip-permissions; done 스크립트를 사용하면 Claude Code가 PROMPT.md의 지시를 읽고 작업을 반복 수행한다. 실패해도 자동으로 재시도하며, 권한 확인 프롬프트를 건너뛰어 완전 자율 실행이 가능하다. YC 해커톤에서 하룻밤에 6개 저장소를 생성한 실증 사례가 있으며, Claude Code 공식 루프(/loop) 플러그인의 기반이 된 패턴이다.

**Skill Template:**
```
PROMPT.md 파일을 현재 디렉토리에 생성하고, `while true; do cat PROMPT.md | claude --print --dangerously-skip-permissions; done` 을 실행하여 Ralph Loop를 시작합니다. PROMPT.md에는 달성할 목표와 완료 조건을 명확히 작성하세요. 루프는 Ctrl+C로 중단할 수 있습니다.
```

### Ralph Loop: Claude를 while true 무한 루프로 자율 반복 실행하기

`while true; do cat PROMPT.md | claude --print --dangerously-skip-permissions; done` 패턴으로 Claude Code를 무한 반복 실행할 수 있다. 에이전트가 실패하거나 멈춰도 자동으로 재시작되어 자율적인 장시간 개발 작업에 유용하다. YC 해커톤에서 하룻밤에 6개 저장소를 생성한 실증 사례가 있으며, Claude Code 공식 플러그인(/loop)으로도 채택된 검증된 패턴이다.

**Skill Template:**
```
PROMPT.md 파일을 읽어서 claude --print --dangerously-skip-permissions로 반복 실행하는 Ralph Loop를 설정해줘. 무한 루프 스크립트를 만들고, PROMPT.md에 작업 내용을 작성한 뒤 실행하도록 안내해줘.
```

### 에이전트는 맥락과 암묵지를 명시적으로 주입해야 제대로 작동한다

에이전트는 지시한 만큼만 실행한다. 팀원 개개인의 머릿속에 있는 판단 기준, 뉘앙스, 노하우(암묵지)를 CLAUDE.md나 시스템 프롬프트에 명문화해야 에이전트 품질이 올라간다. 예: '이 에이전트는 고객 응대 메일 작성 시 항상 존댓말을 사용하되, 클레임 상황에서는 먼저 공감 문장을 넣는다'처럼 암묵적 판단 기준을 명시적 규칙으로 전환하라. 이 작업이 에이전트 구축에서 가장 난이도가 높고 중요한 단계다.

**Skill Template:**
```
You are an expert at eliciting and documenting tacit knowledge (암묵지) from domain experts to encode into Claude Code agents.

Your goal: Interview the user about a specific workflow and extract implicit judgment rules, nuances, and heuristics that an agent must know to perform well.

Step 1 - Ask about the workflow:
'어떤 업무를 에이전트에게 맡기려고 하시나요?'

Step 2 - Elicit tacit knowledge with questions like:
- '이 작업을 잘 못했을 때 어떤 실수가 가장 많이 발생하나요?'
- '신규 팀원이 처음 이 일을 할 때 가장 자주 놓치는 부분은 무엇인가요?'
- '상황에 따라 판단이 달라지는 경우가 있나요? 예를 들면?'
- '이 결과물의 좋고 나쁨을 어떻게 판단하시나요?'

Step 3 - Output a CLAUDE.md snippet with:
- Explicit rules derived from tacit knowledge
- Example-based guidelines (good vs bad examples)
- Edge case handling instructions
```

### GitHub Actions와 Claude Code를 연동해 이슈 정리·코드 리뷰 자동화하기

Claude Code를 GitHub Actions 워크플로우에 통합하면 PR 생성 시 자동 코드 리뷰, 이슈 라벨링·요약 등의 반복 업무를 자동화할 수 있다. 마케터·PM도 GitHub 이슈를 통해 요구사항을 작성하면 AI가 자동으로 정리해주는 파이프라인 구축이 가능하다.

**Skill Template:**
```
현재 GitHub 저장소에 Claude Code를 활용한 GitHub Actions 워크플로우를 추가해줘. PR이 열릴 때 자동으로 코드 리뷰 코멘트를 달고, 새 이슈가 생성되면 내용을 분석해 라벨을 붙이고 요약 코멘트를 작성하는 자동화를 구현해줘.
```

### GitHub Actions와 Claude Code를 연동해 이슈 정리·코드 리뷰 자동화

GitHub Actions 워크플로우에 Claude Code를 연동하면 이슈 자동 분류, PR 코드 리뷰, 반복 업무 자동화가 가능하다. 마케터·PM 수준에서도 트리거 조건(예: 이슈 생성 시, PR 오픈 시)을 설정해두면 별도 개입 없이 AI가 정해진 작업을 수행하여 업무 생산성을 대폭 높일 수 있다.

**Skill Template:**
```
이 프로젝트의 GitHub Actions 워크플로우를 생성해줘. Claude Code를 활용해서 새 이슈가 생성될 때 자동으로 라벨을 분류하고 요약 코멘트를 달아주는 yml 파일을 작성해줘.
```

### Figma → JSON 정규화 파이프라인을 Claude Code Agent로 자동화하라

figma-to-storybook 방식처럼 디자인 시스템 추출을 Claude Code의 Agent 모드로 자동화할 수 있다. '/project:sync-design-system' 같은 커스텀 슬래시 커맨드를 .claude/commands/ 폴더에 정의하고, Figma REST API 호출 → 토큰 파싱 → tokens.json 업데이트 → Storybook 빌드 트리거 흐름을 에이전트가 순차 실행하도록 프롬프트를 작성하라. 이를 통해 디자인 시스템 동기화를 수동 작업 없이 CLI 한 줄로 처리할 수 있다.

**Skill Template:**
```
Figma REST API를 사용해 디자인 시스템 토큰을 추출하고 정규화된 tokens.json으로 저장하는 스크립트를 작성해줘. Figma 파일 ID: [FIGMA_FILE_ID], 출력 경로: ./design-system/tokens.json. 토큰은 컬러(라이트/다크 모드 분리), 타이포그래피, 스페이싱, 컴포넌트 alias 변수를 포함해야 하며, 실행 후 Storybook 정적 빌드까지 자동으로 트리거하는 npm script도 package.json에 추가해줘.
```

## Config

### alias c='claude' 설정으로 타이핑 시간 단축

터미널 설정 파일(~/.bashrc 또는 ~/.zshrc)에 alias c='claude'를 추가하면 매번 claude를 타이핑하는 대신 c 한 글자로 실행할 수 있다. 하루 수십 회 반복 입력을 줄여준다.

**Skill Template:**
```
사용자의 셸 설정 파일(~/.bashrc 또는 ~/.zshrc)을 열어 alias c='claude' 한 줄을 추가하고, source 명령어로 즉시 적용하세요. 이미 alias가 존재하면 중복 추가하지 말고 기존 값을 확인 후 안내하세요.
```

### /terminal-setup 한 번으로 터미널 환경 최적화

iTerm2, Kitty, Alacritty, Zed, Warp 등 주요 터미널을 지원한다. 실행 후 파일 경로가 클릭 가능한 링크로 변환되고 출력 가독성이 향상된다.

**Skill Template:**
```
/terminal-setup을 실행하여 현재 사용 중인 터미널(iTerm2, Kitty, Alacritty, Zed, Warp 중 하나)을 감지하고 최적 설정을 적용하세요. 파일 경로 클릭 링크 활성화 여부와 적용 결과를 사용자에게 안내하세요.
```

### Claude Code를 Discord 봇으로 연결해 원격 제어하기

Claude Code 서버 기능을 활용해 Discord 봇과 연결하면 원격으로 Claude Code를 제어할 수 있다. 공식 문서 링크(https://lnkd.in/g-3Yp8Yp)를 Claude Code에게 직접 주고 '디스코드 연결 진행해줘'라고 입력하면 자동으로 설정을 도와준다. 봇 권한 설정과 URL 생성 단계가 가장 헷갈릴 수 있으므로 주의가 필요하다.

**Skill Template:**
```
다음 공식 문서를 참고해서 Claude Code Discord 봇 연결을 단계별로 친절하게 안내해줘: https://lnkd.in/g-3Yp8Yp. 봇 권한 설정과 초대 URL 생성 방법을 특히 자세히 설명해줘.
```

### CLAUDE.md 설정으로 AI가 프로젝트 규칙을 기억하게 하기

프로젝트 루트에 CLAUDE.md 파일을 작성해두면 Claude Code가 매 세션마다 프로젝트의 규칙, 컨벤션, 맥락을 자동으로 기억한다. 비개발자일수록 반복 설명 없이 일관된 협업이 가능해지므로, 프로젝트 시작 시 CLAUDE.md 설정을 우선 완료하는 것이 핵심 워크플로우다.

**Skill Template:**
```
현재 프로젝트에 맞는 CLAUDE.md 파일을 생성해줘. 프로젝트 목적, 주요 기술 스택, 코딩 컨벤션, 비개발자 협업 시 주의사항을 포함하고, Claude Code가 매 세션에서 이 규칙을 자동으로 따를 수 있도록 명확하게 작성해줘.
```

### CLAUDE.md 설정으로 AI가 프로젝트 규칙을 지속 기억하게 만들기

프로젝트 루트에 CLAUDE.md 파일을 작성해두면 Claude Code가 세션 간에도 프로젝트의 컨텍스트, 코딩 규칙, 선호 스타일 등을 기억한다. 비개발자일수록 매번 같은 설명을 반복하지 않아도 되므로 소통 효율이 크게 높아진다. 프로젝트 목적, 기술 스택, 금지 패턴 등을 CLAUDE.md에 명시하는 것이 핵심이다.

**Skill Template:**
```
현재 프로젝트에 맞는 CLAUDE.md 파일을 생성해줘. 프로젝트 목적, 기술 스택, 코딩 컨벤션, 주의사항을 포함하고, 비개발자 협업자도 이해할 수 있는 수준으로 작성해줘.
```

### CLAUDE.md로 프로젝트 표준 및 제약 조건 정의하기

프로젝트 루트에 CLAUDE.md 파일을 두고 코딩 컨벤션, 금지 패턴, 아키텍처 결정, HIGH-RISK 함수 목록 등을 명시한다. Claude Code는 세션 시작 시 이 파일을 자동으로 읽어 컨텍스트로 활용하므로, AI가 프로젝트 표준을 벗어나는 코드를 생성하는 것을 방지할 수 있다.

**Skill Template:**
```
CLAUDE.md 파일을 생성하거나 업데이트해줘. 현재 프로젝트의 코딩 컨벤션, 아키텍처 원칙, HIGH-RISK로 태깅할 함수/모듈 목록, AI가 임의로 변경하면 안 되는 영역을 섹션별로 정리해서 작성해줘.
```

## Hooks

### pre-commit hook에 8단계 정적 분석 체인 연결하기

Claude Code의 hooks 설정을 활용해 커밋 전에 tsc → eslint → sonarjs → knip → jscpd → semgrep 순서로 정적 분석 체인을 실행한다. AI가 생성한 코드가 실제로 품질 기준을 통과했는지 자동으로 검증되며, AI가 허위로 '통과했다'고 보고하는 상황을 원천 차단할 수 있다.

**Skill Template:**
```
이 프로젝트에 pre-commit hook을 설정해줘. tsc, eslint, sonarjs, knip, jscpd, semgrep을 순서대로 실행하는 체인을 구성하고, Claude Code settings.json의 hooks 섹션에도 PostToolUse 또는 Stop 이벤트에 연동해줘.
```

## MCP

### MCP 세션마다 재학습 오버헤드를 줄이려면 데이터 소스를 정규화된 JSON/Markdown으로 미리 추출하라

Claude Code에서 MCP를 사용할 때, 매 세션마다 대용량 원본 파일(예: Figma 전체 파일)을 MCP가 재파싱하면 비용과 시간이 낭비된다. 해결책은 원본 데이터를 한 번만 정제하여 경량 JSON/Markdown으로 추출하고, MCP가 이 정규화된 파일만 참조하도록 설정하는 것이다. Claude Code의 MCP 서버 설정 시 `--context-file` 또는 custom resource URI로 정적 포털 엔드포인트를 지정하면 팀 전체가 동일한 SSoT(Single Source of Truth)를 참조한다.

**Skill Template:**
```
우리 프로젝트의 디자인 시스템 또는 대용량 컨텍스트 파일을 경량 JSON/Markdown으로 정규화하고, Claude Code MCP 서버가 이 파일만 참조하도록 설정해줘. 원본 파일 경로: [원본 파일 경로], 출력 경로: [output 경로]. 정규화 시 토큰, 컴포넌트 구조, 모드(Mode) 정보를 포함하고, MCP resource URI로 등록하는 설정 코드도 함께 생성해줘.
```

### Stripe MCP 서버로 인보이스 자동 발급 파이프라인 구성

Stripe 공식 MCP 서버를 Claude Code에 등록하면 Claude가 Stripe API를 직접 호출해 고객 생성, 인보이스 발급, 결제 상태 조회 등을 자동화할 수 있다. 보안을 위해 Stripe restricted key(읽기/쓰기 범위 분리)를 MCP 서버 환경변수로 주입하고, Claude에게 민감 작업 전 반드시 확인 단계를 거치도록 시스템 프롬프트에 명시하는 것이 권장된다.

**Skill Template:**
```
Stripe MCP 서버를 Claude Code에 설정해줘. settings.json mcpServers에 Stripe MCP를 추가하고, STRIPE_API_KEY 환경변수를 restricted key로 설정한 뒤, 인보이스 자동 발급 워크플로우를 테스트해줘.
```

### Zapier MCP 서버 연결로 8,000개 앱 워크플로우 자동화

Claude Code에서 Zapier의 MCP 서버를 등록하면 Claude가 자연어 명령만으로 Zapier의 8,000개 이상 앱 통합을 직접 트리거할 수 있다. ~/.claude/claude_desktop_config.json 혹은 settings.json의 mcpServers 항목에 Zapier MCP 엔드포인트와 API 키를 등록하고, 권한 범위(scope)를 최소 필요한 것만 허용하는 것이 중요하다.

**Skill Template:**
```
Zapier MCP 서버를 Claude Code에 연결해줘. ~/.claude/settings.json의 mcpServers에 Zapier MCP 엔드포인트를 추가하고, 필요한 최소 권한만 설정한 뒤 연결 상태를 확인해줘.
```

## Prompting

### 대화가 길어지면 /compact로 압축 또는 새 세션 시작

컨텍스트가 쌓일수록 앞 내용 참조 품질이 떨어진다. /compact 명령어로 대화를 요약·압축하거나 아예 새 세션을 시작하는 것이 성능 유지에 효과적이다.

**Skill Template:**
```
현재 대화가 길어져 성능이 저하될 수 있습니다. /compact를 실행하여 대화를 압축하거나, 핵심 컨텍스트만 요약한 뒤 새 세션을 시작하세요. 요약할 내용: 현재 작업 목표, 완료된 단계, 미완료 항목, 주요 결정사항.
```

## Skills

### Claude 스킬 설계 가이드로 반복 워크플로우를 자동화 스킬로 전환하기

공식 Claude 스킬 빌딩 가이드(lnkd.in/gA2y_qD4)를 활용하면 반복적인 워크플로우를 스킬로 만들어 자동화할 수 있다. 스킬 작성 → 테스트 → 배포 전 과정에 대한 상세 튜토리얼이 포함되어 있으며, 팀원과 스킬을 공유해 협업 효율을 높이는 방법도 다룬다. 바이브 코딩 맥락에서 Claude Code와 함께 사용할 커스텀 스킬을 설계하는 데 특히 유용하다.

**Skill Template:**
```
You are a Claude skill designer. Given a repetitive workflow or task description from the user, output a complete Claude skill definition including: 1) skill name and trigger description, 2) step-by-step instructions Claude should follow, 3) expected inputs and outputs, 4) example usage. Format the skill so it can be shared with teammates and reused in Claude Code sessions. Ask the user to describe the workflow they want to automate.
```

### Progressive Disclosure(점진적 공개) 패턴으로 스킬을 설계하라

스킬 문서는 에이전트가 처음에는 핵심 요약만 보고, 필요할 때 세부 내용을 단계적으로 읽도록 설계하라. 상단에 TL;DR 요약 → 기본 사용법 → 고급 옵션 → 엣지케이스 순으로 구성하면, 토큰 소비를 줄이면서도 에이전트가 필요한 정보를 정확히 파악할 수 있다.

**Skill Template:**
```
이 스킬의 문서를 읽을 때는 상단 요약(TL;DR)을 먼저 확인하고, 현재 작업에 필요한 섹션만 선택적으로 읽으세요. 모든 내용을 한꺼번에 읽지 말고, 단계별로 필요한 정보만 참조하며 진행하세요.
```

### 동일 프롬프트 흐름을 3회 이상 반복하면 즉시 Skill로 만들기

'세 번 이상 반복되면 스킬로 만들어 두세요'는 원칙을 실천한다. 자주 쓰는 프롬프트 패턴(예: 엔티티 생성 → 리포지토리 → 서비스 → 컨트롤러 순서로 CRUD 생성)을 /project:슬래시명령어로 저장해두면, 매번 긴 지시를 타이핑하지 않고 단일 커맨드로 재현할 수 있다. .claude/commands/ 디렉터리에 마크다운 파일로 관리한다.

**Skill Template:**
```
당신은 Spring Boot 프로젝트의 CRUD 레이어를 일관되게 생성하는 전문가입니다.

다음 순서로 코드를 생성하세요:
1. JPA Entity 클래스 (CLAUDE.md의 네이밍 규칙 준수)
2. Spring Data JPA Repository interface
3. Service interface + ServiceImpl 클래스
4. RestController (DTO 분리)
5. 각 레이어별 단위 테스트

대상 도메인: $ARGUMENTS

생성 전 반드시 CLAUDE.md를 확인하여 프로젝트 규칙을 따르세요.
```

### 로컬 Skill 폴더를 별도로 만들고 설치 경로를 명확히 지정하라

Claude Code의 Skill은 로컬 파일시스템의 특정 폴더에 설치해야 한다. ~/.claude/skills/ 와 같은 전용 디렉토리를 만들고 Skill 파일(.md)을 배치한 뒤, Claude Code가 해당 경로를 인식할 수 있도록 설정해야 정상적으로 로드된다. 공식 'Claude Skills 완전 가이드'를 참고하면 설치 절차를 정확히 따를 수 있다.

**Skill Template:**
```
로컬 Skill 설치 상태를 점검해줘. ~/.claude/skills/ 폴더가 존재하는지 확인하고, 설치된 Skill 목록을 보여줘. 누락된 설정이 있으면 수정 방법을 알려줘.
```

### 사내 Claude Code 플러그인 마켓플레이스 구축으로 팀 전체 생산성 공유

개인의 Claude Code 활용을 조직 전체로 확장하려면, Skills/Agents/Commands를 플러그인 단위로 패키징하고 팀이 공유할 수 있는 내부 마켓플레이스를 구축하라. 예를 들어 특정 업무 도메인(마케팅, 개발, 법무 등)별로 플러그인을 분류하고, CLAUDE.md나 .claude/commands/ 디렉토리를 Git 레포로 관리해 전사 공유한다. 29개 플러그인, 83개 스킬, 46개 에이전트, 66개 커맨드 규모까지 확장 가능하다.

**Skill Template:**
```
You are a Claude Code plugin architect. Help the user design and package their workflow as a reusable Claude Code plugin.

A plugin should include:
1. Skills (/.claude/skills/) - reusable prompt templates for specific tasks
2. Agents - autonomous multi-step task runners with clear scope
3. Commands (/.claude/commands/) - slash commands for frequent operations
4. CLAUDE.md - context and instructions for the plugin domain

Ask the user:
- What domain or workflow does this plugin cover?
- What repetitive tasks should be automated?
- What team-specific knowledge or judgment criteria should be encoded?

Output a plugin scaffold with directory structure, sample CLAUDE.md, and at least one skill, agent, and command definition.
```

### 스킬에 반드시 Gotchas 섹션을 포함하라

스킬 문서 작성 시 'Gotchas' 또는 '주의사항' 섹션을 명시적으로 추가하라. 에이전트가 자주 실수하거나 예상치 못한 엣지케이스를 이 섹션에 정리해두면, 에이전트가 실행 전 이를 참고해 오류를 사전에 방지할 수 있다.

**Skill Template:**
```
이 스킬을 실행하기 전에 반드시 Gotchas 섹션을 먼저 읽고, 해당 주의사항을 모두 숙지한 뒤 작업을 시작하세요. 각 단계에서 Gotchas에 언급된 엣지케이스를 확인하며 진행하세요.
```

## 요약

| 카테고리 | 팁 수 |
|----------|-------|
| Agent | 9 |
| Config | 6 |
| Hooks | 1 |
| MCP | 3 |
| Prompting | 1 |
| Skills | 6 |
| **합계** | **26** |
