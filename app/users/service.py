import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from prometheus_client import Counter

cache_hits = Counter("cache_hits_total", "Number of cache hits")
cache_misses = Counter("cache_misses_total", "Number of cache misses")


async def get_all_users(db: AsyncSession, r):
    cache_key = "users"
    cached = await r.get(cache_key)
    if cached:
        cache_hits.inc()
        return json.loads(cached)

    cache_misses.inc()
    result = await db.execute(select(User))
    users = result.scalars().all()
    data = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    await r.set(cache_key, json.dumps(data), ex=60)
    return data


async def create_user(db: AsyncSession, name: str, email: str, r):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await r.delete("users")
    return user
