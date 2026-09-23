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

    plan = state["plan"]
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
        Budget: {budget}

        RESEARCH:
        {research_context}

        TASK:
        Build a feasible day-by-day itinerary using the travel context
        and the provided research.
        """

    itinerary = structured_llm.invoke(itinerary_prompt)
    print("\n=== GENERATED ITINERARY ===")
    print(itinerary)
    return {"itinerary": itinerary}
