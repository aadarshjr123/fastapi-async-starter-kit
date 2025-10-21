"""
Pydantic schemas for user requests and responses.
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr]

    model_config = ConfigDict(from_attributes=True)
