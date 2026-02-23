from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.jwt import JWTHandler
from database.models.users import Users
from sqlalchemy.orm import Session
from database.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = JWTHandler.verify_token(token)
    return payload


def require_admin(user = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user["sub"]).first()

    if db_user.role != "admin":
        raise HTTP_Exceptions.http_403("Access only for admins")
    
    return db_user

