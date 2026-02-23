from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
from typing import List, Optional
from helpers.users import UserValidators


# -- API CRUD --
class CreateUserSchema(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)

    @field_validator("email")
    def validate_email_domain(cls, value):
        ok, msg = UserValidators.validate_email_domain(value)
        if not ok:
            raise ValueError(msg)
        return value

    @field_validator("password")
    def validate_password_strength(cls, value):
        ok, msg = UserValidators.validate_password(value)
        if not ok:
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class UpdateUserSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=3)
    last_name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None)
    role: Optional[str] = None
    status: Optional[bool] = None

    @field_validator("email")
    def validate_email_domain(cls, value):
        ok, msg = UserValidators.validate_email_domain(value)
        if not ok:
            raise ValueError(msg)
        return value

    @field_validator("password")
    def validate_password_strength(cls, value):
        ok, msg = UserValidators.validate_password(value)
        if not ok:
            raise ValueError(msg)
        return value


class LoginUserSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)
    remember_me: bool = False


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ResendVerificationSchema(BaseModel):
    email: EmailStr


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str

# -- API RETURN (RESPONSE) --
class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: bool
    role: str | None

    class Config:
        from_attributes = True


class RegisterResponseSchema(BaseModel):
    message: str
    user: UserResponseSchema


class UserPaginationSchema(BaseModel):
    items: List[UserResponseSchema]
    total: int
    page: int
    page_size: int


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    remember_me: bool = False
    user: UserResponseSchema
