from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from helpers.users.get_user import get_current_user
from database.models.users import Users
from helpers.users.security import UserPassword
from api.schemas import UserResponseSchema, RefreshTokenSchema, ChangePasswordSchema
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.jwt import JWTHandler
from helpers.users.validators import UserValidators


router = APIRouter()


@router.get("/me", summary="Return logged user", response_model=UserResponseSchema)
def get_me(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == current_user["sub"]).first()

    if not user:
        raise HTTP_Exceptions.http_404("User not found.")

    return user


@router.post("/refresh", summary="Refresh JWT access token")
def refresh_token(payload: RefreshTokenSchema, db: Session = Depends(get_db)):
    decoded = JWTHandler.verify_token(payload.refresh_token)

    if decoded.get("type") != "refresh":
        raise HTTP_Exceptions.http_401("Invalid token type. Only refresh tokens are allowed.")

    user_id = decoded.get("sub")

    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTP_Exceptions.http_404("User not found")

    if user.refresh_token != payload.refresh_token:
        raise HTTP_Exceptions.http_401("Invalid refresh token")

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
    user = db.query(Users).filter(Users.id == current_user["sub"]).first()

    if not user:
        raise HTTP_Exceptions.http_400("User not found")

    if not UserPassword.verify_password(payload.current_password, user.password):
        raise HTTP_Exceptions.http_401("Current password is incorrect")

    ok, msg = UserValidators.validate_password(payload.new_password)
    if not ok:
        raise HTTP_Exceptions.http_400(msg)

    user.password = UserPassword.hash_password(payload.new_password)

    user.refresh_token = None
    db.commit()

    return {"message": "Password changed successfully"}