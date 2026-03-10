from sqlalchemy.orm import Session
from modules.delete.domain.delete_user import DeleteUserUseCase


class DeleteUserService:
    """Application service for deleting users"""
    
    @staticmethod
    def execute(db: Session, user_id: int) -> bool:
        """Execute user deletion"""
        return DeleteUserUseCase.delete_user(db, user_id)
