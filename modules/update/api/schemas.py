from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from common.services.validators import UserValidators
from modules.access.api.schemas import UserResponseSchema


class UpdateUserSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = None

    @field_validator("email")
    def validate_email_domain(cls, value):
        if value:
            UserValidators.validate_email_domain(value)
        return value

    @field_validator("password")
    def validate_password_strength(cls, value):
        if value:
            UserValidators.validate_password(value)
        return value
