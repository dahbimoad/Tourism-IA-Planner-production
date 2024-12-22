from sqlalchemy.orm import Session

from Server.app.controllers.auth_controller import signup, signin
from Server.app.schemas.user import UserCreate


# Business logic for user signup
def create_user_service(user: UserCreate, db: Session):
    return signup(user, db)

# Business logic for user signin
def authenticate_user_service(user: UserCreate, db: Session):
    return signin(user, db)
