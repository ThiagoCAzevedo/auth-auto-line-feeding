from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from modules.create.api.schemas import CreateUserSchema, RegisterResponseSchema, EmailSchema
from modules.create.application.register_user_service import RegisterUserService
from database.session import get_db
from common.exceptions import HTTPExceptions
from common.services.email import EmailService
from common.security.jwt import JWTHandler
from modules.create.infrastructure.repositories import VerifyEmailRepository
from modules.update.application.update_user_service import UpdateUserService


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

        # background.add_task(EmailService.send_verification_email, user.email, verification_token)

        return {
            "message": "Successfully created user. Ask for an admin to approve your request.",
            "user": user
        }

    except Exception as e:
        raise HTTPExceptions.http_500("Internal error while creating user", e)
    

# @router.get("/verify-email", summary="Verify user email")
# def verify_email(token: str, db: Session = Depends(get_db)):
#     data = JWTHandler.verify_token(token, token_purpose="email_verification")
#     VerifyEmailRepository.verify_user_email(db, int(data["sub"]))
#     return {"message": "Successfully verified e-mail"}


# @router.post("/resend-verification", summary="Resend user verify email")
# def resend_email_verification(payload: EmailSchema, db: Session = Depends(get_db)):
#     user = VerifyEmailRepository.get_user_by_email(db, payload.email, must_be_unverified=True)

#     verification_token = JWTHandler.create_access_token({
#         "sub": str(user.id),
#         "email": user.email,
#         "purpose": "email_verification"
#     })

#     background_tasks = BackgroundTasks()
#     background_tasks.add_task(EmailService.send_verification_email, user.email, verification_token)

#     return {"message": "Verification email resent successfully."}
