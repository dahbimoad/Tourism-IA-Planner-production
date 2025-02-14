# app/controllers/google_auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.core.security import create_access_token
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings
from datetime import timedelta
from pydantic import BaseModel
from app.services.email_service import email_service
import logging

# Set up logging
logger = logging.getLogger(__name__)
router = APIRouter()


class GoogleAuthRequest(BaseModel):
    token: str

# first user connect to google acc -> google returns the token auth_request.token   the foront end send the token to ther server
@router.post("/auth/google")
async def google_auth(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        #Step 1: Token Verification || verify_oauth2_token() function contacts Google and says "Hey, is this token valid for my application?"
        idinfo = id_token.verify_oauth2_token(
            auth_request.token,  # The token from Google
            requests.Request(),  # Request object for verification
            settings.GOOGLE_CLIENT_ID   # My app's client ID
        )

        # Validate required fields from Google token
        if 'email' not in idinfo:
            logger.error("Email not found in Google token")
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "detail": {
                    "message": "Email not found in Google token",
                    "code": "MISSING_EMAIL"
                }
            }

        # Step 2: Extract User Information
        email = idinfo['email']
        nom = idinfo.get('family_name', '')
        prenom = idinfo.get('given_name', '')

        logger.info(f"Processing Google authentication for email: {email}")

        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        is_new_user = False

        if not user:
            try:
                # Create new user if doesn't exist
                user = User(
                    email=email,
                    nom=nom,
                    prenom=prenom,
                    image=None,
                    image_type=None,
                    password=""
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                is_new_user = True
                logger.info(f"New user created with Google authentication: {email}")

                # Send welcome email for new Google users
                try:
                    await email_service.send_google_welcome_email(
                        email=user.email,
                        name=f"{user.prenom} {user.nom}"
                    )
                    logger.info(f"Welcome email sent successfully to: {email}")
                except Exception as email_error:
                    logger.error(f"Failed to send welcome email to {email}: {str(email_error)}")
                    # Continue with registration even if email fails

            except Exception as db_error:
                db.rollback()
                logger.error(f"Database error during user creation: {str(db_error)}")
                return {
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "detail": {
                        "message": "Failed to create user account",
                        "code": "DATABASE_ERROR",
                        "error": str(db_error)
                    }
                }

        # Create access token
        try:
            access_token = create_access_token(
                data={
                    "sub": email,
                    "id": user.id
                },
                expires_delta=timedelta(minutes=30)
            )
            logger.info(f"Access token created successfully for user: {email}")
        except Exception as token_error:
            logger.error(f"Token creation error for {email}: {str(token_error)}")
            return {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": {
                    "message": "Failed to create access token",
                    "code": "TOKEN_ERROR",
                    "error": str(token_error)
                }
            }

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "nom": user.nom,
                "prenom": user.prenom
            },
            "is_new_user": is_new_user  # Added to indicate if this is a new registration
        }

    except ValueError as ve:
        logger.error(f"Invalid Google token: {str(ve)}")
        return {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": {
                "message": "Invalid Google token",
                "code": "INVALID_TOKEN",
                "error": str(ve)
            }
        }
    except Exception as e:
        logger.error(f"Unexpected error during Google authentication: {str(e)}")
        return {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": {
                "message": "An error occurred during Google authentication",
                "code": "AUTH_ERROR",
                "error": str(e)
            }
        }