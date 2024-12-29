from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.core.security import hash_password, verify_password, create_access_token, verify_token
from app.db.database import get_db
from datetime import timedelta


# Function to signup a user
def signup(user: UserCreate, db: Session):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use")

    # Hash the user's password
    hashed_password = hash_password(user.password)

    # Create new user instance
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return all user information (excluding password)
    return {
        "id": new_user.id,
        "nom": new_user.nom,
        "prenom": new_user.prenom,
        "email": new_user.email,
    }


# Function to signin a user and return a JWT token
def signin(user: UserLogin, db: Session):
    # Check if the user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Verify the password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create JWT token
    access_token = create_access_token(
        data={"sub": db_user.email, "id": db_user.id},  # Include user id in the token
        expires_delta=timedelta(minutes=30)  # Token expires after 30 minutes
    )

    # Return the token and user details
    return {
        "access_token": access_token,
        "token_type": "bearer",
       
    }


# Function to get the current user from the token
def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    email = payload.get("sub")
    user_id = payload.get("id")  # Get user ID from the token
    if email is None or user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Retrieve the user from the database
    user = db.query(User).filter(User.id == user_id, User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
