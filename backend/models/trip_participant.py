from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class TripParticipantStatus(StrEnum):
    UNKNOWN = "unknown"
    INVITED = "invited"
    JOINED = "joined"
    DECLINED = "declined"
    LEFT = "left"


class TripParticipant(BaseModel):
    # Compound primary key: (trip_id, user_id)
    # FK to Trip.trip_id
    trip_id: str
    # FK to User.user_id
    user_id: str

    status: TripParticipantStatus

    created_at: datetime
    updated_at: datetime
