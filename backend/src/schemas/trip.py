from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field

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

class TripBase(BaseModel):
    name: str
    description: str | None = None
    created_by_user_id: str
    start_date: datetime | None = None
    end_date: datetime | None = None

class CreateTripRequest(TripBase):
    pass

class TripResponse(TripBase):
    trip_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
