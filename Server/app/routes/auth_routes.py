from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin , UserOut
from app.services.user_service import create_user_service, authenticate_user_service 
from app.db.database import get_db
from app.controllers.auth_controller import get_current_user
from app.db.models import User



router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)

@router.post("/signin")
def signin_user(user: UserLogin, db: Session = Depends(get_db)):
    return authenticate_user_service(user, db)
@router.get("/me", response_model=UserOut) # sert a retourner les infos de User Authentifié
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve the currently logged-in user's information.
    """
    return {
        "id": current_user.id,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "email": current_user.email,
    }
