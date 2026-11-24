from app.database.connection import SessionLocal
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id
)

db = SessionLocal()

test_email = "user.service.test@example.com"

try:
    # Remove an earlier test record, if one exists.
    existing = get_user_by_email(db, test_email)

    if existing:
        db.delete(existing)
        db.commit()

    # Test user creation.
    user = create_user(
        db=db,
        name="Test User",
        email=test_email,
        password="TestPassword123!"
    )

    print("User creation: SUCCESS")
    print("User ID:", user.id)

    # Test retrieval by email.
    retrieved_user = get_user_by_email(db, test_email)

    print(
        "User retrieval by email:",
        "SUCCESS" if retrieved_user else "FAILED"
    )

    # Test retrieval by ID.
    retrieved_by_id = get_user_by_id(db, user.id)

    print(
        "User retrieval by ID:",
        "SUCCESS" if retrieved_by_id else "FAILED"
    )

    # Test duplicate email prevention.
    try:
        create_user(
            db=db,
            name="Another User",
            email=test_email,
            password="AnotherPassword123!"
        )
    except ValueError as error:
        print("Duplicate email prevention: SUCCESS")
        print("Message:", error)

finally:
    # Remove the temporary test user.
    test_user = get_user_by_email(db, test_email)

    if test_user:
        db.delete(test_user)
        db.commit()

    db.close()