# Agent Spec — MCP Server (TypeScript)

## Job Statement

Expose a minimal, single-tool MCP server that accepts a name string and returns a greeting, serving as a verified starting point for building more complex MCP tool servers in TypeScript.

## Inputs

| Field | Type | Description |
|---|---|---|
| `name` | string | The name to greet. Non-empty, <= 100 characters, no shell metacharacters. |

Validation (implemented in `server.ts`):
- Must be a non-empty string.
- Must be <= 100 characters.
- Must not match the forbidden character regex: `/[\n\r\x00;<>&|`$(){}\[\]]/`.

## Outputs

| Field | Type | Description |
|---|---|---|
| `text` | string | "Hello, {name}! Welcome." on success. |
| `error` | string | Error message if input validation fails. |
| `isError` | boolean | Set to `true` in the MCP response when validation fails. |

## Tools Exposed

- `greet(name: string) -> string` — The only tool registered. Input-validated. No side effects. No filesystem access. No network calls.

For the MCP TypeScript SDK tool registration model, see https://github.com/modelcontextprotocol/typescript-sdk.

## Stop Conditions

- Server exits when the stdio transport closes (MCP client disconnects).
- Server exits on unhandled exception in the main async function.
- Server does not expose a shutdown tool.

## Error Handling

| Error | Response |
|---|---|
| Empty name | MCP error response: "Error: name must be a non-empty string." |
| Name too long | MCP error response: "Error: name must be 100 characters or fewer." |
| Invalid characters | MCP error response: "Error: name contains invalid characters." |
| Unknown tool name | MCP error response: "Error: Unknown tool '{name}'." |
| Unhandled exception | Log to stderr; process exits. |

## HITL Gates

- Gate 1: `OPERATOR_APPROVED_TO_RUN=1` must be set in the launching environment before the server starts. There is no stdio/pipe bypass; MCP clients that auto-launch this server must include the variable in their `env` block (see `server.ts` docstring for an example).
- Gate 2: Any new tool added must be reviewed against the tool allowlist and launch checklist.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- Before adding any new tool: Full review of AGENT_SPEC, TOOL_ALLOWLIST, and launch checklist.
- Monthly: Run `npm audit`.
- Quarterly: Re-run full red-team suite.
- On incident: Follow `INCIDENT_RESPONSE.md`.

Reference: https://github.com/modelcontextprotocol/typescript-sdk
