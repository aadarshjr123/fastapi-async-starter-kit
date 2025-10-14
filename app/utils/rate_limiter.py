# app/rate_limiter.py
import time
from fastapi import Request, HTTPException
from redis.asyncio import Redis

# Use DB 1 for rate limiting
r = Redis(host="redis", port=6379, db=1, decode_responses=True)

MAX_REQUESTS = 10
WINDOW_SIZE = 60  # seconds


async def rate_limiter(request: Request, call_next):
    ip = request.client.host
    window = int(time.time() // WINDOW_SIZE)
    key = f"rate:{ip}:{window}"

    # atomic incr + expire
    async with r.pipeline() as pipe:
        pipe.incr(key)
        pipe.expire(key, WINDOW_SIZE + 5)
        count, _ = await pipe.execute()

    if count > MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests. Try later.")

    return await call_next(request)
