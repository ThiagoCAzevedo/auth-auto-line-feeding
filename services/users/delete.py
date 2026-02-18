from sqlalchemy.orm import Session
from database.models.users import Users

class DeleteUsers:
    def deactivate_user(db: Session, user_id: int) -> bool:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            return False

        user.status = False
        db.commit()
        return True