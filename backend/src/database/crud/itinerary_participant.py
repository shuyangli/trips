from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import ItineraryParticipant, ItineraryParticipantStatus


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
