from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.delete.application.delete_user_service import DeleteUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.services.user import UserService


router = APIRouter()


@router.delete(
    "/{user_id}",
    summary="Permanently delete a user",
    dependencies=[Depends(UserService.ensure_is_admin)]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        DeleteUserService.execute(db, user_id)
        return {"detail": "User deleted successfully."}

    except Exception as e:
        raise HTTPExceptions.http_500("Error deleting user", e)
