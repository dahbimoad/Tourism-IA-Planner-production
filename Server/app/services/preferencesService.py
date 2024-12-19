from sqlalchemy.orm import Session
from db.models import Preferences
from db.schemas import PreferencesCreate #a ajouter pour valider les donnes 

class PreferencesService:
    def __init__(self, db: Session):
        self.db =db 
    
    
    @staticmethod
    def createPreference(self, preferenceData: PreferencesCreate):
        newPreference = Preferences