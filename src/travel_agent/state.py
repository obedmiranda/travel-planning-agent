from typing import TypedDict

from travel_agent.models.evaluation import Evaluation
from travel_agent.models.itinerary import Itinerary
from travel_agent.models.task import Task


class InputState(TypedDict):
    # Original request
    user_request: str


class TravelAgentState(TypedDict):
    # Original request
    user_request: str

    # Parsed request
    destination: str
    required_cities: list[str]
    travelers: int | None
    trip_duration: int | None
    budget: float | None
    interests: list[str]
    max_activities_per_day: int

    # Planning and execution
    can_plan: bool
    missing_information: list[str]
    plan: list[Task]

    # Itinerary
    itinerary: Itinerary

    # Evaluation
    evaluation: Evaluation
    replan_count: int

    # Final output
    final_response: str
