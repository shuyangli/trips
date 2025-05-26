from datetime import datetime
from enum import StrEnum
from typing import Any
import uuid
from pydantic import BaseModel, ConfigDict, field_validator


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

    @field_validator("itinerary_item_id", "user_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v
