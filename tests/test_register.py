from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from modules.register.application.register_user_service import RegisterUserService
from database.models.users import Users
import pytest


class TestRegisterUserService:
    def test_register_user_success(self, db_session):
        """Test successful user registration"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "SecurePass123!"
        }

        user = RegisterUserService.execute(
            db=db_session,
            **user_data
        )

        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.email == user_data["email"]
        assert user.is_verified == False
        assert user.password != user_data["password"]  # Should be hashed

        # Verify user exists in database
        db_user = db_session.query(Users).filter(Users.email == user_data["email"]).first()
        assert db_user is not None
        assert db_user.id == user.id

    def test_register_duplicate_email(self, db_session):
        """Test registration with duplicate email fails"""
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "password": "SecurePass123!"
        }

        # Create first user
        RegisterUserService.execute(db=db_session, **user_data)

        # Try to create duplicate
        with pytest.raises(HTTPException) as exc_info:
            RegisterUserService.execute(db=db_session, **user_data)

        assert "E-mail already exists" in str(exc_info.value.detail)

    def test_register_user_validation(self, db_session):
        """Test user registration with invalid data"""
        # Test with empty email
        with pytest.raises(Exception):  # Should be caught by Pydantic validation
            RegisterUserService.execute(
                db=db_session,
                first_name="Test",
                last_name="User",
                email="",
                password="password123"
            )

    def test_password_hashing(self, db_session):
        """Test that passwords are properly hashed"""
        from common.security.password import UserPassword

        password = "MySecurePassword123!"
        hashed = UserPassword.hash_password(password)

        assert hashed != password
        assert UserPassword.verify_password(password, hashed)

        # Test wrong password fails
        with pytest.raises(HTTPException):
            UserPassword.verify_password("WrongPassword", hashed)