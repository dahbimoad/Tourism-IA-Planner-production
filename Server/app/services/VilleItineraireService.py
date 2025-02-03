from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.database import get_db 
from app.services.VilleService import getVilleIdByName
from app.db.models import Itineraires,VilleItineraire


def createVilleItineraireService(db : Session,newVilleItin : VilleItineraire):
     
    try:
        db.add(newVilleItin)
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()  
    raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de la villeItineraire: {str(e)}")