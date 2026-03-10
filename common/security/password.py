from passlib.hash import argon2
from common.exceptions import HTTPExceptions
from common.logger import logger


log = logger("password_security")


class UserPassword:
    @staticmethod
    def hash_password(password: str) -> str:
        log.debug("Hashing password")
        hashed = argon2.hash(password)
        log.debug("Password hashed successfully")
        return hashed

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        log.debug("Verifying password")
        password_verified = argon2.verify(password, hashed)
        if not password_verified:
            log.warning("Password verification failed")
            raise HTTPExceptions.http_401("Senha atual incorreta")
        log.debug("Password verified successfully")
        return password_verified
