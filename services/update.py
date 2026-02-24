from sqlalchemy.orm import Session
from helpers.services.user import UserService


class UpdateUsers:
    @staticmethod
    def update_user(db: Session, user_id: int, **fields):
        user = UserService.get_user_by_id(db, user_id)

        for column, value in fields.items():
            if value is not None:
                setattr(user, column, value)

        db.commit()
        db.refresh(user)
        return user