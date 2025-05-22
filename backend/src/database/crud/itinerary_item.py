from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import ItineraryItem, ItineraryItemType


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
