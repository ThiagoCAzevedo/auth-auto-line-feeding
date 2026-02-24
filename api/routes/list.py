from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from api.schemas import UserResponseSchema, UserPaginationSchema
from services import ReadUsers
from database.database import get_db
from helpers.http_exceptions import HTTP_Exceptions
from helpers.services.user import UserService


router = APIRouter()


@router.get("/list-all", summary="List all users - Pagination, search and filters included", response_model=UserPaginationSchema, dependencies=[Depends(UserService.ensure_is_admin())])
def list_all_users(
    db: Session = Depends(get_db), page: int = Query(1, ge=1, description="Actual page (>= 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Page size (1-100)"), q: Optional[str] = Query(None, description="Search by name or e-mail"),
    status: Optional[bool] = Query(None, description="Filter by status (true or false)"),
):
    try:
        items, total = ReadUsers.list_users(db=db, page=page, page_size=page_size, q=q, status=status)
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while listing users", e)


@router.get("/list/{user_id}", summary="List specific user", response_model=UserResponseSchema, dependencies=[Depends(UserService.ensure_is_admin)])
def list_specific_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return ReadUsers.list_specific_user(db, user_id)

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while finding specific user", e)