# 2026-04-04 Skill Report

## Agent

### cmux·figaro·claude-squad로 Claude 에이전트 병렬 실행 및 오케스트레이션

cmux는 여러 Claude 에이전트를 병렬 실행하고, figaro는 데스크탑에서 에이전트 함대를 오케스트레이션하며, claude-squad는 터미널에서 병렬 세션을 관리한다. 대규모 작업을 분할·병렬 처리할 때 유용하다.

**skill_template:**
```
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
```

---

## MCP

### Context7 MCP로 최신 라이브러리 문서를 컨텍스트에 주입해 환각 제거

Context7 MCP 서버를 연결하고 프롬프트에 'use context7' 한 줄만 추가하면 최신 라이브러리 문서가 LLM 컨텍스트에 자동 주입되어 환각(hallucinated) API 호출을 방지할 수 있다.

**skill_template:**
```
# Context7 최신 문서 주입 Skill

TRIGGER: 사용자가 외부 라이브러리/프레임워크 코드를 작성하거나 API 사용법을 물을 때

## Instructions
1. 대상 라이브러리를 식별하라.
2. Context7 MCP 도구를 호출해 해당 라이브러리의 최신 공식 문서를 컨텍스트에 주입하라.
3. 주입된 문서를 기반으로만 API 사용 코드를 생성하라. 문서에 없는 API는 사용하지 마라.

## Gotchas
- Context7 MCP 서버가 설정되어 있어야 한다.
- 매우 최신 릴리스(수 시간 이내)는 반영이 안 될 수 있다.
```

---

### Task Master MCP로 PRD → 구조화 태스크 → 자동 실행 파이프라인 구성

Task Master MCP 서버를 연결하면 PRD(제품 요구 문서)를 투입해 의존성이 있는 구조화된 태스크를 자동 생성하고, Claude가 하나씩 순서대로 실행하는 개발 파이프라인을 구성할 수 있다.

**skill_template:**
```
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
```

---

## Skills

### Brand Guidelines 스킬로 브랜드를 인코딩해 모든 출력에 자동 적용

Brand Guidelines 스킬을 설치하면 브랜드 가이드라인을 스킬로 인코딩하여 Claude의 모든 출력에 브랜드 톤·스타일이 자동 적용된다.

**skill_template:**
```
# Brand Guidelines Skill

TRIGGER: 사용자가 마케팅 카피, 블로그, 이메일, 소셜 미디어 콘텐츠 작성을 요청할 때

## Instructions
1. 프로젝트 루트의 `brand-guidelines.md` 또는 CLAUDE.md 내 브랜드 섹션을 참조하라.
2. 톤(Tone), 보이스(Voice), 금지 표현, 필수 표현 규칙을 모든 출력에 적용하라.
3. 출력 전 브랜드 체크리스트를 내부적으로 검증하라.

## Gotchas
- 브랜드 가이드라인 파일이 없으면 사용자에게 먼저 작성을 요청하라.
- 다국어 콘텐츠 시 언어별 톤 차이를 고려하라.
```

---

## Summary

| Category | Count |
|----------|-------|
| Agent | 1 |
| MCP | 2 |
| Skills | 1 |
| **Total** | **4** |