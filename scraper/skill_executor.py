"""수집된 Skills 중 프로젝트에 적합한 1-2개를 추천하고 실행한 뒤 결과를 저장"""

import json
import logging
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

log = logging.getLogger("daily_job")

RESULTS_DIR = Path(__file__).parent.parent / "execution_results"
RESULTS_DIR.mkdir(exist_ok=True)

RECOMMEND_PROMPT = """다음은 오늘 수집된 Claude Code Skill 후보 목록이야.
이 프로젝트(LinkedIn Claude Code Tips Scraper)에 가장 유용하고 바로 실행 가능한 스킬 1~2개를 골라줘.

프로젝트 요약:
- Python + Playwright로 LinkedIn 크롤링
- Claude Agent SDK로 분석
- MCP 서버, 자동 스케줄러, Hooks, 마켓플레이스 구조

Skill 후보 목록:
{skills_list}

아래 JSON 형식으로만 응답해 (마크다운 없이):
{{
  "recommendations": [
    {{
      "title": "스킬 제목",
      "reason": "추천 이유 한 줄",
      "skill_template": "실행할 프롬프트 원문"
    }}
  ]
}}

최대 2개만 골라. 이 프로젝트에 실제로 적용 가능한 것만."""

EXECUTE_SYSTEM = """당신은 Claude Code 전문가입니다.
주어진 Skill 프롬프트를 현재 프로젝트에 맞게 실행하세요.
결과를 마크다운으로 정리해서 출력하세요.
프로젝트 경로: LinkedIn Claude Code Tips Scraper
기술 스택: Python 3.11+, Playwright, Claude Agent SDK, FastMCP, schedule"""


async def _query_claude(prompt: str, system: str = "") -> str:
    result_text = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(system_prompt=system) if system else None,
    ):
        if isinstance(message, ResultMessage):
            result_text = message.result
    return result_text


def _extract_skill_candidates(posts: list[dict]) -> list[dict]:
    """posts에서 skill_worthy 후보 추출"""
    skills = []
    for post in posts:
        analysis = post.get("analysis", {})
        if not analysis.get("is_relevant"):
            continue
        for tip in analysis.get("tips", []):
            if tip.get("skill_worthy") and tip.get("skill_template"):
                skills.append({
                    "title": tip.get("title", ""),
                    "category": tip.get("category", ""),
                    "skill_template": tip.get("skill_template", ""),
                })
    return skills


async def recommend_skills(posts: list[dict]) -> list[dict]:
    """skill_worthy 팁 중 프로젝트에 적합한 1-2개 추천"""
    skills = _extract_skill_candidates(posts)

    if not skills:
        return []

    # 후보가 1-2개면 추천 단계 스킵, 바로 전부 반환
    if len(skills) <= 2:
        log.info(f"Skill 후보 {len(skills)}개 - 추천 스킵, 전부 실행")
        return [
            {"title": s["title"], "reason": "유일한 후보", "skill_template": s["skill_template"]}
            for s in skills
        ]

    skills_text = "\n".join(
        f"- [{s['category']}] {s['title']}: {s['skill_template'][:100]}..."
        for s in skills
    )

    import re
    raw = await _query_claude(RECOMMEND_PROMPT.format(skills_list=skills_text))
    log.debug(f"추천 응답 원문: {raw[:300]}")

    match = re.search(r'\{[\s\S]*\}', raw)
    if not match:
        log.warning("추천 응답에서 JSON 파싱 실패 - 첫 2개 후보 자동 선택")
        return [
            {"title": s["title"], "reason": "자동 선택 (파싱 실패)", "skill_template": s["skill_template"]}
            for s in skills[:2]
        ]

    try:
        data = json.loads(match.group())
        return data.get("recommendations", [])
    except json.JSONDecodeError:
        log.warning("추천 응답 JSON 디코드 실패 - 첫 2개 후보 자동 선택")
        return [
            {"title": s["title"], "reason": "자동 선택 (파싱 실패)", "skill_template": s["skill_template"]}
            for s in skills[:2]
        ]


async def execute_skill(title: str, skill_template: str) -> str:
    """스킬 프롬프트를 실행하고 결과 반환"""
    prompt = f"""다음 Skill을 현재 프로젝트에 적용해줘.

## Skill: {title}

## 프롬프트:
{skill_template}

실행 결과를 마크다운으로 정리해서 출력해."""

    return await _query_claude(prompt, system=EXECUTE_SYSTEM)


async def recommend_and_execute(date: str, posts: list[dict]) -> Path | None:
    """추천 → 실행 → 결과 저장 전체 흐름"""
    print("[*] Skill 추천 중...")
    recommendations = await recommend_skills(posts)

    if not recommendations:
        print("  [*] 추천할 Skill 없음")
        return None

    date_dir = RESULTS_DIR / date
    date_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, rec in enumerate(recommendations[:2]):
        title = rec.get("title", f"skill_{i+1}")
        reason = rec.get("reason", "")
        template = rec.get("skill_template", "")

        print(f"  [{i+1}] 실행 중: {title}")
        print(f"      추천 이유: {reason}")

        output = await execute_skill(title, template)
        results.append({
            "title": title,
            "reason": reason,
            "skill_template": template,
            "output": output,
        })

    # 결과 리포트 저장
    report_lines = [
        f"# {date} Skill Execution Report",
        "",
        f"*Executed at: {datetime.now().isoformat()}*",
        "",
    ]

    for i, r in enumerate(results):
        report_lines.extend([
            f"## {i+1}. {r['title']}",
            "",
            f"**추천 이유:** {r['reason']}",
            "",
            f"**실행 프롬프트:**",
            "```",
            r["skill_template"],
            "```",
            "",
            "**실행 결과:**",
            "",
            r["output"],
            "",
            "---",
            "",
        ])

    report_path = date_dir / "execution-report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    # JSON 원본도 저장
    json_path = date_dir / "execution-data.json"
    json_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"  [OK] 실행 결과 저장: {report_path}")
    return report_path
