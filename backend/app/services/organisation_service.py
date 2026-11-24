from uuid import UUID

from sqlalchemy.orm import Session

from app.models.organisation import SchoolOrganisation
from app.models.user import User


def get_organisation_by_id(db: Session, organisation_id: UUID):
    return (
        db.query(SchoolOrganisation)
        .filter(SchoolOrganisation.id == organisation_id)
        .first()
    )


def get_organisation_by_owner(db: Session, owner_user_id: UUID):
    return (
        db.query(SchoolOrganisation)
        .filter(SchoolOrganisation.owner_user_id == owner_user_id)
        .first()
    )


def create_organisation(
    db: Session,
    name: str,
    owner_user_id: UUID
):
    owner = db.query(User).filter(User.id == owner_user_id).first()

    if not owner:
        raise ValueError("Owner user does not exist.")

    existing_organisation = get_organisation_by_owner(
        db,
        owner_user_id
    )

    if existing_organisation:
        raise ValueError("This user already owns an organisation.")

    new_organisation = SchoolOrganisation(
        name=name,
        owner_user_id=owner_user_id
    )

    db.add(new_organisation)
    db.commit()
    db.refresh(new_organisation)

    return new_organisation