---
name: mcp-MCP-세션마다-재학습-오버헤드를-줄이려면-데이터-소스를-정규화된-JSO
description: MCP 세션마다 재학습 오버헤드를 줄이려면 데이터 소스를 정규화된 JSON/Markdown으로 미리 추출하라
type: skill
category: MCP
source: LinkedIn (2026-04-01)
---

# MCP 세션마다 재학습 오버헤드를 줄이려면 데이터 소스를 정규화된 JSON/Markdown으로 미리 추출하라

Claude Code에서 MCP를 사용할 때, 매 세션마다 대용량 원본 파일(예: Figma 전체 파일)을 MCP가 재파싱하면 비용과 시간이 낭비된다. 해결책은 원본 데이터를 한 번만 정제하여 경량 JSON/Markdown으로 추출하고, MCP가 이 정규화된 파일만 참조하도록 설정하는 것이다. Claude Code의 MCP 서버 설정 시 `--context-file` 또는 custom resource URI로 정적 포털 엔드포인트를 지정하면 팀 전체가 동일한 SSoT(Single Source of Truth)를 참조한다.

---

## 사용법

우리 프로젝트의 디자인 시스템 또는 대용량 컨텍스트 파일을 경량 JSON/Markdown으로 정규화하고, Claude Code MCP 서버가 이 파일만 참조하도록 설정해줘. 원본 파일 경로: [원본 파일 경로], 출력 경로: [output 경로]. 정규화 시 토큰, 컴포넌트 구조, 모드(Mode) 정보를 포함하고, MCP resource URI로 등록하는 설정 코드도 함께 생성해줘.

---

*수집 날짜: 2026-04-01 | 카테고리: MCP*
