from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_service import create_user_service, authenticate_user_service
from app.db.database import get_db
from app.controllers.auth_controller import get_current_user
from app.db.models import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/signup")
async def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = await create_user_service(user, db)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error during signup process",
                "code": "SIGNUP_ERROR",
                "error": str(e)
            }
        )

@router.post("/signin")
def signin_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return authenticate_user_service(user, db)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Signin error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error during signin process",
                "code": "SIGNIN_ERROR",
                "error": str(e)
            }
        )

@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve the currently logged-in user's information
    """
    try:
        return {
            "id": current_user.id,
            "nom": current_user.nom,
            "prenom": current_user.prenom,
            "email": current_user.email,
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error retrieving user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error retrieving user information",
                "code": "USER_INFO_ERROR",
                "error": str(e)
            }
        )


@router.post("/test-email")
async def test_email():
    """Test endpoint for email service"""
    try:
        # First test SMTP connection
        connection_test = await email_service.test_connection()
        if not connection_test:
            return {
                "status": "error",
                "message": "Failed to connect to SMTP server"
            }

        # Try sending a test email
        success = await email_service.send_welcome_email(
            email=settings.MAIL_USERNAME,  # Send to yourself
            name="Test User"
        )

        if success:
            return {
                "status": "success",
                "message": "Test email sent successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to send test email"
            }
    except Exception as e:
        logger.error(f"Test email error: {str(e)}")
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }