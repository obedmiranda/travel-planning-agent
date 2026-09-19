from langgraph.types import interrupt

from travel_agent.nodes.parse_request import parse_travel_information
from travel_agent.state import TravelAgentState


def request_information(state: TravelAgentState) -> dict[str, object]:
    # missing information comes from the planner node

    missing_information = state["missing_information"]
    answer = interrupt({"missing_information": missing_information})
    print("RESUMED ANSWER:", answer)
    parsed_answer = parse_travel_information(answer)

    return {
        "travelers": parsed_answer.travelers,
        "trip_duration": parsed_answer.trip_duration,
        "budget": parsed_answer.budget,
    }
