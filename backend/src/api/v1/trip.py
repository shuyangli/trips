from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.config import get_db
from src.schemas.trip import Trip, CreateTripRequest

router = APIRouter()


@router.post("/trips", response_model=Trip)
def create_trip(trip: CreateTripRequest, db: Session = Depends(get_db)):
    # Check if the user exists
    result = db.execute(
        text("SELECT 1 FROM users WHERE user_id = :user_id"),
        {"user_id": trip.created_by_user_id},
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    # Timezones?
    db.execute(
        text("""
            INSERT INTO trips (name, description, created_by_user_id, start_date, end_date)
            VALUES (:name, :description, :created_by_user_id, :start_date, :end_date)
            RETURNING id
        """),
        {
            "name": trip.name,
            "description": trip.description,
            "created_by_user_id": trip.created_by_user_id,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
        },
    )

    # Fetch the newly created trip
    result = db.execute(
        text(
            "SELECT * FROM trips WHERE name = :name AND created_by_user_id = :created_by_user_id"
        ),
        {"name": trip.name, "created_by_user_id": trip.created_by_user_id},
    ).fetchone()

    db.commit()

    return Trip.from_orm(result)
