from fastapi import Depends
from common.exceptions import HTTPExceptions
from common.security.dependencies import get_current_user
from sqlalchemy.orm import Session
from database.models.users import Users
from database.session import get_db


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, current_user_id: int):
        user = db.query(Users).filter(Users.id == current_user_id).first()
        if not user:
            raise HTTPExceptions.http_404("User not found.")
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, current_user_email: str, verify_user: bool = False):
        user = db.query(Users).filter(Users.email == current_user_email).first()
        if not user:
            raise HTTPExceptions.http_404("User not found.")
        
        if verify_user and user.is_verified:
            raise HTTPExceptions.http_400("User already verified.")
        return user

    @staticmethod
    def ensure_is_admin(
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Verify that the authenticated user has the admin role.

        The JWT payload may become stale or may not include the most recent role,
        so we re‑query the database to be sure.
        """
        # fetch fresh user record using the ID stored in token
        user = UserService.get_user_by_id(db, int(current_user["sub"]))
        if user.role != "admin":
            raise HTTPExceptions.http_403("Access only for admins")
        return True
