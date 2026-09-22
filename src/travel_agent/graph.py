from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from travel_agent.nodes.parse_request import get_request
from travel_agent.nodes.planner import planner
from travel_agent.nodes.request_information import request_information
from travel_agent.nodes.research import research
from travel_agent.nodes.task_planner import task_planner
from travel_agent.state import InputState, TravelAgentState


def route_after_planner(state: TravelAgentState) -> str:
    if state["can_plan"]:
        print("ROUTE: can_plan")
        return "can_plan"

    print("ROUTE: missing_information")
    return "missing_information"


def route_after_research(state: TravelAgentState) -> str:
    for task in state["plan"]:
        if task.status == "pending":
            return "continue_research"
    return "research_completed"


workflow = StateGraph(TravelAgentState, input_schema=InputState)

# Nodes setup
workflow.add_node("parse_request", get_request)
workflow.add_node("planner", planner)
workflow.add_node("request_information", request_information)
workflow.add_node("task_planner", task_planner)
workflow.add_node("research", research)

# Edges setup
workflow.add_edge(START, "parse_request")
workflow.add_edge("parse_request", "planner")

workflow.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "can_plan": "task_planner",
        "missing_information": "request_information",
    },
)

workflow.add_edge("request_information", "planner")
workflow.add_edge("task_planner", "research")

workflow.add_conditional_edges(
    "research",
    route_after_research,
    {
        "continue_research": "research",
        "research_completed": END,
    },
)


checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "test-1"}}

result = graph.invoke(
    {"user_request": "Plan a trip to Japan"},
    config=config,
)

resumed_result = graph.invoke(
    Command(resume="2 people, 7 days, $5000"),
    config=config,
)


# print("\n--- INITIAL STATE ---")
# print(f"Destination: {result['destination']}")
# print(f"Travelers: {result['travelers']}")
# print(f"Trip duration: {result['trip_duration']}")
# print(f"Budget: {result['budget']}")
# print(f"Can plan: {result['can_plan']}")

# print("\n--- RESUMED STATE ---")
# print(f"Destination: {resumed_result['destination']}")
# print(f"Travelers: {resumed_result['travelers']}")
# print(f"Trip duration: {resumed_result['trip_duration']}")
# print(f"Budget: ${resumed_result['budget']}")
# print(f"Can plan: {resumed_result['can_plan']}")

# print("\n--- PLAN ---")
# for index, task in enumerate(resumed_result["plan"], start=1):
#     print(f"{index}. {task.description}")
#     print(f"   Query: {task.search_query}")
#     print(f"   Status: {task.status}")
