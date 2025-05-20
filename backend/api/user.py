from datetime import datetime
from enum import StrEnum
import uuid
from pydantic import BaseModel, Field


class UserStatus(StrEnum):
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str

    # Do we need this?
    password_hash: str
    full_name: str

    # OAuth provider for social logins
    oauth_provider: str | None = None

    # User ID from the OAuth provider
    oauth_provider_user_id: str | None = None

    created_at: datetime
    updated_at: datetime
