import httpx
from typing import List
from fastapi import HTTPException

# Update with the correct local Llama3 API URL
LLAMA_API_URL = "http://localhost:11434/generate_trip_plan"  # Local API URL

class TripPlannerService:
    def __init__(self):
        # No need for an API key now
        pass

    async def fetch_trip_plans(self, data: dict) -> List[dict]:
        async with httpx.AsyncClient() as client:
            try:
                # Make the API request to the local Llama3 API
                response = await client.post(
                    LLAMA_API_URL,
                    json=data,  # Send data as JSON
                    # No Authorization header needed anymore
                )

                # Raise error for unsuccessful response (4xx, 5xx)
                response.raise_for_status()

                return response.json()  # Ensure response format is a JSON list of dicts

            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"API Error: {e}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Request Error: {e}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Unexpected Error: {e}")

    async def generate_trip_plan(self, trip_data: dict) -> List[dict]:
        return await self.fetch_trip_plans(trip_data)
