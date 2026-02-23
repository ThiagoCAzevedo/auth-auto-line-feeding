from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from helpers.users import UserPassword, UserValidators

class RegisterUsers:

    @staticmethod
    def create_user(db: Session, first_name: str, last_name: str, email: str, password: str) -> Users:
        ok, msg = UserValidators.validate_email_domain(email)
        if not ok:
            raise ValueError(msg)

        ok, msg = UserValidators.validate_password(password)
        if not ok:
            raise ValueError(msg)

        user = Users(
            first_name=first_name, last_name=last_name, email=email, password=UserPassword.hash_password(password)
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise ValueError("E-mail already exists.")
        
        return user