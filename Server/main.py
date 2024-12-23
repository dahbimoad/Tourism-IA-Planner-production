from fastapi import FastAPI
from app.routes.auth_routes import router as user_router
from app.db.database import engine, Base

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include user-related routes
app.include_router(user_router, prefix="/user", tags=["user"])
 #/user/signin
#/user/signup