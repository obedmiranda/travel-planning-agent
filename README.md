# travel-planning-agent

An adaptive travel planning agent built with LangGraph that creates, evaluates, and dynamically replans itineraries based on user goals and constraints.

## Current Progress

The agent currently implements the request understanding, planning-readiness, task decomposition, research, and initial itinerary-building stages of the travel planning workflow.

It can:

- Parse a natural-language travel request into structured graph state.
- Extract the destination, number of travelers, trip duration, and budget using structured LLM output.
- Determine whether enough information is available to begin planning.
- Pause execution using a human-in-the-loop interrupt when required information is missing.
- Resume execution with the user's missing information.
- Preserve execution state using LangGraph checkpointing.
- Decompose the travel goal into focused research tasks.
- Generate a web search query for each research task.
- Execute research tasks using web search.
- Synthesize search results into conclusions stored in each task.
- Track research task status individually.
- Continue researching until no pending tasks remain.
- Handle search provider failures without crashing the entire research workflow.
- Pass the completed research plan to the itinerary-building stage.

## Current Flow

```text
User Request
     ↓
Parse Request
     ↓
Planner
     ↓
Can plan?
  /        \
 No        Yes
 ↓          ↓
Request   Task Planner
Information    ↓
 ↓         Research ←─────┐
Interrupt      ↓           │
 ⏸         Pending? ─ Yes ┘
 ↓             │
Resume         No
 ↓             ↓
Planner   Build Itinerary
