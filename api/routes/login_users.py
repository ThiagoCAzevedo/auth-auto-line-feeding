from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas import LoginResponseSchema
from api.schemas import LoginUserSchema
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions
from database.models.users import Users
from helpers.users.security import UserPassword
from helpers.security.jwt import JWTHandler


router = APIRouter()
log = logger("users")


@router.post("", response_model=LoginResponseSchema)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.email == payload.email).first()

        if not user:
            raise HTTP_Exceptions.http_404("User not found.")

        if not UserPassword.verify_password(payload.password, user.password):
            raise HTTP_Exceptions.http_401("Invalid password.")

        refresh_days = 30 if payload.remember_me else 1

        access_token = JWTHandler.create_access_token(
            {"sub": str(user.id), "email": user.email}
        )

        refresh_token = JWTHandler.create_refresh_token(
            {"sub": str(user.id), "email": user.email},
            expires_days=refresh_days
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "remember_me": payload.remember_me,
            "token_type": "bearer",
            "user":user
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Login error: {e}")
        raise HTTP_Exceptions.http_500("Internal Server Error")