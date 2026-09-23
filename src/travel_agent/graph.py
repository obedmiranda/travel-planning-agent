from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from travel_agent.nodes.build_itinerary import build_itinerary
from travel_agent.nodes.evaluator import evaluator
from travel_agent.nodes.finalize import finalize
from travel_agent.nodes.parse_request import get_request
from travel_agent.nodes.planner import planner
from travel_agent.nodes.replanner import replanner
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


def route_after_evaluator(state: TravelAgentState) -> str:
    evaluation = state["evaluation"]
    replan_count = state.get("replan_count", 0)

    if evaluation.valid:
        return "valid"

    if replan_count >= 3:
        return "max_replans"

    return "invalid"


def route_after_replanner(state: TravelAgentState) -> str:
    if state["replanning_failed"]:
        return "unsatisfiable"

    return "revised"


workflow = StateGraph(
    TravelAgentState,
    input_schema=InputState,
)

# Nodes setup
workflow.add_node("parse_request", get_request)
workflow.add_node("planner", planner)
workflow.add_node("request_information", request_information)
workflow.add_node("task_planner", task_planner)
workflow.add_node("research", research)
workflow.add_node("build_itinerary", build_itinerary)
workflow.add_node("evaluator", evaluator)
workflow.add_node("replanner", replanner)
workflow.add_node("finalize", finalize)

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
        "research_completed": "build_itinerary",
    },
)

workflow.add_edge("build_itinerary", "evaluator")

workflow.add_conditional_edges(
    "evaluator",
    route_after_evaluator,
    {
        "valid": "finalize",
        "invalid": "replanner",
        "max_replans": "finalize",
    },
)

workflow.add_conditional_edges(
    "replanner",
    route_after_replanner,
    {
        "revised": "evaluator",
        "unsatisfiable": "finalize",
    },
)

workflow.add_edge("finalize", END)

# Persistence
checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

# Test execution
config: RunnableConfig = {
    "configurable": {
        "thread_id": "test-1",
    }
}

result = graph.invoke(
    {
        "user_request": "Plan a trip to Japan",
    },
    config=config,
)

resumed_result = graph.invoke(
    Command(
        resume="2 people, 7 days, $100",
    ),
    config=config,
)
