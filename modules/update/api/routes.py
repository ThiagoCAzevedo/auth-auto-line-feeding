from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modules.update.api.schemas import UpdateUserSchema, UserResponseSchema
from modules.update.application.update_user_service import UpdateUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.services.user import UserService
from common.logger import logger

log = logger("update_api")

router = APIRouter()


@router.patch(
    "/{user_id}",
    summary="Update any info of a user",
    response_model=UserResponseSchema,
    dependencies=[Depends(UserService.ensure_is_admin)]
)
def update_user(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    log.info(f"Update request for user: {user_id} with fields: {list(payload.model_dump(exclude_none=True).keys())}")
    try:
        user = UpdateUserService.execute(db=db, user_id=user_id, **payload.model_dump(exclude_none=True))
        log.info(f"User updated successfully: {user_id} - {user.email}")
        return user
    except Exception as e:
        log.error(f"Failed to update user {user_id}: {str(e)}", exc_info=True)
        raise HTTPExceptions.http_500("Erro ao atualizar usuário: ", e)
