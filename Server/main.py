from fastapi import FastAPI
from app.routes.auth_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.auth_routes import router as auth_router
from app.db.database import engine, Base

# Create tables in the database
Base.metadata.create_all(bind=engine)
from app.controllers.preferencesController import router as preferences_router
from app.controllers.VilleController import router as villes_router
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.INFO)


app = FastAPI()

# Include user-related routes
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
 #/user/signin
#/user/signup
#get userById 




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)




app.include_router(preferences_router)
app.include_router(villes_router)

