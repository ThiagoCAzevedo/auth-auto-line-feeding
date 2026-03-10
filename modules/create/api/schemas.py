from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator
from typing import Optional
from common.services.validators import UserValidators


class CreateUserSchema(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)

    @field_validator("email")
    def validate_email_domain(cls, value):
        UserValidators.validate_email_domain(value)
        return value

    @field_validator("password")
    def validate_password_strength(cls, value):
        UserValidators.validate_password(value)
        return value

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: bool
    role: Optional[str]

    class Config:
        from_attributes = True


class RegisterResponseSchema(BaseModel):
    message: str
    user: UserResponseSchema
