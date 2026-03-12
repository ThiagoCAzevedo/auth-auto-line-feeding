from fastapi import Depends
from common.exceptions import HTTPExceptions
from common.security.dependencies import get_current_user
from sqlalchemy.orm import Session
from database.models.users import Users
from database.session import get_db
from common.logger import logger


log = logger("user_service")


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, current_user_id: int):
        log.debug(f"Fetching user by ID: {current_user_id}")
        user = db.query(Users).filter(Users.id == current_user_id).first()
        if not user:
            log.warning(f"User not found by ID: {current_user_id}")
            raise HTTPExceptions.http_404("Usuário não encontrado.")
        log.debug(f"User found: {current_user_id} - {user.email}")
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, current_user_email: str, verify_user: bool = False):
        log.debug(f"Fetching user by email: {current_user_email}")
        user = db.query(Users).filter(Users.email == current_user_email).first()
        if not user:
            log.warning(f"User not found by email: {current_user_email}")
            raise HTTPExceptions.http_404("Usuário não encontrado.")
        
        if verify_user and user.is_verified:
            log.warning(f"User already verified: {current_user_email}")
            raise HTTPExceptions.http_400("Usuário já verificado.")
        log.debug(f"User found: {current_user_email} - ID: {user.id}")
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
        user_id = int(current_user["sub"])
        log.debug(f"Checking admin permissions for user: {user_id}")
        # fetch fresh user record using the ID stored in token
        user = UserService.get_user_by_id(db, user_id)
        if user.role != "admin":
            log.warning(f"Admin access denied for user: {user_id} - role: {user.role}")
            raise HTTPExceptions.http_403("Acesso apenas para administradores")
        log.debug(f"Admin access granted for user: {user_id}")
        return True
