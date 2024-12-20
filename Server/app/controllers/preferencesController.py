from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.PlansService import createPlansService 
from app.services.preferencesService import createPreferenceService
from pydantic import BaseModel

router = APIRouter()

class PreferencesCreate(BaseModel):
    lieuDepart: str
    budget: float
    userId: int 


@router.post("/preferences/")
def createPreference(preference: PreferencesCreate,db: Session = Depends(get_db)):
    
    newPlan = createPlansService(db = db )
    
    newPref = createPreferenceService(
    db = db,
    lieuDepart = preference.lieuDepart,
    budget = preference.budget,
    idPlan= newPlan.id,
    userId= preference.userId
    )

    return {"message": "Preference created successfully", "preference": {
        "id": newPref.id,
        "lieuDepart": newPref.lieuDepart,
        "budget": newPref.budget,
        "idPlan": newPref.idPlan,
        "userId": newPref.userId
    }}
