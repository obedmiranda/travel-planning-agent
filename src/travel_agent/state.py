from typing import TypedDict

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
    travelers: int
    trip_duration: int
    budget: float
    interests: list[str]
    max_activities_per_day: int

    # Planning and execution
    plan: list[Task]

    # Itinerary
    itinerary: dict  # type: ignore

    # Evaluation
    evaluation: dict  # type: ignore
    replan_count: int

    # Final output
    final_response: str
