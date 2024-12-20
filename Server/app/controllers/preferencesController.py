from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.PlansService import createPlansService 
from app.services.preferencesService import createPreferenceService
from pydantic import BaseModel,root_validator
from datetime import datetime

router = APIRouter()


class PreferencesCreate(BaseModel):
    lieuDepart: str
    cities: List[str]
    dateDepart: str
    dateRetour: str
    budget: float
    userId: int

    @root_validator(pre=True)
    def check_dates(cls, values):
        date_depart = values.get('dateDepart')
        date_retour = values.get('dateRetour')
        
        try:
            date_depart = datetime.strptime(date_depart, "%Y-%m-%d")
            date_retour = datetime.strptime(date_retour, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Les dates doivent être au format YYYY-MM-DD")
        
       
        if date_retour <= date_depart:
            raise ValueError("La date de retour doit être supérieure à la date de départ")
        
        return values

@router.post("/preferences/")
def createPreference(preference: PreferencesCreate,db: Session = Depends(get_db)):
    
    newPlan = createPlansService(db = db )
    
    newPref = createPreferenceService(
    db = db,
    lieuDepart = preference.lieuDepart,
    cities = preference.cities,
    dateDepart = preference.dateDepart,
    dateRetour = preference.dateRetour,
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
