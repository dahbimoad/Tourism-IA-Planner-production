from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class Plans(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    dateCreation = Column(Date)
    preference = relationship("Preferences", back_populates="plan", uselist=False)
    userPlans = relationship("UserPlan", back_populates="plan")
    idUser = Column(Integer, ForeignKey("users.id"), nullable=False)  
    user = relationship("User", back_populates="plans")  


class Preferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer, autoincrement=True)
    lieuDepart = Column(String)
    budget = Column(Float)
    dateDepart = Column(Date)
    dateRetour = Column(Date)
    idPlan = Column(Integer, ForeignKey("plans.id"), unique=True)
    plan = relationship("Plans", back_populates="preference")
    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="preferences")
    villes = relationship("LieuxToVisit", back_populates="preference")

    __table_args__ = (
        PrimaryKeyConstraint('id', 'lieuDepart'),
        UniqueConstraint('id'),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    email = Column(String)
    password = Column(String)
    preferences = relationship("Preferences", back_populates="user")
    plans = relationship("Plans", back_populates="user")  # Relation vers Plans

class Villes(Base):
    __tablename__ = "villes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    budget = Column(Float)
    activities = relationship("Activities", back_populates="ville")
    itineraries = relationship("Itineraires", secondary="ville_itineraire", back_populates="villes")
    hotels = relationship("Hotels", back_populates="ville")
    lieuxToVisit = relationship("LieuxToVisit", back_populates="ville")


class Activities(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    description = Column(String)
    cout = Column(Float)
    adresse = Column(String)
    idVille = Column(Integer, ForeignKey("villes.id"))
    ville = relationship("Villes", back_populates="activities")
    itineraries = relationship("Itineraires", back_populates="activity")  # Relation ajoutée


class Itineraires(Base):
    __tablename__ = "itineraires"

    id = Column(Integer, primary_key=True, index=True)
    id_activite = Column(Integer, ForeignKey("activities.id", ondelete="SET NULL"), nullable=True)
    id_hotel = Column(Integer, ForeignKey("hotels.id", ondelete="SET NULL"), nullable=True)
    time_spent_by_ville = Column(Float, nullable=False)
    budget = Column(Float, nullable=False)

    villes = relationship("Villes", secondary="ville_itineraire", back_populates="itineraries")
    activity = relationship("Activities", back_populates="itineraries", foreign_keys=[id_activite])
    hotel = relationship("Hotels", back_populates="itineraries", foreign_keys=[id_hotel])


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    adresse = Column(String)
    description = Column(String)
    cout = Column(Float)
    idVille = Column(Integer, ForeignKey("villes.id"))
    ville = relationship("Villes", back_populates="hotels")
    itineraries = relationship("Itineraires", back_populates="hotel")  # Relation ajoutée


class VilleItineraire(Base):
    __tablename__ = "ville_itineraire"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    idVille = Column(Integer, ForeignKey("villes.id"), nullable=False)
    idItineraire = Column(Integer, ForeignKey("itineraires.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('idVille', 'idItineraire', name='uq_ville_itineraire'),  
    )


class UserPlan(Base):
    __tablename__ = "user_plan"

    idPlan = Column(Integer, ForeignKey("plans.id"), primary_key=True)
    idVilleItineraire = Column(Integer, ForeignKey("ville_itineraire.id"), primary_key=True)

    # Définir la clé primaire composite
    __table_args__ = (
        PrimaryKeyConstraint('idPlan', 'idVilleItineraire', name='pk_user_plan'),  # Clé primaire composite
    )

    plan = relationship("Plans", back_populates="userPlans")
    villeItineraire = relationship("VilleItineraire", back_populates="userPlans")



class LieuxToVisit(Base):
    __tablename__ = "lieux_to_visit"

    idPreference = Column(Integer, ForeignKey("preferences.id"), primary_key=True)
    idVille = Column(Integer, ForeignKey("villes.id"), primary_key=True)

    preference = relationship("Preferences", back_populates="villes")
    ville = relationship("Villes", back_populates="lieuxToVisit")
