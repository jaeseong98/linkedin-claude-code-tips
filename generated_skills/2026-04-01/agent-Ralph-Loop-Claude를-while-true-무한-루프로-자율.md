---
name: agent-Ralph-Loop-Claude를-while-true-무한-루프로-자율
description: Ralph Loop: Claude를 while true 무한 루프로 자율 반복 실행하기
type: skill
category: Agent
source: LinkedIn (2026-04-01)
---

# Ralph Loop: Claude를 while true 무한 루프로 자율 반복 실행하기

`while true; do cat PROMPT.md | claude --print --dangerously-skip-permissions; done` 패턴으로 Claude Code를 무한 반복 실행할 수 있다. 에이전트가 실패하거나 멈춰도 자동으로 재시작되어 자율적인 장시간 개발 작업에 유용하다. YC 해커톤에서 하룻밤에 6개 저장소를 생성한 실증 사례가 있으며, Claude Code 공식 플러그인(/loop)으로도 채택된 검증된 패턴이다.

---

## 사용법

PROMPT.md 파일을 읽어서 claude --print --dangerously-skip-permissions로 반복 실행하는 Ralph Loop를 설정해줘. 무한 루프 스크립트를 만들고, PROMPT.md에 작업 내용을 작성한 뒤 실행하도록 안내해줘.

---

*수집 날짜: 2026-04-01 | 카테고리: Agent*
