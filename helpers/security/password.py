from passlib.hash import argon2
from helpers.http_exceptions import HTTP_Exceptions
from services.update import UpdateUsers


class UserPassword:
    @staticmethod
    def hash_password(user, password: str) -> str:
        UpdateUsers.update_user(user, password=argon2.hash(password))
        return True

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        password_verified = argon2.verify(password, hashed)
        if not password_verified:
            raise HTTP_Exceptions.http_401("Current password is incorrect")
        return True