---
name: mcp-Task Master MCP로 PRD → 구조화 태스크 → 자동 실행 파이프라인 구성
description: Task Master MCP로 PRD → 구조화 태스크 → 자동 실행 파이프라인 구성
type: skill
category: Mcp
source: LinkedIn (2026-04-04)
---

# Task Master MCP로 PRD → 구조화 태스크 → 자동 실행 파이프라인 구성

Task Master MCP 서버를 연결하면 PRD(제품 요구 문서)를 투입해 의존성이 있는 구조화된 태스크를 자동 생성하고, Claude가 하나씩 순서대로 실행하는 개발 파이프라인을 구성할 수 있다.

---

## Usage

# Task Master PRD→태스크 실행 Skill

TRIGGER: 사용자가 PRD, 기능 명세, 또는 대규모 구현 계획을 제시할 때

## Instructions
1. PRD를 Task Master MCP에 전달하라.
2. 생성된 태스크 목록의 의존성 그래프를 확인하라.
3. 의존성 순서대로 각 태스크를 하나씩 실행하되, 각 태스크 완료 후 결과를 검증하라.
4. 실패한 태스크는 원인을 분석하고 재시도하라.

## Gotchas
- Task Master MCP 서버가 사전 설치·등록되어 있어야 한다.
- 태스크 간 의존성이 순환(circular)이면 오류가 발생한다.

---

*Collected: 2026-04-04 | Category: Mcp*