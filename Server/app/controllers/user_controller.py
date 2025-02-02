# app/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import PasswordUpdate
from app.schemas.user import UserUpdate, UserOut
from app.services.user_service import update_user_profile
from app.services.user_service import update_user_password
from app.controllers.auth_controller import get_current_user
from app.db.models import User
from typing import Dict, Any


router = APIRouter()


@router.put("/profile", response_model=UserOut, responses={
    200: {
        "description": "Profile successfully updated",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "nom": "Updated Name",
                    "prenom": "Updated Surname",
                    "email": "updated@example.com"
                }
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "email_taken": {
                        "value": {
                            "detail": {
                                "message": "Email already registered",
                                "code": "EMAIL_TAKEN",
                                "field": "email"
                            }
                        }
                    },
                    "no_data": {
                        "value": {
                            "detail": {
                                "message": "No valid fields to update",
                                "code": "NO_UPDATE_DATA"
                            }
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Authentication failed",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "Could not validate credentials",
                        "code": "INVALID_CREDENTIALS"
                    }
                }
            }
        }
    },
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "User not found",
                        "code": "USER_NOT_FOUND"
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "An unexpected error occurred",
                        "code": "INTERNAL_SERVER_ERROR"
                    }
                }
            }
        }
    }
})
async def update_profile(
        user_data: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update the current user's profile information

    Args:
        user_data: The new user data to update
        current_user: The currently authenticated user
        db: Database session

    Returns:
        The updated user information

    Raises:
        HTTPException:
            - 400: Email already taken or no valid update data
            - 401: Invalid authentication
            - 404: User not found
            - 500: Server error
    """
    try:
        updated_user = update_user_profile(db, current_user.id, user_data)
        return {
            "id": updated_user.id,
            "nom": updated_user.nom,
            "prenom": updated_user.prenom,
            "email": updated_user.email
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred",
                "code": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }
        )


@router.put("/password")
async def update_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's password.
    """
    try:
        result = update_user_password(db, current_user.id, password_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred",
                "code": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }
        )