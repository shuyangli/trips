from datetime import datetime
import uuid
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Trip(BaseModel):
    trip_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    name: str
    description: str | None = None

    # FK to User.user_id
    created_by_user_id: str

    start_date: datetime | None = None
    end_date: datetime | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @field_validator("trip_id", "created_by_user_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v


class CreateTripRequest(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
