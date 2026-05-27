> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [MCP SDK docs](https://modelcontextprotocol.io/docs/sdk)

# Writing Your Own MCP Server in Python

The [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) provides a high-level class called `FastMCP` that handles protocol negotiation, serialization, and transport so you can focus on writing tool logic. This page walks through a minimal server, explains the moving parts, and shows how to register it in Claude Desktop.

## Installing the SDK

Use either pip or uv. The `[cli]` extra gives you the `mcp` command-line tool for testing and installing servers:

```
pip install "mcp[cli]"
```

With uv (recommended for project isolation):

```
uv init my-mcp-server
cd my-mcp-server
uv add "mcp[cli]"
```

The SDK requires Python 3.10 or later.

## A minimal server

Create a file called `server.py`:

```python
from mcp.server.fastmcp import FastMCP

# Give the server a name. This appears in client UIs.
mcp = FastMCP("Greeter")

@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting for the given name.

    Args:
        name: The person to greet.
    """
    return f"Hello, {name}. This response came from a local MCP server."

if __name__ == "__main__":
    mcp.run()
```

That is a complete, working MCP server. The `@mcp.tool()` decorator:

1. Registers `greet` as a callable tool.
2. Uses the function's docstring as the tool description that the model sees.
3. Uses the function's type annotations and the `Args:` section of the docstring to generate the JSON Schema for the input parameter.
4. Returns the function's return value as the tool result.

When the model calls this tool, it will pass a JSON object like `{"name": "Alice"}`. The SDK unpacks it into the function's keyword arguments automatically.

## Running and testing locally

The `mcp dev` command starts the server with the MCP Inspector, a browser-based UI for testing tool calls without a full model:

```
mcp dev server.py
```

This runs the server in stdio mode and opens the inspector at `http://localhost:5173`. You can invoke `greet` directly, inspect the request and response JSON, and verify the server behaves as expected before connecting it to a model.

To run the server without the inspector:

```
python server.py
```

Or with uv:

```
uv run server.py
```

## Registering in Claude Desktop

Add an entry to `claude_desktop_config.json` pointing at your `server.py`. The key in `mcpServers` is the name that appears in the Claude Desktop UI:

```json
{
  "mcpServers": {
    "greeter": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

If you are using uv and want the server to run inside the project's virtual environment:

```json
{
  "mcpServers": {
    "greeter": {
      "command": "uv",
      "args": ["run", "--project", "/absolute/path/to/my-mcp-server", "python", "server.py"]
    }
  }
}
```

Use absolute paths. Claude Desktop launches the server from an indeterminate working directory, so relative paths will not resolve correctly.

Restart Claude Desktop after editing the config. Open a conversation and say "Greet Alice using the greeter tool." Claude should return the greeting string.

## Exposing a resource

Resources provide read-only data. Here is a server that exposes the contents of a text file as a resource alongside the greet tool:

```python
from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("Greeter")

@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}."

@mcp.resource("file://notes.txt")
def read_notes() -> str:
    """The contents of notes.txt in the project directory."""
    return Path("notes.txt").read_text()

if __name__ == "__main__":
    mcp.run()
```

The URI `file://notes.txt` is how clients request this resource. The function body can read from any source: a file, a database, an in-memory store.

## Exposing a prompt template

Prompts are reusable message templates:

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent

mcp = FastMCP("Greeter")

@mcp.prompt()
def greeting_prompt(name: str) -> list[PromptMessage]:
    """Generate a prompt that asks the model to write a formal letter greeting."""
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Write a formal one-sentence greeting addressed to {name}."
            )
        )
    ]

if __name__ == "__main__":
    mcp.run()
```

## Transport options

By default, `mcp.run()` uses stdio, which is correct for local servers registered in config files. For a remote server deployed behind HTTPS, use Streamable HTTP:

```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

This starts a Starlette ASGI app on `http://0.0.0.0:8000/mcp` by default. You can customize the port and path:

```python
mcp.settings.host = "0.0.0.0"
mcp.settings.port = 9000
mcp.settings.streamable_http_path = "/api/mcp"
mcp.run(transport="streamable-http")
```

The older SSE transport is still supported (`transport="sse"`) but is being superseded by Streamable HTTP in the [2025-06-18 spec](https://modelcontextprotocol.io/specification/2025-06-18). Prefer Streamable HTTP for new remote servers.

## Structured tool output

The 2025-06-18 spec added structured output for tools. If your tool returns a typed dataclass or Pydantic model, the SDK serializes it as a typed JSON result. Clients that support the new spec version can parse this directly; older clients receive an unstructured text fallback automatically.

```python
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Greeter")

@dataclass
class Greeting:
    message: str
    recipient: str

@mcp.tool()
def greet(name: str) -> Greeting:
    """Return a structured greeting."""
    return Greeting(message=f"Hello, {name}.", recipient=name)

if __name__ == "__main__":
    mcp.run()
```

Note: dataclasses must have type annotations on all fields for structured output to work. Classes without annotations fall back to unstructured text.

## Version notes

The Python SDK is versioned independently of the MCP spec. As of May 2026 the SDK is at v1.19.x (released October 2025). The `FastMCP` class was introduced relatively early and is the recommended authoring interface. The lower-level `Server` class from `mcp.server` is available for cases where you need full control over the protocol, but most use cases do not require it.

If you see import errors for `mcp.server.fastmcp`, upgrade the SDK:

```
pip install --upgrade "mcp[cli]"
```

The [SDK documentation](https://modelcontextprotocol.io/docs/sdk) lists all available language SDKs. TypeScript, C#, Go, Java, and Rust SDKs are also maintained by the MCP project with the same tier-1 or tier-2 support commitments.
