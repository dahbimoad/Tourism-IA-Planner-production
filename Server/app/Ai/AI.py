import pandas as pd
from datetime import datetime
from typing import List, Optional
import random
import requests
import json

from pydantic import BaseModel, Field
import re


# Load datasets
tourism_data_file = r"C:\Projets\Tourism-IA-Planner\Server\app\Ai\Comprehensive_Max_Tourism_Dataset.xlsx"
transport_data_file = r"C:\Projets\Tourism-IA-Planner\Server\app\Ai\Comprehensive_Max_Transport_Dataset.xlsx"

tourism_df = pd.read_excel(tourism_data_file)
transport_df = pd.read_excel(transport_data_file)

OLLAMA_API_BASE = "http://localhost:11434/api"


class PlanRequest(BaseModel):
    lieuDepart: str
    cities: List[str]
    dateDepart: str
    dateRetour: str
    budget: float
    userId: Optional[int] = Field(default=None)

    def calculate_total_days(self) -> int:
        date_depart = datetime.strptime(self.dateDepart, "%Y-%m-%d")
        date_retour = datetime.strptime(self.dateRetour, "%Y-%m-%d")
        return (date_retour - date_depart).days


def clean_activity_response(response: str) -> List[str]:
    """Clean and extract activities from Llama's response."""
    # Remove introductory phrases
    response = re.sub(r"Here are \d+ unique tourist activities.*?:\s*\n*", "", response)
    response = re.sub(r"These activities showcase.*$", "", response, flags=re.MULTILINE)
    response = re.sub(r"\(Note:.*?\)", "", response)
    response = re.sub(r"\n+", "\n", response)

    # Split into individual activities
    activities = []
    for line in response.split("\n"):
        # Remove numbering and clean up
        line = re.sub(r"^\d+\.\s*", "", line.strip())
        line = re.sub(r"^[-•]\s*", "", line)
        line = re.sub(r"^\s*and\s+", "", line)

        if line and not line.startswith("Let me know") and not line.endswith(":"):
            activities.append(line.strip())

    return [a for a in activities if a and len(a) > 5]  # Filter out very short or empty items


def query_llama(prompt: str) -> str:
    """Send a query to Llama 3 via Ollama API"""
    url = f"{OLLAMA_API_BASE}/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        raise Exception(f"Error querying Llama: {response.text}")


def generate_activity_prompt(city: str, num_activities: int) -> str:
    return f"""List exactly {num_activities} specific tourist activities in {city}. 
    Make each activity a single, clear statement without any introduction or explanation.
    Format as a simple list with one activity per line."""


def calculate_plan(plan_request: PlanRequest, total_days: int, used_activities: set):
    departure_city = plan_request.lieuDepart
    cities = plan_request.cities
    budget = plan_request.budget

    days_per_city = total_days // len(cities)
    remaining_days = total_days % len(cities)

    total_cost = 0
    itinerary = []

    for idx, city in enumerate(cities):
        days_spent = days_per_city + (1 if idx < remaining_days else 0)

        # Transport cost calculation
        transport = transport_df[(transport_df['Ville de départ'] == departure_city) &
                                 (transport_df['Ville d\'arrivée'] == city)]
        transport_cost = float(transport.iloc[0]['Distance (km)']) * 2 if not transport.empty else random.uniform(40,
                                                                                                                  60)
        total_cost += transport_cost

        # Hotel selection
        hotel_df = tourism_df[(tourism_df['Ville'] == city) & (tourism_df['Type de donnée'] == 'Hôtel')]
        if not hotel_df.empty:
            hotel = random.choice(hotel_df.to_dict('records'))
            hotel_cost = float(hotel['Coût (MAD)'])
            hotel_name = hotel['Nom de l\'élément']
        else:
            hotel_name = 'Standard Hotel'
            hotel_cost = random.uniform(80, 120)

        total_cost += hotel_cost * days_spent

        # Use Llama 3 to generate activities
        num_activities = random.randint(3, 5)
        activity_prompt = generate_activity_prompt(city, num_activities)
        try:
            activities_response = query_llama(activity_prompt)
            cleaned_activities = clean_activity_response(activities_response)

            # Filter out used activities and limit to requested number
            selected_activities = [
                                      activity
                                      for activity in cleaned_activities
                                      if activity not in used_activities
                                  ][:num_activities]

            if len(selected_activities) < num_activities:
                # If we don't have enough unique activities, generate more
                additional_prompt = generate_activity_prompt(city, num_activities - len(selected_activities))
                additional_activities = clean_activity_response(query_llama(additional_prompt))
                selected_activities.extend([
                                               activity
                                               for activity in additional_activities
                                               if activity not in used_activities
                                           ][:num_activities - len(selected_activities)])

            used_activities.update(selected_activities)

        except Exception as e:
            print(f"Error generating activities with Llama: {e}")
            selected_activities = ["Free City Walk"]

        # Add city plan
        itinerary.append({
            "city": city,
            "hotel": hotel_name,
            "activities": selected_activities,
            "days_spent": days_spent
        })

        departure_city = city

    return itinerary, total_cost


def generate_plans(plan_request: PlanRequest):
    total_days = plan_request.calculate_total_days()

    if len(plan_request.cities) > total_days:
        raise ValueError(
            "Not enough days to visit all cities. Please reduce the number of cities or extend your trip."
        )

    all_plans = []
    used_activities = set()

    for _ in range(3):
        itinerary, total_cost = calculate_plan(plan_request, total_days, used_activities)

        total_cost = total_cost * random.uniform(0.9, 1.1)
        total_cost = round(min(total_cost, plan_request.budget))

        all_plans.append({
            "plan": itinerary,
            "total_cost": total_cost,
            "total_days_spent": total_days
        })

    return all_plans