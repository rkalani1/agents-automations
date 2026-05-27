# Agent Spec — OpenAI Agents SDK TypeScript Service

## Job Statement

Given a sandbox directory of plain-text notes, use the OpenAI Agents SDK (`@openai/agents`) to read each file via a registered `read_notes` tool and produce a 300-500 word structured summary of key themes, decisions, and action items.

## Inputs

| Field | Type | Description |
|---|---|---|
| `sandboxDir` | string (path) | Root sandbox directory. Default: `./sandbox/`. Notes read from `sandboxDir/notes/`. |
| `maxFiles` | number | Maximum files to process. Default: 50. Range: 1-200. |
| `outputFormat` | string | `"markdown"` or `"plaintext"`. Default: `"markdown"`. |

Validation:
- `sandboxDir` must exist and be readable.
- All paths passed to `readNotes` are resolved and checked against `sandboxDir` before any `fs` call.
- `maxFiles` must be between 1 and 200 inclusive.

## Outputs

| Field | Type | Description |
|---|---|---|
| `summary` | string | Structured summary in the requested format. |
| `filesRead` | number | Count of files actually read. |
| `tokensUsed` | number | Approximate token count from SDK usage tracking. |
| `warnings` | string[] | Non-fatal issues. |

## Tools

- `read_notes(path: string) -> string` — defined in `agent.ts` with sandbox path enforcement. Registered via the `@openai/agents` tool registration API.

See `TOOL_ALLOWLIST.md` and `agent.ts`. SDK reference: https://github.com/openai/openai-agents-python (npm: `@openai/agents`).

## Stop Conditions

- Stop after producing one summary output.
- Stop and exit with error if `OPENAI_API_KEY` is missing.
- Stop and exit with error if `sandboxDir/notes/` is empty or missing.
- Stop if `readNotes` throws a path-outside-sandbox error.
- Stop after 3 consecutive tool errors.

## Error Handling

| Error | Response |
|---|---|
| Missing API key | Exit immediately with a clear error message. |
| Sandbox notes dir missing | Exit with clear error; print setup instructions. |
| Path outside sandbox | Throw error; abort run; log the attempt. |
| File not found | Log in warnings; continue. |
| Context overflow | Truncate file list; append truncation warning. |

## HITL Gates

- Gate 1: `OPERATOR_APPROVED_TO_RUN=1` must be set by a human before any live execution.
- Gate 2: Human must review the dry-run output before enabling live mode.
- Gate 3: For production deployments, human must approve `sandboxDir` before the first run.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- After each deploy: Run full eval suite.
- Weekly: Spot-check 5 runs; review warning logs.
- Monthly: Run `npm audit` against `package.json`.
- Quarterly: Re-run red-team suite; verify sandbox path enforcement with new test cases.
- On incident: Follow `INCIDENT_RESPONSE.md`.

Reference: https://github.com/openai/openai-agents-python
