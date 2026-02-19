from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from api.schemas import CreateUserSchema, UserResponseSchema, UpdateUserSchema, UserPaginationSchema, LoginUserSchema
from services.users import RegisterUsers, ReadUsers, UpdateUsers, DeleteUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions
from database.models.users import Users
from helpers.users.security import UserPassword


router = APIRouter()
log = logger("users")


@router.post("", summary="Login user", response_model=UserResponseSchema)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)):

    try:
        user = (
            db.query(Users)
            .filter(Users.email == payload.email)
            .first()
        )

        if not user:
            raise HTTP_Exceptions.http_404("User not found.")

        if not UserPassword.verify_password(payload.password, user.password):
            raise HTTP_Exceptions.http_401("Invalid password.")

        log.info(f"User logged in successfully: {user.email}")

        return user

    except HTTPException as e:
        raise e

    except Exception as e:
        log.error(f"Error while logging in: {e}")
        raise HTTP_Exceptions.http_500("Internal Server Error")