# Claude Code Hooks

이 디렉토리는 Claude Code의 PostToolUse 훅 스크립트를 관리합니다.

## file_logger.py

Write/Edit 툴 사용 후 자동으로 `change_log.txt`에 기록합니다.

설치 위치: `~/.claude/settings.json`의 `hooks.PostToolUse`

## 로그 확인

```bash
cat change_log.txt
```
