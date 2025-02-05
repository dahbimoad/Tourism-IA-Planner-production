from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import PasswordUpdate, UserUpdate, UserOut
from app.services.user_service import update_user_profile, update_user_image, update_user_password
from app.controllers.auth_controller import get_current_user
from app.db.models import User
from app.core.error_handler import error_handler
from typing import Dict, Any
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.put("/profile", response_model=UserOut)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update the current user's profile information"""
    try:
        updated_user = update_user_profile(db, current_user.id, user_data)
        return {
            "id": updated_user.id,
            "nom": updated_user.nom,
            "prenom": updated_user.prenom,
            "email": updated_user.email
        }
    except IntegrityError as e:
        error_handler.raise_validation_error(
            detail="Database integrity error",
            code="DB_INTEGRITY_ERROR",
            field="database"
        )
    except Exception as e:
        error_handler.raise_server_error(error=e)

@router.put("/profile/image")
async def update_profile_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current user's profile picture"""
    try:
        # Validate file type
        content_type = image.content_type
        if content_type not in ["image/jpeg", "image/png", "image/gif"]:
            error_handler.raise_validation_error(
                detail="File type not allowed. Please upload JPEG, PNG or GIF",
                code="INVALID_FILE_TYPE",
                field="image"
            )

        # Read and validate image size
        image_data = await image.read()
        if len(image_data) > 5 * 1024 * 1024:  # 5MB limit
            error_handler.raise_validation_error(
                detail="File size too large. Maximum size is 5MB",
                code="FILE_TOO_LARGE",
                field="image"
            )

        # Update image in database
        await update_user_image(db, current_user.id, image_data, content_type)

        return {
            "message": "Profile picture updated successfully",
            "code": "IMAGE_UPDATED"
        }

    except Exception as e:
        error_handler.raise_server_error(error=e)

@router.get("/profile/image")
async def get_profile_image(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the current user's profile picture with proper error handling"""
    try:
        # Verify if user exists and has an image
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "detail": {
                        "message": "User not found",
                        "code": "USER_NOT_FOUND"
                    }
                }
            )

        if not current_user.image or not current_user.image_type:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "detail": {
                        "message": "No profile picture found",
                        "code": "NO_PROFILE_IMAGE"
                    }
                }
            )

        # Log successful image retrieval
        logger.info(f"Successfully retrieved profile image for user {current_user.id}")

        # Return the image with proper content type
        return Response(
            content=current_user.image,
            media_type=current_user.image_type,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

    except Exception as e:
        logger.error(f"Error retrieving profile image for user {current_user.id}: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": {
                    "message": "Error retrieving profile image",
                    "code": "IMAGE_RETRIEVAL_ERROR",
                    "error": str(e)
                }
            }
        )

@router.put("/password")
async def update_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current user's password"""
    try:
        result = update_user_password(db, current_user.id, password_data)
        return result
    except Exception as e:
        error_handler.raise_server_error(error=e)

@router.get("/profile", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile information"""
    try:
        return {
            "id": current_user.id,
            "nom": current_user.nom,
            "prenom": current_user.prenom,
            "email": current_user.email
        }
    except Exception as e:
        error_handler.raise_server_error(error=e)