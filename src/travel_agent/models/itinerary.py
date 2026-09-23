from pydantic import BaseModel


class ItineraryDay(BaseModel):
    day: int
    city: str
    activities: list[str]

    accommodation_cost: float
    food_cost: float
    transportation_cost: float
    activities_cost: float

    estimated_cost: float


class Itinerary(BaseModel):
    days: list[ItineraryDay]
    estimated_total_cost: float
    currency: str
