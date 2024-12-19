from fastapi import FastAPI
from app.controllers.preferencesController import router as preferences_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "salam 3alaykummmmm"}

app.include_router(preferences_router)
