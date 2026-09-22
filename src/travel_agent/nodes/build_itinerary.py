from travel_agent.state import TravelAgentState


def build_itinerary(state: TravelAgentState):
    print("\n=== BUILD ITINERARY ===")
    plan = state["plan"]
    for task in plan:
        print("TASK:", task.description)
        print("RESULT:", task.result)
