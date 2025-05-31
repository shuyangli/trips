import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from src.auth import get_current_user
from src.schemas.user import User
from src.database.config import get_db
from src.database.crud.trip import create_trip as create_trip_crud, get_trips_for_user
from src.schemas.trip import Trip, CreateTripRequest

router = APIRouter()
logger = logging.Logger(__name__)


@router.post("/trips", response_model=Trip)
def create_trip(
    trip: CreateTripRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Trip:
    try:
        trip_response = create_trip_crud(
            db=db,
            name=trip.name,
            created_by_user_id=current_user.user_id,
            description=trip.description,
            start_date=trip.start_date,
            end_date=trip.end_date,
        )

        if not trip_response:
            # This case should ideally be prevented by database constraints or prior checks,
            # or indicate a more fundamental issue if the insert succeeded but returned nothing.
            # In a real app, raise an appropriate HTTP exception.
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Trip creation failed to return trip data.",
            )

        return Trip.model_validate(trip_response)

    except Exception as e:
        logger.error(f"Error creating trip: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get("/trips", response_model=list[Trip])
def get_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Trip]:
    try:
        trips_data = get_trips_for_user(
            db=db,
            user_id=current_user.user_id,
            future_only=True,
        )
        
        return [Trip.model_validate(trip) for trip in trips_data]
        
    except Exception as e:
        logger.error(f"Error fetching trips: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
