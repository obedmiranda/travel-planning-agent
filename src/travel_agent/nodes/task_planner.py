from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from travel_agent.models.task import Task, TaskPlan
from travel_agent.state import TravelAgentState

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano")


def task_planner(state: TravelAgentState) -> dict[str, list[Task]]:

    user_request = state["user_request"]
    destination = state["destination"]
    travelers = state["travelers"]
    trip_duration = state["trip_duration"]
    budget = state["budget"]

    structured_llm = llm.with_structured_output(TaskPlan)

    task_planner_prompt = f"""
        You are responsible for decomposing a travel planning goal
        into a sequence of research tasks.

        RULES:
        - Create only research tasks needed to later build the itinerary.
        - Do not create tasks that ask the user for additional information.
        - Do not create tasks that build or draft the itinerary.
        - Do not create tasks that evaluate the final itinerary.
        - Do not create tasks for information already available in the travel context.
        - Keep the plan focused and minimal.
        - Create between 3 and 6 tasks.

        USER GOAL:
        {user_request}

        TRAVEL CONTEXT:
        Destination: {destination}
        Travelers: {travelers}
        Trip duration: {trip_duration}
        Budget: {budget}

        TASK:
        Create the tasks necessary to gather the information required
        to build a feasible itinerary.

        Each task should represent a concrete piece of work that can
        later be executed by the research node.
    """

    tasks_planned = structured_llm.invoke(task_planner_prompt)

    return {"plan": tasks_planned.tasks}
