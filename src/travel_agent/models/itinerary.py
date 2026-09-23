from pydantic import BaseModel


class ItineraryDay(BaseModel):
    day: int
    city: str
    activities: list[str]
    estimated_cost: float


class Itinerary(BaseModel):
    days: list[ItineraryDay]
    estimated_total_cost: float
    currency: str
