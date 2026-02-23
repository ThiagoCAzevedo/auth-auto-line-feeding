from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas import UserResponseSchema, UpdateUserSchema
from services.users import UpdateUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions
from helpers.security.dependencies import require_admin


router = APIRouter()
log = logger("users")


@router.patch("/{user_id}", summary="Update any info of a user", response_model=UserResponseSchema, dependencies=[Depends(require_admin)])
def update_user(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    try:
        user = UpdateUsers.update_user(
            db=db, user_id=user_id, first_name=payload.first_name, last_name=payload.last_name, 
            email=payload.email, password=payload.password, role=payload.role, status=payload.status
        )

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while updating user: ", e)

    if not user:
        raise HTTP_Exceptions.http_404("User not found.")

    return user