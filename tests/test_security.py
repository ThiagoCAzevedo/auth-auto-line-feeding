from fastapi import HTTPException
from common.security.password import UserPassword
from common.security.jwt import JWTHandler
from common.services.validators import UserValidators
import pytest


class TestPasswordSecurity:
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "MySecurePassword123!"

        # Hash password
        hashed = UserPassword.hash_password(password)
        assert hashed != password
        assert isinstance(hashed, str)

        # Verify correct password
        assert UserPassword.verify_password(password, hashed)

        # Verify wrong password fails
        with pytest.raises(HTTPException):
            UserPassword.verify_password("WrongPassword", hashed)


class TestJWTHandler:

    def test_access_token_creation_and_verification(self):
        """Test JWT access token creation and verification"""
        payload = {
            "sub": "123",
            "email": "test@example.com",
            "role": "user"
        }

        # Create token
        token = JWTHandler.create_access_token(payload)
        assert token is not None
        assert isinstance(token, str)

        # Verify token
        decoded = JWTHandler.verify_token(token, token_type="access")
        assert decoded["sub"] == "123"
        assert decoded["email"] == "test@example.com"
        assert decoded["role"] == "user"
        assert decoded["type"] == "access"

    def test_refresh_token_creation_and_verification(self):
        """Test JWT refresh token creation and verification"""
        payload = {
            "sub": "456",
            "email": "refresh@example.com",
            "role": "admin"
        }

        # Create token
        token = JWTHandler.create_refresh_token(payload)
        assert token is not None

        # Verify token
        decoded = JWTHandler.verify_token(token, token_type="refresh")
        assert decoded["sub"] == "456"
        assert decoded["email"] == "refresh@example.com"
        assert decoded["type"] == "refresh"

    def test_token_type_validation(self):
        """Test token type validation"""
        payload = {"sub": "123", "email": "test@example.com"}

        # Create access token
        access_token = JWTHandler.create_access_token(payload)

        # Try to verify as refresh token - should fail
        with pytest.raises(HTTPException):
            JWTHandler.verify_token(access_token, token_type="refresh")

    def test_token_purpose_validation(self):
        """Test token purpose validation"""
        payload = {"sub": "123", "email": "test@example.com"}

        # Create password reset token
        reset_token = JWTHandler.create_password_reset_token(payload)

        # Verify with correct purpose
        decoded = JWTHandler.verify_token(reset_token, token_purpose="password_reset", token_type="reset")
        assert decoded["purpose"] == "password_reset"
        assert decoded["type"] == "reset"

        # Try to verify with wrong purpose - should fail
        with pytest.raises(HTTPException):
            JWTHandler.verify_token(reset_token, token_purpose="email_verification")

    def test_invalid_token_verification(self):
        """Test verification of invalid tokens"""
        # Test with completely invalid token
        with pytest.raises(HTTPException):
            JWTHandler.verify_token("invalid.token.here")

        # Test with valid format but wrong signature
        fake_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.fake_signature"
        with pytest.raises(HTTPException):
            JWTHandler.verify_token(fake_token)


class TestEmailValidation:
    def test_email_domain_validation(self):
        """Test email domain validation"""
        # Valid domains
        valid_emails = [
            "user@gruposese.com",
            "test@volkswagen.com.br",
            "admin@gruposese.com"
        ]

        for email in valid_emails:
            # Should not raise exception
            UserValidators.validate_email_domain(email)

        # Invalid domains
        invalid_emails = [
            "user@10minutemail.com",
            "test@temp-mail.org",
            "spam@guerrillamail.com",
            "user@gmail.com",
            "test@hotmail.com"
        ]

        for email in invalid_emails:
            with pytest.raises(HTTPException) as exc_info:
                UserValidators.validate_email_domain(email)
            assert "O e-mail deve ser do domínio" in str(exc_info.value.detail)