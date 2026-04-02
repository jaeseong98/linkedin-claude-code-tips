"""
새로 생성된 Skills를 claude-code-skills 마켓플레이스 레포에 자동 publish
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CATEGORY_MAP = {
    "agent":     "agent",
    "config":    "config",
    "hooks":     "hooks",
    "mcp":       "mcp",
    "prompting": "prompting",
    "skills":    "workflow",
}


def _get_category(filename: str) -> str | None:
    prefix = filename.split("-")[0].lower()
    return CATEGORY_MAP.get(prefix)


def _run_git(cmd: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8"
    )
    return result.returncode, result.stdout + result.stderr


def publish_skills(date: str) -> dict:
    """
    generated_skills/{date}/ 의 .md 파일을 마켓플레이스 레포로 복사 후 push.

    Returns:
        {"copied": int, "skipped": int, "pushed": bool, "error": str | None}
    """
    marketplace_dir = Path(
        os.getenv("MARKETPLACE_REPO_PATH", str(Path.home() / "claude-code-skills"))
    )
    skills_src = Path(__file__).parent.parent / "generated_skills" / date

    result = {"copied": 0, "skipped": 0, "pushed": False, "error": None}

    if not skills_src.exists():
        result["error"] = f"생성된 Skills 없음: {skills_src}"
        return result

    if not marketplace_dir.exists():
        result["error"] = f"마켓플레이스 레포 없음: {marketplace_dir}"
        return result

    # 파일 복사
    for skill_file in skills_src.glob("*.md"):
        category = _get_category(skill_file.name)
        if not category:
            print(f"  [?] 카테고리 미분류: {skill_file.name}")
            result["skipped"] += 1
            continue

        dest_dir = marketplace_dir / "skills" / category
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / skill_file.name

        shutil.copy2(skill_file, dest)
        print(f"  [+] {category}/{skill_file.name}")
        result["copied"] += 1

    if result["copied"] == 0:
        print("  [*] 새 Skills 없음, push 생략")
        return result

    # Git commit & push
    code, out = _run_git(["git", "add", "skills/"], marketplace_dir)
    if code != 0:
        result["error"] = f"git add 실패: {out}"
        return result

    commit_msg = f"feat: {date} Skills {result['copied']}개 추가"
    code, out = _run_git(["git", "commit", "-m", commit_msg], marketplace_dir)
    if code != 0:
        # 변경 없으면 commit 실패 — 정상 케이스
        if "nothing to commit" in out:
            print("  [*] 변경 없음, push 생략")
            return result
        result["error"] = f"git commit 실패: {out}"
        return result

    code, out = _run_git(["git", "push"], marketplace_dir)
    if code != 0:
        result["error"] = f"git push 실패: {out}"
        return result

    result["pushed"] = True
    print(f"  [OK] marketplace push done ({result['copied']} skills)")
    return result
