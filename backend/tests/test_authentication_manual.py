from app.database.connection import SessionLocal
from app.services.user_service import (
    create_user,
    authenticate_user
)

TEST_EMAIL = "auth.test@example.com"
TEST_PASSWORD = "TestPassword123!"

db = SessionLocal()

try:
    # Create a temporary test user
    test_user = create_user(
        db=db,
        name="Authentication Test User",
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )

    print("Test user created:", test_user.email)

    # Test valid credentials
    valid_user = authenticate_user(
        db=db,
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )

    print("Valid credentials accepted:", valid_user is not None)

    # Test incorrect password
    invalid_password_user = authenticate_user(
        db=db,
        email=TEST_EMAIL,
        password="WrongPassword123!"
    )

    print(
        "Incorrect password rejected:",
        invalid_password_user is None
    )

    # Test nonexistent email
    nonexistent_user = authenticate_user(
        db=db,
        email="unknown@example.com",
        password=TEST_PASSWORD
    )

    print("Unknown email rejected:", nonexistent_user is None)

finally:
    # Remove the temporary test user
    if "test_user" in locals():
        db.delete(test_user)
        db.commit()

    db.close()

    print("Test database session closed.")