from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.users import Users
from helpers.users import UserPassword, UserValidators


class UpdateUsers:
    @staticmethod
    def update_user(
        db: Session, user_id: int, first_name: str | None = None, last_name: str | None = None, email: str | None = None, 
        password: str | None = None, role: str | None = None, status: bool | None = None
    ):
        user = db.query(Users).filter(Users.id == user_id).first()

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if email is not None:
            user.email = email

        if password is not None:
            user.password = UserPassword.hash_password(password)

        if role is not None:
            user.role = role

        if status is not None:
            user.status = status

        db.commit()
        db.refresh(user)
        return user