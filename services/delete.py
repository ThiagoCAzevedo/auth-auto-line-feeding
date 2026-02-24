from sqlalchemy.orm import Session
from database.models.users import Users
from helpers.http_exceptions import HTTP_Exceptions
from helpers.services.user import UserService


class DeleteUsers:
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTP_Exceptions.http_404("User not found.")

        db.delete(user)
        db.commit()
        return True