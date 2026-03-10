from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.access.api.schemas import (
    UserResponseSchema, LoginUserSchema, LoginResponseSchema,
    RefreshTokenSchema
)
# the update functionality has been moved to its own module
from modules.update.application.update_user_service import UpdateUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.security.password import UserPassword
from common.security.jwt import JWTHandler
from common.security.dependencies import get_current_user
from common.services.user import UserService


router = APIRouter()


@router.get("/me", summary="Return logged user", response_model=UserResponseSchema)
def get_me(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, int(current_user["sub"]))


@router.post("/login", summary="Login user", response_model=LoginResponseSchema)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, payload.email)
    UserPassword.verify_password(payload.password, user.password)

    refresh_days = 30 if payload.remember_me else 1
    access_token = JWTHandler.create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role}
    )

    refresh_token = JWTHandler.create_refresh_token(
        {"sub": str(user.id), "email": user.email, "role": user.role},
        expires_days=refresh_days
    )

    UpdateUserService.execute(db, user.id, refresh_token=refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "remember_me": payload.remember_me,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout", summary="Logout user")
def logout_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    UpdateUserService.execute(db, int(current_user["sub"]), refresh_token=None)
    return {"message": "Successfully logout user"}
