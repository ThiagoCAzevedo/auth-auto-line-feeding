from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class UserRegisterIn(BaseModel):
    complete_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    roles: str | None = "user"


class UserOut(BaseModel):
    id: int
    complete_name: str
    email: EmailStr
    status: bool
    roles: str | None

    class Config:
        from_attributes = True


class UsersPage(BaseModel):
    items: List[UserOut]
    total: int
    page: int
    page_size: int


class UserUpdateIn(BaseModel):
    complete_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    roles: Optional[str] = None
    status: Optional[bool] = None
