"""MCP 서버 - 저장된 LinkedIn 팁 데이터 조회 및 Skills 생성"""

import json
import os
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DATA_DIR = Path(__file__).parent.parent / "data"
SKILLS_DIR = Path(__file__).parent.parent / "generated_skills"

mcp = FastMCP("linkedin-tips")


def load_day_data(date_str: str) -> dict | None:
    path = DATA_DIR / f"{date_str}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def get_all_dates() -> list[str]:
    return sorted(
        [p.stem for p in DATA_DIR.glob("*.json")],
        reverse=True
    )


@mcp.tool()
def get_latest_tips(limit: int = 10) -> str:
    """가장 최근 저장된 날짜의 팁 목록을 반환합니다."""
    dates = get_all_dates()
    if not dates:
        return "저장된 데이터가 없습니다. 스케줄러를 먼저 실행하세요."

    data = load_day_data(dates[0])
    tips = []
    for post in data.get("posts", []):
        analysis = post.get("analysis", {})
        for tip in analysis.get("tips", []):
            tips.append({
                "tip_id": tip.get("tip_id", ""),
                "category": tip.get("category", "General"),
                "title": tip.get("title", ""),
                "content": tip.get("content", ""),
                "skill_worthy": tip.get("skill_worthy", False),
                "author": post.get("author", {}).get("name", "Unknown"),
                "post_url": post.get("url", "")
            })

    tips = tips[:limit]
    if not tips:
        return f"{dates[0]} 날짜에 추출된 팁이 없습니다."

    result = f"## {dates[0]} 팁 목록 ({len(tips)}개)\n\n"
    for t in tips:
        result += f"### [{t['category']}] {t['title']}\n"
        result += f"{t['content']}\n"
        result += f"- 출처: {t['author']} | {t['post_url']}\n"
        result += f"- Skill 후보: {'✓' if t['skill_worthy'] else '✗'}\n\n"

    return result


@mcp.tool()
def get_tips_by_date(date: str) -> str:
    """특정 날짜(YYYY-MM-DD)의 팁과 요약을 반환합니다."""
    data = load_day_data(date)
    if not data:
        available = get_all_dates()
        return f"{date} 데이터 없음. 사용 가능한 날짜: {', '.join(available[:5])}"

    summary = data.get("daily_summary", {})
    result = f"## {date} 일별 요약\n\n"
    result += f"- 수집: {summary.get('total_posts_scraped', 0)}개 / 관련: {summary.get('relevant_posts', 0)}개\n"
    result += f"- 팁: {summary.get('tips_extracted', 0)}개 / Skill 후보: {summary.get('skill_worthy_tips', 0)}개\n"
    result += f"- 카테고리: {summary.get('categories', [])}\n\n"
    result += "---\n\n"

    for post in data.get("posts", []):
        analysis = post.get("analysis", {})
        if not analysis.get("is_relevant", False):
            continue
        for tip in analysis.get("tips", []):
            result += f"### [{tip.get('category', 'General')}] {tip.get('title', '')}\n"
            result += f"{tip.get('content', '')}\n\n"

    return result


@mcp.tool()
def get_tips_by_category(category: str, days: int = 7) -> str:
    """카테고리별 팁을 최근 N일 범위에서 검색합니다.

    category: MCP, Skills, Hooks, Prompting, Agent, Config, General 중 하나
    days: 검색할 최근 일수 (기본 7)
    """
    dates = get_all_dates()[:days]
    found = []

    for date in dates:
        data = load_day_data(date)
        if not data:
            continue
        for post in data.get("posts", []):
            analysis = post.get("analysis", {})
            for tip in analysis.get("tips", []):
                if tip.get("category", "").lower() == category.lower():
                    found.append({
                        "date": date,
                        "tip": tip,
                        "author": post.get("author", {}).get("name", "Unknown"),
                        "url": post.get("url", "")
                    })

    if not found:
        return f"최근 {days}일 내 [{category}] 카테고리 팁 없음"

    result = f"## [{category}] 팁 ({len(found)}개, 최근 {days}일)\n\n"
    for item in found:
        result += f"### {item['tip']['title']} ({item['date']})\n"
        result += f"{item['tip']['content']}\n"
        result += f"- {item['author']} | {item['url']}\n\n"

    return result


@mcp.tool()
def search_tips(keyword: str, days: int = 30) -> str:
    """저장된 팁에서 키워드로 전문 검색합니다."""
    dates = get_all_dates()[:days]
    found = []
    kw = keyword.lower()

    for date in dates:
        data = load_day_data(date)
        if not data:
            continue
        for post in data.get("posts", []):
            analysis = post.get("analysis", {})
            for tip in analysis.get("tips", []):
                if kw in tip.get("title", "").lower() or kw in tip.get("content", "").lower():
                    found.append({
                        "date": date,
                        "tip": tip,
                        "author": post.get("author", {}).get("name", "Unknown")
                    })

    if not found:
        return f"'{keyword}' 관련 팁 없음 (최근 {days}일)"

    result = f"## '{keyword}' 검색 결과 ({len(found)}개)\n\n"
    for item in found:
        result += f"### [{item['tip']['category']}] {item['tip']['title']} ({item['date']})\n"
        result += f"{item['tip']['content']}\n"
        result += f"- {item['author']}\n\n"

    return result


@mcp.tool()
def generate_skill(tip_id: str) -> str:
    """tip_id에 해당하는 팁을 Claude Code Skill 파일로 생성합니다."""
    dates = get_all_dates()

    target_tip = None
    for date in dates:
        data = load_day_data(date)
        if not data:
            continue
        for post in data.get("posts", []):
            analysis = post.get("analysis", {})
            for tip in analysis.get("tips", []):
                if tip.get("tip_id") == tip_id:
                    target_tip = tip
                    break
            if target_tip:
                break
        if target_tip:
            break

    if not target_tip:
        return f"tip_id '{tip_id}'를 찾을 수 없습니다."

    if not target_tip.get("skill_worthy"):
        return f"이 팁은 Skill 생성 대상이 아닙니다: {target_tip.get('title', '')}"

    template = target_tip.get("skill_template", target_tip.get("content", ""))
    category = target_tip.get("category", "general").lower()
    title_slug = target_tip.get("title", "untitled").lower().replace(" ", "-")[:30]
    skill_name = f"{category}-{title_slug}"

    SKILLS_DIR.mkdir(exist_ok=True)
    skill_path = SKILLS_DIR / f"{skill_name}.md"

    skill_content = f"""---
name: {skill_name}
description: {target_tip.get('title', '')} (LinkedIn에서 수집된 Claude Code 팁)
---

{template}
"""
    skill_path.write_text(skill_content, encoding="utf-8")

    return f"Skill 생성 완료: {skill_path}\n\n내용:\n{skill_content}"


@mcp.tool()
def list_available_dates() -> str:
    """스크랩된 데이터가 있는 날짜 목록을 반환합니다."""
    dates = get_all_dates()
    if not dates:
        return "저장된 데이터 없음"

    result = f"## 저장된 데이터 ({len(dates)}일)\n\n"
    for date in dates:
        data = load_day_data(date)
        if data:
            s = data.get("daily_summary", {})
            result += f"- {date}: 팁 {s.get('tips_extracted', 0)}개 / Skill 후보 {s.get('skill_worthy_tips', 0)}개\n"

    return result


def main():
    mcp.run()


if __name__ == "__main__":
    main()
