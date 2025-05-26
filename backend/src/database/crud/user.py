from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update, insert, select

from src.database.models import users, UserStatus


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    given_name: str,
    family_name: str,
    profile_picture_url: Optional[str] = None,
    oauth_provider: Optional[str] = None,
    oauth_provider_user_id: Optional[str] = None,
) -> dict:
    stmt = (
        insert(users)
        .values(
            email=email,
            password_hash=password_hash,
            given_name=given_name,
            family_name=family_name,
            profile_picture_url=profile_picture_url,
            oauth_provider=oauth_provider,
            oauth_provider_user_id=oauth_provider_user_id,
            # status=UserStatus.UNVERIFIED,
        )
        .returning(users)
    )

    try:
        result = db.execute(stmt)
        db.commit()
        first_result = result.first()
        return dict(first_result._mapping) if first_result else None
    except Exception as e:
        db.rollback()
        raise e


def get_user(db: Session, user_id: UUID) -> Optional[dict]:
    stmt = select(users).where(users.c.user_id == user_id)
    result = db.execute(stmt).first()
    return dict(result._mapping) if result else None


def get_user_by_email(db: Session, email: str) -> Optional[dict]:
    stmt = select(users).where(users.c.email == email)
    result = db.execute(stmt).first()
    return dict(result._mapping) if result else None


def update_user_status(
    db: Session, user_id: UUID, status: UserStatus
) -> Optional[dict]:
    stmt = (
        update(users)
        .where(users.c.user_id == user_id)
        .values(status=status.value)
        .returning(users)
    )
    result = db.execute(stmt)
    db.commit()
    row = result.first()
    return dict(row._mapping) if row else None
