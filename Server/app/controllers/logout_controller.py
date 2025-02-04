# app/controllers/logout_controller.py

from fastapi import APIRouter, Depends, Response, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.auth_controller import get_current_user
from app.db.models import User
from app.core.token_management import token_manager
from typing import Dict
from datetime import datetime
import jwt

router = APIRouter()
security = HTTPBearer()


@router.post("/logout", response_model=Dict[str, str])
async def logout(
        request: Request,
        response: Response,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Handle user logout by invalidating their token and clearing cookies

    Args:
        request: FastAPI Request object to access headers
        response: FastAPI Response object to handle cookies
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Dict with success message
    """
    try:
        # Get the token from the authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            # Invalidate the token using the token manager
            token_manager.invalidate_token(token)

        # Clear the access token cookie if it exists
        response.delete_cookie(
            key="access_token",
            path="/",
            secure=True,
            httponly=True,
            samesite="lax"
        )

        # Clear client-side data
        response.headers["Clear-Site-Data"] = '"cookies", "storage", "cache"'
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        print(f"User {current_user.id} logged out at {datetime.utcnow()}")

        return {
            "message": "Successfully logged out",
            "status": "success"
        }

    except jwt.ExpiredSignatureError:
        # If token is already expired, still proceed with logout
        return {
            "message": "Successfully logged out",
            "status": "success"
        }

    except Exception as e:
        print(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An error occurred during logout",
                "code": "LOGOUT_ERROR",
                "error": str(e)
            }
        )