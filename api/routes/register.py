from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from api.schemas import CreateUserSchema, RegisterResponseSchema, EmailSchema
from services import RegisterUsers
from database.database import get_db
from helpers.http_exceptions import HTTP_Exceptions
from helpers.services.send_email import EmailService
from helpers.security.jwt import JWTHandler
from helpers.services.user import UserService
from services.update import UpdateUsers


router = APIRouter()


@router.post("", summary="Register a new user", status_code=status.HTTP_201_CREATED, response_model=RegisterResponseSchema)
def register_user(payload: CreateUserSchema, background: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        user, verification_token = RegisterUsers.create_user(
            db=db,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password
        )

        background.add_task(EmailService.send_verification_email(), user.email, verification_token)

        return {
            "message": "Successfully created user. Verify your e-mail.",
            "user": user
        }

    except Exception as e:
        raise HTTP_Exceptions.http_500("Internal error while creating user", e)
    

@router.get("/verify-email", summary="Verify user email")
def verify_email(token: str, db: Session = Depends(get_db)):
    data = JWTHandler.verify_token(token, "email_verification")
    UpdateUsers.update_user(db, data["sub"], is_verified=True)
    return {"message": "Successfully verified e-mail"}


@router.post("/resend-verification", summary="Resend user verify email")
def resend_email_verification(payload: EmailSchema,db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, payload.email)

    verification_token = JWTHandler.create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "purpose": "email_verification"
    })

    EmailService.send_verification_email(user.email, verification_token)
    return {"message": "Verification email re-sent successfully."}