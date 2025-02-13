from typing import List, Dict, Any
import json
import logging
from datetime import datetime
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.AI_API_KEY)


def generate_plans(plan_request):
    """Generate optimized travel plans using OpenAI"""
    total_days = plan_request.calculate_total_days()
    daily_budget = plan_request.budget / total_days

    try:
        # Create a detailed prompt for the travel plan
        prompt = f"""You are an expert Moroccan travel planner with deep knowledge of local culture, prices, and attractions. Create 3 detailed, realistic travel plans for a trip with these requirements:

        TRIP DETAILS:
        - Departure: {plan_request.lieuDepart}
        - Cities to visit: {', '.join(plan_request.cities)}
        - Duration: {total_days} days
        - Total budget: {plan_request.budget} MAD (≈{daily_budget:.2f} MAD/day)
        - Dates: {plan_request.dateDepart} to {plan_request.dateRetour}

        DETAILED REQUIREMENTS:

        1. HOTELS & RIADS:
        - Budget ({daily_budget < 1000}):
          * Simple hotels/riads: 200-400 MAD/night
          * Basic amenities, clean, safe locations
        - Mid-range ({1000 <= daily_budget <= 2000}):
          * 3-4 star hotels/authentic riads: 400-800 MAD/night
          * Good locations, breakfast included
        - Luxury ({daily_budget > 2000}):
          * 5-star hotels/luxury riads: 800+ MAD/night
          * Premium locations, full amenities

        2. ACTIVITIES PER CITY:
        - Must include iconic attractions
        - Mix of:
          * Cultural sites (medinas, museums)
          * Local experiences (souks, workshops)
          * Historical monuments
          * Nature/outdoor activities
        - Price ranges:
          * Free activities (walks, public spaces)
          * Budget activities: 50-150 MAD
          * Mid-range activities: 150-300 MAD
          * Premium experiences: 300+ MAD

        3. TRANSPORTATION:
        - Between cities:
          * Train (where available): 100-300 MAD
          * CTM/Supratours bus: 80-200 MAD
          * Grand taxi: 70-150 MAD/person
          * Private transfer: 300-600 MAD
        - Within cities:
          * Petit taxi: 20-50 MAD
          * Public transport: 5-10 MAD

        4. DAILY SCHEDULING:
        - Account for:
          * Prayer times
          * Typical opening hours (shops closed Friday afternoon)
          * Heat (avoid midday activities in summer)
          * Ramadan if applicable
          * Travel time between cities
        - Include time for:
          * Markets (mornings/late afternoons best)
          * Meals at local restaurants
          * Rest/relaxation

        5. SEASONAL CONSIDERATIONS ({plan_request.dateDepart}):
        - Weather appropriate activities
        - Seasonal festivals/events
        - Peak/off-peak pricing
        - Seasonal specialties (food, crafts)

        6. BUDGET ALLOCATION:
        - Hotels: 30-40% of budget
        - Activities: 30-35% of budget
        - Transport: 15-20% of budget
        - Food & extras: 15-20% of budget

        7. CITY-SPECIFIC TIPS:
        - Marrakech: Start medina tours early, visit Jardin Majorelle at opening
        - Fes: Local guide recommended for medina
        - Chefchaouen: Best photos early morning/late afternoon
        - Casablanca: Hassan II Mosque specific prayer times
        - Essaouira: Wind patterns affect beach activities
        - Tangier: Port area busier on boat arrival days
        - Agadir: Beach timing based on tides
        - Rabat: Government area restricted times

        Return exactly 3 plans in this JSON structure:
        {{"plans": [
            {{
                "plan": [
                    {{
                        "city": "city name",
                        "hotel": {{
                            "name": "Specific hotel/riad name",
                            "pricePerNight": 500
                        }},
                        "activities": [
                            {{
                                "name": "Specific activity name",
                                "price": 200
                            }}
                        ],
                        "days_spent": 2
                    }}
                ],
                "total_cost": 5000,
                "total_days_spent": {total_days},
                "breakdown": {{
                    "hotels_total": 2000,
                    "activities_total": 2000,
                    "transport_total": 1000
                }}
            }}
        ]}}

        IMPORTANT RULES:
        1. All plans must be within total budget ± 5%
        2. Sum of days_spent must exactly equal {total_days}
        3. All prices must be realistic for Morocco
        4. Include specific hotel and activity names
        5. Activities must be available in that city
        6. Transport times must be realistic
        7. Each city needs minimum 1 full day
        8. Account for travel time between cities
        9. More days for cities with more attractions

        Only return the JSON. No additional text."""

        # Call OpenAI API with model from settings
        response = client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are a Moroccan travel expert who creates detailed, accurate travel plans. You know exact prices, 
                    authentic local experiences, and optimal visiting times for all Moroccan destinations. You ensure all plans are 
                    realistic, culturally appropriate, and maximize the traveler's experience within their budget."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000,
            response_format={"type": "json_object"}
        )

        # Parse and validate the response
        try:
            content = response.choices[0].message.content
            plans = json.loads(content)

            if isinstance(plans, dict) and "plans" in plans:
                plans = plans["plans"]
            elif not isinstance(plans, list):
                plans = [plans]

            validated_plans = validate_and_adjust_plans(plans, plan_request.budget, total_days)

            # Additional validation for quality
            for plan in validated_plans:
                for city_plan in plan["plan"]:
                    # Ensure minimum activities per city
                    if len(city_plan["activities"]) < 3:
                        raise ValueError(f"Insufficient activities for {city_plan['city']}")

                    # Verify realistic prices
                    if city_plan["hotel"]["pricePerNight"] < 200 or city_plan["hotel"]["pricePerNight"] > 5000:
                        raise ValueError(f"Unrealistic hotel price in {city_plan['city']}")

            return validated_plans

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {e}")
            logger.error(f"Response content: {content}")
            raise ValueError("Failed to generate valid travel plans")

    except Exception as e:
        logger.error(f"Error generating travel plans: {e}")
        raise


def validate_and_adjust_plans(plans: List[Dict[str, Any]], total_budget: float, total_days: int) -> List[
    Dict[str, Any]]:
    """Validate and adjust the generated plans to ensure they meet constraints"""
    validated_plans = []

    for plan in plans:
        # Validate total cost
        if abs(plan["total_cost"] - total_budget) > (total_budget * 0.05):  # 5% tolerance
            plan = adjust_plan_cost(plan, total_budget)

        # Validate days
        total_plan_days = sum(city["days_spent"] for city in plan["plan"])
        if total_plan_days != total_days:
            plan = adjust_plan_days(plan, total_days)

        # Validate breakdown totals match activities
        calculated_totals = {
            "hotels_total": sum(city["hotel"]["pricePerNight"] * city["days_spent"] for city in plan["plan"]),
            "activities_total": sum(sum(activity["price"] for activity in city["activities"]) for city in plan["plan"]),
            "transport_total": plan["breakdown"]["transport_total"]  # Transport is harder to calculate exactly
        }

        plan["breakdown"].update(calculated_totals)
        plan["total_cost"] = sum(calculated_totals.values())

        # Ensure each city has reasonable time allocation
        city_count = len(plan["plan"])
        min_days_per_city = max(1, total_days // (city_count * 2))  # At least 1 day, or proportional minimum

        for city in plan["plan"]:
            if city["days_spent"] < min_days_per_city:
                raise ValueError(f"Insufficient time allocated for {city['city']}")

        validated_plans.append(plan)

    return validated_plans


def adjust_plan_cost(plan: Dict[str, Any], target_budget: float) -> Dict[str, Any]:
    """Adjust plan costs to meet budget constraints while maintaining proportions"""
    current_cost = plan["total_cost"]
    reduction_factor = target_budget / current_cost

    # Adjust all costs proportionally while maintaining minimums
    for city in plan["plan"]:
        # Adjust hotel price with minimum limit
        new_hotel_price = max(200, city["hotel"]["pricePerNight"] * reduction_factor)
        city["hotel"]["pricePerNight"] = new_hotel_price

        # Adjust activities while maintaining minimums
        for activity in city["activities"]:
            activity["price"] = max(50, activity["price"] * reduction_factor)

    # Recalculate totals
    hotels_total = sum(city["hotel"]["pricePerNight"] * city["days_spent"] for city in plan["plan"])
    activities_total = sum(sum(activity["price"] for activity in city["activities"]) for city in plan["plan"])
    transport_total = max(100, plan["breakdown"]["transport_total"] * reduction_factor)

    plan["breakdown"].update({
        "hotels_total": hotels_total,
        "activities_total": activities_total,
        "transport_total": transport_total
    })
    plan["total_cost"] = hotels_total + activities_total + transport_total

    return plan


def adjust_plan_days(plan: Dict[str, Any], target_days: int) -> Dict[str, Any]:
    """Adjust plan days to meet duration constraints while ensuring minimum stays"""
    current_days = sum(city["days_spent"] for city in plan["plan"])
    if current_days == target_days:
        return plan

    # Calculate minimum days needed for each city based on activities
    min_days = {city["city"]: max(1, len(city["activities"]) // 3) for city in plan["plan"]}
    total_min_days = sum(min_days.values())

    if total_min_days > target_days:
        raise ValueError("Not enough days to properly visit all cities")

    # Distribute remaining days proportionally
    remaining_days = target_days - total_min_days
    city_weights = {city["city"]: len(city["activities"]) for city in plan["plan"]}
    total_weight = sum(city_weights.values())

    # Distribute extra days
    for city in plan["plan"]:
        proportion = city_weights[city["city"]] / total_weight
        extra_days = round(remaining_days * proportion)
        city["days_spent"] = min_days[city["city"]] + extra_days

    # Adjust for any rounding errors
    current_total = sum(city["days_spent"] for city in plan["plan"])
    if current_total != target_days:
        diff = target_days - current_total
        # Add or subtract the difference from the city with the most/least days
        if diff > 0:
            max_city = max(plan["plan"], key=lambda x: x["days_spent"])
            max_city["days_spent"] += diff
        else:
            max_city = max(plan["plan"], key=lambda x: x["days_spent"])
            max_city["days_spent"] += diff

    # Update costs based on new durations
    for city in plan["plan"]:
        city["hotel"]["totalPrice"] = city["hotel"]["pricePerNight"] * city["days_spent"]

    return plan