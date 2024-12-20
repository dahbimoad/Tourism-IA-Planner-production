from fastapi import FastAPI
from app.controllers.preferencesController import router as preferences_router
from app.controllers.VilleController import router as villes_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "salam 3alaykummmmm"}

app.include_router(preferences_router)
app.include_router(villes_router)
