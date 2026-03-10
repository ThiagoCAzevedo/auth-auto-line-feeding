from sqlalchemy.orm import Session
from modules.register.domain.register_user import RegisterUserUseCase


class RegisterUserService:
    """Application service that orchestrates user registration"""
    
    @staticmethod
    def execute(db: Session, first_name: str, last_name: str, email: str, password: str):

        if not first_name:
            raise Exception("First name is required")

        if not last_name:
            raise Exception("Last name is required")

        if not email:
            raise Exception("Email is required")

        if not password:
            raise Exception("Password is required")

        use_case = RegisterUserUseCase()
        return use_case.create_user(
            db=db,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )