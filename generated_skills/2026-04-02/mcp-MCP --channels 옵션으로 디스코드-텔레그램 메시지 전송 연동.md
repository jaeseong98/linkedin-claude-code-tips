---
name: mcp-MCP --channels 옵션으로 디스코드-텔레그램 메시지 전송 연동
description: MCP --channels 옵션으로 디스코드/텔레그램 메시지 전송 연동
type: skill
category: Mcp
source: LinkedIn (2026-04-02)
---

# MCP --channels 옵션으로 디스코드/텔레그램 메시지 전송 연동



---

## Usage

name: mcp-discord-telegram-channel
description: MCP --channels 옵션을 활용해 Claude Code 실행 결과를 Discord/Telegram 채널로 자동 전송하는 워크플로우 설정 가이드
instructions: |
  1. MCP 서버 설정에서 --channels 플래그를 추가한다.
  2. 대상 채널(Discord webhook URL 또는 Telegram bot token + chat_id)을 환경변수로 등록한다.
  3. Claude Code 실행 완료 후 결과 요약을 해당 채널로 전송하는 파이프라인을 구성한다.

---

*Collected: 2026-04-02 | Category: Mcp*