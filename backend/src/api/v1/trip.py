"""API routes to manage trips."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.models import User
from src.database.config import get_db
from src.database.crud import get_user_trips
from src.auth import get_current_user

router = APIRouter()


# What we need here:
# - Get all future trips for a user
# - Get all trips for a user between specific dates
# - Create a trip
# - Update a trip
# - Delete a trip
# - Get a trip including all itinerary items


@router.get("/future")
async def get_future_trips(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # The user from get_current_user is already a database model instance
    # We need to get the actual UUID value from the model
    user_id = current_user.user_id
    if not isinstance(user_id, UUID):
        user_id = UUID(str(user_id))
    return get_user_trips(db, user_id)
