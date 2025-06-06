from datetime import datetime
from uuid import UUID
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, and_, or_, update, delete

from src.database.models import (
    itinerary_items,
    trips,
    trip_participants,
    ParticipantStatus,
    ItineraryItemType,
)


def create_itinerary_item(
    db: Session,
    created_by_user_id: UUID,
    type: ItineraryItemType,
    trip_id: UUID | None = None,
    itinerary_datetime: datetime | None = None,
    booking_reference: str | None = None,
    booking_url: str | None = None,
    notes: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict:
    """Create a new itinerary item."""
    item_insert_values = {
        "created_by_user_id": created_by_user_id,
        "type": type,
        "trip_id": trip_id,
        "itinerary_datetime": itinerary_datetime,
        "booking_reference": booking_reference,
        "booking_url": booking_url,
        "notes": notes,
        "details": details,
    }

    stmt_insert_item = (
        insert(itinerary_items)
        .values(item_insert_values)
        .returning(
            itinerary_items.c.itinerary_item_id,
            itinerary_items.c.trip_id,
            itinerary_items.c.created_by_user_id,
            itinerary_items.c.type,
            itinerary_items.c.itinerary_datetime,
            itinerary_items.c.booking_reference,
            itinerary_items.c.booking_url,
            itinerary_items.c.notes,
            itinerary_items.c.details,
            itinerary_items.c.created_at,
            itinerary_items.c.updated_at,
        )
    )

    item_result = db.execute(stmt_insert_item)
    db.commit()
    created_item_row = item_result.first()
    if not created_item_row:
        raise ValueError("Itinerary item creation failed to return item data.")
    return dict(created_item_row._mapping)


def user_has_itinerary_item_access(
    db: Session,
    itinerary_item_id: UUID,
    user_id: UUID,
) -> bool:
    """Check if user has access to an itinerary item (either as creator or through trip access)."""
    # Check if user is the item creator OR has access to the associated trip
    stmt = select(itinerary_items.c.itinerary_item_id).where(
        and_(
            itinerary_items.c.itinerary_item_id == itinerary_item_id,
            or_(
                # User created the item
                itinerary_items.c.created_by_user_id == user_id,
                # User has access to the trip (if item is associated with a trip)
                and_(
                    itinerary_items.c.trip_id.is_not(None),
                    or_(
                        # User owns the trip
                        itinerary_items.c.trip_id.in_(
                            select(trips.c.trip_id).where(
                                trips.c.created_by_user_id == user_id
                            )
                        ),
                        # User is a participant in the trip
                        itinerary_items.c.trip_id.in_(
                            select(trip_participants.c.trip_id).where(
                                and_(
                                    trip_participants.c.user_id == user_id,
                                    trip_participants.c.status.in_(
                                        [
                                            ParticipantStatus.INVITED,
                                            ParticipantStatus.JOINED,
                                        ]
                                    ),
                                )
                            )
                        ),
                    ),
                ),
            ),
        )
    )

    result = db.execute(stmt)
    return result.first() is not None


def get_itinerary_items_for_user(
    db: Session,
    user_id: UUID,
    trip_id: UUID | None = None,
) -> list[dict]:
    """Get itinerary items for a user, optionally filtered by trip."""
    # Build base query for items the user has access to
    stmt = select(
        itinerary_items.c.itinerary_item_id,
        itinerary_items.c.trip_id,
        itinerary_items.c.created_by_user_id,
        itinerary_items.c.type,
        itinerary_items.c.itinerary_datetime,
        itinerary_items.c.booking_reference,
        itinerary_items.c.booking_url,
        itinerary_items.c.notes,
        itinerary_items.c.details,
        itinerary_items.c.created_at,
        itinerary_items.c.updated_at,
    ).where(
        or_(
            # User created the item
            itinerary_items.c.created_by_user_id == user_id,
            # User has access to the trip (if item is associated with a trip)
            and_(
                itinerary_items.c.trip_id.is_not(None),
                or_(
                    # User owns the trip
                    itinerary_items.c.trip_id.in_(
                        select(trips.c.trip_id).where(
                            trips.c.created_by_user_id == user_id
                        )
                    ),
                    # User is a participant in the trip
                    itinerary_items.c.trip_id.in_(
                        select(trip_participants.c.trip_id).where(
                            and_(
                                trip_participants.c.user_id == user_id,
                                trip_participants.c.status.in_(
                                    [
                                        ParticipantStatus.INVITED,
                                        ParticipantStatus.JOINED,
                                    ]
                                ),
                            )
                        )
                    ),
                ),
            ),
        )
    )

    # Filter by trip if specified
    if trip_id is not None:
        stmt = stmt.where(itinerary_items.c.trip_id == trip_id)

    # Order by itinerary_datetime, then created_at
    stmt = stmt.order_by(
        itinerary_items.c.itinerary_datetime.asc().nulls_last(),
        itinerary_items.c.created_at.asc(),
    )

    result = db.execute(stmt)
    return [dict(row._mapping) for row in result.fetchall()]


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
        itinerary_items.c.details,
        itinerary_items.c.created_at,
        itinerary_items.c.updated_at,
    ).where(itinerary_items.c.trip_id == trip_id)

    # Order by itinerary_datetime, then by created_at for items without datetime
    stmt = stmt.order_by(
        itinerary_items.c.itinerary_datetime.asc().nulls_last(),
        itinerary_items.c.created_at.asc(),
    )

    result = db.execute(stmt)
    return [dict(row._mapping) for row in result.fetchall()]


def get_itinerary_item_by_id(
    db: Session,
    itinerary_item_id: UUID,
    user_id: UUID,
) -> dict | None:
    """Get a single itinerary item by ID, ensuring the user has access to it."""
    # First check if user has access
    if not user_has_itinerary_item_access(db, itinerary_item_id, user_id):
        return None

    # If user has access, get the item details
    stmt = select(
        itinerary_items.c.itinerary_item_id,
        itinerary_items.c.trip_id,
        itinerary_items.c.created_by_user_id,
        itinerary_items.c.type,
        itinerary_items.c.itinerary_datetime,
        itinerary_items.c.booking_reference,
        itinerary_items.c.booking_url,
        itinerary_items.c.notes,
        itinerary_items.c.details,
        itinerary_items.c.created_at,
        itinerary_items.c.updated_at,
    ).where(itinerary_items.c.itinerary_item_id == itinerary_item_id)

    result = db.execute(stmt)
    row = result.first()
    if not row:
        return None
    return dict(row._mapping)


def update_itinerary_item(
    db: Session,
    itinerary_item_id: UUID,
    user_id: UUID,
    trip_id: UUID | None = None,
    type: ItineraryItemType | None = None,
    itinerary_datetime: datetime | None = None,
    booking_reference: str | None = None,
    booking_url: str | None = None,
    notes: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict | None:
    """Update an itinerary item if the user has access to it."""
    # First check if user has access
    if not user_has_itinerary_item_access(db, itinerary_item_id, user_id):
        return None

    # Build update values (only include explicitly provided values)
    update_values = {"updated_at": datetime.utcnow()}
    if trip_id is not None:
        update_values["trip_id"] = trip_id
    if type is not None:
        update_values["type"] = type
    if itinerary_datetime is not None:
        update_values["itinerary_datetime"] = itinerary_datetime
    if booking_reference is not None:
        update_values["booking_reference"] = booking_reference
    if booking_url is not None:
        update_values["booking_url"] = booking_url
    if notes is not None:
        update_values["notes"] = notes
    if details is not None:
        update_values["details"] = details

    # Update the item
    stmt = (
        update(itinerary_items)
        .where(itinerary_items.c.itinerary_item_id == itinerary_item_id)
        .values(update_values)
        .returning(
            itinerary_items.c.itinerary_item_id,
            itinerary_items.c.trip_id,
            itinerary_items.c.created_by_user_id,
            itinerary_items.c.type,
            itinerary_items.c.itinerary_datetime,
            itinerary_items.c.booking_reference,
            itinerary_items.c.booking_url,
            itinerary_items.c.notes,
            itinerary_items.c.details,
            itinerary_items.c.created_at,
            itinerary_items.c.updated_at,
        )
    )

    result = db.execute(stmt)
    db.commit()
    row = result.first()
    if not row:
        return None
    return dict(row._mapping)


def delete_itinerary_item(
    db: Session,
    itinerary_item_id: UUID,
    user_id: UUID,
) -> bool:
    """Delete an itinerary item if the user has access to it."""
    # First check if user has access
    if not user_has_itinerary_item_access(db, itinerary_item_id, user_id):
        return False

    # Delete the item
    stmt = delete(itinerary_items).where(
        itinerary_items.c.itinerary_item_id == itinerary_item_id
    )

    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0
