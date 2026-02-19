from sqlalchemy.orm import Session
from database.models.users import Users

class DeleteUsers:
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True