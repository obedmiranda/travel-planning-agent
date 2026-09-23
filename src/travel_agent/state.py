from typing import TypedDict

from travel_agent.models.evaluation import Evaluation
from travel_agent.models.itinerary import Itinerary
from travel_agent.models.task import Task


class InputState(TypedDict):
    user_request: str


class TravelAgentState(TypedDict):
    user_request: str

    destination: str
    required_cities: list[str]
    travelers: int | None
    trip_duration: int | None
    budget: float | None
    interests: list[str]
    max_activities_per_day: int

    can_plan: bool
    missing_information: list[str]
    plan: list[Task]

    itinerary: Itinerary

    evaluation: Evaluation
    replan_count: int
    replanning_failed: bool
    replanning_failure_reason: str | None

    final_response: str
