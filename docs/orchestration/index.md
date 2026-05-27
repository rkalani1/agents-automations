# Orchestration

Orchestration is the set of patterns that determine how one or more agents plan, act, observe, and hand off work. A single model call is not an agent. An agent is a loop — and orchestration is the design of that loop and its boundaries.

## What you will find in this section

| Page | What it covers |
|------|---------------|
| [Single-agent loops](single-agent.md) | Plan → act → observe → reflect. When this is sufficient. |
| [Multi-agent patterns](multi-agent.md) | Supervisor + workers, debate, planner + executor, handoffs |
| [Local-first automation](local-first.md) | stdio MCP only, local state, no remote tool access to user accounts |
| [State, memory, and handoffs](state.md) | Conversation history vs. external memory vs. vector recall |

## Why orchestration design matters

Getting a model to complete a task in a single prompt works for simple queries. It fails for tasks that:

- Require more context than fits in one context window
- Have multiple independent sub-tasks that can run in parallel
- Need specialized capabilities that benefit from separate system prompts
- Require iterative refinement based on intermediate results
- Involve uncertainty about the correct approach before starting

Orchestration patterns exist to handle these cases. The right pattern for your use case depends on the task complexity, the acceptable latency, the budget for API calls, and the tolerance for errors that propagate across agent boundaries.

## Common failure modes

**Infinite loops** — an agent that cannot complete a task will sometimes loop indefinitely. Always set a maximum step count.

**Context overflow** — long agentic runs accumulate history. A context window that fills up causes model degradation or outright failures. Design for summarization or state externalization early.

**Error propagation** — in multi-agent systems, an incorrect output from one agent becomes the input to the next. Errors compound. Build verification steps at agent boundaries.

**Coordination overhead** — adding more agents does not always make a system faster or more capable. Each handoff adds latency and a potential failure point. Prefer single-agent solutions until the task genuinely exceeds what one agent can do.

## Relationship to MCP and computer use

MCP and computer use are not orchestration patterns by themselves — they are the tools that agents within an orchestrated system can call. An orchestration layer determines which agent calls which tool, in what order, with what state. The sections of this field guide are designed to be composed: a multi-agent system might include one agent that uses computer use and another that calls MCP tools, coordinated by a supervisor.
