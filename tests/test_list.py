from fastapi import HTTPException
from modules.register.application.register_user_service import RegisterUserService
from modules.list.application.list_users_service import ListUsersService
from database.models.users import Users
import pytest


class TestListUsers:
    def test_list_all_users(self, db_session):
        """Test listing all users with pagination"""
        # Create test users
        users_data = [
            {
                "first_name": "User",
                "last_name": "One",
                "email": "user1@example.com",
                "password": "Pass123!"
            },
            {
                "first_name": "User",
                "last_name": "Two",
                "email": "user2@example.com",
                "password": "Pass123!"
            },
            {
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
                "password": "Pass123!"
            }
        ]

        created_users = []
        for user_data in users_data:
            user = RegisterUserService.execute(db=db_session, **user_data)
            created_users.append(user)

        # Test listing all users
        items, total = ListUsersService.list_users(db=db_session)

        assert total == 3
        assert len(items) == 3
        emails = [user.email for user in items]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "admin@example.com" in emails

    def test_pagination(self, db_session):
        """Test pagination functionality"""
        # Create multiple users
        for i in range(5):
            user_data = {
                "first_name": f"User{i}",
                "last_name": "Test",
                "email": f"user{i}@example.com",
                "password": "Pass123!"
            }
            RegisterUserService.execute(db=db_session, **user_data)

        # Test first page
        items, total = ListUsersService.list_users(db=db_session, page=1, page_size=2)
        assert total == 5
        assert len(items) == 2

        # Test second page
        items, total = ListUsersService.list_users(db=db_session, page=2, page_size=2)
        assert total == 5
        assert len(items) == 2

        # Test last page
        items, total = ListUsersService.list_users(db=db_session, page=3, page_size=2)
        assert total == 5
        assert len(items) == 1

    def test_search_functionality(self, db_session):
        """Test search by name and email"""
        users_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "Pass123!"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "password": "Pass123!"
            },
            {
                "first_name": "Bob",
                "last_name": "Johnson",
                "email": "bob.johnson@example.com",
                "password": "Pass123!"
            }
        ]

        for user_data in users_data:
            RegisterUserService.execute(db=db_session, **user_data)

        # Search by first name
        items, total = ListUsersService.list_users(db=db_session, q="John")
        assert total == 2  # John Doe and Bob Johnson
        assert len(items) == 2

        # Search by last name
        items, total = ListUsersService.list_users(db=db_session, q="Smith")
        assert total == 1
        assert len(items) == 1
        assert items[0].email == "jane.smith@example.com"

        # Search by email
        items, total = ListUsersService.list_users(db=db_session, q="john.doe")
        assert total == 1
        assert len(items) == 1
        assert items[0].email == "john.doe@example.com"

    def test_status_filtering(self, db_session):
        """Test filtering by user status"""
        # Create users with different statuses
        user1 = RegisterUserService.execute(
            db=db_session,
            first_name="Active",
            last_name="User",
            email="active@example.com",
            password="Pass123!"
        )
        user1.status = True
        db_session.commit()

        user2 = RegisterUserService.execute(
            db=db_session,
            first_name="Inactive",
            last_name="User",
            email="inactive@example.com",
            password="Pass123!"
        )
        user2.status = False
        db_session.commit()

        # Filter active users
        items, total = ListUsersService.list_users(db=db_session, status=True)
        assert total == 1
        assert len(items) == 1
        assert items[0].email == "active@example.com"

        # Filter inactive users
        items, total = ListUsersService.list_users(db=db_session, status=False)
        assert total == 1
        assert len(items) == 1
        assert items[0].email == "inactive@example.com"

    def test_get_user_by_id(self, db_session):
        """Test getting a specific user by ID"""
        user_data = {
            "first_name": "Specific",
            "last_name": "User",
            "email": "specific@example.com",
            "password": "Pass123!"
        }

        created_user = RegisterUserService.execute(db=db_session, **user_data)

        # Get user by ID
        retrieved_user = ListUsersService.get_user_by_id(db=db_session, user_id=created_user.id)

        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
        assert retrieved_user.first_name == created_user.first_name

    def test_get_nonexistent_user(self, db_session):
        """Test getting a user that doesn't exist"""

        with pytest.raises(HTTPException) as exc_info:
            ListUsersService.get_user_by_id(db=db_session, user_id=99999)

        assert "User not found" in str(exc_info.value.detail)