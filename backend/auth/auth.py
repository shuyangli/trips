from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import firebase_admin
import logging
from firebase_admin import auth
from sqlalchemy.orm import Session

from database.config import get_db
from database import crud
from auth.oauth import OAUTH2_SCHEME


router = APIRouter()

firebase_app = firebase_admin.initialize_app()


class GoogleToken(BaseModel):
    token: str


logger = logging.getLogger(__name__)


@router.post(
    "/update-user",
    tags=["auth"],
    description="Creates the user in the database if they don't exist. Returns OK if the user was created or already existed, or UNAUTHORIZED if the token is invalid.",
)
async def authenticate(
    token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> None:
    try:
        decoded_token = auth.verify_id_token(token, app=firebase_app)
    except auth.CertificateFetchError as e:
        logger.error(f"Certificate fetch error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Certificate fetch error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.UserDisabledError:
        raise HTTPException(
            status_code=401,
            detail="User is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Provided token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="No auth token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    idinfo = decoded_token

    email = idinfo["email"]
    given_name = idinfo.get("given_name", "")
    family_name = idinfo.get("family_name", "")
    profile_picture_url = idinfo.get("picture", "")
    google_id = idinfo["sub"]

    user = crud.get_user_by_email(db, email)

    if not user:
        try:
            user = crud.create_user(
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
