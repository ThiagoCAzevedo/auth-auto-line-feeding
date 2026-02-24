from fastapi import APIRouter, Depends
from api.schemas import UserResponseSchema, RefreshTokenSchema, ChangePasswordSchema
from sqlalchemy.orm import Session
from database.database import get_db
from helpers.security.password import UserPassword
from helpers.security.jwt import JWTHandler
from helpers.services.validators import UserValidators
from helpers.services.user import UserService
from services.update import UpdateUsers


router = APIRouter()


@router.get("/me", summary="Return logged user", response_model=UserResponseSchema)
def get_me(current_user = Depends(UserService.get_current_user()), db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, current_user["sub"])


@router.post("/refresh", summary="Refresh JWT access token")
def refresh_token(payload: RefreshTokenSchema, db: Session = Depends(get_db)):
    decoded = JWTHandler.verify_token(payload.refresh_token, "refresh")
    user = UserService.get_user_by_id(db, decoded.get("sub")["sub"])

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
def change_password(payload: ChangePasswordSchema, current_user = Depends(UserService.get_current_user()), db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, current_user["sub"])
    UserPassword.verify_password(payload.current_password, user.password)
    UserValidators.validate_password(payload.new_password)
    UserPassword.hash_password(user, payload.new_password)
    UpdateUsers.update_user(db, current_user, refresh_token=None)

    return {"message": "Password changed successfully"}