from travel_agent.state import TravelAgentState


def replanner(state: TravelAgentState) -> dict[str, object]:
    evaluation = state["evaluation"]

    print("\n=== REPLANNER ===")
    print("Violations:", evaluation.violations)

    return {}
