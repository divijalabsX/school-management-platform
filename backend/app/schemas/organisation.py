from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class OrganisationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)


class OrganisationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    owner_user_id: UUID
    created_at: datetime
    updated_at: datetime