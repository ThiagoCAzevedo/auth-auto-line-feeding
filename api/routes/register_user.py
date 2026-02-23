from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from api.schemas import CreateUserSchema, RegisterResponseSchema, ResendVerificationSchema
from services.users import RegisterUsers
from database.database import get_db
from helpers.log.logger import logger
from helpers.http_exceptions import HTTP_Exceptions
from helpers.users.send_email import send_verification_email
from helpers.security.jwt import JWTHandler
from database.models.users import Users


router = APIRouter()
log = logger("users")


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

        background.add_task(send_verification_email, user.email, verification_token)

        return {
            "message": "Successfully created user. Verify your e-mail.",
            "user": user
        }

    except Exception as e:
        raise HTTP_Exceptions.http_500("Internal error while creating user", e)
    

@router.get("/verify-email", summary="Verify user email")
def verify_email(token: str, db: Session = Depends(get_db)):
    data = JWTHandler.verify_token(token)

    if data.get("purpose") != "email_verification":
        raise HTTP_Exceptions.http_400("Invalid token purpose.")

    user = db.query(Users).filter(Users.id == data["sub"]).first()

    if not user:
        raise HTTP_Exceptions.http_404("User not found.")

    user.is_verified = True
    db.commit()

    return {"message": "Successfully verified e-mail"}


@router.post("/resend-verification", summary="Resend user verify email")
def resend_email_verification(payload: ResendVerificationSchema,db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == payload.email).first()

    if not user:
        raise HTTP_Exceptions.http_404("User not found.")

    if user.is_verified:
        raise HTTP_Exceptions.http_400("User already verified.")

    verification_token = JWTHandler.create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "purpose": "email_verification"
    })

    send_verification_email(user.email, verification_token)

    return {"message": "Verification email re-sent successfully."}