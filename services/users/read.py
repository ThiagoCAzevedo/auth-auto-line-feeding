from typing import Optional, Tuple, List
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session
from database.models.users import Users


class ReadUsers:
    @staticmethod
    def list_users(
            db: Session, page: int = 1, page_size: int = 10, q: Optional[str] = None, 
            status: Optional[bool] = None
        ) -> Tuple[List[Users], int]:

        query = db.query(Users)
        if status is not None:
            query = query.filter(Users.status == status)

        if q:
            like = f"%{q}%"
            query = query.filter(or_(Users.complete_name.ilike(like), Users.email.ilike(like)))

        sort_columns = {
            "created_at": Users.created_at,
            "updated_at": Users.updated_at,
            "complete_name": Users.complete_name,
            "email": Users.email,
            "status": Users.status,
            "id": Users.id,
        }
        sort_col = sort_columns.get("created_at", Users.created_at)
        query = query.order_by(desc(sort_col))

        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        offset = (page - 1) * page_size
        return query.offset(offset).limit(page_size).all(), query.count()

    @staticmethod
    def list_specific_user(db: Session, user_id: int) -> Users:
        return db.query(Users).filter(Users.id == user_id).first()