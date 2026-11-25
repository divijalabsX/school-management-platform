from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.organisation import (
    OrganisationCreate,
    OrganisationResponse
)
from app.services.organisation_service import (
    create_organisation,
    get_organisation_by_owner
)
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/api/v1/organisations",
    tags=["Organisations"]
)


@router.post(
    "/",
    response_model=OrganisationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_organisation(
    organisation_data: OrganisationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        new_organisation = create_organisation(
            db=db,
            name=organisation_data.name,
            owner_user_id=current_user.id
        )

        return new_organisation

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


@router.get(
    "/me",
    response_model=OrganisationResponse
)
def get_my_organisation(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    organisation = get_organisation_by_owner(
        db=db,
        owner_user_id=current_user.id
    )

    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No organisation found for this user."
        )

    return organisation