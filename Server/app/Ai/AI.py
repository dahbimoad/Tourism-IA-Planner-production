from typing import List
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime
from app.services.openai_planner import generate_plans as ai_generate_plans


class PlanRequest(BaseModel):
    lieuDepart: str
    cities: List[str]
    dateDepart: str
    dateRetour: str
    budget: float
    userId: int = None

    def calculate_total_days(self) -> int:
        """Calculate the total number of days between departure and return dates"""
        date_depart = datetime.strptime(self.dateDepart, "%Y-%m-%d")
        date_retour = datetime.strptime(self.dateRetour, "%Y-%m-%d")
        return (date_retour - date_depart).days


def generate_plans(plan_request: PlanRequest):
    """Generate optimized travel plans using OpenAI"""
    try:
        # Validate request
        total_days = plan_request.calculate_total_days()
        if len(plan_request.cities) > total_days:
            raise ValueError(
                "Not enough days to visit all cities. Please reduce the number of cities or extend your trip."
            )

        # Generate plans using OpenAI
        plans = ai_generate_plans(plan_request)

        return plans

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating plans: {str(e)}"
        )


# Ensure these are explicitly exported
__all__ = ['PlanRequest', 'generate_plans']