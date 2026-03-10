from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from modules.list.domain.list_users import ListUsersUseCase
from database.models.users import Users


class ListUsersService:
    """Application service for reading users"""

    @staticmethod
    def list_users(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        q: Optional[str] = None,
        status: Optional[bool] = None
    ) -> Tuple[List[Users], int]:
        """Execute user listing"""
        use_case = ListUsersUseCase()
        return use_case.list_users(db, page, page_size, q, status)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Users:
        """Execute get user by ID"""
        use_case = ListUsersUseCase()
        return use_case.get_user_by_id(db, user_id)