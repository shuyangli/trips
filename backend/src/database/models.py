from enum import StrEnum
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    MetaData,
    Table,
    JSON,
    Float,
    Enum as SQLEnum,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

metadata_obj = MetaData()


class UserStatus(StrEnum):
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class ParticipantStatus(StrEnum):
    UNKNOWN = "unknown"
    INVITED = "invited"
    JOINED = "joined"
    DECLINED = "declined"
    LEFT = "left"


class ItineraryItemType(StrEnum):
    UNKNOWN = "unknown"
    FLIGHT = "flight"
    GROUND_TRANSPORTATION = "ground"
    CAR_RENTAL = "car_rental"
    ACCOMMODATION = "accommodation"
    ACTIVITY = "activity"


metadata = MetaData()

users = Table(
    "users",
    metadata_obj,
    Column(
        "user_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("email", String, unique=True, nullable=False),
    Column("password_hash", String, nullable=False),
    Column("given_name", String, nullable=False),
    Column("family_name", String, nullable=False),
    Column("profile_picture_url", String, nullable=True),
    Column("oauth_provider", String, nullable=True),
    Column("oauth_provider_user_id", String, nullable=True),
    Column(
        "status",
        SQLEnum(UserStatus, create_type=False),
        nullable=False,
        server_default=text("'UNVERIFIED'"),
    ),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

trips = Table(
    "trips",
    metadata_obj,
    Column(
        "trip_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column(
        "created_by_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
    ),
    Column("start_date", DateTime(timezone=True), nullable=True),
    Column("end_date", DateTime(timezone=True), nullable=True),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

trip_participants = Table(
    "trip_participants",
    metadata_obj,
    Column(
        "trip_id", UUID(as_uuid=True), ForeignKey("trips.trip_id"), primary_key=True
    ),
    Column(
        "user_id", UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True
    ),
    Column(
        "status",
        SQLEnum(ParticipantStatus, create_type=False),
        nullable=False,
        server_default=text("'UNKNOWN'"),
    ),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

trip_segments = Table(
    "trip_segments",
    metadata_obj,
    Column(
        "trip_segment_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("trip_id", UUID(as_uuid=True), ForeignKey("trips.trip_id"), nullable=False),
    Column("location_name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("latitude", Float, nullable=True),
    Column("longitude", Float, nullable=True),
    Column("start_date", DateTime(timezone=True), nullable=True),
    Column("end_date", DateTime(timezone=True), nullable=True),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

itinerary_items = Table(
    "itinerary_items",
    metadata_obj,
    Column(
        "itinerary_item_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("trip_id", UUID(as_uuid=True), ForeignKey("trips.trip_id"), nullable=True),
    Column(
        "created_by_user_id",
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
    ),
    Column("type", SQLEnum(ItineraryItemType, create_type=False), nullable=False),
    Column("itinerary_datetime", DateTime(timezone=True), nullable=True),
    Column("booking_reference", String, nullable=True),
    Column("booking_url", String, nullable=True),
    Column("notes", String, nullable=True),
    Column("raw_details_json", JSON, nullable=True),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

itinerary_participants = Table(
    "itinerary_participants",
    metadata_obj,
    Column(
        "itinerary_item_id",
        UUID(as_uuid=True),
        ForeignKey("itinerary_items.itinerary_item_id"),
        primary_key=True,
    ),
    Column(
        "user_id", UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True
    ),
    Column(
        "status",
        SQLEnum(ParticipantStatus, create_type=False),
        nullable=False,
        server_default=text("'UNKNOWN'"),
    ),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)
