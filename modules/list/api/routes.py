from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from modules.list.api.schemas import UserResponseSchema, UserPaginationSchema
from modules.list.application.list_users_service import ListUsersService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.services.user import UserService
from common.logger import logger


log = logger("list_api")


router = APIRouter()


@router.get(
    "/list-all",
    summary="List all users - Pagination, search and filters included",
    response_model=UserPaginationSchema,
    dependencies=[Depends(UserService.ensure_is_admin)]
)
def list_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Actual page (>= 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Page size (1-100)"),
    q: Optional[str] = Query(None, description="Search by name or e-mail"),
    status: Optional[bool] = Query(None, description="Filter by status (true or false)"),
):
    log.info(f"Listing users - page: {page}, size: {page_size}, query: {q}, status: {status}")
    try:
        items, total = ListUsersService.list_users(db=db, page=page, page_size=page_size, q=q, status=status)
        log.info(f"Users listed successfully - returned {len(items)} items out of {total} total")
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    except Exception as e:
        log.error(f"Failed to list users: {str(e)}", exc_info=True)
        raise HTTPExceptions.http_500("Erro ao listar usuários", e)


@router.get(
    "/list/{user_id}",
    summary="List specific user",
    response_model=UserResponseSchema,
    dependencies=[Depends(UserService.ensure_is_admin)]
)
def list_specific_user(user_id: int, db: Session = Depends(get_db)):
    log.info(f"Fetching specific user: {user_id}")
    try:
        user = ListUsersService.get_user_by_id(db, user_id)
        log.info(f"User retrieved successfully: {user_id} - {user.email}")
        return user

    except Exception as e:
        log.error(f"Failed to retrieve user {user_id}: {str(e)}", exc_info=True)
        raise HTTPExceptions.http_500("Erro ao encontrar usuário específico", e)
