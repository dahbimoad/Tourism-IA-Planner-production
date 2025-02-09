from fastapi import APIRouter, HTTPException
from app.Ai.AI import PlanRequest, generate_plans

# Initialize APIRouter for the plan-related endpoints
plans_router = APIRouter()

@plans_router.post("/preferences/")
async def generate_plans_endpoint(plan_request: PlanRequest):
    try:
        return generate_plans(plan_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")