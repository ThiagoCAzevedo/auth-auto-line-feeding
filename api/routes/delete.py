from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import DeleteUsers
from database.database import get_db
from helpers.http_exceptions import HTTP_Exceptions
from helpers.services.user import UserService


router = APIRouter()


@router.delete("/{user_id}", summary="Permanently delete a user", dependencies=[Depends(UserService.ensure_is_admin())])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        DeleteUsers.delete_user(db, user_id)
        return {"detail": "User deleted successfully."}

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error deleting user", e)