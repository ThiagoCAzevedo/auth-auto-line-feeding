from sqlalchemy.orm import Session
from modules.register.domain.register_user import RegisterUserUseCase


class RegisterUserService:
    """Application service that orchestrates user registration"""
    
    @staticmethod
    def execute(
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ):
        """Execute user registration"""
        return RegisterUserUseCase.create_user(db, first_name, last_name, email, password)
