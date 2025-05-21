from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth
from database.config import get_db
from sqlalchemy.orm import Session
from database import crud

from api import User

router = APIRouter()

firebase_app = firebase_admin.initialize_app()


class GoogleToken(BaseModel):
    token: str


@router.post("/update-user")
async def authenticate(token_data: GoogleToken, db: Session = Depends(get_db)) -> User:
    try:
        decoded_token = auth.verify_id_token(token_data.token, app=firebase_app)
        idinfo = decoded_token

        # Get user info from the token
        email = idinfo["email"]
        given_name = idinfo.get("given_name", "")
        family_name = idinfo.get("family_name", "")
        profile_picture_url = idinfo.get("picture", "")
        google_id = idinfo["sub"]

        # Check if user exists
        user = crud.get_user_by_email(db, email)

        if not user:
            # Create new user
            user = crud.create_user(
                db=db,
                email=email,
                password_hash="",  # No password for OAuth users
                given_name=given_name,
                family_name=family_name,
                profile_picture_url=profile_picture_url,
                oauth_provider="google",
                oauth_provider_user_id=google_id,
            )

        return User.model_validate(user)

    except ValueError as e:
        print("ValueError", e)
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print("Exception", e)
        raise HTTPException(status_code=500, detail=str(e))
