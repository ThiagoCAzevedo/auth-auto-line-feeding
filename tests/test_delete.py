from fastapi import HTTPException
from modules.register.application.register_user_service import RegisterUserService
from modules.delete.application.delete_user_service import DeleteUserService
from database.models.users import Users
import pytest


class TestDeleteUser:
    def test_delete_existing_user(self, db_session):
        """Test deleting an existing user"""
        # Create a test user
        user_data = {
            "first_name": "Delete",
            "last_name": "Test",
            "email": "delete@example.com",
            "password": "Pass123!"
        }

        user = RegisterUserService.execute(db=db_session, **user_data)

        # Verify user exists
        db_user = db_session.query(Users).filter(Users.id == user.id).first()
        assert db_user is not None

        # Delete the user
        result = DeleteUserService.execute(db=db_session, user_id=user.id)
        assert result == True

        # Verify user is deleted
        db_user = db_session.query(Users).filter(Users.id == user.id).first()
        assert db_user is None

    def test_delete_nonexistent_user(self, db_session):
        """Test deleting a user that doesn't exist"""
        with pytest.raises(HTTPException) as exc_info:
            DeleteUserService.execute(db=db_session, user_id=99999)

        assert "User not found" in str(exc_info.value.detail)

    def test_delete_user_with_dependencies(self, db_session):
        """Test deleting a user (simplified - no actual dependencies in this schema)"""
        # Create a test user
        user_data = {
            "first_name": "Dependency",
            "last_name": "Test",
            "email": "dependency@example.com",
            "password": "Pass123!"
        }

        user = RegisterUserService.execute(db=db_session, **user_data)

        # In a real scenario, you might have foreign key constraints
        # For this simple schema, deletion should work fine
        result = DeleteUserService.execute(db=db_session, user_id=user.id)
        assert result == True

        # Verify deletion
        db_user = db_session.query(Users).filter(Users.id == user.id).first()
        assert db_user is None

    def test_delete_user_audit_trail(self, db_session):
        """Test that deletion is properly logged (would be tested via logs in real scenario)"""
        # Create a test user
        user_data = {
            "first_name": "Audit",
            "last_name": "Trail",
            "email": "audit@example.com",
            "password": "Pass123!"
        }

        user = RegisterUserService.execute(db=db_session, **user_data)

        # Get user info before deletion for audit purposes
        user_info = {
            "id": user.id,
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}"
        }

        # Delete the user
        result = DeleteUserService.execute(db=db_session, user_id=user.id)
        assert result == True

        # In a real audit system, you would verify audit logs were created
        # For this test, we just ensure the operation completes
        assert result == True