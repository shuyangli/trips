from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.models import itinerary_items


def get_itinerary_items_for_trip(
    db: Session,
    trip_id: UUID,
) -> list[dict]:
    """Get all itinerary items for a trip, ordered by itinerary_datetime."""
    stmt = select(
        itinerary_items.c.itinerary_item_id,
        itinerary_items.c.trip_id,
        itinerary_items.c.created_by_user_id,
        itinerary_items.c.type,
        itinerary_items.c.itinerary_datetime,
        itinerary_items.c.booking_reference,
        itinerary_items.c.booking_url,
        itinerary_items.c.notes,
        itinerary_items.c.raw_details_json,
        itinerary_items.c.created_at,
        itinerary_items.c.updated_at,
    ).where(itinerary_items.c.trip_id == trip_id)
    
    # Order by itinerary_datetime, then by created_at for items without datetime
    stmt = stmt.order_by(
        itinerary_items.c.itinerary_datetime.asc().nulls_last(),
        itinerary_items.c.created_at.asc()
    )
    
    result = db.execute(stmt)
    return [dict(row._mapping) for row in result.fetchall()]