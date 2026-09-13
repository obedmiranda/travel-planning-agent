# travel-planning-agent
An adaptive travel planning agent built with LangGraph that creates, evaluates, and dynamically replans itineraries based on user goals and constraints

## Current Progress

The agent can currently parse a natural-language travel request and extract the destination into the graph state using structured LLM output.

Example:

Input:
`Plan my trip to Japan`

Parsed state:
`destination: Japan`

### Current Flow

The current graph implements the first step of the agent:

`User Request → Parse Request → State`

The Parse Request node uses structured LLM output to extract the travel destination and store it in the graph state.
