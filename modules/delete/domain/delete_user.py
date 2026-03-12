from sqlalchemy.orm import Session
from database.models.users import Users
from common.exceptions import HTTPExceptions
from common.services.user import UserService
from modules.delete.infrastructure.repositories import UserDeleteRepository
from common.logger import logger


log = logger("delete_domain")


class DeleteUserUseCase:
    """Domain logic for deleting users"""

    def __init__(self, user_repository: UserDeleteRepository = None):
        self.user_repository = user_repository or UserDeleteRepository()

    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete a user"""
        log.debug(f"Deleting user: {user_id}")

        try:
            result = self.user_repository.delete_user(db, user_id)
            log.info(f"User deleted successfully: {user_id}")
            return result
        except Exception as e:
            log.error(f"Failed to delete user {user_id}: {str(e)}")
            raise HTTPExceptions.http_404("User not found.")
