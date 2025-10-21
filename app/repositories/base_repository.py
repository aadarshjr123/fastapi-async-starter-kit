"""
Base repository class providing reusable CRUD patterns.
All repositories for specific models should extend this class.
"""

from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class BaseRepository(Generic[T]):
    """
    A reusable async repository base class for SQLAlchemy models.
    """

    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def get_all(self) -> List[T]:
        """Fetch all records for the model."""
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id_: int) -> Optional[T]:
        """Fetch a record by its primary key."""
        return await self.db.get(self.model, id_)

    async def create(self, **kwargs) -> T:
        """Create a new record and commit to DB."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance: T) -> None:
        """Delete a record."""
        await self.db.delete(instance)
        await self.db.commit()
