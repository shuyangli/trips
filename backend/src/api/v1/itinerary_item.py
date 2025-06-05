import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from src.auth import get_current_user
from src.schemas.user import User
from src.database.config import get_db
from src.database.crud.itinerary_item import (
    create_itinerary_item as create_itinerary_item_crud,
    get_itinerary_items_for_user,
    get_itinerary_item_by_id,
    update_itinerary_item,
    delete_itinerary_item,
)
from src.schemas.itinerary_item import (
    ItineraryItem,
    CreateItineraryItemRequest,
    ItineraryItemUpdate,
    ItineraryItemType,
    FlightItineraryItem,
    GroundTransportationItineraryItem,
    CarRentalItineraryItem,
    AccommodationItineraryItem,
    ActivityItineraryItem,
)

router = APIRouter()
logger = logging.Logger(__name__)


def _validate_itinerary_item(item_data: Any) -> ItineraryItem:
    """Validate and convert database item to the appropriate itinerary item type."""
    item_type = item_data.type
    if item_type == ItineraryItemType.FLIGHT:
        return FlightItineraryItem.model_validate(item_data)
    elif item_type == ItineraryItemType.GROUND_TRANSPORTATION:
        return GroundTransportationItineraryItem.model_validate(item_data)
    elif item_type == ItineraryItemType.CAR_RENTAL:
        return CarRentalItineraryItem.model_validate(item_data)
    elif item_type == ItineraryItemType.ACCOMMODATION:
        return AccommodationItineraryItem.model_validate(item_data)
    elif item_type == ItineraryItemType.ACTIVITY:
        return ActivityItineraryItem.model_validate(item_data)
    else:
        raise ValueError(f"Unknown itinerary item type: {item_type}")


@router.post("/itinerary-items", response_model=ItineraryItem)
def create_itinerary_item(
    item: CreateItineraryItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryItem:
    """Create a new itinerary item."""
    try:
        # Convert trip_id to UUID if provided
        trip_uuid = None
        if item.trip_id:
            try:
                trip_uuid = uuid.UUID(item.trip_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid trip ID format",
                )

        item_response = create_itinerary_item_crud(
            db=db,
            created_by_user_id=current_user.user_id,
            type=item.type,
            trip_id=trip_uuid,
            itinerary_datetime=item.itinerary_datetime,
            booking_reference=item.booking_reference,
            booking_url=item.booking_url,
            notes=item.notes,
            raw_details_json=item.raw_details_json,
        )

        if not item_response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Itinerary item creation failed to return item data.",
            )

        return _validate_itinerary_item(item_response)

    except Exception as e:
        logger.error(f"Error creating itinerary item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get("/itinerary-items", response_model=list[ItineraryItem])
def get_itinerary_items(
    trip_id: Optional[str] = Query(None, description="Filter by trip ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ItineraryItem]:
    """Get itinerary items for the current user, optionally filtered by trip."""
    try:
        # Convert trip_id to UUID if provided
        trip_uuid = None
        if trip_id:
            try:
                trip_uuid = uuid.UUID(trip_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid trip ID format",
                )

        items_data = get_itinerary_items_for_user(
            db=db,
            user_id=current_user.user_id,
            trip_id=trip_uuid,
        )

        return [_validate_itinerary_item(item) for item in items_data]

    except Exception as e:
        logger.error(f"Error fetching itinerary items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get("/itinerary-items/{item_id}", response_model=ItineraryItem)
def get_itinerary_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryItem:
    """Get a specific itinerary item by ID."""
    try:
        # Convert string item_id to UUID
        item_uuid = uuid.UUID(item_id)

        # Get item details
        item_data = get_itinerary_item_by_id(
            db=db,
            itinerary_item_id=item_uuid,
            user_id=current_user.user_id,
        )

        if not item_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Itinerary item not found or you don't have access to it",
            )

        return _validate_itinerary_item(item_data)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format",
        )
    except Exception as e:
        logger.error(f"Error fetching itinerary item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.put("/itinerary-items/{item_id}", response_model=ItineraryItem)
def update_itinerary_item_endpoint(
    item_id: str,
    item_update: ItineraryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ItineraryItem:
    """Update an itinerary item."""
    try:
        # Convert string item_id to UUID
        item_uuid = uuid.UUID(item_id)

        # Convert trip_id to UUID if provided
        trip_uuid = None
        if item_update.trip_id:
            try:
                trip_uuid = uuid.UUID(item_update.trip_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid trip ID format",
                )

        # Update item
        updated_item = update_itinerary_item(
            db=db,
            itinerary_item_id=item_uuid,
            user_id=current_user.user_id,
            trip_id=trip_uuid,
            type=item_update.type,
            itinerary_datetime=item_update.itinerary_datetime,
            booking_reference=item_update.booking_reference,
            booking_url=item_update.booking_url,
            notes=item_update.notes,
            raw_details_json=item_update.raw_details_json,
        )

        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Itinerary item not found or you don't have permission to update it",
            )

        return _validate_itinerary_item(updated_item)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format",
        )
    except Exception as e:
        logger.error(f"Error updating itinerary item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.delete("/itinerary-items/{item_id}")
def delete_itinerary_item_endpoint(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an itinerary item."""
    try:
        # Convert string item_id to UUID
        item_uuid = uuid.UUID(item_id)

        # Delete item
        deleted = delete_itinerary_item(
            db=db,
            itinerary_item_id=item_uuid,
            user_id=current_user.user_id,
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Itinerary item not found or you don't have permission to delete it",
            )

        return {"message": "Itinerary item deleted successfully"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format",
        )
    except Exception as e:
        logger.error(f"Error deleting itinerary item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
