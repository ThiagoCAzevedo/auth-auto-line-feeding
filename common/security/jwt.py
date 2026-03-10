from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from config.settings import settings
from common.exceptions import HTTPExceptions
import jwt


class JWTHandler:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_days: int = None):
        if expires_days is None:
            expires_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
            
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )

    @staticmethod
    def verify_token(token: str, token_purpose: str = None, token_type: str = None) -> dict:
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            if token_type and decoded.get("type") != token_type:
                raise HTTPExceptions.http_401(f"Invalid token type. Expected: {token_type}.")
            
            if token_purpose and decoded.get("purpose") != token_purpose:
                raise HTTPExceptions.http_401("Invalid token purpose.")
            
            return decoded

        except jwt.ExpiredSignatureError:
            raise HTTPExceptions.http_401("Token expired.")

        except jwt.InvalidTokenError:
            raise HTTPExceptions.http_401("Invalid token.")
        
    @staticmethod
    def create_password_reset_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

        to_encode.update({
            "exp": expire,
            "purpose": "password_reset",
            "type": "reset"
        })

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
