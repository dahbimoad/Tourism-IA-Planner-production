from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.controllers.auth_controller import signup, signin

# Business logic for user signup
def create_user_service(user: UserCreate, db: Session):
    return signup(user, db)

# Business logic for user signin
def authenticate_user_service(user: UserCreate, db: Session):
    return signin(user, db)
