from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.delete.application.delete_user_service import DeleteUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.services.user import UserService
from common.logger import logger


log = logger("delete_api")


router = APIRouter()


@router.delete(
    "/{user_id}",
    summary="Permanently delete a user",
    dependencies=[Depends(UserService.ensure_is_admin)]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    log.info(f"Delete request for user: {user_id}")
    try:
        DeleteUserService.execute(db, user_id)
        log.info(f"User deleted successfully: {user_id}")
        return {"detail": "Usuário deletado com sucesso."}

    except Exception as e:
        log.error(f"Failed to delete user {user_id}: {str(e)}", exc_info=True)
        raise HTTPExceptions.http_500("Erro ao deletar usuário", e)
