from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from database.models.users import Users


class UserUpdateRepositoryInterface(ABC):
    """Interface for user update operations"""

    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[Users]:
        """Get a user by ID for updating"""
        pass

    @abstractmethod
    def update_user(self, db: Session, user_id: int, **fields) -> Users:
        """Update user fields"""
        pass


class UserUpdateRepository(UserUpdateRepositoryInterface):
    """SQLAlchemy implementation of UserUpdateRepositoryInterface"""

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[Users]:
        """Get a user by ID for updating"""
        return db.query(Users).filter(Users.id == user_id).first()

    def update_user(self, db: Session, user_id: int, **fields) -> Users:
        """Update user fields"""
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise Exception("User not found")

        for column, value in fields.items():
            if value is not None:
                setattr(user, column, value)

        db.commit()
        db.refresh(user)
        return user