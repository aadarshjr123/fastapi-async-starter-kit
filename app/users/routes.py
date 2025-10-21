"""
User API endpoints — thin controller layer using the UserService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.utils.logging_utils import log_time
from app.users.service import UserService
from app.users.schemas import UserCreate, UserRead
from app.utils import redis_manager

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead], summary="List all users")
@log_time
async def list_users(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all users (cached in Redis).
    """
    if not redis_manager.redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    service = UserService(db, redis_manager.redis_client)
    try:
        return await service.list_users()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {e}",
        )


@router.post("/", response_model=UserRead, summary="Create a new user")
@log_time
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user and clear cached user list.
    """
    if not redis_manager.redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")

    service = UserService(db, redis_manager.redis_client)
    try:
        return await service.create_user(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {e}",
        )
