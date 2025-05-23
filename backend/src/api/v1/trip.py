from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from src.database.config import get_db
from src.database.crud.trip import Trip as DbTrip
from src.schemas.trip import Trip, CreateTripRequest

router = APIRouter()
logger = logging.Logger(__name__)


@router.post("/trips", response_model=Trip)
def create_trip(trip: CreateTripRequest, db: Session = Depends(get_db)):
    db_trip = DbTrip(
        name=trip.name,
        description=trip.description,
        created_by_user_id=trip.created_by_user_id,
        start_date=trip.start_date,
        end_date=trip.end_date,
    )

    try:
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
    except Exception as e:
        logger.error(f"Failed to create trip: {e}")
        raise e

    return Trip.model_validate(db_trip)
