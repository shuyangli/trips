from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from backend.src.database.config import get_db
from backend.src.models.trip import Trip
from backend.src.schemas.trip import TripCreate, TripResponse
from backend.src.database.models import User  # Import the User model

router = APIRouter()

@router.post("/trips", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = db.query(User).filter(User.user_id == trip.created_by_user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new trip
    db_trip = Trip(
        name=trip.name,
        description=trip.description,
        created_by_user_id=trip.created_by_user_id,
        start_date=trip.start_date,
        end_date=trip.end_date,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return TripResponse.from_orm(db_trip)
