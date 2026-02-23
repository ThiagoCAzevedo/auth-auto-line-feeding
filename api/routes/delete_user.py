from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.users import DeleteUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.dependencies import require_admin


router = APIRouter()
log = logger("users")


@router.delete("/{user_id}", summary="Permanently delete a user", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):

    try:
        deleted = DeleteUsers.delete_user(db, user_id)

        if not deleted:
            raise HTTP_Exceptions.http_404("User not found.")

        return {"detail": "User deleted successfully."}

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error deleting user", e)