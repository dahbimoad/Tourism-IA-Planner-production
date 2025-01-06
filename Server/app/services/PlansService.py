from sqlalchemy.orm import Session
from app.db.models import Plans
from fastapi import HTTPException 
from datetime import datetime



def createPlansService(db : Session,idUser: int):
    newPlan = Plans(
        dateCreation=datetime.now(),  
        idUser = idUser
    )

    db.add(newPlan)
    db.commit()
    db.refresh(newPlan)

    return newPlan