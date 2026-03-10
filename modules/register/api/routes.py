from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from modules.register.api.schemas import CreateUserSchema, RegisterResponseSchema
from modules.register.application.register_user_service import RegisterUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.logger import logger


log = logger("register_api")


router = APIRouter()


@router.post("", summary="Register a new user", status_code=status.HTTP_201_CREATED, response_model=RegisterResponseSchema)
def register_user(payload: CreateUserSchema, background: BackgroundTasks, db: Session = Depends(get_db)):
    log.info(f"User registration attempt for email: {payload.email}")
    try:
        user = RegisterUserService.execute(
            db=db,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password
        )

        log.info(f"User registered successfully: {user.id} - {user.email}")
        return {
            "message": "Usuário criado com sucesso. Solicite a um administrador para aprovar sua solicitação.",
            "user": user
        }

    except Exception as e:
        log.error(f"User registration failed for email {payload.email}: {str(e)}", exc_info=True)
        raise HTTPExceptions.http_500("Erro interno ao criar usuário", e)