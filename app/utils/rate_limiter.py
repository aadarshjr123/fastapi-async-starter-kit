"""
Simple Redis-based rate limiter middleware for FastAPI.
"""

import time
import logging
from fastapi import Request, HTTPException
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger("app.utils.rate_limiter")

# Configurable parameters (can be moved to env)
MAX_REQUESTS = 100
WINDOW_SIZE = 60  # seconds

# Use Redis DB 1 for rate limiting
redis_client = Redis.from_url(f"{settings.REDIS_URL}/1", decode_responses=True)


async def rate_limiter(request: Request, call_next):
    """
    Rate-limit incoming requests based on client IP and fixed window.
    """
    ip = request.client.host
    window = int(time.time() // WINDOW_SIZE)
    key = f"rate:{ip}:{window}"

    try:
        async with redis_client.pipeline() as pipe:
            pipe.incr(key)
            pipe.expire(key, WINDOW_SIZE + 5)
            count, _ = await pipe.execute()

        if count > MAX_REQUESTS:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

    except Exception as e:
        logger.error(f"Rate limiter failed: {e}")

    return await call_next(request)
