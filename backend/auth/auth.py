from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from firebase_admin import auth

from src.firebase import get_firebase_app

from src.database.config import get_db
from src.database.crud import get_user_by_email
from src.database.models import User


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify the Firebase token
        decoded_token = auth.verify_id_token(token, app=get_firebase_app())
        email = decoded_token["email"]

        # Get user from database using email
        user = get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        return user

    except (
        auth.CertificateFetchError,
        auth.UserDisabledError,
        auth.InvalidIdTokenError,
        ValueError,
    ):
        raise credentials_exception
