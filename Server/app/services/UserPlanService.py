from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import UserPlan

def createUserPlanService(db: Session, idPlan: int, idVilleItineraire: int):
    newUserPlan = UserPlan(
        idPlan=idPlan,
        idVilleItineraire=idVilleItineraire
    )

    try:
        db.add(newUserPlan)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout du plan utilisateur: {str(e)}")

    return newUserPlan
