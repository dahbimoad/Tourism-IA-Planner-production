from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.trip_planner import TripPlannerService

router = APIRouter()

# Define the input structure (request body)
class TripPlanRequest(BaseModel):
    lieuDepart: str
    cities: list[str]
    dateDepart: str
    dateRetour: str
    budget: float
    userId: int

# Define the output structure (response from Llama 3)
class CityPlan(BaseModel):
    city: str
    activities: list[str]
    hotel: str
    transport_cost: float
    transport_time: int

class TravelPlan(BaseModel):
    plan: list[CityPlan]
    total_cost: float
    total_days_spent: int

# Initialize service
trip_planner_service = TripPlannerService()

# Endpoint to generate trip plans
@router.post("/generate_trip_plan", response_model=List[TravelPlan])
async def generate_trip_plans(request: TripPlanRequest):
    try:
        # Convert the incoming request to a dictionary and send it to the service
        trip_data = request.dict()
        trip_plans = await trip_planner_service.generate_trip_plan(trip_data)
        return trip_plans
    except HTTPException as e:
        # Catch and re-raise HTTP exceptions with specific error messages
        raise e
    except Exception as e:
        # Catch unexpected errors and return 500
        raise HTTPException(status_code=500, detail=f"Error generating trip plans: {str(e)}")
