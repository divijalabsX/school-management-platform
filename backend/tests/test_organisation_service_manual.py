from uuid import uuid4

from app.database.connection import SessionLocal
from app.services.user_service import create_user, get_user_by_email
from app.services.organisation_service import (
    create_organisation,
    get_organisation_by_id,
    get_organisation_by_owner
)

db = SessionLocal()

test_email = "organisation.service.test@example.com"

try:
    # Remove any previous test data.
    existing_user = get_user_by_email(db, test_email)

    if existing_user:
        existing_organisation = get_organisation_by_owner(
            db,
            existing_user.id
        )

        if existing_organisation:
            db.delete(existing_organisation)
            db.commit()

        db.delete(existing_user)
        db.commit()

    # Create a temporary test user.
    user = create_user(
        db=db,
        name="Organisation Test User",
        email=test_email,
        password="TestPassword123!"
    )

    print("Test user creation: SUCCESS")

    # Test organisation creation.
    organisation = create_organisation(
        db=db,
        name="Test School Organisation",
        owner_user_id=user.id
    )

    print("Organisation creation: SUCCESS")
    print("Organisation ID:", organisation.id)

    # Test retrieval by organisation ID.
    retrieved_by_id = get_organisation_by_id(
        db,
        organisation.id
    )

    print(
        "Organisation retrieval by ID:",
        "SUCCESS" if retrieved_by_id else "FAILED"
    )

    # Test retrieval by owner ID.
    retrieved_by_owner = get_organisation_by_owner(
        db,
        user.id
    )

    print(
        "Organisation retrieval by owner:",
        "SUCCESS" if retrieved_by_owner else "FAILED"
    )

    # Test duplicate organisation prevention.
    try:
        create_organisation(
            db=db,
            name="Another Test Organisation",
            owner_user_id=user.id
        )
    except ValueError as error:
        print("Duplicate organisation prevention: SUCCESS")
        print("Message:", error)

    # Test rejection of a non-existent owner.
    try:
        create_organisation(
            db=db,
            name="Invalid Organisation",
            owner_user_id=uuid4()
        )
    except ValueError as error:
        print("Invalid owner rejection: SUCCESS")
        print("Message:", error)

finally:
    # Remove temporary test data.
    test_user = get_user_by_email(db, test_email)

    if test_user:
        test_organisation = get_organisation_by_owner(
            db,
            test_user.id
        )

        if test_organisation:
            db.delete(test_organisation)
            db.commit()

        db.delete(test_user)
        db.commit()

    db.close()