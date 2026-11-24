from uuid import uuid4

from app.database.connection import SessionLocal
from app.services.user_service import create_user, get_user_by_email
from app.services.organisation_service import (
    create_organisation,
    get_organisation_by_owner
)
from app.services.school_service import (
    create_school,
    get_school_by_id,
    get_schools_by_organisation
)

db = SessionLocal()

test_email = "school.service.test@example.com"
test_school_code = "TEST-SCHOOL-001"

try:
    # Remove any previous test data.
    existing_user = get_user_by_email(db, test_email)

    if existing_user:
        existing_organisation = get_organisation_by_owner(
            db,
            existing_user.id
        )

        if existing_organisation:
            for school in get_schools_by_organisation(
                db,
                existing_organisation.id
            ):
                db.delete(school)

            db.delete(existing_organisation)
            db.commit()

        db.delete(existing_user)
        db.commit()

    # Create a temporary user and organisation.
    user = create_user(
        db=db,
        name="School Test User",
        email=test_email,
        password="TestPassword123!"
    )

    organisation = create_organisation(
        db=db,
        name="School Test Organisation",
        owner_user_id=user.id
    )

    print("Test user and organisation creation: SUCCESS")

    # Test school creation.
    school = create_school(
        db=db,
        organisation_id=organisation.id,
        name="Test Public School",
        school_code=test_school_code,
        established_year=2010,
        school_type="Private"
    )

    print("School creation: SUCCESS")
    print("School ID:", school.id)

    # Test retrieval by school ID.
    retrieved_school = get_school_by_id(
        db,
        school.id
    )

    print(
        "School retrieval by ID:",
        "SUCCESS" if retrieved_school else "FAILED"
    )

    # Test retrieval by organisation ID.
    organisation_schools = get_schools_by_organisation(
        db,
        organisation.id
    )

    print(
        "Schools retrieval by organisation:",
        "SUCCESS" if school.id in [
            item.id for item in organisation_schools
        ] else "FAILED"
    )

    # Test duplicate school-code prevention.
    try:
        create_school(
            db=db,
            organisation_id=organisation.id,
            name="Another Test School",
            school_code=test_school_code
        )
    except ValueError as error:
        print("Duplicate school-code prevention: SUCCESS")
        print("Message:", error)

    # Test rejection of a non-existent organisation.
    try:
        create_school(
            db=db,
            organisation_id=uuid4(),
            name="Invalid Test School"
        )
    except ValueError as error:
        print("Invalid organisation rejection: SUCCESS")
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
            for school in get_schools_by_organisation(
                db,
                test_organisation.id
            ):
                db.delete(school)

            db.delete(test_organisation)
            db.commit()

        db.delete(test_user)
        db.commit()

    db.close()