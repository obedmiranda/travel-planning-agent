from travel_agent.state import TravelAgentState


def finalize(state: TravelAgentState) -> dict[str, str]:
    itinerary = state["itinerary"]
    evaluation = state["evaluation"]
    replan_count = state.get("replan_count", 0)

    if evaluation.valid:
        final_response = str(itinerary)
    else:
        violations = "; ".join(evaluation.violations)

        final_response = (
            "Unable to produce an itinerary that satisfies all constraints "
            f"after {replan_count} replanning attempts. "
            f"Remaining violations: {violations}"
        )

    print("\n=== FINAL RESPONSE ===")
    print(final_response)

    return {"final_response": final_response}
