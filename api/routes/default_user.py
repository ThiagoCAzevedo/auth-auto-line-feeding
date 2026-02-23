from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from helpers.users.get_user import get_current_user
from database.models.users import Users
from api.schemas import UserResponseSchema, RefreshTokenSchema
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.jwt import JWTHandler


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