from sqlalchemy.orm import Session
from database.models.users import Users
from common.security.jwt import JWTHandler
from common.exceptions import HTTPExceptions


class VerifyEmailRepository:
    """Infrastructure for email verification operations"""
    
    @staticmethod
    def verify_user_email(db: Session, user_id: int):
        """Mark user as verified"""
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPExceptions.http_404("User not found.")
        
        user.is_verified = True
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str, must_be_unverified: bool = False):
        """Get user by email with optional verification check"""
        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            raise HTTPExceptions.http_404("User not found.")
        
        if must_be_unverified and user.is_verified:
            raise HTTPExceptions.http_400("User already verified.")
        return user
