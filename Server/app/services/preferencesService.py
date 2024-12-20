from sqlalchemy.orm import Session
from app.db.models import Preferences
from fastapi import HTTPException
from app.db.database import get_db 




def createPreferenceService(db : Session, lieuDepart: str, budget: float, idPlan: int, userId:int):
    
    newPref = Preferences(
        lieuDepart = lieuDepart,
        budget = budget,
        idPlan = idPlan,
        userId = userId
    )
    db.add(newPref)
    db.commit()
    db.refresh(newPref)

    return newPref