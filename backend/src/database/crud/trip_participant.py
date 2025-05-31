from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, and_, delete

from src.database.models import trip_participants, users, trips, ParticipantStatus


def invite_user_to_trip(
    db: Session,
    trip_id: UUID,
    user_email: str,
    inviter_user_id: UUID,
) -> dict | None:
    """Invite a user to a trip by email. Returns the invitation record if successful."""
    # First find the user by email
    user_stmt = select(users.c.user_id).where(users.c.email == user_email)
    user_result = db.execute(user_stmt)
    user_row = user_result.first()
    
    if not user_row:
        return None  # User not found
    
    invited_user_id = user_row.user_id
    
    # Check if user is already invited or participating
    existing_stmt = select(trip_participants.c.status).where(
        and_(
            trip_participants.c.trip_id == trip_id,
            trip_participants.c.user_id == invited_user_id
        )
    )
    existing_result = db.execute(existing_stmt)
    existing_row = existing_result.first()
    
    if existing_row:
        return None  # User already has a relationship with this trip
    
    # Create invitation
    invitation_values = {
        "trip_id": trip_id,
        "user_id": invited_user_id,
        "status": ParticipantStatus.INVITED,
    }
    
    stmt = (
        insert(trip_participants)
        .values(invitation_values)
        .returning(
            trip_participants.c.trip_id,
            trip_participants.c.user_id,
            trip_participants.c.status,
            trip_participants.c.created_at,
            trip_participants.c.updated_at,
        )
    )
    
    result = db.execute(stmt)
    db.commit()
    created_row = result.first()
    if not created_row:
        return None
    return dict(created_row._mapping)


def get_user_invitations(
    db: Session,
    user_id: UUID,
) -> list[dict]:
    """Get all pending invitations for a user."""
    stmt = select(
        trip_participants.c.trip_id,
        trip_participants.c.user_id,
        trip_participants.c.status,
        trip_participants.c.created_at,
        trip_participants.c.updated_at,
        trips.c.name.label("trip_name"),
        trips.c.description.label("trip_description"),
        trips.c.start_date,
        trips.c.end_date,
        users.c.given_name.label("inviter_given_name"),
        users.c.family_name.label("inviter_family_name"),
    ).select_from(
        trip_participants.join(trips, trip_participants.c.trip_id == trips.c.trip_id)
        .join(users, trips.c.created_by_user_id == users.c.user_id)
    ).where(
        and_(
            trip_participants.c.user_id == user_id,
            trip_participants.c.status == ParticipantStatus.INVITED
        )
    ).order_by(trip_participants.c.created_at.desc())
    
    result = db.execute(stmt)
    return [dict(row._mapping) for row in result.fetchall()]


def respond_to_invitation(
    db: Session,
    trip_id: UUID,
    user_id: UUID,
    response: ParticipantStatus,  # Should be JOINED or DECLINED
) -> dict | None:
    """Respond to a trip invitation."""
    if response not in [ParticipantStatus.JOINED, ParticipantStatus.DECLINED]:
        return None
    
    # Update the invitation status
    stmt = (
        update(trip_participants)
        .where(
            and_(
                trip_participants.c.trip_id == trip_id,
                trip_participants.c.user_id == user_id,
                trip_participants.c.status == ParticipantStatus.INVITED
            )
        )
        .values(
            status=response,
            updated_at=datetime.utcnow()
        )
        .returning(
            trip_participants.c.trip_id,
            trip_participants.c.user_id,
            trip_participants.c.status,
            trip_participants.c.created_at,
            trip_participants.c.updated_at,
        )
    )
    
    result = db.execute(stmt)
    db.commit()
    updated_row = result.first()
    if not updated_row:
        return None
    return dict(updated_row._mapping)


def get_trip_participants(
    db: Session,
    trip_id: UUID,
) -> list[dict]:
    """Get all participants for a trip (including pending invitations)."""
    stmt = select(
        trip_participants.c.trip_id,
        trip_participants.c.user_id,
        trip_participants.c.status,
        trip_participants.c.created_at,
        trip_participants.c.updated_at,
        users.c.email,
        users.c.given_name,
        users.c.family_name,
    ).select_from(
        trip_participants.join(users, trip_participants.c.user_id == users.c.user_id)
    ).where(
        trip_participants.c.trip_id == trip_id
    ).order_by(trip_participants.c.created_at.asc())
    
    result = db.execute(stmt)
    return [dict(row._mapping) for row in result.fetchall()]