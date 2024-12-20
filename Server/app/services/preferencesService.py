from sqlalchemy.orm import Session
from app.db.models import Preferences,LieuxToVisit
from fastapi import HTTPException
from app.db.database import get_db 
from app.services.VilleService import getVilleIdByName




def createPreferenceService(db : Session, lieuDepart: str, cities : list[str],dateDepart: str, dateRetour: str,budget: float, idPlan: int, userId:int):
    

    newPref = Preferences(
        lieuDepart = lieuDepart,
        dateDepart = dateDepart,
        dateRetour = dateRetour,
        budget = budget,
        idPlan = idPlan,
        userId = userId
    )
    db.add(newPref)
    db.flush()
    db.refresh(newPref)
    db.commit()
    
    
    for city in cities:
        cityId = getVilleIdByName(db,city)
        newLieu = LieuxToVisit(
            idPreference = newPref.id,
            idVille = cityId
        )
        db.add(newLieu)
        db.commit()


    return newPref
    