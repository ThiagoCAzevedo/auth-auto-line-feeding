from sqlalchemy.orm import Session
from database.models.users import Users
from modules.update.infrastructure.repositories import UserUpdateRepository
from common.logger import logger


log = logger("update_domain")


class UpdateUserUseCase:
    """Domain logic for updating users"""

    def __init__(self, user_repository: UserUpdateRepository = None):
        self.user_repository = user_repository or UserUpdateRepository()

    def update_user(self, db: Session, user_id: int, **fields):
        """Update user fields"""
        log.debug(f"Updating user {user_id} with fields: {list(fields.keys())}")

        user = self.user_repository.update_user(db, user_id, **fields)

        log.info(f"User updated successfully: {user_id} - {user.email}")
        return user
