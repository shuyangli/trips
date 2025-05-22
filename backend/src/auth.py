from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from firebase_admin import auth
import logging

from src.firebase import get_firebase_app
from src.database.config import get_db
from src.database.crud import get_user_by_email
from src.database.models import User

logger = logging.getLogger(__name__)


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        decoded_token = auth.verify_id_token(token, app=get_firebase_app())
    except (
        auth.CertificateFetchError,
        auth.UserDisabledError,
        auth.InvalidIdTokenError,
        ValueError,
    ):
        raise credentials_exception

    email = decoded_token["email"]

    user = get_user_by_email(db, email)
    if user is None:
        logger.error(f"User authenticated but not found: {email}")
        raise credentials_exception
    return user
