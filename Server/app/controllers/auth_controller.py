# app/controllers/auth_controller.py
from http.client import HTTPException

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, verify_token
from app.db.database import get_db
from datetime import timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.error_handler import error_handler
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


def signup(user: UserCreate, db: Session):
    try:
        # Basic validation before database operations
        if not isinstance(user.email, str) or '@' not in user.email:
            error_handler.raise_validation_error(
                detail="Invalid email format",
                code="INVALID_EMAIL",
                field="email"
            )

        # Check if user exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            error_handler.raise_validation_error(
                detail="Email is already in use",
                code="EMAIL_TAKEN",
                field="email"
            )

        # Validate password
        try:
            UserCreate.validate_password(user.password)
        except ValueError as e:
            error_handler.raise_validation_error(
                detail=str(e),
                code="INVALID_PASSWORD",
                field="password"
            )

        # Validate names
        try:
            UserCreate.validate_name(user.nom, 'nom')
        except ValueError as e:
            error_handler.raise_validation_error(
                detail=str(e),
                code="INVALID_NAME",
                field="nom"
            )

        try:
            UserCreate.validate_name(user.prenom, 'prenom')
        except ValueError as e:
            error_handler.raise_validation_error(
                detail=str(e),
                code="INVALID_NAME",
                field="prenom"
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

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    except HTTPException:
        # Re-raise HTTP exceptions (including our validation errors)
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error in signup: {str(e)}")
        error_handler.raise_server_error(error=e)

def signin(user: UserLogin, db: Session):
    try:
        # Check user exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            error_handler.raise_auth_error(
                detail="Invalid credentials",
                code="INVALID_CREDENTIALS"
            )

        # Verify password
        if not verify_password(user.password, db_user.password):
            error_handler.raise_auth_error(
                detail="Invalid credentials",
                code="INVALID_CREDENTIALS"
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
        error_handler.raise_server_error(error=e)


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
            error_handler.raise_auth_error(
                detail="Invalid token content",
                code="INVALID_TOKEN_CONTENT"
            )

        user = db.query(User).filter(
            User.id == user_id,
            User.email == email
        ).first()

        if not user:
            error_handler.raise_not_found(
                detail="User not found",
                code="USER_NOT_FOUND"
            )

        return user

    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        error_handler.raise_auth_error(error=e)