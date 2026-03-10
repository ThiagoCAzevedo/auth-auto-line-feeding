from sqlalchemy.orm import Session
from database.models.users import Users
from common.exceptions import HTTPExceptions
from common.services.user import UserService


class DeleteUserUseCase:
    """Domain logic for deleting users"""
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPExceptions.http_404("User not found.")

        db.delete(user)
        db.commit()
        return True
