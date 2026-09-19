from travel_agent.models.task import Task
from travel_agent.state import TravelAgentState


def research(state: TravelAgentState):
    plan = state["plan"]

    for task in plan:
        if task.status == "pending":
            print("FOUND:", task.description)
            break


if __name__ == "__main__":
    test_state: TravelAgentState = {
        "user_request": "Plan a trip to Japan",
        "destination": "Japan",
        "travelers": 2,
        "trip_duration": 7,
        "budget": 5000.0,
        "can_plan": True,
        "missing_information": [],
        "plan": [
            Task(
                description="Research hotels",
                search_query="Japan hotels for 2 travelers 7 nights",
            ),
            Task(
                description="Research transportation",
                search_query="Japan transportation costs Tokyo Kyoto Osaka",
            ),
            Task(
                description="Research attractions",
                search_query="Japan attractions Tokyo Kyoto Osaka admission prices",
            ),
        ],
        "itinerary": {},
        "evaluation": {},
        "replan_count": 0,
        "final_response": "",
        "required_cities": [],
        "interests": [],
        "max_activities_per_day": 2,
    }

    research(test_state)
