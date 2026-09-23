from travel_agent.models.evaluation import Evaluation
from travel_agent.state import TravelAgentState


def evaluator(state: TravelAgentState):
    trip_duration = state["trip_duration"]
    itinerary = state["itinerary"]
    budget = state["budget"]

    violations: list[str] = []

    if trip_duration != len(itinerary.days):
        violations.append(
            f"Expected {trip_duration} days but itinerary contains {len(itinerary.days)} days."
        )

    if budget is not None and itinerary.estimated_total_cost > budget:
        violations.append(
            f"Budget exceeded: maximum is ${budget}, "
            f"but itinerary costs ${itinerary.estimated_total_cost}."
        )

    evaluation = Evaluation(
        valid=len(violations) == 0,
        violations=violations,
    )
    print("\n=== EVALUATION ===")
    print(evaluation)
    return {"evaluation": evaluation}
