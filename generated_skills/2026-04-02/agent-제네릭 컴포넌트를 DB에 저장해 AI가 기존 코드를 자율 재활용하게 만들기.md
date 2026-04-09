---
name: agent-제네릭 컴포넌트를 DB에 저장해 AI가 기존 코드를 자율 재활용하게 만들기
description: 제네릭 컴포넌트를 DB에 저장해 AI가 기존 코드를 자율 재활용하게 만들기
type: skill
category: Agent
source: LinkedIn (2026-04-02)
---

# 제네릭 컴포넌트를 DB에 저장해 AI가 기존 코드를 자율 재활용하게 만들기



---

## Usage

PostgreSQL 등 로컬 DB에 제네릭 컴포넌트(유틸 함수, 공통 모듈, 아키텍처 패턴)를 저장하고, Claude Code 에이전트가 새 태스크 수행 전 DB에서 관련 기존 코드를 검색·로드하여 재활용하는 파이프라인을 구성하라. MCP 서버를 통해 DB 조회 도구를 에이전트에 연결하고, CLAUDE.md에 '새 기능 구현 전 반드시 기존 제네릭 컴포넌트 DB를 조회할 것'이라는 규칙을 명시하라.

---

*Collected: 2026-04-02 | Category: Agent*