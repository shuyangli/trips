from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import logging
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import auth
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.database.crud.user import get_user_by_email, create_user
from src.auth import OAUTH2_SCHEME
from src.firebase import get_firebase_app


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/signin",
    description="Creates the user in the database if they don't exist. Returns OK if the user was created or already existed, or UNAUTHORIZED if the token is invalid.",
)
async def authenticate(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> None:
    try:
        decoded_token = auth.verify_id_token(token, app=get_firebase_app())
    except auth.CertificateFetchError as e:
        logger.error(f"Certificate fetch error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Certificate fetch error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (auth.UserDisabledError, auth.InvalidIdTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    idinfo = decoded_token

    email = idinfo["email"]
    given_name = idinfo.get("given_name", "")
    family_name = idinfo.get("family_name", "")
    profile_picture_url = idinfo.get("picture", "")
    google_id = idinfo["sub"]

    user = get_user_by_email(db, email)

    if not user:
        try:
            user = create_user(
                db=db,
                email=email,
                password_hash="",
                given_name=given_name,
                family_name=family_name,
                profile_picture_url=profile_picture_url,
                oauth_provider="google",
                oauth_provider_user_id=google_id,
            )
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise HTTPException(status_code=500, detail="Failed to create user")


# The following are only useful for FastAPI docs page - we authenticate by stuffing a token.

fake_token = ""


@router.post("/supply-token")
async def supply_token(token: str):
    global fake_token
    fake_token = token


@router.post("/token")
async def fake_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": fake_token, "token_type": "bearer"}
