from langchain_openai import ChatOpenAI

from travel_agent.models.search_result import SearchResult
from travel_agent.models.task import Task
from travel_agent.state import TravelAgentState
from travel_agent.tools.web_search import web_search

llm = ChatOpenAI(model="gpt-5-nano")


def synthesize_research(
    task_description: str, search_results: list[SearchResult,]
) -> str:

    research_prompt = f"""
        You are a travel research assistant.

        RESEARCH TASK:
        {task_description}

        SEARCH RESULTS:
        {search_results}

        TASK:
        Analyze the search results and produce a concise conclusion
        that directly answers the research task.

        Base your conclusion only on the provided search results.
        Do not invent information that is not supported by them.
    """

    response = llm.invoke(research_prompt)

    return str(response.content)


def research(state: TravelAgentState):
    plan = state["plan"]

    for task in plan:
        if task.status == "pending":
            results = web_search(task.search_query)

            research_result = synthesize_research(
                task.description,
                results,
            )

            task.result = research_result
            task.status = "completed"

            print("TASK:", task.description)
            print("RESULT:", research_result)

            break


if __name__ == "__main__":
    test_state: TravelAgentState = {
        "user_request": "Plan a trip to Japan",
        "destination": "Japan",
        "travelers": 2,
        "trip_duration": 7,
        "budget": 5000.0,
        "can_plan": True,
        "missing_information": [],
        "plan": [
            Task(
                description="Research hotels",
                search_query="Japan hotels for 2 travelers 7 nights",
            ),
            Task(
                description="Research transportation",
                search_query="Japan transportation costs Tokyo Kyoto Osaka",
            ),
            Task(
                description="Research attractions",
                search_query="Japan attractions Tokyo Kyoto Osaka admission prices",
            ),
        ],
        "itinerary": {},
        "evaluation": {},
        "replan_count": 0,
        "final_response": "",
        "required_cities": [],
        "interests": [],
        "max_activities_per_day": 2,
    }

    research(test_state)
