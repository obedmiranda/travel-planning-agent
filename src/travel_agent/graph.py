from langgraph.graph import END, START, StateGraph

from travel_agent.nodes.parse_request import get_request
from travel_agent.state import InputState, TravelAgentState

workflow = StateGraph(TravelAgentState, input_schema=InputState)

workflow.add_node("parse_request", get_request)
workflow.add_edge(START, "parse_request")
workflow.add_edge("parse_request", END)

graph = workflow.compile()

# user_request en el invoke es el mismo que definimos en la estructura del state
result = graph.invoke({"user_request": "Plan my trip to Japan"})

print(result)
