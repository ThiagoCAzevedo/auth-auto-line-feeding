from passlib.hash import argon2
from common.exceptions import HTTPExceptions


class UserPassword:
    @staticmethod
    def hash_password(password: str) -> str:
        return argon2.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        password_verified = argon2.verify(password, hashed)
        if not password_verified:
            raise HTTPExceptions.http_401("Current password is incorrect")
