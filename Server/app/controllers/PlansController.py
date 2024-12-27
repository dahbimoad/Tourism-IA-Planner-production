from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.preferencesService import createPreferenceService
from pydantic import BaseModel



