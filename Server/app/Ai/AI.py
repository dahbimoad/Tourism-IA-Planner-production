import random
import re
from datetime import datetime, timedelta
from typing import List, Optional

import openai
import pandas as pd
import requests
from openai import OpenAI
from pydantic import BaseModel, Field


import re
import os

from app.core.config import settings

# Get the current directory where AI.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Define the paths relative to the current directory
tourism_data_file = os.path.join(current_dir, "Comprehensive_Max_Tourism_Dataset.xlsx")
transport_data_file = os.path.join(current_dir, "Comprehensive_Max_Transport_Dataset.xlsx")
tourism_df = pd.read_excel(tourism_data_file)
transport_df = pd.read_excel(transport_data_file)

client = OpenAI(api_key=settings.AI_API_KEY)
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
    """Send a query to OpenAI's API instead of Llama."""
    try:
        # Call OpenAI's API using the correct method
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate OpenAI model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,  # Adjust as needed
            temperature=0.7,  # Adjust for creativity
        )
        # Extract the response content correctly
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error querying OpenAI: {str(e)}")


def generate_activity_prompt(city: str, num_activities: int) -> str:
    return f"""List exactly {num_activities} specific tourist activities in {city} along with their approximate prices in MAD. 
    Ensure that the prices are realistic and reflect typical costs for tourists in Morocco.
    Format each activity as: "Activity Name - Price in MAD".
    Do not include any additional text or explanations."""


def parse_activity_response(response: str) -> List[dict]:
    """Parse the response from Llama3 to extract activities and their prices."""
    activities = []
    for line in response.split("\n"):
        line = line.strip()
        if " - " in line:
            # Remove any leading numbers/symbols before splitting
            clean_line = re.sub(r'^[\d•*.\s]+', '', line)  # Remove numbering/bullets
            activity_name, price_part = clean_line.split(" - ", 1)

            # Clean any remaining special characters at start
            activity_name = re.sub(r'^[^a-zA-Z]+', '', activity_name.strip())

            price = re.search(r"\d+", price_part)
            if price and activity_name:
                activities.append({
                    "name": activity_name.strip(),
                    "price": int(price.group())
                })
    return activities


def adjust_activities_to_budget(activities: List[dict], remaining_budget: float) -> List[dict]:
    """Adjust activities to fit within the remaining budget."""
    # Sort activities by price (ascending)
    sorted_activities = sorted(activities, key=lambda x: x["price"])

    selected_activities = []
    total_cost = 0

    for activity in sorted_activities:
        if total_cost + activity["price"] <= remaining_budget:
            selected_activities.append(activity)
            total_cost += activity["price"]
        else:
            break

    return selected_activities


def adjust_hotel_to_budget(city: str, budget: float, budget_tier: str) -> dict:
    """Select an appropriate hotel based on the budget tier."""
    hotel_df = tourism_df[(tourism_df['Ville'] == city) & (tourism_df['Type de donnée'] == 'Hôtel')]
    
    if hotel_df.empty:
        # Fallback price ranges based on budget tier
        if budget_tier == "Economy":
            price_range = (100, 200)
        elif budget_tier == "Standard":
            price_range = (200, 1000)
        else:  # Premium
            price_range = (1000, 5000)
        
        return {
            "Nom de l'élément": f"{budget_tier} Hotel",
            "Coût (MAD)": random.uniform(*price_range)
        }
    
    sorted_hotels = hotel_df.sort_values(by='Coût (MAD)')
    total_hotels = len(sorted_hotels)
    
    # Select percentile range based on budget tier
    if budget_tier == "Economy":
        # Bottom 30% of hotels
        max_index = int(total_hotels * 0.3)
        hotel_range = (0, max(0, max_index - 1))
    elif budget_tier == "Standard":
        # Middle 40% of hotels
        min_index = int(total_hotels * 0.3)
        max_index = int(total_hotels * 0.7)
        hotel_range = (min_index, max(min_index, max_index - 1))
    else:  # Premium
        # Top 30% of hotels
        min_index = int(total_hotels * 0.7)
        hotel_range = (min_index, total_hotels - 1)
    
    # Ensure we have a valid range
    if hotel_range[0] >= total_hotels:
        hotel_range = (0, total_hotels - 1)
    if hotel_range[0] == hotel_range[1]:
        selected_index = hotel_range[0]
    else:
        selected_index = random.randint(hotel_range[0], hotel_range[1])
    
    selected_hotel = sorted_hotels.iloc[selected_index].to_dict()
    return selected_hotel

def adjust_transport_to_budget(departure_city: str, arrival_city: str, budget: float) -> float:
    """Adjust transport cost based on the budget."""
    transport = transport_df[(transport_df['Ville de départ'] == departure_city) &
                             (transport_df['Ville d\'arrivée'] == arrival_city)]
    if not transport.empty:
        base_cost = float(transport.iloc[0]['Distance (km)']) * 2
        if budget < 1000:  # Low budget
            return base_cost * 0.8  # 20% discount
        elif budget > 5000:  # High budget
            return base_cost * 1.2  # 20% premium
        else:  # Medium budget
            return base_cost
    else:
        return random.uniform(40, 60)



def get_nearest_city(current_city: str, remaining_cities: List[str], transport_df: pd.DataFrame) -> str:
    distances = []
    for city in remaining_cities:
        try:
            # Check both directions for transport data
            forward_distance = transport_df[
                (transport_df['Ville de départ'] == current_city) &
                (transport_df['Ville d\'arrivée'] == city)
            ]['Distance (km)'].values

            reverse_distance = transport_df[
                (transport_df['Ville de départ'] == city) &
                (transport_df['Ville d\'arrivée'] == current_city)
            ]['Distance (km)'].values

            distance = forward_distance[0] if forward_distance.size > 0 else reverse_distance[0]
            distances.append((city, float(distance)))
        except:
            # Default to large distance if no data exists
            distances.append((city, float('inf')))

    if not distances:
        return random.choice(remaining_cities) if remaining_cities else None

    return min(distances, key=lambda x: x[1])[0]


def optimize_city_order(departure_city: str, cities: List[str], transport_df: pd.DataFrame, start_city: str = None) -> List[str]:
    # Ensure the departure city is included in the list of cities to visit
    all_cities = [departure_city] + [city for city in cities if city != departure_city]

    remaining_cities = all_cities.copy()
    optimized_route = []
    current_city = departure_city

    # Remove the departure city from the remaining cities to avoid revisiting
    remaining_cities.remove(current_city)

    # Check if start_city is valid
    if start_city and start_city in remaining_cities:
        optimized_route.append(start_city)
        remaining_cities.remove(start_city)
        current_city = start_city
    else:
        # Start with the nearest city to departure
        next_city = get_nearest_city(current_city, remaining_cities, transport_df)
        if next_city:
            optimized_route.append(next_city)
            remaining_cities.remove(next_city)
            current_city = next_city
        else:
            print("Warning: No starting city found. Returning incomplete route.")
            return optimized_route

    # Build the rest of the route
    while remaining_cities:
        next_city = get_nearest_city(current_city, remaining_cities, transport_df)
        if next_city:
            optimized_route.append(next_city)
            remaining_cities.remove(next_city)
            current_city = next_city
        else:
            print("Warning: Route ended early due to missing transport data.")
            break

    return optimized_route

def calculate_plan(plan_request: PlanRequest, total_days: int, used_activities: set, budget_tier: str = "Premium"):
    # ... existing code ...
    departure_city = plan_request.lieuDepart
    cities = optimize_city_order(departure_city, plan_request.cities, transport_df)

    # Ensure departure city is explicitly included if missing
    if departure_city not in cities:
        cities.insert(0, departure_city)

    budget = plan_request.budget

    # Calculate distances with error handling
    total_distance = 0
    distances = []

    for i in range(len(cities)):
        from_city = departure_city if i == 0 else cities[i - 1]
        try:
            distance = transport_df[
                (transport_df['Ville de départ'] == from_city) &
                (transport_df['Ville d\'arrivée'] == cities[i])
            ]['Distance (km)'].iloc[0]
            distances.append(float(distance))
            total_distance += float(distance)
        except IndexError:
            # Default to 100km if no data exists
            distances.append(100.0)
            total_distance += 100.0
            print(f"Warning: Missing distance between {from_city} and {cities[i]}")

    # Rest of the code remains unchanged...

    # Calculate days per city proportionally to distance
    days_distribution = [1] * len(cities)  # Minimum 1 day per city
    remaining_days = total_days - len(cities)

    if remaining_days > 0:
        for _ in range(remaining_days):
            city_weights = [d / total_distance for d in distances]
            idx = random.choices(range(len(cities)), weights=city_weights)[0]
            days_distribution[idx] += 1

    # Rest of the function remains the same
    total_cost = 0
    transport_total = 0
    itinerary = []
    current_date = datetime.strptime(plan_request.dateDepart, "%Y-%m-%d")

    for idx, city in enumerate(cities):
        days_spent = days_distribution[idx]
        transport_cost = adjust_transport_to_budget(departure_city, city, budget)
        transport_total += transport_cost
        total_cost += transport_cost

        hotel = adjust_hotel_to_budget(city, budget, budget_tier)
        hotel_cost = float(hotel['Coût (MAD)'])
        hotel_name = hotel['Nom de l\'élément']
        total_hotel_cost = hotel_cost * days_spent
        total_cost += total_hotel_cost

        remaining_budget = budget - total_cost

        if remaining_budget < 0:
            selected_activities = [{"name": "Free City Walk", "price": 0}]
        else:
            num_activities = random.randint(3, 5) if budget > 1000 else random.randint(1, 3)
            activity_prompt = generate_activity_prompt(city, num_activities)
            try:
                activities_response = query_llama(activity_prompt)
                activities_with_prices = parse_activity_response(activities_response)
                selected_activities = [
                                          activity
                                          for activity in activities_with_prices
                                          if activity["name"] not in used_activities
                                      ][:num_activities]

                if len(selected_activities) < num_activities:
                    additional_prompt = generate_activity_prompt(city, num_activities - len(selected_activities))
                    additional_activities = parse_activity_response(query_llama(additional_prompt))
                    selected_activities.extend([
                                                   activity
                                                   for activity in additional_activities
                                                   if activity["name"] not in used_activities
                                               ][:num_activities - len(selected_activities)])

                used_activities.update(activity["name"] for activity in selected_activities)

            except Exception as e:
                print(f"Error generating activities with Llama: {e}")
                selected_activities = [{"name": "Free City Walk", "price": 0}]

            selected_activities = adjust_activities_to_budget(selected_activities, remaining_budget)

            if not selected_activities:
                selected_activities = [{"name": "Free City Walk", "price": 0}]

        total_activities_cost = sum(activity["price"] for activity in selected_activities)
        total_cost += total_activities_cost

        start_date = current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=days_spent)
        end_date = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")

        itinerary.append({
            "city": city,
            "hotel": {
                "name": hotel_name,
                "pricePerNight": hotel_cost,
                "totalPrice": total_hotel_cost
            },
            "activities": selected_activities,
            "days_spent": days_spent,
            "total_activities_cost": total_activities_cost
        })

        departure_city = city

    return itinerary, total_cost, transport_total
def generate_plans(plan_request: PlanRequest):
    total_days = plan_request.calculate_total_days()

    if len(plan_request.cities) > total_days:
        raise ValueError(
            "Not enough days to visit all cities. Please reduce the number of cities or extend your trip."
        )

    # Calculate minimum required budget for Economy tier (30% of original budget)
    economy_budget = plan_request.budget * 0.3
    used_activities = set()

    # Test Economy tier feasibility
    try:
        test_request_economy = PlanRequest(
            lieuDepart=plan_request.lieuDepart,
            cities=plan_request.cities,
            dateDepart=plan_request.dateDepart,
            dateRetour=plan_request.dateRetour,
            budget=economy_budget,
            userId=plan_request.userId
        )
        _, test_total_cost_economy, _ = calculate_plan(test_request_economy, total_days, used_activities.copy(), budget_tier="Economy")
        if test_total_cost_economy > plan_request.budget:
            raise ValueError(
                f"Not enough budget. Your budget of {plan_request.budget} MAD is insufficient. Please increase your budget or reduce the number of cities."
            )
    except Exception as e:
        if "Not enough budget" in str(e):
            raise

    # Check Premium tier feasibility (80% of budget)
    premium_budget = plan_request.budget * 0.8
    can_accommodate_premium = False
    try:
        test_request_premium = PlanRequest(
            lieuDepart=plan_request.lieuDepart,
            cities=plan_request.cities,
            dateDepart=plan_request.dateDepart,
            dateRetour=plan_request.dateRetour,
            budget=premium_budget,
            userId=plan_request.userId
        )
        _, test_total_cost_premium, _ = calculate_plan(test_request_premium, total_days, used_activities.copy(), budget_tier="Premium")
        if test_total_cost_premium <= plan_request.budget:
            can_accommodate_premium = True
    except:
        pass  # If calculation fails, assume Premium not feasible

    # Check Standard tier feasibility (50% of budget)
    standard_budget = plan_request.budget * 0.5
    can_accommodate_standard = False
    try:
        test_request_standard = PlanRequest(
            lieuDepart=plan_request.lieuDepart,
            cities=plan_request.cities,
            dateDepart=plan_request.dateDepart,
            dateRetour=plan_request.dateRetour,
            budget=standard_budget,
            userId=plan_request.userId
        )
        _, test_total_cost_standard, _ = calculate_plan(test_request_standard, total_days, used_activities.copy(), budget_tier="Standard")
        if test_total_cost_standard <= plan_request.budget:
            can_accommodate_standard = True
    except:
        pass  # If calculation fails, assume Standard not feasible

    # Determine which tiers to generate
    if can_accommodate_premium:
        # Generate all three tiers
        budget_tiers = [
            {"name": "Premium", "percentage": random.uniform(0.8, 1)},
            {"name": "Standard", "percentage": random.uniform(0.5, 0.8)},
            {"name": "Economy", "percentage": random.uniform(0.3, 0.5)}
        ]
    elif can_accommodate_standard:
        # Generate one Standard and two Economy
        budget_tiers = [
            {"name": "Standard", "percentage": random.uniform(0.5, 0.8)},
            {"name": "Economy", "percentage": random.uniform(0.35, 0.5)},
            {"name": "Economy", "percentage": random.uniform(0.3, 0.35)}
        ]
    else:
        # Generate three Economy
        budget_tiers = [
            {"name": "Economy", "percentage": random.uniform(0.4, 0.5)},
            {"name": "Economy", "percentage": random.uniform(0.35, 0.4)},
            {"name": "Economy", "percentage": random.uniform(0.3, 0.35)}
        ]

    all_plans = []
    original_budget = plan_request.budget

    for tier in budget_tiers:
        used_activities = set()  # Reset activities for each tier
        tier_budget = original_budget * tier["percentage"]
        
        modified_request = PlanRequest(
            lieuDepart=plan_request.lieuDepart,
            cities=plan_request.cities,
            dateDepart=plan_request.dateDepart,
            dateRetour=plan_request.dateRetour,
            budget=tier_budget,
            userId=plan_request.userId
        )
        
        itinerary, total_cost, transport_total = calculate_plan(
            modified_request, 
            total_days, 
            used_activities,
            budget_tier=tier["name"]
        )

        hotels_total = sum(city['hotel']['totalPrice'] for city in itinerary)
        activities_total = sum(city['total_activities_cost'] for city in itinerary)
        total_cost = hotels_total + activities_total + int(transport_total)
        
        all_plans.append({
            "plan": itinerary,
            "total_cost": total_cost,
            "total_days_spent": total_days,
            "budget_tier": tier["name"],
            "budget_percentage": int(tier["percentage"] * 100),
            "breakdown": {
                "hotels_total": hotels_total,
                "activities_total": activities_total,
                "transport_total": int(transport_total)
            }
        })

    return all_plans