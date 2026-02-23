from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from dotenv import load_dotenv
import jwt
import os


load_dotenv("config/.env")


class JWTHandler:

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        return jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            os.getenv("ALGORITHM", "HS256")
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_days: int = 1):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        return jwt.encode(
            to_encode,
            os.getenv("SECRET_KEY"),
            os.getenv("ALGORITHM", "HS256")
        )

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            decoded = jwt.decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM", "HS256")]
            )
            return decoded

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired.",
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            )
        
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
            os.getenv("SECRET_KEY"),
            os.getenv("ALGORITHM", "HS256")
        )