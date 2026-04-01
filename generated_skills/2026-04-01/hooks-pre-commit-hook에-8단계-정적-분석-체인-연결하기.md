---
name: hooks-pre-commit-hook에-8단계-정적-분석-체인-연결하기
description: pre-commit hook에 8단계 정적 분석 체인 연결하기
type: skill
category: Hooks
source: LinkedIn (2026-04-01)
---

# pre-commit hook에 8단계 정적 분석 체인 연결하기

Claude Code의 hooks 설정을 활용해 커밋 전에 tsc → eslint → sonarjs → knip → jscpd → semgrep 순서로 정적 분석 체인을 실행한다. AI가 생성한 코드가 실제로 품질 기준을 통과했는지 자동으로 검증되며, AI가 허위로 '통과했다'고 보고하는 상황을 원천 차단할 수 있다.

---

## 사용법

이 프로젝트에 pre-commit hook을 설정해줘. tsc, eslint, sonarjs, knip, jscpd, semgrep을 순서대로 실행하는 체인을 구성하고, Claude Code settings.json의 hooks 섹션에도 PostToolUse 또는 Stop 이벤트에 연동해줘.

---

*수집 날짜: 2026-04-01 | 카테고리: Hooks*
