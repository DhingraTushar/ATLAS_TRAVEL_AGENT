import os
import requests
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

load_dotenv()

# --- 1. Define Input Schemas ---


class FlightInput(BaseModel):
    origin: str = Field(..., description="IATA code for origin (e.g., DEL)")
    destination: str = Field(...,
                             description="IATA code for destination (e.g., BOM)")
    date: str = Field(..., description="Travel date in YYYY-MM-DD format")


class TrainInput(BaseModel):
    source_code: str = Field(...,
                             description="Station code for origin (e.g., NDLS)")
    dest_code: str = Field(...,
                           description="Station code for destination (e.g., BCT)")
    date: str = Field(..., description="Travel date in YYYY-MM-DD format")

# --- 2. Define Native CrewAI Tools ---


class SearchFlightsTool(BaseTool):
    name: str = "Search Flights"
    description: str = "Finds flights using Amadeus. Inputs: origin, destination, date."
    args_schema: Type[BaseModel] = FlightInput

    def _run(self, origin: str, destination: str, date: str) -> str:
        try:
            amadeus = Client(
                client_id=os.getenv('AMADEUS_CLIENT_ID'),
                client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
            )
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=date,
                adults=1
            )
            if not response.data:
                return "No flights found."

            results = []
            for flight in response.data[:3]:
                price = flight['price']['total']
                airline = flight['validatingAirlineCodes'][0]
                results.append(f"Flight: {airline} | Price: {price} EUR")
            return "\n".join(results)
        except Exception as e:
            return f"Error: {str(e)}"


class SearchTrainsTool(BaseTool):
    name: str = "Search Trains"
    description: str = "Finds Indian trains using RapidAPI. Inputs: source_code, dest_code, date."
    args_schema: Type[BaseModel] = TrainInput

    def _run(self, source_code: str, dest_code: str, date: str) -> str:
        url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
        querystring = {"fromStationCode": source_code,
                       "toStationCode": dest_code, "dateOfJourney": date}
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            if 'data' in data:
                trains = []
                for t in data['data'][:3]:
                    name = t.get('trainName', 'Train')
                    number = t.get('trainNumber', 'N/A')
                    trains.append(f"{name} ({number})")
                return "\n".join(trains)
            return "No trains found."
        except Exception as e:
            return f"Error: {str(e)}"
