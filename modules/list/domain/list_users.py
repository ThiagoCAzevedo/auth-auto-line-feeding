from typing import Optional, Tuple, List
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session
from database.models.users import Users
from common.exceptions import HTTPExceptions
from common.services.user import UserService


class ListUsersUseCase:
    """Domain logic for listing users with pagination and filtering"""
    
    @staticmethod
    def list_users(
            db: Session, 
            page: int = 1, 
            page_size: int = 10, 
            q: Optional[str] = None, 
            status: Optional[bool] = None
        ) -> Tuple[List[Users], int]:
        """List users with pagination, search, and filtering"""

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
        return query.offset(offset).limit(page_size).all(), query.count()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Users:
        """Get a specific user by ID"""
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPExceptions.http_404("User not found.")
        return user
