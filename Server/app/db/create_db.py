from database import Base, engine
from models import Plans, Preferences, User, Villes  # Importer tes modèles

# Créer toutes les tables dans la base de données
Base.metadata.create_all(bind=engine)
