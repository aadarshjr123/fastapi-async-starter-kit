"""
Redis Queue (RQ) setup and connection factory.
"""

import redis
from rq import Queue
from app.core.config import settings

# Global Redis connection for RQ
redis_conn = redis.Redis.from_url(settings.REDIS_URL, decode_responses=False)

# Default queue instance
queue = Queue("default", connection=redis_conn)
