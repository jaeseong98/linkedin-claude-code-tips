---
name: agent-Ralph-Loop-Claude-Code를-무한-루프로-돌려-자율-개발
description: Ralph Loop: Claude Code를 무한 루프로 돌려 자율 개발 에이전트로 활용하기
type: skill
category: Agent
source: LinkedIn (2026-04-01)
---

# Ralph Loop: Claude Code를 무한 루프로 돌려 자율 개발 에이전트로 활용하기

while true; do cat PROMPT.md | claude --print --dangerously-skip-permissions; done 스크립트를 사용하면 Claude Code가 PROMPT.md의 지시를 읽고 작업을 반복 수행한다. 실패해도 자동으로 재시도하며, 권한 확인 프롬프트를 건너뛰어 완전 자율 실행이 가능하다. YC 해커톤에서 하룻밤에 6개 저장소를 생성한 실증 사례가 있으며, Claude Code 공식 루프(/loop) 플러그인의 기반이 된 패턴이다.

---

## 사용법

PROMPT.md 파일을 현재 디렉토리에 생성하고, `while true; do cat PROMPT.md | claude --print --dangerously-skip-permissions; done` 을 실행하여 Ralph Loop를 시작합니다. PROMPT.md에는 달성할 목표와 완료 조건을 명확히 작성하세요. 루프는 Ctrl+C로 중단할 수 있습니다.

---

*수집 날짜: 2026-04-01 | 카테고리: Agent*
