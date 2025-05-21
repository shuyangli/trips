from datetime import datetime
from enum import StrEnum
import uuid
from pydantic import BaseModel, ConfigDict, Field


class UserStatus(StrEnum):
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class User(BaseModel):
    user_id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    email: str

    # Do we need this?
    password_hash: str

    given_name: str
    family_name: str
    profile_picture_url: str | None = None

    # OAuth provider for social logins
    oauth_provider: str | None = None

    # User ID from the OAuth provider
    oauth_provider_user_id: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")
