from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from helpers.security.jwt import JWTHandler


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = JWTHandler.verify_token(token)
    return payload