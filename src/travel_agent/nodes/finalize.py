from travel_agent.state import TravelAgentState


def finalize(state: TravelAgentState) -> dict[str, str]:
    itinerary = state["itinerary"]

    final_response = str(itinerary)

    print("\n=== FINAL RESPONSE ===")
    print(final_response)

    return {"final_response": final_response}
