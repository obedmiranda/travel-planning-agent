from travel_agent.state import TravelAgentState


def finalize(state: TravelAgentState) -> dict[str, str]:
    itinerary = state["itinerary"]
    evaluation = state["evaluation"]
    replan_count = state.get("replan_count", 0)

    replanning_failed = state.get("replanning_failed", False)

    if replanning_failed:
        reason = state.get(
            "replanning_failure_reason",
            "The travel constraints could not be satisfied.",
        )

        final_response = f"TRIP PLANNING FAILED\n\n{reason}"

        print("\n=== FINAL RESPONSE ===")
        print(final_response)

        return {"final_response": final_response}

    if not evaluation.valid:
        violations = "\n".join(f"- {violation}" for violation in evaluation.violations)

        final_response = (
            "TRIP PLANNING FAILED\n\n"
            f"Unable to satisfy all constraints after "
            f"{replan_count} replanning attempts.\n\n"
            f"Remaining issues:\n{violations}"
        )

        print("\n=== FINAL RESPONSE ===")
        print(final_response)

        return {"final_response": final_response}

    lines = [
        "TRAVEL ITINERARY",
        "=" * 50,
        "",
    ]

    for day in itinerary.days:
        lines.append(f"DAY {day.day} — {day.city}")
        lines.append("-" * 50)

        for activity in day.activities:
            lines.append(f"• {activity}")

        lines.append(
            f"\nEstimated day cost: ${day.estimated_cost:,.2f} {itinerary.currency}"
        )
        lines.append("")

    lines.extend(
        [
            "=" * 50,
            "TRIP SUMMARY",
            f"Duration: {len(itinerary.days)} days",
            (
                f"Estimated total cost: "
                f"${itinerary.estimated_total_cost:,.2f} "
                f"{itinerary.currency}"
            ),
            "Constraint check: PASSED",
        ]
    )

    final_response = "\n".join(lines)

    print("\n=== FINAL RESPONSE ===")
    print(final_response)

    return {"final_response": final_response}
