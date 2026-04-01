---
name: agent-Figma-JSON-정규화-파이프라인을-Claude-Code-Agent로
description: Figma → JSON 정규화 파이프라인을 Claude Code Agent로 자동화하라
type: skill
category: Agent
source: LinkedIn (2026-04-01)
---

# Figma → JSON 정규화 파이프라인을 Claude Code Agent로 자동화하라

figma-to-storybook 방식처럼 디자인 시스템 추출을 Claude Code의 Agent 모드로 자동화할 수 있다. '/project:sync-design-system' 같은 커스텀 슬래시 커맨드를 .claude/commands/ 폴더에 정의하고, Figma REST API 호출 → 토큰 파싱 → tokens.json 업데이트 → Storybook 빌드 트리거 흐름을 에이전트가 순차 실행하도록 프롬프트를 작성하라. 이를 통해 디자인 시스템 동기화를 수동 작업 없이 CLI 한 줄로 처리할 수 있다.

---

## 사용법

Figma REST API를 사용해 디자인 시스템 토큰을 추출하고 정규화된 tokens.json으로 저장하는 스크립트를 작성해줘. Figma 파일 ID: [FIGMA_FILE_ID], 출력 경로: ./design-system/tokens.json. 토큰은 컬러(라이트/다크 모드 분리), 타이포그래피, 스페이싱, 컴포넌트 alias 변수를 포함해야 하며, 실행 후 Storybook 정적 빌드까지 자동으로 트리거하는 npm script도 package.json에 추가해줘.

---

*수집 날짜: 2026-04-01 | 카테고리: Agent*
