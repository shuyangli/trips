from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, and_

from src.database.models import trips


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
    """Get trips for a user, optionally filtering to future trips only."""
    stmt = select(
        trips.c.trip_id,
        trips.c.name,
        trips.c.description,
        trips.c.created_by_user_id,
        trips.c.start_date,
        trips.c.end_date,
        trips.c.created_at,
        trips.c.updated_at,
    ).where(trips.c.created_by_user_id == user_id)
    
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
