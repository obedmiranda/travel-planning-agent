from travel_agent.state import TravelAgentState


def get_request(state: TravelAgentState) -> dict[str, str]:

    user_request = state["user_request"]

    return {"destination": user_request}
