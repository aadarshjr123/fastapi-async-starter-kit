from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.logging_utils import log_time
from app.main import redis_client
from app.users.service import get_all_users, create_user

router = APIRouter()


@router.get("/", summary="Get all users")
@log_time
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db, redis_client)


@router.post("/", summary="Create a new user")
@log_time
async def add_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    return await create_user(db, name, email, redis_client)
