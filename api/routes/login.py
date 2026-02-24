from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas import LoginResponseSchema, EmailSchema, LoginUserSchema, ResetPasswordSchema
from database.database import get_db
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.password import UserPassword
from helpers.security.jwt import JWTHandler
from helpers.services.validators import UserValidators
from helpers.services.user import UserService
from services.update import UpdateUsers
from helpers.services.send_email import EmailService

router = APIRouter()


@router.post("", summary="Login user", response_model=LoginResponseSchema)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    try:
        user = UserService.get_user_by_email(db, payload.email)
        UserPassword.verify_password(payload.password, user.password)

        refresh_days = 30 if payload.remember_me else 1
        access_token = JWTHandler.create_access_token(
            {"sub": str(user.id), "email": user.email}
        )

        refresh_token = JWTHandler.create_refresh_token(
            {"sub": str(user.id), "email": user.email},
            expires_days=refresh_days
        )

        UpdateUsers.update_user(db, user.id, refresh_token=refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "remember_me": payload.remember_me,
            "token_type": "bearer",
            "user":user
        }

    except Exception:
        raise HTTP_Exceptions.http_500("Internal Server Error")
    

@router.post("/forgot-password", summary="User forgot password")
def forgot_password(payload: EmailSchema, db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, payload.email)

    message = "If this email exists, a password recovery email was sent."

    if not user:
        return {"message": message}

    reset_token = JWTHandler.create_password_reset_token({
        "sub": str(user.id),
        "email": user.email
    })

    UpdateUsers.update_user(db, user.id, reset_password_token=reset_token)
    EmailService.send_password_reset_email(user.email, reset_token)
    return {"message": message}


@router.post("/reset-password", summary="User reset password")
def reset_password(payload: ResetPasswordSchema, db: Session = Depends(get_db)):
    decoded = JWTHandler.verify_token(payload.token, "password_reset")
    user = UserService.get_user_by_id(db, decoded.get("sub"))

    if user.reset_password_token != payload.token:
        raise HTTP_Exceptions.http_401("Invalid or already used reset token")

    UserValidators.validate_password(payload.new_password)
    UpdateUsers.update_user(
        db,
        user.id,
        password=UserPassword.hash_password(payload.new_password),
        reset_password_token=None
    )
    return {"message": "Password updated successfully."}