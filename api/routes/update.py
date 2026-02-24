from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas import UserResponseSchema, UpdateUserSchema
from services import UpdateUsers
from database.database import get_db
from helpers.http_exceptions import HTTP_Exceptions
from helpers.services.user import UserService


router = APIRouter()


@router.patch("/{user_id}", summary="Update any info of a user", response_model=UserResponseSchema, dependencies=[Depends(UserService.ensure_is_admin())])
def update_user(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    try:
        user = UpdateUsers.update_user(db=db, user_id=user_id, **payload.model_dump(exclude_none=True))

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while updating user: ", e)

    return user