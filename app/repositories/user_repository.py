"""
Repository for interacting with the User model.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for CRUD operations on User entities.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_name(self, name: str) -> Optional[User]:
        """
        Fetch a user by their username.
        """
        result = await self.db.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    async def get_all_users(self) -> List[User]:
        """
        Return all users in the database.
        (Alias for clarity in business layer)
        """
        return await super().get_all()

    async def create_user(self, name: str, email: Optional[str] = None) -> User:
        """
        Create and persist a new user.
        """
        return await super().create(name=name, email=email)
