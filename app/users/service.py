"""
Service layer for user management with Redis caching and Prometheus metrics.
"""

import json
import logging
from prometheus_client import Counter
from app.repositories.user_repository import UserRepository
from app.users.schemas import UserCreate, UserRead

logger = logging.getLogger(__name__)

# === Prometheus Metrics ===
cache_hits = Counter("cache_hits_total", "Number of cache hits")
cache_misses = Counter("cache_misses_total", "Number of cache misses")


class UserService:
    """
    Handles all user-related business logic,
    combining repository operations with Redis caching.
    """

    def __init__(self, db, redis):
        self.repo = UserRepository(db)
        self.redis = redis

    async def list_users(self) -> list[UserRead]:
        """
        Retrieve all users, using Redis cache when available.
        """
        cache_key = "users"
        cached_data = await self.redis.get(cache_key)

        if cached_data:
            cache_hits.inc()
            logger.debug("Cache hit for 'users'")
            return json.loads(cached_data)

        cache_misses.inc()
        logger.debug("Cache miss for 'users', fetching from DB")
        users = await self.repo.get_all_users()
        data = [UserRead.from_orm(u).dict() for u in users]

        # Cache for 60 seconds
        await self.redis.set(cache_key, json.dumps(data), ex=60)
        return data

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Create a new user and invalidate cache.
        """
        logger.info(f"Creating user '{user_data.name}'")
        user = await self.repo.create_user(name=user_data.name, email=user_data.email)
        await self.redis.delete("users")
        return UserRead.from_orm(user)
