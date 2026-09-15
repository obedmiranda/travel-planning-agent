from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.parsed_request import ParsedRequest
from travel_agent.state import TravelAgentState

load_dotenv()
llm = ChatOpenAI(model="gpt-5-nano")


def get_request(state: TravelAgentState) -> dict[str, str]:
    """
    Extract the travel destination from the user's request
    and return it as a state update.
    """
    user_request = state["user_request"]

    structured_llm = llm.with_structured_output(ParsedRequest)

    request_prompt = f"""
        Analyze the user request and extract the following travel information:

        - Destination: the city, country, or geographic place the user wants to visit.
        - Travelers: the number of people traveling.
        - Trip Duration: the amount of time the trip should take
        - Budget: the amount of money available for the trip

        User request: {user_request}
    """

    parsed_request = structured_llm.invoke(request_prompt)

    return {
        "destination": parsed_request.destination,
        "travelers": parsed_request.travelers,
        "trip_duration": parsed_request.trip_duration,
        "budget": parsed_request.budget,
    }
