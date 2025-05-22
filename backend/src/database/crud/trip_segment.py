from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.database.models import TripSegment


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
