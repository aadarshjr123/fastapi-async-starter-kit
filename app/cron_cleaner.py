"""
Scheduled Redis cleanup script (used by Docker job-cleaner service).
"""

import asyncio
import logging
from app.tasks import clean_old_jobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.cron_cleaner")


async def run_cleanup(interval: int = 300):
    """
    Periodically runs Redis job cleanup every `interval` seconds.
    """
    while True:
        logger.info("🧹 Running scheduled Redis cleanup...")
        clean_old_jobs()
        await asyncio.sleep(interval)


if __name__ == "__main__":
    try:
        asyncio.run(run_cleanup())
    except KeyboardInterrupt:
        logger.info("🛑 Cleanup job stopped by user.")
