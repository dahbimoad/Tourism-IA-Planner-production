from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.PlansService import createPlansService 
from app.services.preferencesService import createPreferenceService,getPreferencesService,getPreferencesById,deletePreferenceById,updatePreferenceService
from pydantic import BaseModel,root_validator
from datetime import datetime
from fastapi import HTTPException
from typing import Optional
from app.db.models import User
from app.routes.auth_routes import get_current_user_info
import pdb


router = APIRouter()



class PreferencesCreate(BaseModel):
    lieuDepart: str
    cities: list[str]
    dateDepart: datetime
    dateRetour: datetime
    budget: float

    
    #Validation de la date entrer par le User;
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
def createPreference(preference: PreferencesCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_info)):
    # Vous pouvez aussi imprimer l'ID de l'utilisateur pour vérifier
    newPlan = createPlansService(db=db)
    
    newPref = createPreferenceService(
        db=db,
        lieuDepart=preference.lieuDepart,
        cities=preference.cities,
        dateDepart=preference.dateDepart,
        dateRetour=preference.dateRetour,
        budget=preference.budget,
        idPlan=newPlan.id,
        userId=current_user["id"],
    )

    return {"message": "Preference created successfully", "preference": {
        "id": newPref.id,
        "lieuDepart": newPref.lieuDepart,
        "budget": newPref.budget,
        "idPlan": newPref.idPlan,
        "userId": newPref.userId
    }}


@router.get("/preferences/")
def getAll(db: Session = Depends(get_db)):
    preferences = getPreferencesService(db)
    return {
        "message": "Preferences retrieved successfully",
        "preferences": [
            {
                "id": pref.id,
                "lieuDepart": pref.lieuDepart,
                "budget": pref.budget,
                "dateDepart": pref.dateDepart,
                "dateRetour": pref.dateRetour,
                "idPlan": pref.idPlan,
                "userId": pref.userId
            }
            for pref in preferences
        ]
    }

@router.get("/preferences/{id}")    
def getById( id: int, db: Session = Depends(get_db)):
    preference = getPreferencesById(db,id)
    if preference:
        return {
            "preference": 
            {
                "id": preference.id,
                "lieuDepart":preference.lieuDepart,
                "budget": preference.budget,
                "dateDepart": preference.dateDepart,
                "dateRetour": preference.dateRetour,
                "idPlan": preference.idPlan,
                "userId": preference.userId
            }
        }
    else:   
        return {"error": "preference not found"}, 404 


@router.delete("/preferences/{id}")
def deletePreference(id: int, db: Session = Depends(get_db)):
    deleted_preference = deletePreferenceById(db, id)
    
    if not deleted_preference:
        raise HTTPException(status_code=404, detail="Preference not found")
    
    return {"message": "Preference deleted successfully", "deleted_preference": {
        "id": deleted_preference.id,
        "lieuDepart": deleted_preference.lieuDepart,
        "budget": deleted_preference.budget,
        "dateDepart": deleted_preference.dateDepart,
        "dateRetour": deleted_preference.dateRetour,
        "idPlan": deleted_preference.idPlan,
        "userId": deleted_preference.userId
    }}


class PreferencesUpdate(BaseModel):
    lieuDepart: Optional[str] = None
    cities: Optional[list[str]] = None
    dateDepart: Optional[str] = None
    dateRetour: Optional[str] = None
    budget: Optional[float] = None
    userId: Optional[int] = None
    idPlan: Optional[int] = None  

    @root_validator(pre=True)
    def check_dates(cls, values):
        date_depart = values.get('dateDepart')
        date_retour = values.get('dateRetour')

        if date_depart and date_retour:
            try:
                date_depart = datetime.strptime(date_depart, "%Y-%m-%d")
                date_retour = datetime.strptime(date_retour, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Les dates doivent être au format YYYY-MM-DD")
        
            if date_retour <= date_depart:
                raise ValueError("La date de retour doit être supérieure à la date de départ")

        return values

@router.put("/preferences/{id}")
def updatePreference(
    id: int,
    preference: PreferencesUpdate,  
    db: Session = Depends(get_db)
):
    
    updatedPr = updatePreferenceService(
        db=db,
        preference_id=id,
        lieuDepart=preference.lieuDepart,
        cities=preference.cities,
        dateDepart=preference.dateDepart,
        dateRetour=preference.dateRetour,
        budget=preference.budget,
        idPlan=preference.idPlan, 
        userId=preference.userId
    )
    
    return {
        "message": "Preference updated successfully",
        "preference": {
            "id": updatedPr.id,
            "lieuDepart": updatedPr.lieuDepart,
            "budget": updatedPr.budget,
            "dateDepart": updatedPr.dateDepart,
            "dateRetour": updatedPr.dateRetour,
            "idPlan": updatedPr.idPlan,
            "userId": updatedPr.userId
        }
    }
