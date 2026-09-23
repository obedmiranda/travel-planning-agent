from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.itinerary import Itinerary
from travel_agent.state import TravelAgentState

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano")


def build_itinerary(state: TravelAgentState) -> dict[str, Itinerary]:
    plan = state["plan"]
    destination = state["destination"]
    travelers = state["travelers"]
    trip_duration = state["trip_duration"]
    budget = state["budget"]

    structured_llm = llm.with_structured_output(Itinerary)

    research_context = "\n\n".join(
        f"Research objective: {task.description}\nResearch result: {task.result}"
        for task in plan
    )

    itinerary_prompt = f"""
        You are responsible for building a travel itinerary.

        TRAVEL CONTEXT:
        Destination: {destination}
        Travelers: {travelers}
        Trip duration: {trip_duration}
        Budget: ${budget} USD

        RESEARCH:
        {research_context}

        TASK:
        Build a feasible day-by-day itinerary using the travel context
        and the provided research.

        COST RULES:
        For every day, estimate:
        - accommodation_cost
        - food_cost
        - transportation_cost
        - activities_cost

        estimated_cost must equal the sum of those four cost categories.

        Costs must represent the total cost for all travelers, not per person.

        Do not omit necessary travel expenses merely to satisfy the budget.
        Do not assign zero cost to accommodation, food, or transportation
        unless the provided research clearly supports that cost.

        Use realistic estimates based on the provided research.

        All estimated costs must be expressed in USD.

        estimated_total_cost must equal the sum of the estimated_cost
        of all itinerary days.

        The user's maximum total budget is ${budget} USD.
    """

    itinerary = structured_llm.invoke(itinerary_prompt)

    print("\n=== GENERATED ITINERARY ===")
    print(itinerary)

    return {"itinerary": itinerary}
