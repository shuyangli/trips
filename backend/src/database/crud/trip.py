from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, and_, or_, update

from src.database.models import trips, trip_participants


def create_trip(
    db: Session,
    name: str,
    created_by_user_id: UUID,
    description: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> dict:
    trip_insert_values = {
        "name": name,
        "description": description,
        "created_by_user_id": created_by_user_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    stmt_insert_trip = (
        insert(trips)
        .values(trip_insert_values)
        .returning(
            trips.c.trip_id,
            trips.c.name,
            trips.c.description,
            trips.c.created_by_user_id,
            trips.c.start_date,
            trips.c.end_date,
            trips.c.created_at,
            trips.c.updated_at,
        )
    )

    trip_result = db.execute(stmt_insert_trip)
    db.commit()
    created_trip_row = trip_result.first()
    if not created_trip_row:
        raise ValueError("Trip creation failed to return trip data.")
    return dict(created_trip_row._mapping)


def get_trips_for_user(
    db: Session,
    user_id: UUID,
    future_only: bool = True,
) -> list[dict]:
    """Get trips for a user (created by them or where they are a participant), optionally filtering to future trips only."""
    # Get trips where user is owner OR participant
    stmt = select(
        trips.c.trip_id,
        trips.c.name,
        trips.c.description,
        trips.c.created_by_user_id,
        trips.c.start_date,
        trips.c.end_date,
        trips.c.created_at,
        trips.c.updated_at,
    ).where(
        or_(
            trips.c.created_by_user_id == user_id,
            trips.c.trip_id.in_(
                select(trip_participants.c.trip_id).where(
                    trip_participants.c.user_id == user_id
                )
            )
        )
    )
    
    if future_only:
        now = datetime.utcnow()
        stmt = stmt.where(
            and_(
                trips.c.start_date.is_not(None),
                trips.c.start_date >= now
            )
        )
    
    stmt = stmt.order_by(trips.c.start_date.asc())
    
    result = db.execute(stmt)
    return [dict(row._mapping) for row in result.fetchall()]


def user_has_trip_access(
    db: Session,
    trip_id: UUID,
    user_id: UUID,
) -> bool:
    """Check if user has access to a trip (either as owner or participant)."""
    # Check if user is the trip owner OR a trip participant
    stmt = select(trips.c.trip_id).where(
        and_(
            trips.c.trip_id == trip_id,
            or_(
                trips.c.created_by_user_id == user_id,
                trips.c.trip_id.in_(
                    select(trip_participants.c.trip_id).where(
                        and_(
                            trip_participants.c.trip_id == trip_id,
                            trip_participants.c.user_id == user_id
                        )
                    )
                )
            )
        )
    )
    
    result = db.execute(stmt)
    return result.first() is not None


def get_trip_by_id(
    db: Session,
    trip_id: UUID,
    user_id: UUID,
) -> dict | None:
    """Get a single trip by ID, ensuring the user has access to it."""
    # First check if user has access
    if not user_has_trip_access(db, trip_id, user_id):
        return None
    
    # If user has access, get the trip details
    stmt = select(
        trips.c.trip_id,
        trips.c.name,
        trips.c.description,
        trips.c.created_by_user_id,
        trips.c.start_date,
        trips.c.end_date,
        trips.c.created_at,
        trips.c.updated_at,
    ).where(trips.c.trip_id == trip_id)
    
    result = db.execute(stmt)
    row = result.first()
    if not row:
        return None
    return dict(row._mapping)


def update_trip(
    db: Session,
    trip_id: UUID,
    user_id: UUID,
    name: str | None = None,
    description: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> dict | None:
    """Update a trip if the user has access to it."""
    # First check if user has access
    if not user_has_trip_access(db, trip_id, user_id):
        return None
    
    # Build update values (only include non-None values)
    update_values = {"updated_at": datetime.utcnow()}
    if name is not None:
        update_values["name"] = name
    if description is not None:
        update_values["description"] = description
    if start_date is not None:
        update_values["start_date"] = start_date
    if end_date is not None:
        update_values["end_date"] = end_date
    
    # Update the trip
    stmt_update = (
        update(trips)
        .where(trips.c.trip_id == trip_id)
        .values(update_values)
        .returning(
            trips.c.trip_id,
            trips.c.name,
            trips.c.description,
            trips.c.created_by_user_id,
            trips.c.start_date,
            trips.c.end_date,
            trips.c.created_at,
            trips.c.updated_at,
        )
    )
    
    result = db.execute(stmt_update)
    db.commit()
    updated_row = result.first()
    if not updated_row:
        return None
    return dict(updated_row._mapping)
