from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: bool
    role: Optional[str]
    is_verified: Optional[bool]

    class Config:
        from_attributes = True


class UserPaginationSchema(BaseModel):
    items: List[UserResponseSchema]
    total: int
    page: int
    page_size: int
