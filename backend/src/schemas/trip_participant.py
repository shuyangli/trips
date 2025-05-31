from datetime import datetime
import uuid
from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator

from src.database.models import ParticipantStatus


class TripParticipant(BaseModel):
    trip_id: str
    user_id: str
    status: ParticipantStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @field_validator("trip_id", "user_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v


class TripInvitation(BaseModel):
    trip_id: str
    user_id: str
    status: ParticipantStatus
    created_at: datetime
    updated_at: datetime

    # Trip details
    trip_name: str
    trip_description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

    # Inviter details
    inviter_given_name: str
    inviter_family_name: str

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @field_validator("trip_id", "user_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v


class InviteUserRequest(BaseModel):
    email: str


class RespondToInvitationRequest(BaseModel):
    response: ParticipantStatus


class TripParticipantWithUser(BaseModel):
    trip_id: str
    user_id: str
    status: ParticipantStatus
    created_at: datetime
    updated_at: datetime

    # User details
    email: str
    given_name: str
    family_name: str

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @field_validator("trip_id", "user_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v
