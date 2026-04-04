---
name: mcp-Context7 MCP로 최신 라이브러리 문서를 컨텍스트에 주입해 환각 제거
description: Context7 MCP로 최신 라이브러리 문서를 컨텍스트에 주입해 환각 제거
type: skill
category: Mcp
source: LinkedIn (2026-04-04)
---

# Context7 MCP로 최신 라이브러리 문서를 컨텍스트에 주입해 환각 제거

Context7 MCP 서버를 연결하고 프롬프트에 'use context7' 한 줄만 추가하면 최신 라이브러리 문서가 LLM 컨텍스트에 자동 주입되어 환각(hallucinated) API 호출을 방지할 수 있다.

---

## Usage

# Context7 최신 문서 주입 Skill

TRIGGER: 사용자가 외부 라이브러리/프레임워크 코드를 작성하거나 API 사용법을 물을 때

## Instructions
1. 대상 라이브러리를 식별하라.
2. Context7 MCP 도구를 호출해 해당 라이브러리의 최신 공식 문서를 컨텍스트에 주입하라.
3. 주입된 문서를 기반으로만 API 사용 코드를 생성하라. 문서에 없는 API는 사용하지 마라.

## Gotchas
- Context7 MCP 서버가 설정되어 있어야 한다.
- 매우 최신 릴리스(수 시간 이내)는 반영이 안 될 수 있다.

---

*Collected: 2026-04-04 | Category: Mcp*