from fastapi import FastAPI
from app.routes.auth_routes import router as user_router
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
 #/user/signin
#/user/signup


# Autoriser l'origine spécifique de votre frontend
origins = [
    "http://localhost:5173",
    "https://tourism-ia-planner-production-client.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Liste des origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les en-têtes
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root_endpoint():
    return {"message": "hellooo world !"}

app.include_router(preferences_router)
app.include_router(villes_router)