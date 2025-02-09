from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.controllers.auth_controller import signup, signin
from fastapi import HTTPException ,  status
from app.schemas.user import UserUpdate
from app.db.models import User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.security import verify_password, hash_password
from app.schemas.user import PasswordUpdate


# Business logic for user signup
def create_user_service(user: UserCreate, db: Session):
    return signup(user, db)

# Business logic for user signin
def authenticate_user_service(user: UserCreate, db: Session):
    return signin(user, db)


def update_user_profile(db: Session, user_id: int, user_data: UserUpdate):
    """
    Update user profile with validation for empty fields and proper error handling
    """
    try:
        # Get the user from database
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "User not found",
                    "code": "USER_NOT_FOUND"
                }
            )

        # Convert model to dict and filter out None and empty string values
        update_data = {
            key: value for key, value in user_data.dict(exclude_unset=True).items()
            if value is not None and value.strip() != "" if isinstance(value, str)
        }

        # Check if there are any valid fields to update
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "No valid fields provided for update. Fields cannot be empty.",
                    "code": "NO_VALID_UPDATE_DATA"
                }
            )

        # Validate email if it's being updated
        if 'email' in update_data:
            # Check email format
            if not update_data['email'] or not '@' in update_data['email']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Invalid email format",
                        "code": "INVALID_EMAIL_FORMAT",
                        "field": "email"
                    }
                )

            # Check if email is already taken
            if update_data['email'] != db_user.email:
                existing_user = db.query(User).filter(User.email == update_data['email']).first()
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "message": "Email already registered",
                            "code": "EMAIL_TAKEN",
                            "field": "email"
                        }
                    )

        # Validate name fields
        for field in ['nom', 'prenom']:
            if field in update_data:
                if len(update_data[field].strip()) < 2:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "message": f"{field.capitalize()} must be at least 2 characters long",
                            "code": f"INVALID_{field.upper()}_LENGTH",
                            "field": field
                        }
                    )

        try:
            # Update user fields with validated data
            for field, value in update_data.items():
                setattr(db_user, field, value)

            db.commit()
            db.refresh(db_user)

            # Return the user model object directly
            return db_user

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Database integrity error",
                    "code": "DB_INTEGRITY_ERROR",
                    "error": str(e)
                }
            )

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Database error",
                    "code": "DB_ERROR",
                    "error": str(e)
                }
            )

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
def update_user_password(db: Session, user_id: int, password_data: PasswordUpdate):
    """Update user password with validation"""
    try:
        # Get the user from database
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "User not found",
                    "code": "USER_NOT_FOUND"
                }
            )

        # Verify current password
        if not verify_password(password_data.current_password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Current password is incorrect",
                    "code": "INVALID_CURRENT_PASSWORD",
                    "field": "current_password"
                }
            )

        # Verify new password is different from current
        if verify_password(password_data.new_password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "New password must be different from current password",
                    "code": "SAME_PASSWORD",
                    "field": "new_password"
                }
            )

        # Update password
        db_user.password = hash_password(password_data.new_password)
        db.commit()

        return {
            "message": "Password updated successfully",
            "code": "PASSWORD_UPDATED"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred",
                "code": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }
        )