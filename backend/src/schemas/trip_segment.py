from datetime import datetime
from typing import Any
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TripSegment(BaseModel):
    trip_segment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # FK to Trip.trip_id
    trip_id: str

    # This should specify where a group of people should be together.
    location_name: str
    description: str
    latitude: float | None = None
    longitude: float | None = None

    start_date: datetime | None = None
    end_date: datetime | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @field_validator("trip_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v
