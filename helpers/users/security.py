from passlib.hash import argon2


class UserPassword:
    @staticmethod
    def hash_password(password: str) -> str:
        return argon2.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return argon2.verify(password, hashed)