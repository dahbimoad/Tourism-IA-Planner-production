from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.database import get_db 
from app.services.VilleService import getVilleIdByName
from app.db.models import Itineraires,VilleItineraire




def createItineraireService(db : Session,newItineraire : Itineraires):
     
    try:
        db.add(newItineraire)
        db.commit()
        db.refresh(newItineraire)
        return True
        
    except Exception as e:
        db.rollback()  
    raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de l'itinéraire: {str(e)}")
    






def deleteItineraireService(db: Session, itineraireId: int):
    itineraire = db.query(Itineraires).filter(Itineraires.id == itineraireId).first()
    
    if not itineraire:
        raise HTTPException(status_code=404, detail="Itinéraire non trouvé")
    
    try:
        db.delete(itineraire)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'itinéraire: {str(e)}")
    
    return {"message": "Itinéraire supprimé avec succès"}





def addVilleItineraire(db : Session,villeId : int,ItineraireId : int):
    
    
    newVilleItin = VilleItineraire(
        idVille = villeId,
        idItineraire  = ItineraireId 
    )
    try:
        db.add(newVilleItin)
        db.flush()
        db.refresh(newVilleItin)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout  de VilleItinéraire: {str(e)}")
    
    return newVilleItin



