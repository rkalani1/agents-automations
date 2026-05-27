> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18), [Anthropic computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

# Single-Agent Loops

A single-agent loop is the simplest form of agent orchestration. One model instance runs a repeated cycle: plan, act, observe, and optionally reflect. All state is either in the context window or explicitly managed by the loop. There is no handoff to another agent.

This pattern covers more use cases than its simplicity suggests. Most real-world automation problems can be solved with a well-designed single-agent loop. Understanding it in depth is a prerequisite for knowing when you genuinely need something more complex.

## The core loop: plan → act → observe → reflect

### Plan

At the start of each iteration, the model receives the current state and decides what to do next. In a tool-using agent, this means the model reviews the conversation history, the available tools, and the current task, and produces either a tool call or a final answer.

The "plan" phase does not require a separate reasoning step. In most implementations, it is implicit: the model's output is itself the plan. For tasks that benefit from explicit planning, you can prompt the model to reason step by step before committing to an action, or use a model with built-in extended thinking.

### Act

The agent executes the plan. For a tool-using agent, this means calling the tool and obtaining a result. The "act" phase is the bridge between the model's world (tokens) and the real world (API calls, filesystem operations, browser clicks).

Acts should be atomic where possible: a single tool call whose result can be fully observed. Acts that spawn multiple side effects (sending an email AND modifying a database) are harder to reason about and harder to recover from on failure.

### Observe

The result of the action is added to the conversation history. The model has no state between turns except what is in the context; observation is how it learns what happened. This means the quality of your tool result formatting matters. A tool that returns raw JSON with 50 fields makes it hard for the model to extract the relevant information. Format results to surface the most important signal clearly.

### Reflect

Reflection is optional but valuable for complex tasks. After observing a result, the model (or a separate call) evaluates whether the observation suggests a plan change. This can be as simple as "did this step succeed?" or as elaborate as a structured self-critique of intermediate outputs.

Explicit reflection prompts are most useful when:
- The model has just received unexpected output from a tool
- The task involves multi-step reasoning that benefits from explicit checkpointing
- You are using a smaller or less capable model that benefits from structured reasoning scaffolding

For capable models on clear tasks, reflection is often implicit in the next plan step.

## A concrete implementation

```python
from anthropic import Anthropic

client = Anthropic()

def run_agent_loop(
    task: str,
    tools: list[dict],
    tool_executor,  # callable: (name, input) -> str
    system: str = "",
    max_turns: int = 20,
) -> str:
    messages = [{"role": "user", "content": task}]

    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages,
        )

        # Add assistant turn to history
        messages.append({"role": "assistant", "content": response.content})

        # Collect tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                # --- Act ---
                result = tool_executor(block.name, block.input)
                # --- Observe ---
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })

        # No tool calls = model is done
        if not tool_results:
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        # Feed observations back
        messages.append({"role": "user", "content": tool_results})

    return "Max turns reached without completion."
```

Key design decisions in this loop:

- `max_turns` is enforced. Without this, a stuck agent runs until it hits a context length limit or exhausts your budget.
- Tool results are added as `tool_result` content blocks. This is the format the model expects; plain strings in user messages work for simple cases but are not protocol-correct.
- The loop exits as soon as the model returns a turn with no tool calls.
- The response history is maintained in `messages`. This is the agent's entire memory.

## When a single-agent loop is enough

The single-agent loop is sufficient when:

**The task fits in one context window.** A task that requires reading 5 documents, synthesizing them, and writing a report can be done in a single loop if the documents fit in context. If they do not, you need external state management, not necessarily multiple agents.

**The task is sequential, not parallel.** If every step depends on the previous step's result, parallelism gains you nothing. A loop is simpler than a multi-agent system for sequential workflows.

**The task does not require specialized capabilities.** Multiple specialized agents with different system prompts are useful when the same model cannot simultaneously be a "strict code reviewer" and a "creative writer." If the task does not require that kind of role switching, a single system prompt is simpler.

**Errors do not cascade unacceptably.** In a single-agent loop, a wrong tool call produces a wrong observation that the model can often recover from in the next turn. In multi-agent systems, wrong outputs from one agent become the input to the next, amplifying errors. Single-agent loops are more self-correcting.

**Latency from sequential steps is acceptable.** A single agent processes steps sequentially. If your task has genuinely independent sub-tasks and latency matters, parallelism via multiple agents or async tool execution is worth the added complexity.

## Step count guidelines

Empirically:

- Routine tasks (single web lookup, single file read, simple calculation): 1–5 steps
- Multi-step research or data gathering: 10–30 steps
- Complex workflows (writing, then revising, then formatting): 20–50 steps
- Open-ended exploration tasks: unbounded, requiring a maximum step guardrail

For any production deployment, set `max_turns` based on the task type and monitor the distribution of actual step counts. If agents regularly hit the maximum, either the maximum is too low or the task genuinely needs a different approach.

## Handling stuck loops

A model can get stuck repeating the same tool call with the same arguments, usually because the tool returned an error or unexpected result and the model does not know how to proceed. Detect this with a simple repetition check:

```python
from collections import Counter

def check_repetition(messages: list[dict], window: int = 4) -> bool:
    # Look at the last `window` assistant messages for repeated tool calls
    tool_calls = []
    for msg in messages[-window:]:
        if isinstance(msg.get("content"), list):
            for block in msg["content"]:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    key = (block["name"], str(block["input"]))
                    tool_calls.append(key)
    counts = Counter(tool_calls)
    return any(count >= 2 for count in counts.values())
```

If repetition is detected, inject a user message that tells the model it appears stuck and asks it to try a different approach or return what it has so far.

## Logging and observability

Every action in a production single-agent loop should be logged with:
- Turn number
- Tool name and input
- Tool result (or error)
- Token counts for input and output

This data is essential for diagnosing failures, tuning prompts, and estimating costs. Log to a persistent store, not just stdout, because context windows do not survive process restarts.
