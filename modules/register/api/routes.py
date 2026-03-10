from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from modules.register.api.schemas import CreateUserSchema, RegisterResponseSchema
from modules.register.application.register_user_service import RegisterUserService
from database.session import get_db
from common.exceptions import HTTPExceptions


router = APIRouter()


@router.post("", summary="Register a new user", status_code=status.HTTP_201_CREATED, response_model=RegisterResponseSchema)
def register_user(payload: CreateUserSchema, background: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        user = RegisterUserService.execute(
            db=db,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password
        )

        return {
            "message": "Successfully created user. Ask for an admin to approve your request.",
            "user": user
        }

    except Exception as e:
        raise HTTPExceptions.http_500("Internal error while creating user", e)