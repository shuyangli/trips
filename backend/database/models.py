from datetime import datetime, timezone
import uuid
from enum import StrEnum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Float,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserStatus(StrEnum):
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"
    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    oauth_provider = Column(String, nullable=True)
    oauth_provider_user_id = Column(String, nullable=True)
    status = Column(
        SQLEnum(UserStatus, create_type=False),
        nullable=False,
        default=UserStatus.UNVERIFIED,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    trips = relationship("Trip", back_populates="creator")
    trip_participations = relationship("TripParticipant", back_populates="user")
    itinerary_items = relationship("ItineraryItem", back_populates="creator")
    itinerary_participants = relationship("ItineraryParticipant", back_populates="user")


class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_by_user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    creator = relationship("User", back_populates="trips")
    participants = relationship("TripParticipant", back_populates="trip")
    segments = relationship("TripSegment", back_populates="trip")
    itinerary_items = relationship("ItineraryItem", back_populates="trip")


class TripParticipantStatus(StrEnum):
    UNKNOWN = "unknown"
    INVITED = "invited"
    JOINED = "joined"
    DECLINED = "declined"
    LEFT = "left"


class TripParticipant(Base):
    __tablename__ = "trip_participants"

    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.trip_id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    status = Column(
        SQLEnum(TripParticipantStatus, create_type=False),
        nullable=False,
        default=TripParticipantStatus.UNKNOWN,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    trip = relationship("Trip", back_populates="participants")
    user = relationship("User", back_populates="trip_participations")


class TripSegment(Base):
    __tablename__ = "trip_segments"

    trip_segment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.trip_id"), nullable=False)
    location_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    trip = relationship("Trip", back_populates="segments")


class ItineraryItemType(StrEnum):
    UNKNOWN = "unknown"
    FLIGHT = "flight"
    GROUND_TRANSPORTATION = "ground"
    CAR_RENTAL = "car_rental"
    ACCOMMODATION = "accommodation"
    ACTIVITY = "activity"


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    itinerary_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.trip_id"), nullable=True)
    created_by_user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    type = Column(SQLEnum(ItineraryItemType, create_type=False), nullable=False)
    itinerary_datetime = Column(DateTime(timezone=True), nullable=True)
    booking_reference = Column(String, nullable=True)
    booking_url = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    raw_details_json = Column(JSON, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    trip = relationship("Trip", back_populates="itinerary_items")
    creator = relationship("User", back_populates="itinerary_items")
    participants = relationship("ItineraryParticipant", back_populates="itinerary_item")


class ItineraryParticipantStatus(StrEnum):
    UNKNOWN = "unknown"
    INVITED = "invited"
    JOINED = "joined"
    DECLINED = "declined"
    LEFT = "left"


class ItineraryParticipant(Base):
    __tablename__ = "itinerary_participants"

    itinerary_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("itinerary_items.itinerary_item_id"),
        primary_key=True,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    status = Column(
        SQLEnum(ItineraryParticipantStatus, create_type=False),
        nullable=False,
        default=ItineraryParticipantStatus.UNKNOWN,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    itinerary_item = relationship("ItineraryItem", back_populates="participants")
    user = relationship("User", back_populates="itinerary_participants")
