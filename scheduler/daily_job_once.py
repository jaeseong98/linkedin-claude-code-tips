"""Task Scheduler / cron 용 1회 실행 진입점"""

import asyncio
from scheduler.daily_job import run_daily_scrape

if __name__ == "__main__":
    asyncio.run(run_daily_scrape())
