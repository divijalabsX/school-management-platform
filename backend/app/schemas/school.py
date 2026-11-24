from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class SchoolCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    school_code: str | None = Field(default=None, max_length=50)
    established_year: int | None = Field(default=None, ge=1800, le=2100)
    school_type: str | None = Field(default=None, max_length=50)


class SchoolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organisation_id: UUID
    name: str
    school_code: str | None
    established_year: int | None
    school_type: str | None
    status: str
    created_at: datetime
    updated_at: datetime