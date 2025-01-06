import pandas as pd
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

# Initialize APIRouter for the plan-related endpoints
router = APIRouter()

# Load datasets
tourism_data_file = r"C:\Users\osaka\Desktop\New folder\Tourism-IA-Planner\Server\app\Ai\Comprehensive_Max_Tourism_Dataset.xlsx"
transport_data_file = r"C:\Users\osaka\Desktop\New folder\Tourism-IA-Planner\Server\app\Ai\Comprehensive_Max_Transport_Dataset.xlsx"

tourism_df = pd.read_excel(tourism_data_file)
transport_df = pd.read_excel(transport_data_file)

class PlanRequest(BaseModel):
    lieuDepart: str
    cities: List[str]
    dateDepart: str
    dateRetour: str
    budget: float
    userId: int

    def calculate_total_days(self) -> int:
        date_depart = datetime.strptime(self.dateDepart, "%Y-%m-%d")
        date_retour = datetime.strptime(self.dateRetour, "%Y-%m-%d")
        return (date_retour - date_depart).days

def calculate_plan(plan_request: PlanRequest, total_days: int, used_activities: set):
    departure_city = plan_request.lieuDepart
    cities = plan_request.cities
    budget = plan_request.budget

    # Ensure days are equally distributed
    days_per_city = total_days // len(cities)
    remaining_days = total_days % len(cities)

    total_cost = 0
    itinerary = []

    for idx, city in enumerate(cities):
        days_spent = days_per_city + (1 if idx < remaining_days else 0)

        # Transport cost
        transport = transport_df[(transport_df['Ville de départ'] == departure_city) &
                                 (transport_df['Ville d\'arrivée'] == city)]
        transport_cost = float(transport.iloc[0]['Distance (km)']) * 2 if not transport.empty else random.uniform(40, 60)
        total_cost += transport_cost

        # Hotel selection
        hotel_df = tourism_df[(tourism_df['Ville'] == city) & (tourism_df['Type de donnée'] == 'Hôtel')]
        if not hotel_df.empty:
            hotel = random.choice(hotel_df.to_dict('records'))
            hotel_cost = float(hotel['Coût (MAD)'])
        else:
            hotel = {'Nom de l\'élément': 'Standard Hotel'}
            hotel_cost = random.uniform(80, 120)

        total_cost += hotel_cost * days_spent

        # Activity selection
        city_activities = tourism_df[(tourism_df['Ville'] == city) & (tourism_df['Type de donnée'] == 'Activité')]
        selected_activities = []

        if not city_activities.empty:
            sorted_activities = sorted(city_activities.to_dict('records'), key=lambda x: float(x['Coût (MAD)']))
            random.shuffle(sorted_activities)
            activity_count = random.randint(3, 5)
            for activity in sorted_activities:
                activity_name = activity['Nom de l\'élément']
                if activity_name not in used_activities:
                    selected_activities.append(activity_name)
                    used_activities.add(activity_name)
                if len(selected_activities) >= activity_count:
                    break

        if not selected_activities:
            selected_activities = ["Free City Walk"]

        # Add city plan
        itinerary.append({
            "city": city,
            "hotel": hotel['Nom de l\'élément'],
            "activities": selected_activities,
            "days_spent": days_spent
        })

        departure_city = city

    return itinerary, total_cost

@router.post("/generate-plans")
def generate_plans(plan_request: PlanRequest):
    total_days = plan_request.calculate_total_days()

    # Error handling for insufficient days
    if len(plan_request.cities) > total_days:
        raise HTTPException(
            status_code=400,
            detail="Not enough days to visit all cities. Please reduce the number of cities or extend your trip."
        )

    all_plans = []
    used_activities = set()

    for _ in range(3):
        itinerary, total_cost = calculate_plan(plan_request, total_days, used_activities)

        # Ensure the cost is slightly varied but under budget
        total_cost = total_cost * random.uniform(0.9, 1.1)
        total_cost = round(min(total_cost, plan_request.budget))

        all_plans.append({
            "plan": itinerary,
            "total_cost": total_cost,
            "total_days_spent": total_days
        })

    return all_plans
