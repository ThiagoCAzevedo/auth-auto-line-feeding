from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from common.security.password import UserPassword
from common.exceptions import HTTPExceptions
from common.security.jwt import JWTHandler
from common.logger import logger


log = logger("register_domain")


class RegisterUserUseCase:
    """Domain logic for creating and registering a user"""
    
    @staticmethod
    def create_user(
        db: Session, 
        first_name: str, 
        last_name: str, 
        email: str, 
        password: str, 
    ):
        """Create a new user and generate verification token"""
        log.debug(f"Creating user: {email}")
        
        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=UserPassword.hash_password(password),
            is_verified=False
        )

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            log.info(f"User created successfully: {user.id} - {email}")
        except IntegrityError:
            db.rollback()
            log.warning(f"User creation failed - email already exists: {email}")
            raise HTTPExceptions.http_400("E-mail already exists.")
        
        # verification_token = JWTHandler.create_access_token({
        #     "sub": str(user.id),
        #     "email": user.email,
        #     "purpose": "email_verification"
        # })

        return user#, verification_token
