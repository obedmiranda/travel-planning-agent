from langgraph.types import interrupt

from travel_agent.state import TravelAgentState


def request_information(state: TravelAgentState):
    # missing information comes from the planner node

    missing_information = state["missing_information"]
    answer = interrupt({"missing_information": missing_information})
    print("RESUMED ANSWER:", answer)
