from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.replanning_decision import ReplanningDecision
from travel_agent.state import TravelAgentState

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano")


def replanner(state: TravelAgentState) -> dict[str, object]:
    itinerary = state["itinerary"]
    evaluation = state["evaluation"]
    plan = state["plan"]

    destination = state["destination"]
    travelers = state["travelers"]
    trip_duration = state["trip_duration"]
    budget = state["budget"]

    replan_count = state.get("replan_count", 0) + 1

    research_context = "\n\n".join(
        f"Research objective: {task.description}\nResearch result: {task.result}"
        for task in plan
    )

    structured_llm = llm.with_structured_output(ReplanningDecision)

    replan_prompt = f"""
        You are responsible for revising a travel itinerary that failed validation.

        TRAVEL CONTEXT:
        Destination: {destination}
        Travelers: {travelers}
        Trip duration: {trip_duration}
        Budget: ${budget} USD

        CURRENT ITINERARY:
        {itinerary}

        VALIDATION VIOLATIONS:
        {evaluation.violations}

        AVAILABLE RESEARCH:
        {research_context}

        TASK:
        Determine whether the validation violations can be fixed
        while keeping the itinerary realistic and consistent with
        the available research.

        If the constraints can realistically be satisfied:
        - Return status="revised".
        - Return a revised itinerary.
        - Preserve parts that do not need to change.
        - All costs must remain realistic and expressed in USD.

        If the constraints cannot realistically be satisfied:
        - Return status="unsatisfiable".
        - Do not invent unrealistic costs just to satisfy the constraints.
        - Do not reduce real travel, lodging, food, or transportation
          costs to zero simply to fit the budget.
        - Explain why the constraints cannot be satisfied in reason.
    """

    decision = structured_llm.invoke(replan_prompt)

    print(f"\n=== REPLAN ATTEMPT {replan_count} ===")
    print(decision)

    if decision.status == "unsatisfiable":
        return {
            "replan_count": replan_count,
            "replanning_failed": True,
            "replanning_failure_reason": decision.reason,
        }

    if decision.itinerary is None:
        return {
            "replan_count": replan_count,
            "replanning_failed": True,
            "replanning_failure_reason": (
                "Replanner did not produce a revised itinerary."
            ),
        }

    return {
        "itinerary": decision.itinerary,
        "replan_count": replan_count,
        "replanning_failed": False,
        "replanning_failure_reason": None,
    }
