from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.database import get_db 
from app.services.VilleService import getVilleIdByName
from app.db.models import Activities




def addActivite(db: Session, new_activity: Activities):
    try:
        db.add(new_activity)
        db.commit()  
        db.refresh(new_activity)  
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de l'activité: {str(e)}")


        