from typing import Literal

from pydantic import BaseModel

from travel_agent.models.itinerary import Itinerary


class ReplanningDecision(BaseModel):
    status: Literal["revised", "unsatisfiable"]
    itinerary: Itinerary | None = None
    reason: str | None = None
