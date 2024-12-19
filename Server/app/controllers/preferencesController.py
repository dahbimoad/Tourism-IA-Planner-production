from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.preferencesService import createPreferenceService
from pydantic import BaseModel

router = APIRouter()

class PreferencesCreate(BaseModel):
    lieuDepart: str
    budget: float
    idPlan: int 
    userId: int 


@router.post("/preferences/")
def createPreference(preference: PreferencesCreate,db: Session = Depends(get_db)):
    newpreef = createPreferenceService(
    db = db,
    lieuDepart = preference.lieuDepart,
    budget = preference.budget,
    idPlan=preference.idPlan,
    userId=preference.userId
    )

    return {"message": "Preference created successfully", "preference": {
        "id": newpreef.id,
        "lieuDepart": newpreef.lieuDepart,
        "budget": newpreef.budget,
        "idPlan": newpreef.idPlan,
        "userId": newpreef.userId
    }}
