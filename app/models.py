"""
SQLAlchemy ORM models for the application.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import Base


class User(Base):
    """
    User model for authentication and user management.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
