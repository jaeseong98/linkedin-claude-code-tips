---
name: agent-cmux·figaro·claude-squad로 Claude 에이전트 병렬 실행 및 오케스트레이션
description: cmux·figaro·claude-squad로 Claude 에이전트 병렬 실행 및 오케스트레이션
type: skill
category: Agent
source: LinkedIn (2026-04-04)
---

# cmux·figaro·claude-squad로 Claude 에이전트 병렬 실행 및 오케스트레이션

cmux는 여러 Claude 에이전트를 병렬 실행하고, figaro는 데스크탑에서 에이전트 함대를 오케스트레이션하며, claude-squad는 터미널에서 병렬 세션을 관리한다. 대규모 작업을 분할·병렬 처리할 때 유용하다.

---

## Usage

# 멀티 에이전트 병렬 실행 Skill

TRIGGER: 사용자가 대규모 리팩토링, 다중 파일 동시 수정, 또는 독립적인 여러 태스크를 병렬로 처리하고 싶을 때

## Instructions
1. 작업을 독립적으로 실행 가능한 단위로 분할하라.
2. 각 단위를 별도 Agent로 위임하되, isolation: worktree 옵션으로 컨텍스트를 격리하라.
3. 모든 에이전트 완료 후 결과를 통합하고 충돌을 해결하라.

## Tools
- cmux: CLI 기반 병렬 에이전트 실행
- claude-squad: 터미널 병렬 세션 관리
- figaro: 데스크탑 GUI 오케스트레이션

## Gotchas
- 에이전트 간 같은 파일을 수정하면 merge conflict가 발생한다. 파일 단위로 분리하라.
- 병렬 에이전트 수가 많으면 API 비용이 비례 증가한다.

---

*Collected: 2026-04-04 | Category: Agent*