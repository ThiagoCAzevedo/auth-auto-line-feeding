from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from common.services.validators import UserValidators


class EmailSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: bool
    role: Optional[str]
    is_verified: bool

    class Config:
        from_attributes = True


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    remember_me: bool
    token_type: str
    user: UserResponseSchema


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
