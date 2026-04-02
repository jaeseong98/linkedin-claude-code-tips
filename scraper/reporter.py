"""날짜별 Skill 후보 리포트 생성"""

from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def generate_report(date: str, posts: list[dict]) -> Path:
    by_cat: dict[str, list[dict]] = {}
    for post in posts:
        analysis = post.get("analysis", {})
        if not analysis.get("is_relevant"):
            continue
        for tip in analysis.get("tips", []):
            if not tip.get("skill_worthy"):
                continue
            cat = tip.get("category", "etc")
            by_cat.setdefault(cat, []).append(tip)

    lines = [f"# {date} Skill Report", ""]

    for cat in sorted(by_cat):
        lines.append(f"## {cat}")
        lines.append("")
        for tip in by_cat[cat]:
            title = tip.get("title", "")
            desc = tip.get("description", "")
            template = tip.get("skill_template", "N/A")
            lines.extend([
                f"### {title}",
                "",
                desc,
                "",
                "**skill_template:**",
                "```",
                template,
                "```",
                "",
                "---",
                "",
            ])

    lines.extend(["## Summary", "", "| Category | Count |", "|----------|-------|"])
    total = 0
    for cat in sorted(by_cat):
        lines.append(f"| {cat} | {len(by_cat[cat])} |")
        total += len(by_cat[cat])
    lines.append(f"| **Total** | **{total}** |")

    report_path = REPORTS_DIR / f"{date}-skill-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
