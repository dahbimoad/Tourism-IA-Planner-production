from sqlalchemy.orm import Session
from app.db.models import Preferences,LieuxToVisit
from fastapi import HTTPException
from app.db.database import get_db 
from app.services.VilleService import getVilleIdByName





def createPreferenceService(db: Session, lieuDepart: str, cities: list[str], dateDepart: str, dateRetour: str, budget: float, idPlan: int, userId: int):
    try:
        
        newPref = Preferences(
            lieuDepart=lieuDepart,
            dateDepart=dateDepart,
            dateRetour=dateRetour,
            budget=budget,
            idPlan=idPlan,
            userId=userId
        )

        db.add(newPref)
        db.flush()  
        db.refresh(newPref)  
        db.commit()  

       
        for city in cities:
            cityId = getVilleIdByName(db, city)
            if not cityId:
                raise HTTPException(status_code=400, detail=f"La ville '{city}' n'existe pas ou est invalide.")

            newLieu = LieuxToVisit(
                idPreference=newPref.id,
                idVille=cityId
            )
            db.add(newLieu)
            db.commit()  

        return newPref

    except IntegrityError as e:
        
        db.rollback()  
        raise HTTPException(status_code=400, detail="Erreur d'intégrité des données : " + str(e.orig))

    except SQLAlchemyError as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur avec la base de données : " + str(e))

    except Exception as e:
       
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur interne du serveur : " + str(e))



def getPreferencesService(db : Session):
    return db.query(Preferences).all()    

def getPreferencesById(db : Session, Id: int):
    preference = db.query(Preferences).filter(Preferences.id == Id).first()
    if preference:
        return preference
    else:
        return None


def deletePreferenceById(db: Session, id: int):
    preference = db.query(Preferences).filter(Preferences.id == id).first()  
    if not preference:
        return None
    db.query(LieuxToVisit).filter(LieuxToVisit.idPreference == id).delete()
    db.delete(preference)
    db.commit()
    return preference


def updatePreferenceService(
    db: Session, 
    preference_id: int, 
    lieuDepart: str = None, 
    cities: list[str] = None, 
    dateDepart: str = None, 
    dateRetour: str = None, 
    budget: float = None, 
    idPlan: int = None, 
    userId: int = None
):

    preference = db.query(Preferences).filter(Preferences.id == preference_id).first()

    if not preference:
        raise HTTPException(status_code=404, detail="Preference not found")
    
    
    if lieuDepart is not None:
        preference.lieuDepart = lieuDepart
    if dateDepart is not None:
        preference.dateDepart = dateDepart
    if dateRetour is not None:
        preference.dateRetour = dateRetour
    if budget is not None:
        preference.budget = budget
    if idPlan is not None:
        preference.idPlan = idPlan
    if userId is not None:
        preference.userId = userId
    
    
    if cities is not None:
       
        db.query(LieuxToVisit).filter(LieuxToVisit.idPreference == preference_id).delete()


        for city in cities:
            cityId = getVilleIdByName(db, city)
            newLieu = LieuxToVisit(
                idPreference=preference_id,
                idVille=cityId
            )
            db.add(newLieu)
    
    db.commit()
    db.refresh(preference)
    return preference

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


def getPreferencesService(db : Session):
    return db.query(Preferences).all()    

def getPreferencesById(db : Session, Id: int):
    preference = db.query(Preferences).filter(Preferences.id == Id).first()
    if preference:
        return preference
    else:
        return None


def deletePreferenceById(db: Session, id: int):
    preference = db.query(Preferences).filter(Preferences.id == id).first()  
    if not preference:
        return None
    db.query(LieuxToVisit).filter(LieuxToVisit.idPreference == id).delete()
    db.delete(preference)
    db.commit()
    return preference


def updatePreferenceService(
    db: Session, 
    preference_id: int, 
    lieuDepart: str = None, 
    cities: list[str] = None, 
    dateDepart: str = None, 
    dateRetour: str = None, 
    budget: float = None, 
    idPlan: int = None, 
    userId: int = None
):

    preference = db.query(Preferences).filter(Preferences.id == preference_id).first()

    if not preference:
        raise HTTPException(status_code=404, detail="Preference not found")
    
    
    if lieuDepart is not None:
        preference.lieuDepart = lieuDepart
    if dateDepart is not None:
        preference.dateDepart = dateDepart
    if dateRetour is not None:
        preference.dateRetour = dateRetour
    if budget is not None:
        preference.budget = budget
    if idPlan is not None:
        preference.idPlan = idPlan
    if userId is not None:
        preference.userId = userId
    
    
    if cities is not None:
       
        db.query(LieuxToVisit).filter(LieuxToVisit.idPreference == preference_id).delete()


        for city in cities:
            cityId = getVilleIdByName(db, city)
            newLieu = LieuxToVisit(
                idPreference=preference_id,
                idVille=cityId
            )
            db.add(newLieu)
    
    db.commit()
    db.refresh(preference)
    return preference


def PreferenceToAi(preference):
    return {
        "lieuDepart": preference.lieuDepart,
        "cities": preference.cities,
        "dateDepart": preference.dateDepart,
        "dateRetour": preference.dateRetour,
        "budget": preference.budget
    }


    

