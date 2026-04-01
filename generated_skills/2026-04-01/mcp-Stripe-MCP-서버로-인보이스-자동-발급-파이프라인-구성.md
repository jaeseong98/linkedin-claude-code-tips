---
name: mcp-Stripe-MCP-서버로-인보이스-자동-발급-파이프라인-구성
description: Stripe MCP 서버로 인보이스 자동 발급 파이프라인 구성
type: skill
category: MCP
source: LinkedIn (2026-04-01)
---

# Stripe MCP 서버로 인보이스 자동 발급 파이프라인 구성

Stripe 공식 MCP 서버를 Claude Code에 등록하면 Claude가 Stripe API를 직접 호출해 고객 생성, 인보이스 발급, 결제 상태 조회 등을 자동화할 수 있다. 보안을 위해 Stripe restricted key(읽기/쓰기 범위 분리)를 MCP 서버 환경변수로 주입하고, Claude에게 민감 작업 전 반드시 확인 단계를 거치도록 시스템 프롬프트에 명시하는 것이 권장된다.

---

## 사용법

Stripe MCP 서버를 Claude Code에 설정해줘. settings.json mcpServers에 Stripe MCP를 추가하고, STRIPE_API_KEY 환경변수를 restricted key로 설정한 뒤, 인보이스 자동 발급 워크플로우를 테스트해줘.

---

*수집 날짜: 2026-04-01 | 카테고리: MCP*
