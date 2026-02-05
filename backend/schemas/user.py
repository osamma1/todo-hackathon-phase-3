from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: str
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    created_at: datetime


class UserUpdate(BaseModel):
    name: Optional[str] = None