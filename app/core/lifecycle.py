"""
Application startup and shutdown lifecycle management.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.utils import redis_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for startup and shutdown events.
    Initializes and gracefully closes async resources.
    """
    try:
        await redis_manager.init_redis()
        logger.info("🚀 Redis connected successfully.")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")

    yield  # ---- Application runs here ----

    try:
        await redis_manager.close_redis()
        logger.info("🧹 Redis connection closed.")
    except Exception as e:
        logger.warning(f"⚠️ Error while closing Redis: {e}")
