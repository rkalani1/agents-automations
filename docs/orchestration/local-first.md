> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [Connect local MCP servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

# Local-First Automation

Local-first automation is a design constraint, not a framework. It means: the agent uses only tools that run on the same machine as the agent, all state is stored locally, and no tool makes outbound calls to services that hold user accounts, credentials, or personal data.

This constraint deliberately limits capability in exchange for three properties: predictability, auditability, and safety. Every action the agent takes is visible on the local machine. No data leaves without an explicit network action that you have reviewed. The blast radius of a model error or prompt injection is bounded by what the local filesystem and local processes can affect.

Local-first is the right default for development, testing, and any automation that handles sensitive data. It is also the right permanent architecture for many production use cases that do not require remote services.

## The constraint set

A local-first agent satisfies all of these:

1. All MCP servers use stdio transport (no HTTP, no remote endpoints)
2. All tool outputs are written to local files or local databases, not sent to remote services
3. No tool calls external APIs that authenticate with user credentials
4. Environment variables supply any required configuration; no secrets are fetched from remote stores at runtime
5. Logs are written to local files, not shipped to external log aggregators
6. Network access, if any, is limited to read-only public endpoints (documentation, package registries)

## stdio MCP only

The stdio transport starts each MCP server as a local child process. Communication happens over standard input and output on the local machine. No network port is opened. No authentication token is required. The server process exits when the host process exits.

This is the transport used by `claude_desktop_config.json`. It is also the right transport for local agent scripts:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp/agent-workspace"],
    env=None,
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Use the session to call tools
            tools = await session.list_tools()
            result = await session.call_tool("read_file", {"path": "/tmp/agent-workspace/data.txt"})
            print(result)
```

The MCP server process is spawned by your code, runs locally, and is terminated when your `async with` block exits. Nothing touches the network.

## Local state management

Local-first agents store intermediate results on the filesystem. Use a dedicated working directory to keep agent outputs separate from other files:

```python
import os
import json
from pathlib import Path
from datetime import datetime

class LocalAgentState:
    def __init__(self, run_id: str, base_dir: str = "/tmp/agent-runs"):
        self.run_dir = Path(base_dir) / run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.run_dir / "actions.jsonl"

    def log_action(self, turn: int, tool: str, input_data: dict, result: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "turn": turn,
            "tool": tool,
            "input": input_data,
            "result_preview": result[:500],  # Truncate to keep logs manageable
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def save_artifact(self, name: str, content: str):
        artifact_path = self.run_dir / name
        artifact_path.write_text(content)
        return str(artifact_path)

    def load_artifact(self, name: str) -> str:
        return (self.run_dir / name).read_text()
```

Each agent run gets its own directory under `/tmp/agent-runs/<run_id>/`. Intermediate files, final outputs, and the action log are all written there. After the run, you can inspect every step without relying on the model's context window.

## Environment variables for configuration

Do not fetch secrets from remote services during an agent run. Supply all configuration as environment variables at process start time. This makes the agent's behavior reproducible from a known starting state:

```python
import os

def get_config() -> dict:
    required = ["OPENAI_API_KEY", "AGENT_MODEL"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")
    return {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model": os.environ["AGENT_MODEL"],
        "max_turns": int(os.environ.get("AGENT_MAX_TURNS", "20")),
        "workspace": os.environ.get("AGENT_WORKSPACE", "/tmp/agent-workspace"),
    }
```

This pattern works with `.env` files (via `python-dotenv`), with shell exports, and with secrets injected by CI/CD systems. The agent code never contains a literal secret.

## Local logging

Log to local files. Use structured logs (JSON lines) rather than plain text so you can parse and query them later:

```python
import logging
import json
from datetime import datetime

class JSONLineHandler(logging.Handler):
    def __init__(self, filepath: str):
        super().__init__()
        self._file = open(filepath, "a")

    def emit(self, record: logging.LogRecord):
        entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": self.format(record),
        }
        self._file.write(json.dumps(entry) + "\n")
        self._file.flush()

    def close(self):
        self._file.close()
        super().close()
```

Log the full input and output of every tool call. Log token counts. Log errors with the full stack trace. These logs are the only way to audit what the agent did without re-running it.

## What local-first precludes

Being explicit about the boundaries:

- No calls to email providers (Gmail, Outlook API), messaging platforms (Slack, Teams), or social networks
- No writes to cloud storage (S3, GCS, Dropbox) unless you explicitly opt out of the local-first constraint for a specific step
- No reads from SaaS APIs that authenticate with user OAuth tokens
- No browser automation against sites where the user is logged in (see [Operating boundaries](../browser-use/boundaries.md))
- No remote MCP connectors (HTTP transport with OAuth)

If a task requires any of these, it has left the local-first boundary. That is not a failure — many valuable automations require remote services. But it means you have accepted a different risk profile and should apply the corresponding safeguards from the [Security](../mcp/security.md) and [Operating boundaries](../browser-use/boundaries.md) pages.

## When local-first is not enough

Local-first is insufficient when:

- The task requires data that only exists in a remote service (a CRM, a ticketing system, a live data feed)
- The task requires writing outputs to a shared location (publishing a document, updating a shared database)
- The agent is part of a multi-user system where local state cannot be shared

In these cases, extend the architecture incrementally: add one remote tool at a time, document what data it can access, and apply authentication and authorization at each boundary.

## Example: local research pipeline

A local-first research agent that reads local files, runs web searches against public URLs, and writes findings to a local report:

```python
# All tools use local execution or public read-only endpoints
tools = [
    {
        "name": "read_local_file",
        "description": "Read a file from the local workspace.",
        # Backed by the local filesystem MCP server (stdio)
    },
    {
        "name": "search_web",
        "description": "Search the public web for information.",
        # Read-only. No authentication. No user account.
    },
    {
        "name": "write_local_file",
        "description": "Write text to a file in the local workspace.",
        # Writes only to the designated workspace directory.
    },
]

state = LocalAgentState(run_id="research-2026-05-06")
result = run_agent_loop(
    task="Summarize the three most recent papers on transformer efficiency from arXiv.",
    tools=tools,
    tool_executor=local_tool_executor,
    system="You are a research assistant. Store all notes and the final report in the local workspace.",
    max_turns=30,
)
state.save_artifact("report.md", result)
```

The agent reads local context, searches public web endpoints, and writes its outputs to local files. Nothing touches a user account. The entire run is reproducible from the starting state.
