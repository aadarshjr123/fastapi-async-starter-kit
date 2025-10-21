"""
Worker utility for connecting to the Redis queue.
"""

from rq import Queue
import redis
from app.core.config import settings

# Reusable Redis connection
redis_conn = redis.Redis.from_url(settings.REDIS_URL, decode_responses=False)

# Default queue (used by JobService)
queue = Queue("default", connection=redis_conn)
