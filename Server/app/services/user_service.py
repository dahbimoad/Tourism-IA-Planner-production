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

        # Check if email is being updated and if it's already taken
        if user_data.email and user_data.email != db_user.email:
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Email already registered",
                        "code": "EMAIL_TAKEN",
                        "field": "email"
                    }
                )

        # Update user fields
        update_data = user_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "No valid fields to update",
                    "code": "NO_UPDATE_DATA"
                }
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            db.commit()
            db.refresh(db_user)
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