from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.planning_decision import PlanningDecision
from travel_agent.state import TravelAgentState

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano")


def planner(
    state: TravelAgentState,
) -> dict[str, bool | list[str]]:

    user_request = state["user_request"]
    destination = state["destination"]
    travelers = state["travelers"]
    trip_duration = state["trip_duration"]
    budget = state["budget"]

    structured_llm = llm.with_structured_output(PlanningDecision)

    planner_prompt = f"""
        PERSONA:
        You are a travel planning agent responsible for determining
        whether enough information exists to begin planning a trip.

        TASK:
        Determine whether the available information is sufficient to
        begin creating a reasonable travel plan.

        RULES:
        When the user is asking to plan a trip, the following information
        is required before planning can begin:
        - Destination
        - Number of travelers
        - Trip duration
        - Budget

        These required fields must not be inferred or assumed.
        If any of them are missing, can_plan must be false and the missing
        fields must be included in missing_information.

        Do not require every possible travel preference.
        Missing optional preferences should not prevent planning when
        reasonable assumptions can be made.

        EXAMPLES:

        Example 1:
        User request: "Plan a trip to Japan"
        Available information:
        - Destination: Japan
        - Travelers: unknown
        - Trip duration: unknown
        - Budget: unknown

        Decision:
        - can_plan: false
        - missing_information: ["travelers", "trip duration", "budget"]

        Example 2:
        User request: "Plan a 7-day trip to Japan for two people with a $5,000 budget"
        Available information:
        - Destination: Japan
        - Travelers: 2
        - Trip duration: 7 days
        - Budget: $5,000

        Decision:
        - can_plan: true
        - missing_information: []

        CONTEXT:
        User request: {user_request}
        Destination: {destination}
        Travelers: {travelers}
        Trip duration: {trip_duration}
        Budget: {budget}

        FORMAT:
        Return whether planning can begin and identify only information
        that is essential before planning can start.
    """

    decision = structured_llm.invoke(planner_prompt)

    return {
        "can_plan": decision.can_plan,
        "missing_information": decision.missing_information,
    }
