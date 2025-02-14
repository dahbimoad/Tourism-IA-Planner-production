from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, verify_token
from app.db.database import get_db
from datetime import timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.error_handler import error_handler
from app.services.email_service import email_service
import logging
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def signup(user: UserCreate, db: Session):
    try:
        # Basic validation before database operations
        if not isinstance(user.email, str) or '@' not in user.email:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": {
                        "message": "Validation error",
                        "code": "VALIDATION_ERROR",
                        "error": "400: {'message': 'Invalid email format', 'code': 'INVALID_EMAIL', 'field': 'email'}"
                    }
                }
            )

        # Check if user exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "detail": {
                        "message": "Conflict error",
                        "code": "CONFLICT_ERROR",
                        "error": "409: {'message': 'Email is already in use', 'code': 'EMAIL_TAKEN', 'field': 'email'}"
                    }
                }
            )

        # Hash password
        hashed_password = hash_password(user.password)

        # Create user
        new_user = User(
            nom=user.nom.title(),
            prenom=user.prenom.title(),
            email=user.email.lower(),
            password=hashed_password
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            # Send welcome email
            try:
                await email_service.send_welcome_email(
                    email=new_user.email,
                    name=f"{new_user.prenom} {new_user.nom}"
                )
                logger.info(f"Welcome email sent to {new_user.email}")
            except Exception as email_error:
                logger.error(f"Failed to send welcome email: {str(email_error)}")
                # Continue with registration even if email fails

            return {"message": "User created successfully"}

        except Exception as db_error:
            db.rollback()
            logger.error(f"Database error in signup: {str(db_error)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": {
                        "message": "Internal server error",
                        "code": "SERVER_ERROR",
                        "error": "Failed to create user in database"
                    }
                }
            )

    except Exception as e:
        logger.error(f"Error in signup: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": {
                    "message": "Internal server error",
                    "code": "SERVER_ERROR",
                    "error": str(e)
                }
            }
        )

def signin(user: UserLogin, db: Session):
    try:
        # Check user exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": {
                        "message": "Authentication error",
                        "code": "AUTH_ERROR",
                        "error": "401: {'message': 'Invalid credentials', 'code': 'INVALID_CREDENTIALS'}"
                    }
                }
            )

        # Verify password
        if not verify_password(user.password, db_user.password):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": {
                        "message": "Authentication error",
                        "code": "AUTH_ERROR",
                        "error": "401: {'message': 'Invalid credentials', 'code': 'INVALID_CREDENTIALS'}"
                    }
                }
            )

        # Create token
        access_token = create_access_token(
            data={
                "sub": user.email,
                "id": db_user.id
            },
            expires_delta=timedelta(minutes=30)
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error in signin: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": {
                    "message": "Internal server error",
                    "code": "SERVER_ERROR",
                    "error": str(e)
                }
            }
        )

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = verify_token(token)

        email = payload.get("sub")
        user_id = payload.get("id")

        if not email or not user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": {
                        "message": "Authentication error",
                        "code": "AUTH_ERROR",
                        "error": "401: {'message': 'Invalid token content', 'code': 'INVALID_TOKEN_CONTENT'}"
                    }
                }
            )

        user = db.query(User).filter(
            User.id == user_id,
            User.email == email
        ).first()

        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "detail": {
                        "message": "Not found",
                        "code": "NOT_FOUND",
                        "error": "404: {'message': 'User not found', 'code': 'USER_NOT_FOUND'}"
                    }
                }
            )

        return user

    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": {
                    "message": "Authentication error",
                    "code": "AUTH_ERROR",
                    "error": str(e)
                }
            }
        )