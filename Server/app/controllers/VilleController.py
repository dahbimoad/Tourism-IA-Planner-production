from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.VilleService import getVillesService,getVilleIdByName


router = APIRouter()

#GetAll()
@router.get("/villes/")
def get_villes(db: Session = Depends(get_db)):
    villes = getVillesService(db)
    return {
        "villes": [
            {"idVille": ville.id, "name": ville.nom, "budget": ville.budget}
            for ville in villes
        ]
    }

#GetByName()
@router.get("/villes/{name}/id")
def get_ville_id(name: str, db: Session = Depends(get_db)):
    idVille = getVilleIdByName(db, name)
    if idVille:
        return {"idVille": idVille}
    else:
        return {"error": "Ville not found"}, 404

