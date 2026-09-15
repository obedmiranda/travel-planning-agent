import json

from langgraph.graph import END, START, StateGraph

from travel_agent.nodes.parse_request import get_request
from travel_agent.nodes.planner import planner
from travel_agent.state import InputState, TravelAgentState

workflow = StateGraph(TravelAgentState, input_schema=InputState)

workflow.add_node("parse_request", get_request)
workflow.add_node("planner", planner)

workflow.add_edge(START, "parse_request")
workflow.add_edge("parse_request", "planner")
workflow.add_edge("planner", END)

graph = workflow.compile()

# user_request en el invoke es el mismo que definimos en la estructura del state
# result = graph.invoke({"user_request": "Plan a trip to Japan"})
# result = graph.invoke(
#     {"user_request": "Plan a 7-day trip to Japan for two people with a $5,000 budget"}
# )

result = graph.invoke({"user_request": "Give me some activity ideas in Japan"})
print(json.dumps(result, indent=2))
