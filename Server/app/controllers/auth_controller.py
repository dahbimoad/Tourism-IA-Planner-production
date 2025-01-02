from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, verify_token
from app.db.database import get_db
from datetime import timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


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

    return {"message": "User created successfully"}


# Signin: Authenticate a user and return a JWT token
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
        data={
            "sub": user.email,  # L'email de l'utilisateur
            "id": db_user.id  # L'ID de l'utilisateur récupéré de la base de données
        },
        expires_delta=timedelta(minutes=30)  # Token expires after 30 minutes
    )

    return {"access_token": access_token, "token_type": "bearer"}


security = HTTPBearer()  # Déclare un schéma de sécurité pour le token


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    token = credentials.credentials
    print(f"Extracted token: {token}")

    try:
        payload = verify_token(token)
    except HTTPException as e:
        print(f"Error verifying token: {e.detail}")
        raise e

    email = payload.get("sub")
    id = payload.get("id")

    if not email or not id:
        print(f"Invalid token: missing user data (sub: {email}, id: {id})")
        raise HTTPException(status_code=401, detail="Invalid credentials in token")

    print(f"Payload: sub={email}, id={id}")

    # Search user in database using id or email
    user = db.query(User).filter(User.id == id, User.email == email).first()
    if user is None:
        print(f"User not found in database: {email}, id={id}")
        raise HTTPException(status_code=404, detail="User not found in database")

    return user
