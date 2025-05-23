from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.schemas.trip import Trip, CreateTripRequest
from src.database.models import User  # Import the User model

router = APIRouter()

@router.post("/trips", response_model=Trip)
def create_trip(trip: CreateTripRequest, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = (
        db.query(User).filter(User.user_id == trip.created_by_user_id).first()
    )
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new trip
    db_trip = Trip(
        name=trip.name,
        description=trip.description,
        created_by_user_id=trip.created_by_user_id,
        start_date=trip.start_date,
        end_date=trip.end_date,
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return Trip.from_orm(db_trip)
