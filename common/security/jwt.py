from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from config.settings import settings
from common.exceptions import HTTPExceptions
from common.logger import logger
import jwt


log = logger("jwt_security")


class JWTHandler:
    @staticmethod
    def create_access_token(data: dict):
        log.debug("Creating access token")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        token = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
        log.debug("Access token created successfully")
        return token

    @staticmethod
    def create_refresh_token(data: dict, expires_days: int = None):
        if expires_days is None:
            expires_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
            
        log.debug(f"Creating refresh token with {expires_days} days expiry")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        token = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
        log.debug("Refresh token created successfully")
        return token

    @staticmethod
    def verify_token(token: str, token_purpose: str = None, token_type: str = None) -> dict:
        log.debug("Verifying token")
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            if token_type and decoded.get("type") != token_type:
                log.warning(f"Token type mismatch - expected: {token_type}, got: {decoded.get('type')}")
                raise HTTPExceptions.http_401(f"Tipo de token inválido. Esperado: {token_type}.")
            
            if token_purpose and decoded.get("purpose") != token_purpose:
                log.warning(f"Token purpose mismatch - expected: {token_purpose}, got: {decoded.get('purpose')}")
                raise HTTPExceptions.http_401("Propósito do token inválido.")
            
            log.debug("Token verified successfully")
            return decoded

        except jwt.ExpiredSignatureError:
            log.warning("Token verification failed - expired signature")
            raise HTTPExceptions.http_401("Token expirado.")

        except jwt.InvalidTokenError:
            log.warning("Token verification failed - invalid token")
            raise HTTPExceptions.http_401("Token inválido.")
        
    @staticmethod
    def create_password_reset_token(data: dict):
        log.debug("Creating password reset token")
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

        to_encode.update({
            "exp": expire,
            "purpose": "password_reset",
            "type": "reset"
        })

        token = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
        log.debug("Password reset token created successfully")
        return token
