> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18), [OpenAI Agents SDK](https://openai.com/index/new-tools-for-building-agents/)

# Multi-Agent Patterns

Multi-agent systems use more than one model instance to complete a task. Each agent typically has a specialized role, a tailored system prompt, and a defined interface for receiving inputs and returning outputs. The agents are coordinated by a pattern — supervisor, debate, planner/executor, or handoff — that determines who talks to whom and in what order.

Use multi-agent architecture when the task genuinely cannot be completed by a single-agent loop: when parallelism would reduce latency significantly, when the task requires role-switching incompatible with a single system prompt, when sub-task outputs need independent verification, or when the context required exceeds a single window.

## Pattern 1: Supervisor + Workers

The most common multi-agent pattern. A supervisor agent breaks the task into sub-tasks and dispatches them to worker agents. Workers execute their assigned sub-task and return results. The supervisor aggregates results and decides whether to run additional workers or return the final answer.

```
+------------------+
|   Supervisor     |
| (planning agent) |
+--------+---------+
         |
    [dispatches sub-tasks]
         |
   +-----+------+-------+
   |             |       |
+--+---+    +---+--+  +--+---+
|Worker|    |Worker|  |Worker|
|  A   |    |  B   |  |  C   |
+------+    +------+  +------+
   |             |       |
   +------+------+-------+
          |
    [results returned to supervisor]
          |
   +------+------+
   | Supervisor  |
   | (synthesis) |
   +-------------+
```

Implementation sketch:

```python
def supervisor_loop(task: str, worker_agents: dict) -> str:
    # Supervisor receives the task and decides which workers to invoke
    plan = call_supervisor(task)

    results = {}
    for sub_task in plan.sub_tasks:
        worker = worker_agents[sub_task.worker_type]
        # Workers can run in parallel if they are independent
        results[sub_task.id] = worker.run(sub_task.instructions)

    # Supervisor synthesizes the results
    return call_supervisor_synthesis(task, results)
```

Strengths: workers can be specialized (a "code writer" agent vs. a "code reviewer" agent vs. a "test writer" agent); independent sub-tasks can run in parallel; the supervisor can retry failed sub-tasks without re-running the whole pipeline.

Weaknesses: the supervisor itself can fail or produce a poor plan; each worker invocation adds latency and token cost; error propagation from worker to supervisor requires careful handling.

## Pattern 2: Debate / Ensemble

Two or more agents independently solve the same problem. A judge agent (or a voting mechanism) selects the best answer or synthesizes across answers.

```
+----------+    +----------+
| Agent A  |    | Agent B  |
| (draft 1)|    | (draft 2)|
+----+-----+    +-----+----+
     |                |
     +------+  +------+
            |  |
       +----+--+----+
       |   Judge    |
       | (evaluator)|
       +------------+
              |
         [final answer]
```

Use this pattern when:
- The task has a verifiable correct answer (code that passes tests, a calculation that can be checked)
- You want to reduce the variance of model outputs
- The cost of a wrong answer is high enough to justify multiple model calls

Weaknesses: doubles or triples the API cost and latency; the judge can itself be wrong; for creative or open-ended tasks, "better" is subjective.

## Pattern 3: Planner + Executor

The planner produces a complete plan before any execution begins. The executor follows the plan step by step, checking in with the planner only if it encounters a step it cannot complete.

```
+----------+
|  Planner |
|(full plan|
| upfront) |
+----+-----+
     |
  [step list]
     |
+----v-----+
| Executor |
|(runs each|
|step, logs|
|  results)|
+----+-----+
     |
  [failure? check in]
     |
+----v-----+
|  Planner |
|(re-plans  |
|from here)|
+----------+
```

This pattern works well when:
- The task structure is predictable enough that a plan can be made upfront
- The executor is reliable at following explicit instructions
- Re-planning is cheaper than the cost of unplanned exploration

Weaknesses: a bad initial plan propagates through all execution steps; tasks that require information discovered during execution cannot be fully planned upfront; the executor's failures may not map cleanly back to planner-understandable descriptions.

## Pattern 4: Handoffs (sequential pipeline)

Agents in sequence. Agent A produces an output that becomes the input to Agent B. Each agent adds value and passes a refined artifact downstream.

```
+----------+     +----------+     +----------+
| Agent A  | --> | Agent B  | --> | Agent C  |
| (gather) |     | (analyze)|     | (format) |
+----------+     +----------+     +----------+
```

The OpenAI Agents SDK formalizes this pattern with explicit handoff definitions. An agent can declare: "when my task is complete, hand off to Agent B with this context." The SDK handles the message routing between agents.

Implementation using the OpenAI Agents SDK pattern:

```python
# Pseudocode reflecting the Agents SDK handoff concept
from agents import Agent, handoff

researcher = Agent(
    name="researcher",
    instructions="Gather relevant data for the given topic. When done, hand off to the analyst.",
    tools=[web_search_tool],
)

analyst = Agent(
    name="analyst",
    instructions="Analyze the data provided. Write a structured summary. Hand off to the formatter.",
)

formatter = Agent(
    name="formatter",
    instructions="Format the analyst's output as a professional report.",
)

# Define handoff chain
researcher.handoffs = [handoff(analyst)]
analyst.handoffs = [handoff(formatter)]

result = await researcher.run("Research the current state of fusion energy.")
```

Strengths: each agent has a clear, narrow responsibility; system prompts can be highly specialized; the pipeline is easy to reason about and test in isolation.

Weaknesses: errors at stage N affect all downstream stages; the pipeline is inherently sequential unless you introduce parallel branches; handoff context needs to be carefully formatted so the receiving agent has what it needs without the full upstream history.

## Coordination: what to pass in a handoff

When one agent hands off to another, the receiving agent needs context without being overwhelmed by the full upstream conversation history. Common approaches:

**Structured summary** — the handing-off agent produces a machine-readable summary (JSON or a defined template) that the receiving agent consumes as input. This is the most reliable approach.

**Excerpt** — pass the last N messages plus a task description. Cheap to implement but risks dropping important earlier context.

**Full transcript** — pass everything. Simple but expensive and can cause context overflow on long pipelines.

**External state** — write intermediate results to a shared store (file, database, vector store). The receiving agent reads what it needs. See [State, memory, and handoffs](state.md) for this approach.

## Parallelism

Independent sub-tasks in the supervisor pattern can run concurrently. In Python, use `asyncio.gather`:

```python
import asyncio

async def run_parallel_workers(sub_tasks: list, workers: dict) -> list:
    tasks = [
        workers[st.worker_type].run_async(st.instructions)
        for st in sub_tasks
    ]
    return await asyncio.gather(*tasks)
```

Be aware of rate limits. Multiple parallel agents hitting the same API endpoint simultaneously may trigger throttling. Implement exponential backoff or use a token-bucket rate limiter in front of parallel agent invocations.

## Error handling across agent boundaries

Each agent boundary is a potential failure point. Define an error contract for each agent:

- What does the agent return when it cannot complete the task?
- Does it return a partial result or raise an exception?
- How does the supervisor / downstream agent handle a failure?

A common pattern: agents return a result object with a `success` flag and an `error_message` field. The supervisor checks the flag before proceeding and can retry the sub-task, skip it, or abort the whole pipeline.

## When not to use multi-agent

Multi-agent systems are not inherently better than single-agent systems. They are appropriate when:
- Parallelism provides meaningful latency reduction
- Specialization (different system prompts) produces meaningfully better outputs
- The task genuinely exceeds a single context window

They add complexity, cost, and failure modes. If a well-crafted single-agent loop can solve the problem, prefer it.
