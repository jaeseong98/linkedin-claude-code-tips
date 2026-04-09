# 2026-04-07 Skill Report

## Agent

### tmux 기반 멀티 Claude Code 오케스트레이션으로 사람 병목 제거

여러 Claude Code 인스턴스를 tmux session/window/pane 위계로 나누어 운영하면, 별도 프로토콜(MCP, A2A 등) 없이 4개의 tmux pane으로 50개 이상의 Claude Code를 동시에 관리할 수 있다. 세션 간 메시징은 tmux send-keys로 처리하고, 큰 맥락은 파일 경로와 함께 핸드오프하면 대부분의 에이전트 간 통신이 가능하다.

**skill_template:**
```
# tmux 기반 멀티 Claude Code 오케스트레이터 구성

## 언제 사용하나
여러 Claude Code 에이전트를 동시에 운영하면서 에이전트 간 맥락 전달이 필요할 때. 사람이 컨텍스트 스위칭 병목이 되는 상황을 해소하고 싶을 때.

## 구성 방법
1. tmux session/window/pane으로 에이전트 위계를 설계한다 (조직구조처럼 정보의 위계를 둔다)
2. 각 pane에서 독립적인 Claude Code 인스턴스를 실행한다
3. 세션 간 메시징은 `tmux send-keys -t <target-pane>` 으로 처리한다
4. 큰 맥락은 파일로 작성 후 파일 경로와 함께 핸드오프한다
5. 원격 에이전트가 필요하면 tmux 세션에 ssh를 열어 리모트 Claude Code와 통신한다

## Gotchas
- tmux send-keys의 문자열 이스케이프에 주의 (특수문자, 줄바꿈)
- 에이전트 수가 많아지면 pane 관리가 복잡해지므로 session/window/pane 네이밍 컨벤션을 미리 정할 것
- 각 에이전트의 컨텍스트 윈도우 한계를 고려해 핸드오프 파일 크기를 적절히 관리할 것
```

---

## Summary

| Category | Count |
|----------|-------|
| Agent | 1 |
| **Total** | **1** |