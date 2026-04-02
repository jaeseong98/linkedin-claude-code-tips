"""Claude Agent SDK로 게시글에서 팁 추출 및 분류 (API 키 불필요, Claude Code 인증 사용)"""

import json
import re
import uuid

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

ANALYSIS_PROMPT = """다음 LinkedIn 게시글을 분석해줘.

게시글 내용:
{content}

아래 JSON 형식으로만 응답해줘 (마크다운 코드블록 없이, JSON 텍스트만):
{{
  "is_relevant": true 또는 false,
  "categories": ["MCP", "Skills", "Hooks", "Prompting", "Agent", "Config", "General" 중 해당하는 것들],
  "tips": [
    {{
      "tip_id": "여기에 uuid 문자열",
      "category": "카테고리",
      "title": "팁 제목 한 줄",
      "content": "팁 내용 구체적으로",
      "skill_worthy": true 또는 false,
      "skill_template": "skill_worthy가 true일 때 Skill 프롬프트 내용, 아니면 빈 문자열"
    }}
  ],
  "summary": "게시글 요약 1-2문장"
}}

Claude Code 관련 실용적 팁이 없으면 is_relevant를 false로, tips를 빈 배열로."""


async def analyze_post(post: dict) -> dict:
    """단일 게시글 분석 (Claude Agent SDK 사용)"""
    content = post.get("content", "")
    if not content or len(content) < 50:
        return {"is_relevant": False, "categories": [], "tips": [], "summary": "내용 없음"}

    prompt = ANALYSIS_PROMPT.format(content=content[:3000])

    try:
        result_text = ""
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                system_prompt="당신은 Claude Code 관련 LinkedIn 게시글을 분석하는 전문가입니다. JSON만 출력하세요. 마크다운 없이 순수 JSON만.",
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result

        # JSON 파싱 (마크다운 코드블록 및 다양한 형태 처리)
        raw = result_text.strip()
        match = re.search(r'\{[\s\S]*\}', raw)
        if match:
            raw = match.group()
        analysis = json.loads(raw)

        # tip_id 보장
        for tip in analysis.get("tips", []):
            if not tip.get("tip_id") or tip["tip_id"] in ("여기에 uuid 문자열", "uuid-형식"):
                tip["tip_id"] = str(uuid.uuid4())

        return analysis

    except Exception as e:
        print(f"[!] 분석 실패: {e}")
        return {"is_relevant": False, "categories": [], "tips": [], "summary": f"분석 오류: {e}"}


async def analyze_posts_batch(posts: list[dict]) -> list[dict]:
    """게시글 목록 일괄 분석"""
    import asyncio

    results = []
    for i, post in enumerate(posts):
        author = post.get("author", {}).get("name", "?")
        print(f"[*] 분석 중 ({i+1}/{len(posts)}): {author}", flush=True)
        analysis = await analyze_post(post)
        results.append({**post, "analysis": analysis})
        await asyncio.sleep(0.3)

    return results


def build_daily_summary(analyzed_posts: list[dict]) -> dict:
    """일별 요약 생성"""
    relevant = [p for p in analyzed_posts if p["analysis"]["is_relevant"]]
    all_tips = [tip for p in relevant for tip in p["analysis"]["tips"]]
    skill_worthy = [t for t in all_tips if t.get("skill_worthy")]

    category_counts: dict[str, int] = {}
    for tip in all_tips:
        cat = tip.get("category", "General")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "total_posts_scraped": len(analyzed_posts),
        "relevant_posts": len(relevant),
        "tips_extracted": len(all_tips),
        "skill_worthy_tips": len(skill_worthy),
        "categories": category_counts,
    }
