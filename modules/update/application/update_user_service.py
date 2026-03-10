from sqlalchemy.orm import Session
from modules.update.domain.update_user import UpdateUserUseCase


class UpdateUserService:
    """Application service for updating users"""
    
    @staticmethod
    def execute(db: Session, user_id: int, **fields):
        """Execute user update"""
        return UpdateUserUseCase.update_user(db, user_id, **fields)
