from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update

from src.database.models import User, UserStatus


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    given_name: str,
    family_name: str,
    profile_picture_url: Optional[str] = None,
    oauth_provider: Optional[str] = None,
    oauth_provider_user_id: Optional[str] = None,
) -> User:
    db_user = User(
        email=email,
        password_hash=password_hash,
        given_name=given_name,
        family_name=family_name,
        profile_picture_url=profile_picture_url,
        oauth_provider=oauth_provider,
        oauth_provider_user_id=oauth_provider_user_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def update_user_status(
    db: Session, user_id: UUID, status: UserStatus
) -> Optional[User]:
    user = get_user(db, user_id)
    if user:
        stmt = update(User).where(User.user_id == user_id).values(status=status.value)
        db.execute(stmt)
        db.commit()
        db.refresh(user)
    return user
