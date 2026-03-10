from sqlalchemy.orm import Session
from database.models.users import Users


class UpdateUserUseCase:
    """Domain logic for updating users"""
    
    @staticmethod
    def update_user(db: Session, user_id: int, **fields):
        """Update user fields"""
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise Exception("User not found")

        for column, value in fields.items():
            if value is not None:
                setattr(user, column, value)

        db.commit()
        db.refresh(user)
        return user
