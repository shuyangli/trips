from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update

from src.database.models import TripParticipant, TripParticipantStatus


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
        stmt = (
            update(TripParticipant)
            .where(
                TripParticipant.trip_id == trip_id, TripParticipant.user_id == user_id
            )
            .values(status=status.value)
        )
        db.execute(stmt)
        db.commit()
        db.refresh(participant)
    return participant
