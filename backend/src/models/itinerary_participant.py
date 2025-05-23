from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, ConfigDict


class ItineraryParticipantStatus(StrEnum):
    UNKNOWN = "unknown"
    INVITED = "invited"
    JOINED = "joined"
    DECLINED = "declined"
    LEFT = "left"


class ItineraryParticipant(BaseModel):
    # Compound primary key: (itinerary_item_id, user_id)
    # FK to ItineraryItem.itinerary_item_id
    itinerary_item_id: str
    # FK to User.user_id
    user_id: str

    status: ItineraryParticipantStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")
