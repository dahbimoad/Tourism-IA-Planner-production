from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Server.app.db.database import get_db
from Server.app.schemas.user import UserCreate, UserLogin
from Server.app.services.user_service import create_user_service, authenticate_user_service

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)

@router.post("/signin")
def signin_user(user: UserLogin, db: Session = Depends(get_db)):
    return authenticate_user_service(user, db)
