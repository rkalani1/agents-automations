> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18), [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

# State, Memory, and Handoffs

An agent's ability to act depends on its ability to know what has happened. That knowledge can live in three places: the active context window (conversation history), an external memory store that the agent reads and writes as a tool, or a vector database that retrieves semantically relevant past experience. Each has different characteristics, costs, and failure modes.

Understanding when to use each is one of the most practically important architectural decisions in agent design.

## Conversation history (in-context memory)

The simplest form of agent state. Every message, tool call, and tool result from the current session is passed to the model on each turn. The model has perfect recall of everything in its context window.

```python
messages = [
    {"role": "user", "content": "What files are in my workspace?"},
    {"role": "assistant", "content": [{"type": "tool_use", "name": "list_files", "input": {}, "id": "t1"}]},
    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t1", "content": "[report.md, data.csv]"}]},
    # The model can see all of the above on the next call.
]
```

Strengths:
- Zero setup. No external infrastructure.
- Perfect fidelity: every detail is preserved exactly.
- The model can refer to any earlier step without needing to fetch it.
- Simplest to debug: the full context is inspectable as a JSON array.

Weaknesses:
- Finite capacity. Every model has a maximum context length. Long agentic runs accumulate history and eventually fill the window.
- Token cost. Every input token costs money. Passing 50,000 tokens of history on every turn is expensive.
- Latency. Larger contexts take longer to process.
- No persistence across process restarts. If the process dies, the history is gone unless you have explicitly saved it.
- No sharing. If two agents need to share state, they cannot both read the same context window.

When to use: tasks that complete within a single session, context windows that will not overflow, tasks that do not require state sharing across agents or processes.

### Managing context growth

To prevent overflow, use one of these approaches:

**Sliding window** — keep only the last N turns:

```python
def trim_history(messages: list, keep_turns: int = 10) -> list:
    # Always keep the first message (the original task)
    if len(messages) <= keep_turns * 2 + 1:
        return messages
    return [messages[0]] + messages[-(keep_turns * 2):]
```

**Summarization** — when history exceeds a threshold, ask the model to summarize it into a compact representation:

```python
def summarize_history(messages: list, client) -> list:
    summary_prompt = "Summarize the work done so far and the key findings in under 200 words."
    summary_response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=messages + [{"role": "user", "content": summary_prompt}],
    )
    summary_text = summary_response.content[0].text
    # Replace history with summary + the original task
    return [
        messages[0],  # Original task
        {"role": "assistant", "content": f"[Summary of prior work: {summary_text}]"},
    ]
```

## External memory store

An external memory store is a persistent key-value or document store that the agent reads from and writes to using tools. The model does not passively receive this data — it actively chooses when to read and write.

```python
# Tool definitions the agent can call
tools = [
    {
        "name": "save_note",
        "description": "Save a note for later reference. Key must be unique.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["key", "content"]
        }
    },
    {
        "name": "load_note",
        "description": "Load a previously saved note by key.",
        "input_schema": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"]
        }
    }
]

# Implementation backed by local files or a SQLite database
import sqlite3

class ExternalMemoryStore:
    def __init__(self, db_path: str = "/tmp/agent-memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS notes (key TEXT PRIMARY KEY, content TEXT)")
        self.conn.commit()

    def save(self, key: str, content: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO notes (key, content) VALUES (?, ?)",
            (key, content)
        )
        self.conn.commit()

    def load(self, key: str) -> str | None:
        row = self.conn.execute("SELECT content FROM notes WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None
```

Strengths:
- Persistent across process restarts.
- Shareable across agents in a multi-agent system.
- Keeps the context window lean by moving data out of the message history.
- Auditable: you can inspect the store at any point.

Weaknesses:
- The agent must choose to save and load. If it forgets to save important information, it is lost from the store.
- The agent must know the key to retrieve a specific piece of information. Keys must be meaningful and consistent.
- Adds latency: each read and write is a tool call and a round trip through the model.
- The model can make errors in key naming, causing misses or overwrites.

When to use: multi-session tasks, tasks where intermediate results need to persist beyond a single run, multi-agent systems where agents need to share state, tasks where you want to decouple the agent's working memory from the API call cost.

## Vector recall

A vector store holds embeddings of text chunks. When the agent needs relevant past information, it sends a query, the store returns the top-k semantically similar chunks, and those chunks are injected into the current context.

```python
# Pseudocode using a generic vector store interface
from vector_store import VectorStore, embed

memory = VectorStore()

def remember(content: str, metadata: dict):
    embedding = embed(content)
    memory.upsert(embedding, content, metadata)

def recall(query: str, top_k: int = 5) -> list[str]:
    query_embedding = embed(query)
    results = memory.query(query_embedding, top_k=top_k)
    return [r.content for r in results]

# Tool definition
tools = [
    {
        "name": "recall_memory",
        "description": "Search for relevant past notes and findings by semantic similarity to a query string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }
]
```

Strengths:
- The agent does not need to remember exact keys. A natural-language query finds relevant content.
- Scales to large knowledge bases without filling the context window.
- Works well for retrieval over long-term accumulated experience.

Weaknesses:
- Requires an embedding model (additional API cost and latency) and a vector database (infrastructure cost).
- Recall is approximate. Semantically similar is not the same as logically relevant. The agent may retrieve misleading chunks.
- Metadata management (what was stored when, by which run) is important for avoiding stale or contradictory recalls.
- Poor fit for structured data. Use a key-value store for data you need exact matches on.

When to use: long-term agent memory across many sessions, retrieval over a large corpus of past experience, tasks where the agent needs to find relevant past work without knowing exactly what to look for.

## Handoff state

When one agent hands off to another, it must pass enough state for the receiving agent to continue without the full upstream context. The right approach depends on how much context is needed:

**Minimal handoff (structured summary)**

```python
# The handing-off agent produces a structured context object
handoff_context = {
    "task_description": "Analyze the revenue trends in Q1 2026.",
    "data_sources_used": ["revenue_q1.csv", "sales_breakdown.xlsx"],
    "findings_so_far": "Revenue grew 12% YoY. Decline in EMEA offset by APAC growth.",
    "next_step": "Identify the top three product lines driving APAC growth.",
}
```

**External state pointer**

```python
# The handing-off agent saves results to an external store
run_id = state.save_artifact("analysis_results.json", json.dumps(results))
handoff_context = {
    "task_description": "...",
    "artifacts_path": f"/tmp/agent-runs/{run_id}/analysis_results.json",
}
# The receiving agent reads the artifact when it needs it
```

**Full transcript (use sparingly)**

Passing the full upstream message history to the receiving agent is simple but expensive and risks context overflow. Only use this if the receiving agent genuinely needs to reason about the upstream conversation rather than just its outputs.

## Comparison summary

| Approach | Persistence | Sharing | Scale | Retrieval style | Cost |
|----------|------------|---------|-------|----------------|------|
| Conversation history | Session only | No | Context window limit | Direct (all visible) | Input tokens per turn |
| External store (key-value) | Persistent | Yes | Unlimited | Exact key lookup | Tool call overhead |
| Vector recall | Persistent | Yes | Unlimited | Semantic similarity | Embedding + query cost |

The right answer for most agents: start with conversation history. Add an external key-value store when you need persistence or cross-agent sharing. Add vector recall only when the knowledge base is large enough that exact-key retrieval is impractical.

Do not build all three into a system upfront. Add complexity incrementally as the task requirements make it necessary.
