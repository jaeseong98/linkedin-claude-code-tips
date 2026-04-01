"""
Claude Code PostToolUse Hook - 파일 변경 자동 로거
Write/Edit 툴 사용 후 change_log.txt에 기록
"""

import json
import sys
from datetime import datetime
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "change_log.txt"


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "unknown")
        tool_input = data.get("tool_input", {})

        file_path = tool_input.get("file_path", tool_input.get("path", ""))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] {tool_name}: {file_path}\n"

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

    except Exception:
        pass  # hook 실패해도 Claude Code 작업에 영향 없어야 함


if __name__ == "__main__":
    main()
