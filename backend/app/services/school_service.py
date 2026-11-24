from uuid import UUID

from sqlalchemy.orm import Session

from app.models.school import School
from app.models.organisation import SchoolOrganisation


def get_school_by_id(db: Session, school_id: UUID):
    return (
        db.query(School)
        .filter(School.id == school_id)
        .first()
    )


def get_schools_by_organisation(
    db: Session,
    organisation_id: UUID
):
    return (
        db.query(School)
        .filter(School.organisation_id == organisation_id)
        .all()
    )


def create_school(
    db: Session,
    organisation_id: UUID,
    name: str,
    school_code: str | None = None,
    established_year: int | None = None,
    school_type: str | None = None
):
    # Verify that the parent organisation exists.
    organisation = (
        db.query(SchoolOrganisation)
        .filter(SchoolOrganisation.id == organisation_id)
        .first()
    )

    if not organisation:
        raise ValueError("School organisation does not exist.")

    # Check whether the school code is already registered.
    if school_code:
        existing_school = (
            db.query(School)
            .filter(School.school_code == school_code)
            .first()
        )

        if existing_school:
            raise ValueError("This school code is already registered.")

    new_school = School(
        organisation_id=organisation_id,
        name=name,
        school_code=school_code,
        established_year=established_year,
        school_type=school_type
    )

    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    return new_school