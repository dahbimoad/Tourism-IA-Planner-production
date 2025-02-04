# app/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import PasswordUpdate
from app.schemas.user import UserUpdate, UserOut
from app.services.user_service import update_user_profile, update_user_image, update_user_password
from app.controllers.auth_controller import get_current_user
from app.db.models import User
from typing import Dict, Any

router = APIRouter()


@router.put("/profile", response_model=UserOut)
async def update_profile(
        user_data: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update the current user's profile information
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


@router.put("/profile/image")
async def update_profile_image(
        image: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Update the current user's profile picture
    """
    try:
        content_type = image.content_type
        if content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "File type not allowed. Please upload JPEG, PNG or GIF",
                    "code": "INVALID_FILE_TYPE",
                    "field": "image"
                }
            )

        # Read image content
        image_data = await image.read()
        if len(image_data) > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "File size too large. Maximum size is 5MB",
                    "code": "FILE_TOO_LARGE",
                    "field": "image"
                }
            )

        # Update image in database
        await update_user_image(db, current_user.id, image_data, content_type)

        return {
            "message": "Profile picture updated successfully",
            "code": "IMAGE_UPDATED"
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


@router.get("/profile/image")
async def get_profile_image(
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve the current user's profile picture
    """
    if not current_user.image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No profile picture found",
                "code": "NO_PROFILE_IMAGE"
            }
        )

    return Response(
        content=current_user.image,
        media_type=current_user.image_type
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