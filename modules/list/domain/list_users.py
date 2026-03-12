from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from database.models.users import Users
from common.exceptions import HTTPExceptions
from common.services.user import UserService
from modules.list.infrastructure.repositories import UserRepository
from common.logger import logger


log = logger("list_domain")


class ListUsersUseCase:
    """Domain logic for listing users with pagination and filtering"""

    def __init__(self, user_repository: UserRepository = None):
        self.user_repository = user_repository or UserRepository()

    def list_users(
            self,
            db: Session,
            page: int = 1,
            page_size: int = 10,
            q: Optional[str] = None,
            status: Optional[bool] = None
        ) -> Tuple[List[Users], int]:
        """List users with pagination, search, and filtering"""
        log.debug(f"Listing users with filters - page: {page}, size: {page_size}, query: {q}, status: {status}")

        items, total = self.user_repository.list_users(db, page, page_size, q, status)

        log.info(f"Users query completed - found {total} total users, returning {len(items)} items")
        return items, total

    def get_user_by_id(self, db: Session, user_id: int) -> Users:
        """Get a specific user by ID"""
        log.debug(f"Fetching user by ID: {user_id}")

        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            log.warning(f"User not found: {user_id}")
            raise HTTPExceptions.http_404("User not found.")
        log.debug(f"User found: {user_id} - {user.email}")
        return user
