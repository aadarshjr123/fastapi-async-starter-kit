from datetime import datetime, timedelta, timezone
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.auth.password_utils import hash_password, verify_password
from app.core.config import settings


class AuthService:
    """
    Handles user authentication, registration, and token management.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, name: str, password: str) -> dict:
        existing = await self.db.execute(select(User).where(User.name == name))
        if existing.scalar_one_or_none():
            raise ValueError("Username already taken")

        hashed = hash_password(password)
        user = User(name=name, hashed_password=hashed)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return {"id": user.id, "name": user.name}

    async def authenticate(self, username: str, password: str):
        result = await self.db.execute(select(User).where(User.name == username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
