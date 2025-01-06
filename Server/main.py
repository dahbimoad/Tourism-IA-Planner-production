from fastapi import FastAPI
from app.routes.auth_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.db.database import engine, Base, SessionLocal
from app.db.models import Villes
from app.Ai.AI import router as plans_router

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
 #/user/signin
#/user/signup
#get userById
app.include_router(plans_router, prefix="/ai", tags=["Plans"])




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174","https://touristai.online","https://tourism-ia-planner-production-client.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = SessionLocal()
    
    try:
        # Check if data already exists to avoid duplicate insertions
        existing_cities = db.query(Villes).first()
        
        if not existing_cities:
            # Initial cities data
            initial_cities = [
                Villes(nom="Marrakech", budget=1000),
                Villes(nom="Casablanca", budget=2000),
                Villes(nom="Fès", budget=1500),
                Villes(nom="Tangier", budget=1200),
                Villes(nom="Agadir", budget=1300),
                Villes(nom="Rabat", budget=2500),
                Villes(nom="Chefchaouen", budget=800),
                Villes(nom="Essaouira", budget=900)
            ]
            
            # Add all cities
            db.add_all(initial_cities)
            
            # Commit the changes
            db.commit()
            print("Initial cities data has been added successfully!")
        
    except Exception as e:
        print(f"Error adding initial data: {e}")
        db.rollback()
    
    finally:
        db.close()




app.include_router(preferences_router)
app.include_router(villes_router)
