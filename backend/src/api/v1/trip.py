import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from src.auth import get_current_user
from src.schemas.user import User
from src.database.config import get_db
from src.database.crud.trip import (
    create_trip as create_trip_crud,
    get_trips_for_user,
    get_trip_by_id,
    update_trip,
)
from src.database.crud.itinerary_item import get_itinerary_items_for_trip
from src.database.crud.trip_participant import (
    invite_user_to_trip,
    get_user_invitations,
    respond_to_invitation,
    get_trip_participants,
)
from src.schemas.trip import Trip, CreateTripRequest, TripDetails
from src.schemas.itinerary_item import ItineraryItem
from src.schemas.trip_participant import (
    TripInvitation,
    InviteUserRequest,
    RespondToInvitationRequest,
    TripParticipantWithUser,
    ParticipantStatus,
)

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


@router.get("/trips/{trip_id}", response_model=TripDetails)
def get_trip_details(
    trip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TripDetails:
    try:
        # Convert string trip_id to UUID
        trip_uuid = uuid.UUID(trip_id)

        # Get trip details
        trip_data = get_trip_by_id(
            db=db,
            trip_id=trip_uuid,
            user_id=current_user.user_id,
        )

        if not trip_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found or you don't have access to it",
            )

        # Get itinerary items for this trip
        itinerary_items = get_itinerary_items_for_trip(
            db=db,
            trip_id=trip_uuid,
        )

        # Add itinerary items to trip data
        trip_data["itinerary_items"] = itinerary_items

        return TripDetails.model_validate(trip_data)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID format",
        )
    except Exception as e:
        logger.error(f"Error fetching trip details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.put("/trips/{trip_id}", response_model=Trip)
def update_trip_details(
    trip_id: str,
    trip: CreateTripRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Trip:
    try:
        # Convert string trip_id to UUID
        trip_uuid = uuid.UUID(trip_id)

        # Update trip
        updated_trip = update_trip(
            db=db,
            trip_id=trip_uuid,
            user_id=current_user.user_id,
            name=trip.name,
            description=trip.description,
            start_date=trip.start_date,
            end_date=trip.end_date,
        )

        if not updated_trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found or you don't have permission to update it",
            )

        return Trip.model_validate(updated_trip)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID format",
        )
    except Exception as e:
        logger.error(f"Error updating trip: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.post("/trips/{trip_id}/invite")
def invite_user_to_trip_endpoint(
    trip_id: str,
    invite_request: InviteUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Invite a user to a trip by email."""
    try:
        trip_uuid = uuid.UUID(trip_id)

        # Check if current user has access to this trip
        from src.database.crud.trip import user_has_trip_access

        if not user_has_trip_access(db, trip_uuid, current_user.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found or you don't have permission to invite users",
            )

        invitation = invite_user_to_trip(
            db=db,
            trip_id=trip_uuid,
            user_email=invite_request.email,
            inviter_user_id=current_user.user_id,
        )

        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found, already invited, or already participating in this trip",
            )

        return {"message": "Invitation sent successfully"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID format",
        )
    except Exception as e:
        logger.error(f"Error inviting user to trip: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get("/invitations", response_model=list[TripInvitation])
def get_my_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TripInvitation]:
    """Get all pending invitations for the current user."""
    try:
        invitations_data = get_user_invitations(
            db=db,
            user_id=current_user.user_id,
        )

        return [
            TripInvitation.model_validate(invitation) for invitation in invitations_data
        ]

    except Exception as e:
        logger.error(f"Error fetching user invitations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.post("/trips/{trip_id}/respond")
def respond_to_trip_invitation(
    trip_id: str,
    response_request: RespondToInvitationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Respond to a trip invitation (accept or decline)."""
    try:
        trip_uuid = uuid.UUID(trip_id)

        if response_request.response not in [
            ParticipantStatus.JOINED,
            ParticipantStatus.DECLINED,
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Response must be either 'JOINED' or 'DECLINED'",
            )

        response_result = respond_to_invitation(
            db=db,
            trip_id=trip_uuid,
            user_id=current_user.user_id,
            response=response_request.response,
        )

        if not response_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found or already responded to",
            )

        action = (
            "accepted"
            if response_request.response == ParticipantStatus.JOINED
            else "declined"
        )
        return {"message": f"Invitation {action} successfully"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID format",
        )
    except Exception as e:
        logger.error(f"Error responding to invitation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get(
    "/trips/{trip_id}/participants", response_model=list[TripParticipantWithUser]
)
def get_trip_participants_endpoint(
    trip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TripParticipantWithUser]:
    """Get all participants for a trip."""
    try:
        trip_uuid = uuid.UUID(trip_id)

        # Check if current user has access to this trip
        from src.database.crud.trip import user_has_trip_access

        if not user_has_trip_access(db, trip_uuid, current_user.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found or you don't have permission to view participants",
            )

        participants_data = get_trip_participants(
            db=db,
            trip_id=trip_uuid,
        )

        return [
            TripParticipantWithUser.model_validate(participant)
            for participant in participants_data
        ]

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid trip ID format",
        )
    except Exception as e:
        logger.error(f"Error fetching trip participants: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
