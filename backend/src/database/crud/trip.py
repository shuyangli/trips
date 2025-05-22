from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import Trip


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
