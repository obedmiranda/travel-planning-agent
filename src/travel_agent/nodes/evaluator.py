from travel_agent.models.evaluation import Evaluation
from travel_agent.state import TravelAgentState


def evaluator(state: TravelAgentState) -> dict[str, Evaluation]:
    trip_duration = state["trip_duration"]
    itinerary = state["itinerary"]
    budget = state["budget"]

    violations: list[str] = []

    # Validate trip duration
    if trip_duration != len(itinerary.days):
        violations.append(
            f"Expected {trip_duration} days but itinerary contains "
            f"{len(itinerary.days)} days."
        )

    # Validate each day's cost breakdown
    for day in itinerary.days:
        calculated_day_cost = (
            day.accommodation_cost
            + day.food_cost
            + day.transportation_cost
            + day.activities_cost
        )

        if abs(day.estimated_cost - calculated_day_cost) > 0.01:
            violations.append(
                f"Day {day.day} cost mismatch: "
                f"estimated cost is ${day.estimated_cost:.2f}, "
                f"but cost breakdown totals ${calculated_day_cost:.2f}."
            )

    # Validate itinerary total
    calculated_total_cost = sum(day.estimated_cost for day in itinerary.days)

    if abs(itinerary.estimated_total_cost - calculated_total_cost) > 0.01:
        violations.append(
            f"Trip cost mismatch: estimated total is "
            f"${itinerary.estimated_total_cost:.2f}, "
            f"but daily costs total ${calculated_total_cost:.2f}."
        )

    # Validate budget
    if budget is not None and itinerary.estimated_total_cost > budget:
        violations.append(
            f"Budget exceeded: maximum is ${budget:.2f}, "
            f"but itinerary costs "
            f"${itinerary.estimated_total_cost:.2f}."
        )

    evaluation = Evaluation(
        valid=len(violations) == 0,
        violations=violations,
    )

    print("\n=== EVALUATION ===")
    print(evaluation)

    return {"evaluation": evaluation}
