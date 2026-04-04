"""분석 완료된 posts에서 skill_worthy 팁을 .md 파일로 생성"""

import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "generated_skills"


def generate_skill_files(date: str, posts: list[dict]) -> int:
    """generated_skills/{date}/ 에 스킬 파일 생성. 생성된 개수 반환."""
    date_dir = SKILLS_DIR / date
    date_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for post in posts:
        analysis = post.get("analysis", {})
        if not analysis.get("is_relevant"):
            continue
        for tip in analysis.get("tips", []):
            if not tip.get("skill_worthy") or not tip.get("skill_template"):
                continue

            title = tip.get("title", "untitled")
            category = tip.get("category", "etc").lower()
            safe_title = re.sub(r'[/\\:*?<>|"]', '-', title[:60])
            filename = f"{category}-{safe_title}.md"
            filepath = date_dir / filename

            desc = tip.get("description", "") or tip.get("content", "")
            template = tip.get("skill_template", "N/A")

            lines = [
                "---",
                f"name: {filename.replace('.md', '')}",
                f"description: {title}",
                "type: skill",
                f"category: {category.capitalize()}",
                f"source: LinkedIn ({date})",
                "---",
                "",
                f"# {title}",
                "",
                desc,
                "",
                "---",
                "",
                "## Usage",
                "",
                template,
                "",
                "---",
                "",
                f"*Collected: {date} | Category: {category.capitalize()}*",
            ]

            filepath.write_text("\n".join(lines), encoding="utf-8")
            count += 1

    return count
