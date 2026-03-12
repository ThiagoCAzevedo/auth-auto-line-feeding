from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models.users import Users
class UpdateUserService:
    """Application service for updating users"""

    @staticmethod
    def execute(db: Session, user_id: int, **fields):
        user = db.query(Users).filter(Users.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in fields.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user