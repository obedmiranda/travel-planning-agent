# travel-planning-agent

An adaptive travel planning agent built with LangGraph that creates, evaluates, and dynamically replans itineraries based on user goals and constraints.

## Current Progress

The agent currently implements the initial request parsing and planning-readiness stages of the travel planning workflow.

It can:

- Parse a natural-language travel request into structured graph state.
- Extract the destination, number of travelers, trip duration, and budget using structured LLM output.
- Determine whether enough information is available to begin planning.
- Require destination, travelers, trip duration, and budget when the user requests a full trip plan.
- Route execution conditionally based on the planner's decision.
- Pause execution using a human-in-the-loop interrupt when required information is missing.
- Preserve execution state using LangGraph checkpointing.

Example:

Input:

`Plan a trip to Japan`

Parsed state:

```text
destination: Japan
travelers: None
trip_duration: None
budget: None
```

Planner decision:

```text
can_plan: False
missing_information:
  - travelers
  - trip duration
  - budget
```

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
Yes        No
 ↓          ↓
END    Request Information
             ↓
          Interrupt
             ⏸
```

The **Parse Request** node extracts available travel information and stores it in the graph state.

The **Planner** evaluates whether the available information is sufficient for the user's request. For full trip-planning requests, destination, number of travelers, trip duration, and budget are required before planning can continue.

If required information is missing, the graph routes to the **Request Information** node, which uses a LangGraph interrupt to pause execution while preserving the current state.

## Next Step

Resume an interrupted execution with user-provided information, update the structured travel state, and route the updated state back through the Planner.
