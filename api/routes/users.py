from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from api.schemas import CreateUserSchema, UserResponseSchema, UpdateUserSchema, UserPaginationSchema
from services.users import RegisterUsers, GetUsers, UpdateUsers, DeleteUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions


router = APIRouter()
log = logger("users")

#  -- GET ROUTES --
@router.get("/list", summary="List all users - Pagination, search and filters included", response_model=UserPaginationSchema)
def list_all_users(
    db: Session = Depends(get_db), page: int = Query(1, ge=1, description="Actual page (>= 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Page size (1-100)"), q: Optional[str] = Query(None, description="Search by name or e-mail"),
    status: Optional[bool] = Query(None, description="Filter by status (true or false)"),
):
    try:
        items, total = GetUsers.list_users(
            db=db, page=page, page_size=page_size, q=q, 
            status=status
        )
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while listing users", e)


@router.get("/list/{user_id}", summary="List specific user", response_model=UserResponseSchema)
def list_specific_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = GetUsers.list_specific_user(
            db, user_id
        )
        if not user:
            raise HTTP_Exceptions.http_404("User not found.")
        return user

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while finding specific user", e)
    

# -- POST ROUTES --
@router.post("/register", summary="Register a new user", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(payload: CreateUserSchema, db: Session = Depends(get_db)):
    try:
        user = RegisterUsers.create_user(
            db=db, name=payload.complete_name, email=payload.email, password=payload.password, 
            role=payload.role or "user"
        )
        return user

    except ValueError as ve:
        raise HTTP_Exceptions.http_409("User already exists", ve)
    
    except Exception as e:
        raise HTTP_Exceptions.http_500("Interal error while creating user", e)


# -- PATCH ROUTES --
@router.patch("/update/{user_id}", summary="Update any info of a user", response_model=UserResponseSchema)
def update_user(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    try:
        user = UpdateUsers.update_user(
            db=db, user_id=user_id, complete_name=payload.complete_name, email=payload.email,
            password=payload.password, role=payload.role, status=payload.status
        )

    except ValueError as ve:
        detail = str(ve)
        if "cadastrado" in detail:
            raise HTTP_Exceptions.http_409("E-mail already exists", ve)
        raise HTTP_Exceptions.http_400("Error while updating user", ve)

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while updating user", e)

    if not user:
        raise HTTP_Exceptions.http_404("User not found.")

    return user


# -- DELETE ROUTES --
@router.delete("/deactivate/{user_id}", summary="Deactivate user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        deleted = DeleteUsers.deactivate_user(db, user_id)

        if not deleted:
            raise HTTP_Exceptions.http_404("User not found.")

        return {"detail": "Successfully deactivated user."}

    except Exception as e:
        raise HTTP_Exceptions.http_500("Error while deactivating user", e)