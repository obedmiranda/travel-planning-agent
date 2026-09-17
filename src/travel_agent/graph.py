from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

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


# graph = workflow.compile()

checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "test-1"}}

# user_request en el invoke es el mismo que definimos en la estructura del state
# result = graph.invoke({"user_request": "Plan a trip to Japan"})
# result = graph.invoke(
#     {"user_request": "Plan a 7-day trip to Japan for two people with a $5,000 budget"}
# )

# result = graph.invoke({"user_request": "Give me some activity ideas in Japan"})

# result = graph.invoke({"user_request": "Plan a trip to Japan"})
# print(json.dumps(result, indent=2))

result = graph.invoke({"user_request": "Plan a trip to Japan"}, config=config)

print(result)
