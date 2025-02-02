from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Hotels







def createHotelService(db: Session, nom: str, adresse: str, description: str, cout: float, idVille: int):
    newHotel = Hotels(
        nom=nom,
        adresse=adresse,
        description=description,
        cout=cout,
        idVille=idVille
    )

    try:
        db.add(newHotel)
        db.flush()
        db.refresh(newHotel)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de l'hôtel: {str(e)}")

    return newHotel



