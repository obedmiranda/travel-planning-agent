from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.parsed_request import ParsedRequest
from travel_agent.state import TravelAgentState

load_dotenv()
llm = ChatOpenAI(model="gpt-5-nano")


def get_request(
    state: TravelAgentState,
) -> dict[str, str | int | float | None]:

    user_request = state["user_request"]

    parsed_request = parse_travel_information(user_request)

    return {
        "destination": parsed_request.destination,
        "travelers": parsed_request.travelers,
        "trip_duration": parsed_request.trip_duration,
        "budget": parsed_request.budget,
    }


def parse_travel_information(text: str) -> ParsedRequest:
    structured_llm = llm.with_structured_output(ParsedRequest)

    request_prompt = f"""
        Analyze the text and extract the following travel information:

        - Destination: the city, country, or geographic place the user wants to visit.
        - Travelers: the number of people traveling.
        - Trip Duration: the amount of time the trip should take.
        - Budget: the amount of money available for the trip.

        Do not invent information that is not present.

        Text: {text}
    """

    result = structured_llm.invoke(request_prompt)

    return ParsedRequest.model_validate(result)
