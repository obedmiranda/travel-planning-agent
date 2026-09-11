from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.parsed_request import ParsedRequest
from travel_agent.state import TravelAgentState

load_dotenv()
llm = ChatOpenAI(model="gpt-5-nano")


def get_request(state: TravelAgentState) -> dict[str, str]:

    user_request = state["user_request"]

    structured_llm = llm.with_structured_output(ParsedRequest)

    request_prompt = f"""
        Analyze the user request and extract the destination.

        The destination can be a city, country, or other geographic place.

        User request: {user_request}
        """

    parsed_request = structured_llm.invoke(request_prompt)

    return {"destination": parsed_request.destination}
