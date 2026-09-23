# Travel Planning Agent

An adaptive travel planning agent built with Python and LangGraph that researches travel options, creates structured itineraries, evaluates them against user constraints, and dynamically replans when necessary.

The project was built as a practical implementation of the **Planning Agent** cognitive architecture, combining planning, tool use, deterministic validation, human-in-the-loop interaction, and adaptive replanning.

## Overview

The agent takes a natural-language travel request such as:

```text
Plan a trip to Japan
```

It extracts the available travel information and determines whether enough context exists to begin planning.

If required information is missing, the workflow pauses and asks the user for it. Once the required information is available, the agent decomposes the travel goal into research tasks, executes web searches, synthesizes the findings, builds an itinerary, evaluates it against the user's constraints, and replans when necessary.

The workflow can also determine that a set of constraints is not realistically satisfiable instead of forcing an invalid itinerary.

## MVP Status

The end-to-end MVP workflow is complete.

The agent can:

- Parse a natural-language travel request into structured graph state.
- Extract destination, number of travelers, trip duration, and budget using structured LLM output.
- Determine whether enough information is available to begin planning.
- Pause execution using a human-in-the-loop interrupt when required information is missing.
- Resume execution with the user's additional information.
- Preserve execution state using LangGraph checkpointing.
- Decompose the travel goal into focused research tasks.
- Generate web search queries for individual research tasks.
- Execute research tasks using web search.
- Synthesize search results into conclusions stored in each task.
- Track research task execution status individually.
- Continue researching until no pending tasks remain.
- Handle search provider failures without crashing the entire research workflow.
- Build a structured day-by-day itinerary from completed research.
- Estimate accommodation, food, transportation, and activity costs.
- Validate itinerary duration and cost calculations deterministically.
- Validate the itinerary against the user's total budget.
- Replan an itinerary when validation fails.
- Detect when constraints cannot realistically be satisfied.
- Limit replanning attempts to prevent infinite planning loops.
- Produce a human-readable final itinerary with daily cost breakdowns.
- Explain why a valid itinerary could not be produced when constraints are unsatisfiable.

## Agent Flow

```text
START
  ↓
Parse Request
  ↓
Planner
  ↓
Can plan?
 /       \
No       Yes
↓         ↓
Request   Task Planner
Information    ↓
↓           Research ←─────┐
Interrupt      ↓            │
⏸          Pending? ─ Yes ┘
↓              │
Resume         No
↓              ↓
Planner    Build Itinerary
                 ↓
              Evaluator
             /         \
          Valid        Invalid
            ↓             ↓
        Finalize      Replanner
                       /      \
                  Revised   Unsatisfiable
                     ↓           ↓
                 Evaluator    Finalize
                     ↺
```

The evaluator also enforces a maximum number of replanning attempts. If the itinerary remains invalid after the configured limit, the workflow terminates and reports the remaining constraint violations.

## Architecture

The workflow is implemented as a LangGraph state graph.

Each node has a focused responsibility.

### Parse Request

Converts the user's natural-language request into structured travel information.

Currently extracts:

- Destination
- Number of travelers
- Trip duration
- Budget

The parser supports partial information so the workflow can progressively collect missing values.

### Planner

Determines whether enough information is available to begin planning.

The planner does not create the itinerary. Its responsibility is **planning readiness**.

If required information is missing, execution is routed to the human-in-the-loop information request.

### Request Information

Uses a LangGraph interrupt to pause execution when required information is missing.

The user's response is parsed and merged back into the graph state before returning to the planner.

LangGraph checkpointing allows the workflow to preserve state while execution is paused.

### Task Planner

Once enough information is available, the task planner decomposes the travel goal into focused research tasks.

Each task contains:

- A research objective
- A search query
- Execution status
- A synthesized result

The task planner creates research work only. It does not build or evaluate the itinerary.

### Research

Executes one pending research task at a time.

Each task uses web search to gather external information and an LLM to synthesize the search results into a concise conclusion.

After processing a task, the graph checks whether additional pending tasks remain.

```text
Research
   ↓
Process one pending task
   ↓
Pending tasks remaining?
   ├── Yes → Research
   └── No  → Build Itinerary
```

This makes individual task execution observable and allows the graph to track research progress explicitly.

### Build Itinerary

Uses the completed research together with the user's travel constraints to generate a structured day-by-day itinerary.

Each day contains:

- City
- Activities
- Accommodation cost
- Food cost
- Transportation cost
- Activity cost
- Estimated daily cost

The itinerary also contains an estimated total cost and currency.

Costs represent the total cost for all travelers.

### Evaluator

The evaluator performs deterministic validation in Python instead of relying entirely on another LLM judgment.

It currently validates:

- Requested trip duration
- Daily cost calculations
- Total itinerary cost calculation
- Total budget constraint

For every day:

```text
accommodation
+ food
+ transportation
+ activities
----------------
estimated daily cost
```

The evaluator independently calculates the expected daily total and compares it with the generated value.

It also verifies:

```text
sum(all daily costs) = estimated total trip cost
```

This prevents the itinerary generator or replanner from satisfying the budget simply by returning inconsistent totals.

### Replanner

If the evaluator finds constraint violations, the itinerary is sent to the replanner.

The replanner receives:

- The current itinerary
- Validation violations
- Original travel constraints
- Existing research

It can make one of two decisions.

```text
Replanning Decision
├── revised
│   └── Return a corrected itinerary
│
└── unsatisfiable
    └── Explain why the constraints cannot realistically be satisfied
```

A revised itinerary is sent back through the evaluator.

If the constraints are determined to be unsatisfiable, the workflow terminates through the finalization stage instead of generating unrealistic values simply to pass validation.

The graph also limits replanning attempts to prevent infinite loops.

### Finalize

Produces the final user-facing response.

For a valid itinerary, the output contains:

- Day-by-day activities
- Daily accommodation cost
- Daily food cost
- Daily transportation cost
- Daily activity cost
- Daily total
- Estimated trip total
- Constraint validation result

If the constraints cannot be satisfied, the final response explains why instead of returning an invalid itinerary.

## State

The graph uses a shared `TravelAgentState` to represent the current execution state.

Conceptually:

```text
State₀
  ↓
Node
  ↓
State₁
  ↓
Node
  ↓
State₂
```

Nodes consume the parts of state they need and return partial updates.

The state tracks information such as:

```text
user_request
destination
travelers
trip_duration
budget
can_plan
missing_information
plan
itinerary
evaluation
replan_count
replanning_failed
replanning_failure_reason
final_response
```

State represents the current workflow execution.

Checkpointing provides persistence so execution can pause and resume during human-in-the-loop interactions.

## Research Tasks

Research tasks are modeled separately from graph nodes.

A node represents reusable workflow behavior.

A task represents a specific unit of work created by the planner.

Example:

```text
Node:
Research

Tasks:
- Research affordable accommodation in Tokyo
- Compare transportation options
- Estimate food costs
- Find low-cost attractions
```

Each task tracks its own execution status:

```text
pending
in_progress
completed
failed
```

This allows the research node to execute tasks incrementally.

## Tool Use

The research stage uses a web search tool backed by SerpApi.

The tool receives a search query and returns structured search results containing:

- Title
- URL
- Snippet

The research node then uses an LLM to synthesize those results into a conclusion relevant to the current research task.

This separates:

```text
Tool execution
      ↓
Raw evidence
      ↓
LLM synthesis
      ↓
Task result
```

The current MVP intentionally uses a small tool surface rather than introducing a large tool registry or autonomous tool-selection layer.

## Cost Validation

An important design goal is preventing the agent from satisfying constraints through mathematically inconsistent or obviously incomplete cost totals.

Each itinerary day contains explicit cost categories:

```text
Accommodation
Food
Transportation
Activities
```

The evaluator recalculates daily and trip totals independently.

For example:

```text
Accommodation:      $60
Food:               $40
Transportation:     $20
Activities:         $10
--------------------------------
Expected day total: $130
```

If the generated `estimated_cost` does not equal `$130`, the itinerary fails validation.

This does not attempt to prove that every market price is objectively correct. Instead, it ensures that the agent's generated cost model is internally consistent and that required travel expense categories are represented.

## Failure Handling

The workflow handles several failure scenarios.

### Missing user information

Execution pauses and waits for the required information.

### Search provider failure

The affected research task is marked as failed instead of crashing the entire graph.

### Invalid itinerary

The evaluator records the violations and routes the itinerary to the replanner.

### Unsatisfiable constraints

The replanner can determine that the requested constraints cannot realistically be satisfied based on the available research.

### Replanning limit

Replanning is limited to a maximum of three attempts to prevent infinite execution loops.

If the itinerary remains invalid, the workflow terminates and reports the remaining violations.

## Example Behavior

A request such as:

```text
Plan a trip to Japan
```

does not contain enough information to begin planning.

The graph pauses and can resume with:

```text
2 people, 7 days, $5000
```

The agent then researches the trip, builds an itinerary, validates its cost and duration, and returns the final plan.

For an intentionally unrealistic constraint such as:

```text
2 people, 7 days, $100
```

the agent can research realistic travel costs, determine that the generated itinerary exceeds the budget, and conclude that the constraint cannot reasonably be satisfied instead of forcing travel costs to zero.

## Project Structure

```text
travel-planning-agent/
├── README.md
├── .gitignore
├── LICENSE
├── pyproject.toml
├── .env.example
├── src/
│   └── travel_agent/
│       ├── __init__.py
│       ├── graph.py
│       ├── state.py
│       ├── nodes/
│       │   ├── __init__.py
│       │   ├── parse_request.py
│       │   ├── planner.py
│       │   ├── request_information.py
│       │   ├── task_planner.py
│       │   ├── research.py
│       │   ├── build_itinerary.py
│       │   ├── evaluator.py
│       │   ├── replanner.py
│       │   └── finalize.py
│       ├── tools/
│       │   ├── __init__.py
│       │   └── web_search.py
│       └── models/
│           ├── __init__.py
│           ├── task.py
│           ├── parsed_request.py
│           ├── planning_decision.py
│           ├── search_result.py
│           ├── itinerary.py
│           ├── evaluation.py
│           └── replanning_decision.py
└── tests/
```

## Tech Stack

- Python
- LangGraph
- LangChain
- OpenAI
- Pydantic
- SerpApi
- python-dotenv

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_api_key
```

Do not commit the `.env` file.

An `.env.example` file can be used to document the required environment variables without exposing credentials.

## Running the Agent

Install the project dependencies and configure the required environment variables.

From the project root, run:

```bash
PYTHONPATH=src python src/travel_agent/graph.py
```

The current development entry point contains a sample request used to exercise the graph and human-in-the-loop resume flow.

## Current MVP Limitations

The current version intentionally keeps the scope focused on the Planning Agent architecture.

Known limitations include:

- Travel prices are estimates derived from web search results rather than live booking inventory.
- The agent does not book flights, hotels, transportation, or activities.
- Search quality depends on the external search results returned for each generated query.
- Currency handling is currently simplified around USD itinerary estimates.
- Cost validation checks internal consistency but does not independently verify every generated market price.
- Research tasks use a generic web search tool rather than specialized travel APIs.
- Long-term user memory is not implemented.
- The project does not implement a large autonomous tool-selection system.
- The current interface is a development/CLI workflow rather than a production UI.

These limitations are intentional for the MVP and keep the project focused on planning, tool use, evaluation, replanning, and graph orchestration.

## What This Project Demonstrates

This project demonstrates several agentic AI concepts in one workflow:

- Structured LLM outputs
- Shared graph state
- Conditional routing
- Planning readiness
- Task decomposition
- Human-in-the-loop execution
- Checkpointing and resume
- Tool use
- External research
- Evidence synthesis
- Iterative task execution
- Deterministic evaluation
- Constraint validation
- Adaptive replanning
- Unsatisfiable constraint detection
- Loop termination
- Separation between reasoning, execution, validation, and presentation

The project intentionally favors explicit workflow architecture over a single large prompt so that planning decisions, state transitions, tool execution, validation, and failure handling remain observable.

## Future Improvements

Possible future extensions include:

- Live hotel and flight pricing APIs
- Dedicated accommodation and transportation tools
- Improved search query generation and source selection
- Additional deterministic constraints such as maximum activities per day
- Required-city validation
- Travel-time feasibility checks
- Date-aware planning
- Multi-currency support and exchange-rate handling
- Source citations in the final itinerary
- Persistent user travel preferences
- Automated tests for graph routing and evaluator behavior
- API or web interface
- Production persistence instead of in-memory checkpointing

## License

See the `LICENSE` file for license information.
