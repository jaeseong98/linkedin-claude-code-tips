"""매일 지정 시각에 LinkedIn 크롤링 + 분석 + 저장"""

import asyncio
import json
import logging
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import schedule
import time

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logger(date: str) -> logging.Logger:
    """날짜별 로그 파일 + 콘솔 동시 출력 로거 설정"""
    logger = logging.getLogger("daily_job")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 파일 핸들러 (DEBUG 레벨 — 모든 로그)
    fh = logging.FileHandler(LOG_DIR / f"{date}.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
    ))
    logger.addHandler(fh)

    # 콘솔 핸들러 (INFO 레벨, cp949 안전)
    ch = logging.StreamHandler(
        open(sys.stdout.fileno(), mode='w', encoding='utf-8', errors='replace', closefd=False)
    )
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(ch)

    return logger


def get_keywords() -> list[str]:
    raw = os.getenv("SEARCH_KEYWORDS", "Claude Code,MCP tips,Claude Code skills")
    return [k.strip() for k in raw.split(",") if k.strip()]


def load_previous_contents() -> set[str]:
    """이전 날짜 JSON들에서 content[:100] 키를 모아 중복 판단용 set 생성"""
    seen = set()
    for json_file in DATA_DIR.glob("*.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            for post in data.get("posts", []):
                content = post.get("content", "")
                if content:
                    seen.add(content[:100])
        except Exception:
            continue
    return seen


async def run_daily_scrape():
    today = datetime.now().strftime("%Y-%m-%d")
    log = setup_logger(today)
    output_path = DATA_DIR / f"{today}.json"

    log.info("=" * 50)
    log.info(f"일별 스크랩 시작: {datetime.now().isoformat()}")
    log.info("=" * 50)

    if output_path.exists():
        log.warning(f"{today} 데이터 이미 존재함. 덮어쓸게요.")

    keywords = get_keywords()
    log.info(f"검색 키워드: {keywords}")

    # ── Step 1: 크롤링 ──
    try:
        from scraper.linkedin_scraper import LinkedInScraper
        scraper = LinkedInScraper()
        raw_posts = await scraper.scrape_all_keywords(keywords)
        log.info(f"Step 1 완료: {len(raw_posts)}개 게시글 수집")
    except Exception:
        log.error(f"Step 1 크롤링 실패:\n{traceback.format_exc()}")
        return

    # ── Step 1.5: 중복 제거 ──
    previous_contents = load_previous_contents()
    before = len(raw_posts)
    raw_posts = [p for p in raw_posts if p.get("content", "")[:100] not in previous_contents]
    deduped = before - len(raw_posts)
    if deduped:
        log.info(f"이전 수집분과 중복 {deduped}개 제거 -> {len(raw_posts)}개 신규")

    if not raw_posts:
        log.warning("수집된 신규 게시글 0개 - 이후 단계 스킵 없이 빈 결과 저장")

    # ── Step 2: Claude 분석 ──
    try:
        from scraper.analyzer import analyze_posts_batch, build_daily_summary
        log.info("Step 2: Claude API 분석 시작...")
        analyzed_posts = await analyze_posts_batch(raw_posts)
        log.info(f"Step 2 완료: {len(analyzed_posts)}개 분석")
    except Exception:
        log.error(f"Step 2 분석 실패:\n{traceback.format_exc()}")
        analyzed_posts = raw_posts  # 분석 실패 시 원본으로 계속

    # ── Step 3: 일별 요약 ──
    daily_summary = build_daily_summary(analyzed_posts)

    # ── Step 4: JSON 저장 ──
    output = {
        "date": today,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "query_keywords": keywords,
        "posts": analyzed_posts,
        "daily_summary": daily_summary
    }

    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    log.info(f"Step 4 완료: {output_path}")
    log.info(f"  수집: {daily_summary['total_posts_scraped']}개")
    log.info(f"  관련: {daily_summary['relevant_posts']}개")
    log.info(f"  팁:   {daily_summary['tips_extracted']}개")
    log.info(f"  Skill 후보: {daily_summary['skill_worthy_tips']}개")
    log.info(f"  카테고리: {daily_summary['categories']}")

    # ── Step 5: Skill 리포트 생성 ──
    try:
        log.info("Step 5: Skill 리포트 생성 중...")
        from scraper.reporter import generate_report
        report_path = generate_report(today, analyzed_posts)
        log.info(f"Step 5 완료: {report_path}")
    except Exception:
        log.error(f"Step 5 리포트 생성 실패:\n{traceback.format_exc()}")

    # ── Step 6: Skill 파일 생성 ──
    try:
        log.info("Step 6: Skill 파일 생성 중...")
        from scraper.skill_generator import generate_skill_files
        skill_count = generate_skill_files(today, analyzed_posts)
        log.info(f"Step 6 완료: {skill_count}개 Skill 파일 -> generated_skills/{today}/")
    except Exception:
        log.error(f"Step 6 Skill 파일 생성 실패:\n{traceback.format_exc()}")

    # ── Step 7: 추천 Skill 실행 + 결과 저장 ──
    try:
        log.info("Step 7: 추천 Skill 실행 중...")
        from scraper.skill_executor import recommend_and_execute
        exec_path = await recommend_and_execute(today, analyzed_posts)
        if exec_path:
            log.info(f"Step 7 완료: {exec_path}")
        else:
            log.info("Step 7 완료: 추천할 Skill 없음")
    except Exception:
        log.error(f"Step 7 Skill 실행 실패:\n{traceback.format_exc()}")

    # ── Step 8: 마켓플레이스 publish ──
    try:
        log.info("Step 8: 마켓플레이스 publish 중...")
        from scraper.publisher import publish_skills
        pub_result = publish_skills(today)
        if pub_result["error"]:
            log.error(f"Step 8 publish 실패: {pub_result['error']}")
        elif pub_result["pushed"]:
            log.info(f"Step 8 완료: {pub_result['copied']}개 Skills push")
        else:
            log.info("Step 8 완료: 새 Skills 없음")
    except Exception:
        log.error(f"Step 8 publish 실패:\n{traceback.format_exc()}")

    log.info("=" * 50)
    log.info(f"파이프라인 완료: {datetime.now().isoformat()}")
    log.info("=" * 50)


def job():
    asyncio.run(run_daily_scrape())


def main():
    run_time = os.getenv("DAILY_RUN_TIME", "09:00")
    print(f"[스케줄러 시작] 매일 {run_time}에 실행됩니다.")
    print("Ctrl+C로 종료")

    schedule.every().day.at(run_time).do(job)

    # 시작 시 즉시 한 번 실행하려면 아래 주석 해제
    # job()

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
