from sqlalchemy.orm import Session
from app.db.models import Villes
from fastapi import HTTPException
from app.db.database import get_db 







def getVillesService(db : Session):
    return db.query(Villes).all()

def getVilleIdByName(db: Session, name: str):
    ville = db.query(Villes).filter(Villes.nom == name).first()
    if ville:
        return ville.id
    else:
        return None 




            
  


