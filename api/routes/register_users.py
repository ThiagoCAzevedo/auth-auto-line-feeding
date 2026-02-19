from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.schemas import CreateUserSchema, UserResponseSchema
from services.users import RegisterUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions


router = APIRouter()
log = logger("users")


@router.post("", summary="Register a new user", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(payload: CreateUserSchema, db: Session = Depends(get_db)):
    try:
        user = RegisterUsers.create_user(
            db=db, name=payload.complete_name, email=payload.email, password=payload.password, 
            role=payload.role or "user"
        )
        return user
    
    except Exception as e:
        raise HTTP_Exceptions.http_500("Interal error while creating user", e)