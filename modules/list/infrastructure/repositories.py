from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from database.models.users import Users


class UserRepositoryInterface(ABC):
    """Interface for user data access operations"""

    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[Users]:
        """Get a user by ID"""
        pass

    @abstractmethod
    def list_users(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10,
        q: Optional[str] = None,
        status: Optional[bool] = None
    ) -> Tuple[List[Users], int]:
        """List users with pagination and filtering"""
        pass


class UserRepository(UserRepositoryInterface):
    """SQLAlchemy implementation of UserRepositoryInterface"""

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[Users]:
        """Get a user by ID"""
        return db.query(Users).filter(Users.id == user_id).first()

    def list_users(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10,
        q: Optional[str] = None,
        status: Optional[bool] = None
    ) -> Tuple[List[Users], int]:
        """List users with pagination and filtering"""
        from sqlalchemy import or_, desc

        query = db.query(Users)

        if status is not None:
            query = query.filter(Users.status == status)

        if q:
            like = f"%{q}%"
            query = query.filter(or_(
                Users.first_name.ilike(like),
                Users.last_name.ilike(like),
                Users.email.ilike(like)
            ))

        sort_col = Users.created_at
        query = query.order_by(desc(sort_col))

        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        offset = (page - 1) * page_size

        total = query.count()
        items = query.offset(offset).limit(page_size).all()

        return items, total