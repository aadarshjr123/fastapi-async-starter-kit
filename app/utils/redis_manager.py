"""
Centralized Redis connection management utilities.
"""

import asyncio
import logging
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger("app.utils.redis")

redis_client: Redis | None = None


async def init_redis(retries: int = 10, delay: float = 2.0):
    """
    Initialize the global Redis client with retry logic.
    """
    global redis_client
    for attempt in range(1, retries + 1):
        try:
            client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
            await client.ping()
            redis_client = client
            logger.info(f"✅ Redis connected (attempt {attempt})")
            return
        except Exception as e:
            logger.warning(f"⚠️ Redis not ready (attempt {attempt}/{retries}): {e}")
            await asyncio.sleep(delay)
    logger.error("❌ Failed to connect to Redis after retries.")


async def close_redis():
    """
    Gracefully close the Redis connection on shutdown.
    """
    global redis_client
    if redis_client:
        await redis_client.aclose()
        logger.info("🧹 Redis connection closed.")
        redis_client = None
