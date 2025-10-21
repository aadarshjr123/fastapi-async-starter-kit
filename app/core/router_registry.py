"""
Centralized router registration for all API modules.
"""

from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.queue.routes import router as queue_router
from app.monitoring import router as monitoring_router


def register_routers(app: FastAPI) -> None:
    """
    Register all routers into the FastAPI application.
    """
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(queue_router)
    app.include_router(monitoring_router)
