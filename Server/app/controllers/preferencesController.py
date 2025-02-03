from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, root_validator, Field
from datetime import datetime
from typing import Optional, List

from app.db.database import get_db
from app.controllers.auth_controller import get_current_user
from app.services.PlansService import createPlansService
from app.services.preferencesService import (
    createPreferenceService, getPreferencesService, getPreferencesById,
    deletePreferenceById, updatePreferenceService,PreferenceToAi
)
from app.services.ItineraireService import createItineraireService
from app.services.activiteService import addActivite
from app.services.hotelService import createHotelService
from app.services.VilleItineraireService import createVilleItineraireService
from app.db.models import User,Villes,Activities,Hotels,Itineraires,VilleItineraire
from app.Ai.AI import generate_plans ,PlanRequest
 

router = APIRouter()


class PreferencesCreate(BaseModel):
    lieuDepart: str
    cities: List[str]
    dateDepart: str  
    dateRetour: str  
    budget: float

    
    @root_validator(pre=True)
    def check_dates(cls, values):
        date_depart = values.get('dateDepart')
        date_retour = values.get('dateRetour')

        try:
            date_depart = datetime.strptime(date_depart, "%Y-%m-%d")
            date_retour = datetime.strptime(date_retour, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Les dates doivent être au format YYYY-MM-DD")

        if date_retour <= date_depart:
            raise ValueError("La date de retour doit être supérieure à la date de départ")

        return values


class PreferencesUpdate(BaseModel):
    lieuDepart: Optional[str] = None
    cities: Optional[List[str]] = None
    dateDepart: Optional[str] = None
    dateRetour: Optional[str] = None
    budget: Optional[float] = None
    userId: Optional[int] = None
    idPlan: Optional[int] = None

    @root_validator(pre=True)
    def check_dates(cls, values):
        date_depart = values.get('dateDepart')
        date_retour = values.get('dateRetour')

        if date_depart and date_retour:
            try:
                date_depart = datetime.strptime(date_depart, "%Y-%m-%d")
                date_retour = datetime.strptime(date_retour, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Les dates doivent être au format YYYY-MM-DD")

            if date_retour <= date_depart:
                raise ValueError("La date de retour doit être supérieure à la date de départ")

        return values


@router.post("/preferences/")
def createPreference(
        preference: PreferencesCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

   
    newPlan = createPlansService(db=db,idUser=user_id)

    
    newPref = createPreferenceService(
        db=db,
        lieuDepart=preference.lieuDepart,
        cities=preference.cities,
        dateDepart=preference.dateDepart,
        dateRetour=preference.dateRetour,
        budget=preference.budget,
        idPlan=newPlan.id,
        userId=user_id  
    )

    
    try:
        
        plan_request = PlanRequest(
            lieuDepart=preference.lieuDepart,
            cities=preference.cities,
            dateDepart=preference.dateDepart,
            dateRetour=preference.dateRetour,
            budget=preference.budget,
            userId=user_id,
        )

        generated_plans = generate_plans(plan_request) 


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error generating plans: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating plans: {str(e)}")

    
    return {
        "message": "Preference created successfully",
        "preference": {
            "id": newPref.id,
            "lieuDepart": newPref.lieuDepart,
            "budget": newPref.budget,
            "idPlan": newPref.idPlan,
            "userId": newPref.userId
        },
        "generated_plans": generated_plans
    }

@router.get("/preferences/")
def getAll(db: Session = Depends(get_db)):
    preferences = getPreferencesService(db)
    return {
        "message": "Preferences retrieved successfully",
        "preferences": [
            {
                "id": pref.id,
                "lieuDepart": pref.lieuDepart,
                "budget": pref.budget,
                "dateDepart": pref.dateDepart,
                "dateRetour": pref.dateRetour,
                "idPlan": pref.idPlan,
                "userId": pref.userId
            }
            for pref in preferences
        ]
    }



@router.get("/preferences/{id}")
def getById(id: int, db: Session = Depends(get_db)):
    preference = getPreferencesById(db, id)
    if preference:
        return {
            "preference": {
                "id": preference.id,
                "lieuDepart": preference.lieuDepart,
                "budget": preference.budget,
                "dateDepart": preference.dateDepart,
                "dateRetour": preference.dateRetour,
                "idPlan": preference.idPlan,
                "userId": preference.userId
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Preference not found")



@router.delete("/preferences/{id}")
def deletePreference(id: int, db: Session = Depends(get_db)):
    deleted_preference = deletePreferenceById(db, id)

    if not deleted_preference:
        raise HTTPException(status_code=404, detail="Preference not found")

    return {
        "message": "Preference deleted successfully",
        "deleted_preference": {
            "id": deleted_preference.id,
            "lieuDepart": deleted_preference.lieuDepart,
            "budget": deleted_preference.budget,
            "dateDepart": deleted_preference.dateDepart,
            "dateRetour": deleted_preference.dateRetour,
            "idPlan": deleted_preference.idPlan,
            "userId": deleted_preference.userId
        }
    }



@router.put("/preferences/{id}")
def updatePreference(id: int,preference: PreferencesUpdate,db: Session = Depends(get_db)):
    
    updatedPr = updatePreferenceService(
        db=db,
        preference_id=id,
        lieuDepart=preference.lieuDepart,
        cities=preference.cities,
        dateDepart=preference.dateDepart,
        dateRetour=preference.dateRetour,
        budget=preference.budget,
        idPlan=preference.idPlan,
        userId=preference.userId
    )

    return {
        "message": "Preference updated successfully",
        "preference": {
            "id": updatedPr.id,
            "lieuDepart": updatedPr.lieuDepart,
            "budget": updatedPr.budget,
            "dateDepart": updatedPr.dateDepart,
            "dateRetour": updatedPr.dateRetour,
            "idPlan": updatedPr.idPlan,
            "userId": updatedPr.userId
        }
    }


@router.post("/preferencesFavori/")
async def addTofavori(
    request: Request,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    plan_data = await request.json()

    villeItin = VilleItineraire()

    for ville in plan_data["plan"]:
        city_name = ville["city"]
        activities = ville["activities"]
        ville_obj = db.query(Villes).filter(Villes.nom == city_name).first()
        if not ville_obj:
            print(f"Ville {city_name} introuvable.")
            continue


       


        for activity in activities:
            activity_obj = Activities(
                nom=activity["name"],
                description=f"Activité {activity['name']} à {city_name}",
                cout=activity["price"],  
                adresse=f"{city_name} centre ville",
                idVille=ville_obj.id
            )
            addActivite(db,activity_obj)

        hotel = ville["hotel"]
        
        
        newhotel = Hotels(
            nom = hotel["name"],
            adresse = "test",
            description = "test",
            cout = hotel["pricePerNight"],
            idVille = ville_obj.id
        )   
        createHotelService(db,newhotel) 

        newItin = Itineraires(
            id_activite = activity_obj.id,
            id_hotel = newhotel.id,
            time_spent_by_ville = ville["days_spent"],
            budget = ville["hotel"]["totalPrice"] + ville["total_activities_cost"]

        )
        createItineraireService(db,newItin)
        villeItin.idItineraire = newItin.id
        villeItin.idVille = ville_obj.id
        createVilleItineraireService(db,villeItin)


    if not plan_data:
        raise HTTPException(status_code=400, detail="Aucune donnée reçue")

    return {"message": "Données reçues", "data": plan_data}