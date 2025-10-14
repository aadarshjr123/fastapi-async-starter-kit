from fastapi import FastAPI
from app.utils.rate_limiter import rate_limiter
from app.metrics.prometheus import instrumentator
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router
from redis.asyncio import Redis
import logging
import os

app = FastAPI(title="Async FastAPI Boilerplate", version="1.0.0")

# Middlewares
app.middleware("http")(rate_limiter)
instrumentator.instrument(app).expose(app)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = Redis(host="redis", port=6379, decode_responses=True)
    logging.info("✅ Connected to Redis")


@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.aclose()
