---
name: agent-에이전트는-맥락과-암묵지를-명시적으로-주입해야-제대로-작동한다
description: 에이전트는 맥락과 암묵지를 명시적으로 주입해야 제대로 작동한다
type: skill
category: Agent
source: LinkedIn (2026-04-01)
---

# 에이전트는 맥락과 암묵지를 명시적으로 주입해야 제대로 작동한다

에이전트는 지시한 만큼만 실행한다. 팀원 개개인의 머릿속에 있는 판단 기준, 뉘앙스, 노하우(암묵지)를 CLAUDE.md나 시스템 프롬프트에 명문화해야 에이전트 품질이 올라간다. 예: '이 에이전트는 고객 응대 메일 작성 시 항상 존댓말을 사용하되, 클레임 상황에서는 먼저 공감 문장을 넣는다'처럼 암묵적 판단 기준을 명시적 규칙으로 전환하라. 이 작업이 에이전트 구축에서 가장 난이도가 높고 중요한 단계다.

---

## 사용법

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

---

*수집 날짜: 2026-04-01 | 카테고리: Agent*
