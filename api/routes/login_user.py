from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas import LoginResponseSchema, ForgotPasswordSchema, LoginUserSchema, ResetPasswordSchema
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions
from database.models.users import Users
from helpers.users.security import UserPassword
from helpers.security.jwt import JWTHandler
from helpers.users.send_email import send_password_reset_email
from helpers.users.validators import UserValidators


router = APIRouter()
log = logger("users")


@router.post("", summary="Login user", response_model=LoginResponseSchema)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.email == payload.email).first()

        if not user:
            raise HTTP_Exceptions.http_404("User not found.")

        if not UserPassword.verify_password(payload.password, user.password):
            raise HTTP_Exceptions.http_401("Invalid password.")
        
        if not user.is_verified:
            raise HTTP_Exceptions.http_401("Email not verified. Please check your inbox.")

        refresh_days = 30 if payload.remember_me else 1

        access_token = JWTHandler.create_access_token(
            {"sub": str(user.id), "email": user.email}
        )

        refresh_token = JWTHandler.create_refresh_token(
            {"sub": str(user.id), "email": user.email},
            expires_days=refresh_days
        )

        user.refresh_token = refresh_token
        db.commit()

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
    

@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordSchema,
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.email == payload.email).first()

    message = "If this email exists, a password recovery email was sent."

    if not user:
        return {"message": message}

    reset_token = JWTHandler.create_password_reset_token({
        "sub": str(user.id),
        "email": user.email
    })

    user.reset_password_token = reset_token
    # user.reset_password_expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
    db.commit()

    # envia email
    send_password_reset_email(user.email, reset_token)

    return {"message": message}


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordSchema,
    db: Session = Depends(get_db)
):
    # decodifica token
    decoded = JWTHandler.verify_token(payload.token)

    if decoded.get("purpose") != "password_reset":
        raise HTTPException(400, "Invalid token purpose.")

    user_id = decoded.get("sub")

    # busca usuário
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTP_Exceptions.http_404("User not found")

    # valida token salvo no banco
    if user.reset_password_token != payload.token:
        raise HTTP_Exceptions.http_401("Invalid or already used reset token")

    # valida expiração
    # if user.reset_password_expiration:
    #     raise HTTP_Exceptions.http_401("Reset token expired")

    # valida força da senha (se quiser)
    ok, msg = UserValidators.validate_password(payload.new_password)
    if not ok:
        raise HTTP_Exceptions.http_400(msg)

    # atualiza senha
    user.password = UserPassword.hash_password(payload.new_password)

    # limpa token
    user.reset_password_token = None
    # user.reset_password_expiration = None

    db.commit()

    return {"message": "Password updated successfully."}