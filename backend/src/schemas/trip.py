from datetime import datetime
import uuid
from pydantic import BaseModel, Field

class TripBase(BaseModel):
    name: str
    description: str | None = None
    created_by_user_id: str
    start_date: datetime | None = None
    end_date: datetime | None = None

class TripCreate(TripBase):
    pass

class TripResponse(TripBase):
    trip_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
