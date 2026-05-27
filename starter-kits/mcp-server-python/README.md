# MCP Server — Python Starter Kit

## What This Kit Is

This starter kit provides a minimal Model Context Protocol (MCP) server implemented with the official MCP Python SDK. The server exposes one trivial `greet` tool as a working example. It is inert by default — the server does not start unless `OPERATOR_APPROVED_TO_RUN=1` is set in the launching environment. There is no stdio / pipe bypass: when an MCP client (e.g. Claude Desktop) auto-launches this server, the operator must add `OPERATOR_APPROVED_TO_RUN=1` to the client's `env` block for that server (see `server.py` docstring for a `claude_desktop_config.json` example).

MCP (Model Context Protocol) is an open standard for connecting AI models to external tools and data sources. The Python SDK is the reference implementation for building MCP servers in Python. Source and documentation are at https://github.com/modelcontextprotocol/python-sdk.

## Who This Kit Is For

- Python engineers building custom tool servers for MCP-compatible AI clients (Claude, Cursor, etc.).
- Teams who need a reviewed starting point before exposing custom tools to an AI agent.
- Security reviewers auditing the tool surface of an MCP server.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `server.py` | Inert MCP server. Exposes one `greet` tool. Starts only when `OPERATOR_APPROVED_TO_RUN=1` is set in the environment. |
| `requirements.txt` | Python dependencies. |
| `AGENT_SPEC.md` | Filled agent spec for the MCP server's tool surface. |
| `PROMPT.md` | System prompt for agents that consume this server. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list. |
| `INCIDENT_RESPONSE.md` | Incident response runbook. |

## How to Use

# Run: python server.py

1. Install dependencies: `pip install -r requirements.txt`
2. Review `server.py` to understand the tool surface.
3. Run in dry-run mode (no `OPERATOR_APPROVED_TO_RUN=1`) to see what would start.
4. Complete the launch checklist.
5. Set `OPERATOR_APPROVED_TO_RUN=1` and run `python server.py` to start the server.
6. Connect an MCP-compatible client (e.g., Claude Desktop) to the server's stdio transport.

## MCP Security Model

MCP servers run as local processes and communicate with AI clients over stdio or HTTP. The tools you expose become part of the agent's tool surface. Treat each tool registration as a security decision: a malicious prompt injection in the AI client could invoke any tool your server exposes. This is why the tool allowlist and red-team suite in this kit focus heavily on what the `greet` tool can and cannot do.

Reference: https://github.com/modelcontextprotocol/python-sdk

Field Guide:  /agent-builder-field-guide/
