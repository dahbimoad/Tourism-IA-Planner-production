from fastapi import FastAPI
from app.routes.auth_routes import router as user_router
from app.db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include user-related routes
app.include_router(user_router, prefix="/user", tags=["user"])
 #/user/signin
#/user/signup




# Autoriser l'origine spécifique de votre frontend
origins = [
    "http://localhost:5173",  # Ajoutez l'URL de votre frontend React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Liste des origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les en-têtes
)