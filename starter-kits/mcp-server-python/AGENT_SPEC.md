# Agent Spec — MCP Server (Python)

## Job Statement

Expose a minimal, single-tool MCP server that accepts a name string and returns a greeting, serving as a verified starting point for building more complex MCP tool servers.

## Inputs

| Field | Type | Description |
|---|---|---|
| `name` | string | The name to greet. Non-empty, <= 100 characters, no shell metacharacters. |

Validation (implemented in `server.py`):
- Must be a non-empty string.
- Must be <= 100 characters.
- Must not contain newlines, null bytes, semicolons, shell operators, or other injection-prone characters.

## Outputs

| Field | Type | Description |
|---|---|---|
| `greeting` | string | A greeting string: "Hello, {name}! Welcome." |
| `error` | string | An error message if input validation fails. |

## Tools Exposed

- `greet(name: str) -> str` — The only tool registered on this server. Input-validated. No side effects. No filesystem access. No network calls.

For the MCP tool registration model, see https://github.com/modelcontextprotocol/python-sdk.

## Stop Conditions

- The server exits if the MCP client disconnects (stdio transport closes).
- The server exits if an unhandled exception occurs in the main loop.
- The server does not expose a shutdown tool — the process is terminated by the client or the OS.

## Error Handling

| Error | Response |
|---|---|
| Empty name | Return error string: "Error: name must be a non-empty string." |
| Name too long | Return error string: "Error: name must be 100 characters or fewer." |
| Invalid characters | Return error string: "Error: name contains invalid characters." |
| Unhandled exception | Log to stderr; let the MCP client handle the error response. |

## HITL Gates

- Gate 1: `OPERATOR_APPROVED_TO_RUN=1` must be set in the launching environment before the server starts. There is no stdio/pipe bypass; MCP clients that auto-launch this server must include the variable in their `env` block (see `server.py` docstring for an example).
- Gate 2: Any new tool added to this server must be reviewed against the tool allowlist and launch checklist before deployment.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- Before any new tool is added: Full review of AGENT_SPEC, TOOL_ALLOWLIST, and launch checklist.
- Monthly: Run `pip audit` against `requirements.txt`.
- Quarterly: Re-run full red-team suite.
- On incident: Follow `INCIDENT_RESPONSE.md`.

Reference: https://github.com/modelcontextprotocol/python-sdk
