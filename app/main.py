"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.lifecycle import lifespan
from app.core.router_registry import register_routers
from app.utils.rate_limiter import rate_limiter
from app.utils.profile_middleware import RequestProfilerMiddleware

app = FastAPI(
    title="Async FastAPI Starter",
    version="1.0.0",
    lifespan=lifespan,
    description="An async FastAPI backend with JWT Auth, Redis caching, RQ, and Prometheus monitoring.",
)

# === Middleware ===
app.middleware("http")(rate_limiter)
app.add_middleware(RequestProfilerMiddleware)

# === Routers ===
register_routers(app)

# === Monitoring ===
Instrumentator().instrument(app).expose(app)


# === Healthcheck ===
@app.get("/", tags=["System"])
async def root():
    return {"status": "ok", "message": "🚀 FastAPI Async Starter running!"}
