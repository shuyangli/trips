from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import insert

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
