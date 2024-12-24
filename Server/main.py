from fastapi import FastAPI
from app.controllers.preferencesController import router as preferences_router
from app.controllers.VilleController import router as villes_router
from app.db.database import Base, engine
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.INFO)


app = FastAPI()



@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "salam 3alaykummmmm"}

app.include_router(preferences_router)
app.include_router(villes_router)
