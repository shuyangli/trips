from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models import (
    User,
    Trip,
    TripParticipant,
    TripSegment,
    ItineraryItem,
    ItineraryParticipant,
    UserStatus,
    TripParticipantStatus,
    ItineraryParticipantStatus,
    ItineraryItemType,
)


# User CRUD operations
def create_user(
    db: Session,
    email: str,
    password_hash: str,
    full_name: str,
    oauth_provider: Optional[str] = None,
    oauth_provider_user_id: Optional[str] = None,
) -> User:
    db_user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        oauth_provider=oauth_provider,
        oauth_provider_user_id=oauth_provider_user_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def update_user_status(
    db: Session, user_id: UUID, status: UserStatus
) -> Optional[User]:
    user = get_user(db, user_id)
    if user:
        user.status = status
        db.commit()
        db.refresh(user)
    return user


# Trip CRUD operations
def create_trip(
    db: Session,
    name: str,
    created_by_user_id: UUID,
    description: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Trip:
    db_trip = Trip(
        name=name,
        description=description,
        created_by_user_id=created_by_user_id,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


def get_trip(db: Session, trip_id: UUID) -> Optional[Trip]:
    return db.query(Trip).filter(Trip.trip_id == trip_id).first()


def get_user_trips(db: Session, user_id: UUID) -> List[Trip]:
    return db.query(Trip).filter(Trip.created_by_user_id == user_id).all()


# Trip Participant CRUD operations
def add_trip_participant(
    db: Session,
    trip_id: UUID,
    user_id: UUID,
    status: TripParticipantStatus = TripParticipantStatus.INVITED,
) -> TripParticipant:
    db_participant = TripParticipant(
        trip_id=trip_id,
        user_id=user_id,
        status=status,
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


def update_participant_status(
    db: Session, trip_id: UUID, user_id: UUID, status: TripParticipantStatus
) -> Optional[TripParticipant]:
    participant = (
        db.query(TripParticipant)
        .filter(TripParticipant.trip_id == trip_id, TripParticipant.user_id == user_id)
        .first()
    )
    if participant:
        participant.status = status
        db.commit()
        db.refresh(participant)
    return participant


# Trip Segment CRUD operations
def create_trip_segment(
    db: Session,
    trip_id: UUID,
    location_name: str,
    description: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> TripSegment:
    db_segment = TripSegment(
        trip_id=trip_id,
        location_name=location_name,
        description=description,
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment


def get_trip_segments(db: Session, trip_id: UUID) -> List[TripSegment]:
    return db.query(TripSegment).filter(TripSegment.trip_id == trip_id).all()


# Itinerary Item CRUD operations
def create_itinerary_item(
    db: Session,
    created_by_user_id: UUID,
    type: ItineraryItemType,
    trip_id: Optional[UUID] = None,
    itinerary_datetime: Optional[datetime] = None,
    booking_reference: Optional[str] = None,
    booking_url: Optional[str] = None,
    notes: Optional[str] = None,
    raw_details_json: Optional[dict] = None,
) -> ItineraryItem:
    db_item = ItineraryItem(
        created_by_user_id=created_by_user_id,
        type=type.value,
        trip_id=trip_id,
        itinerary_datetime=itinerary_datetime,
        booking_reference=booking_reference,
        booking_url=booking_url,
        notes=notes,
        raw_details_json=raw_details_json,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_trip_itinerary_items(db: Session, trip_id: UUID) -> List[ItineraryItem]:
    return db.query(ItineraryItem).filter(ItineraryItem.trip_id == trip_id).all()


# Shared Itinerary Item Participant CRUD operations
def add_itinerary_participant(
    db: Session,
    itinerary_item_id: UUID,
    user_id: UUID,
    status: ItineraryParticipantStatus = ItineraryParticipantStatus.INVITED,
) -> ItineraryParticipant:
    db_participant = ItineraryParticipant(
        itinerary_item_id=itinerary_item_id,
        user_id=user_id,
        status=status,
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


def update_itinerary_participant_status(
    db: Session,
    itinerary_item_id: UUID,
    user_id: UUID,
    status: ItineraryParticipantStatus,
) -> Optional[ItineraryParticipant]:
    participant = (
        db.query(ItineraryParticipant)
        .filter(
            ItineraryParticipant.itinerary_item_id == itinerary_item_id,
            ItineraryParticipant.user_id == user_id,
        )
        .first()
    )
    if participant:
        participant.update(
            {
                ItineraryParticipant.status: status,
                ItineraryParticipant.updated_at: datetime.now(timezone.utc),
            }
        )
        db.commit()
        db.refresh(participant)
    return participant
