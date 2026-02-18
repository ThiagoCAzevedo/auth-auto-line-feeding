from sqlalchemy import and_
from sqlalchemy.orm import Session
from database.models.users import Users
from helpers.users import UserPassword, UserValidators


class UpdateUsers:
    def update_user(
        db: Session, user_id: int, complete_name: str | None = None, email: str | None = None, 
        password: str | None = None, role: str | None = None, status: bool | None = None
    ):
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            return None

        if complete_name is not None:
            user.complete_name = complete_name

        if email is not None:
            ok, msg = UserValidators.validate_email_domain(email)
            if not ok:
                raise ValueError(msg)

            existing = (
                db.query(Users)
                .filter(and_(Users.email == email, Users.id != user_id))
                .first()
            )
            if existing:
                raise ValueError("E-mail already exists.")

            user.email = email

        if password is not None:
            ok, msg = UserPassword.validate_password(password)
            if not ok:
                raise ValueError(msg)

            user.set_password(password)

        if role is not None:
            user.role = role

        if status is not None:
            user.status = status

        db.commit()
        db.refresh(user)
        return user