from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from database.models.users import Users


class UserDeleteRepositoryInterface(ABC):
    """Interface for user deletion operations"""

    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[Users]:
        """Get a user by ID for deletion"""
        pass

    @abstractmethod
    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete a user"""
        pass


class UserDeleteRepository(UserDeleteRepositoryInterface):
    """SQLAlchemy implementation of UserDeleteRepositoryInterface"""

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[Users]:
        """Get a user by ID for deletion"""
        return db.query(Users).filter(Users.id == user_id).first()

    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete a user"""
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise Exception("User not found")

        db.delete(user)
        db.commit()
        return True