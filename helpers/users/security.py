from passlib.hash import argon2


class UserPassword:
    def hash_password(self, password: str) -> str:
        return argon2.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return argon2.verify(password, hashed)