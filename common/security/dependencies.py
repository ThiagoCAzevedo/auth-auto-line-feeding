from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from common.security.jwt import JWTHandler


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = JWTHandler.verify_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresh não pode ser usado para autenticação."
        )

    return payload
