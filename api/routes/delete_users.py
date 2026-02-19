from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.users import DeleteUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions


router = APIRouter()
log = logger("users")


@router.delete("/delete/{user_id}", summary="Permanently delete a user")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    try:
        deleted = DeleteUsers.delete_user(db, user_id)

        if not deleted:
            raise HTTP_Exceptions.http_404("User not found.")

        return {"detail": "User deleted successfully."}

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error deleting user", e)