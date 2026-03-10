from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.update.api.schemas import (
    UpdateUserSchema, UserResponseSchema, LoginUserSchema, LoginResponseSchema,
    RefreshTokenSchema, ChangePasswordSchema, 
    ResetPasswordSchema, EmailSchema
)
from modules.update.application.update_user_service import UpdateUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.security.password import UserPassword
from common.security.jwt import JWTHandler
from common.security.dependencies import get_current_user
from common.services.validators import UserValidators
from common.services.user import UserService


router = APIRouter()


# DEFAULT ROUTES
@router.get("/me", summary="Return logged user", response_model=UserResponseSchema)
def get_me(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, int(current_user["sub"]))


@router.patch(
    "/{user_id}",
    summary="Update any info of a user",
    response_model=UserResponseSchema,
    dependencies=[Depends(UserService.ensure_is_admin)]
)
def update_user(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    try:
        user = UpdateUserService.execute(db=db, user_id=user_id, **payload.model_dump(exclude_none=True))
        return user
    except Exception as e:
        raise HTTPExceptions.http_500("Error while updating user: ", e)


@router.post("/refresh", summary="Refresh JWT access token")
def refresh_token(payload: RefreshTokenSchema, db: Session = Depends(get_db)):
    decoded = JWTHandler.verify_token(payload.refresh_token, token_type="refresh")
    user = UserService.get_user_by_id(db, int(decoded.get("sub")))

    access_token = JWTHandler.create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/change-password")
def change_password(
    payload: ChangePasswordSchema,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, int(current_user["sub"]))
    UserPassword.verify_password(payload.current_password, user.password)
    UserValidators.validate_password(payload.new_password)
    UpdateUserService.execute(
        db,
        int(current_user["sub"]),
        password=UserPassword.hash_password(payload.new_password),
        refresh_token=None
    )

    return {"message": "Password changed successfully"}


# LOGIN ROUTES
@router.post("", summary="Login user", response_model=LoginResponseSchema)
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


@router.post("/forgot-password", summary="User forgot password")
def forgot_password(payload: EmailSchema, db: Session = Depends(get_db)):
    message = "If this email exists, a password recovery email was sent."

    try:
        user = UserService.get_user_by_email(db, payload.email)
        
        reset_token = JWTHandler.create_password_reset_token({
            "sub": str(user.id),
            "email": user.email
        })

        UpdateUserService.execute(db, user.id, reset_password_token=reset_token)
    except HTTPExceptions.http_404:
        pass

    return {"message": message}


@router.post("/reset-password", summary="Reset password")
def reset_password(payload: ResetPasswordSchema, db: Session = Depends(get_db)):
    try:
        data = JWTHandler.verify_token(payload.token, token_purpose="password_reset")
        UserValidators.validate_password(payload.new_password)
        
        UpdateUserService.execute(
            db,
            int(data["sub"]),
            password=UserPassword.hash_password(payload.new_password),
            reset_password_token=None
        )
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPExceptions.http_400("Invalid or expired reset token", e)


# LOGOUT ROUTES
@router.post("/", summary="Logout user")
def logout_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    UpdateUserService.execute(db, int(current_user["sub"]), refresh_token=None)
    return {"message": "Successfully logout user"}
