from datetime import datetime
import uuid

from pydantic import BaseModel, Field


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

    created_at: int
    updated_at: int
