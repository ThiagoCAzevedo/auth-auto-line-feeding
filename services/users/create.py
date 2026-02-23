from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from helpers.users import UserPassword
from fastapi import HTTPException
from helpers.security.jwt import JWTHandler

class RegisterUsers:

    @staticmethod
    def create_user(
        db: Session, 
        first_name: str, 
        last_name: str, 
        email: str, 
        password: str, 
    ):
        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=UserPassword.hash_password(password),
            is_verified=False  # se você tiver esse campo
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="E-mail already exists.")
        
        verification_token = JWTHandler.create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "purpose": "email_verification"
        })

        return user, verification_token