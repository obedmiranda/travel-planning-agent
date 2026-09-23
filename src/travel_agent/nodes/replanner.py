from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.itinerary import Itinerary
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

    structured_llm = llm.with_structured_output(Itinerary)

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
        Revise the current itinerary so that it fixes the validation violations.

        Preserve parts of the itinerary that do not need to change.
        Use the available research when making changes.

        All estimated costs must be expressed in USD.
        The total estimated cost must not exceed ${budget} USD.
        The itinerary must contain exactly {trip_duration} days.
    """

    revised_itinerary = structured_llm.invoke(replan_prompt)

    print(f"\n=== REPLAN ATTEMPT {replan_count} ===")
    print(revised_itinerary)

    return {
        "itinerary": revised_itinerary,
        "replan_count": replan_count,
    }
