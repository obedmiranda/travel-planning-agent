from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from travel_agent.nodes.parse_request import get_request
from travel_agent.nodes.planner import planner
from travel_agent.nodes.request_information import request_information
from travel_agent.state import InputState, TravelAgentState


def route_after_planner(state: TravelAgentState) -> str:
    if state["can_plan"]:
        print("ROUTE: can_plan")
        return "can_plan"

    print("ROUTE: missing_information")
    return "missing_information"


workflow = StateGraph(TravelAgentState, input_schema=InputState)

# Nodes setup
workflow.add_node("parse_request", get_request)
workflow.add_node("planner", planner)
workflow.add_node("request_information", request_information)

# Edges setup
workflow.add_edge(START, "parse_request")
workflow.add_edge("parse_request", "planner")


workflow.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "can_plan": END,
        "missing_information": "request_information",
    },
)


checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "test-1"}}

result = graph.invoke({"user_request": "Plan a trip to Japan"}, config=config)

resumed_result = graph.invoke(Command(resume="2 people, 7 days, $5000"), config=config)
print(result)
