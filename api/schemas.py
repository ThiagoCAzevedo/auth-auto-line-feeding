from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


# -- API CRUD --
class CreateUserSchema(BaseModel):
    complete_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    role: str | None = "user"


class UpdateUserSchema(BaseModel):
    complete_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    status: Optional[bool] = None
    role: Optional[str] = None


class LoginUserSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)


# -- API RETURN (RESPONSE) --
class UserResponseSchema(BaseModel):
    id: int
    complete_name: str
    email: EmailStr
    status: bool
    role: str | None

    class Config:
        from_attributes = True


class UserPaginationSchema(BaseModel):
    items: List[UserResponseSchema]
    total: int
    page: int
    page_size: int