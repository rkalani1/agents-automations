# Agent Spec — OpenAI Agents SDK Python Service

## Job Statement

Given a sandbox directory of plain-text notes, use the OpenAI Agents SDK to read each file via a registered `read_notes` tool and produce a 300-500 word structured summary of key themes, decisions, and action items.

## Inputs

| Field | Type | Description |
|---|---|---|
| `sandbox_dir` | string (path) | Root sandbox directory. Default: `./sandbox/`. The agent reads from `sandbox_dir/notes/`. |
| `max_files` | integer | Maximum files to read. Default: 50. Range: 1-200. |
| `output_format` | enum | `markdown` or `plaintext`. Default: `markdown`. |

Validation:
- `sandbox_dir` must exist and be writable-by-none (read-only for the agent).
- All paths passed to `read_notes` are resolved and checked against `sandbox_dir` before the file is opened.
- `max_files` must be between 1 and 200 inclusive.

## Outputs

| Field | Type | Description |
|---|---|---|
| `summary` | string | Structured summary in the requested format. |
| `files_read` | integer | Number of files actually read. |
| `tokens_used` | integer | Approximate token count from the SDK's usage tracking. |
| `warnings` | list[string] | Non-fatal issues. |

## Tools

- `read_notes(path: str) -> str` — decorated with `@function_tool` from the `agents` package. Enforces sandbox boundary at the Python level before opening any file.

See `TOOL_ALLOWLIST.md` and `agent.py` for implementation. SDK reference: https://github.com/openai/openai-agents-python.

## Stop Conditions

- Agent stops after producing one summary output.
- Agent stops and exits with error if `OPENAI_API_KEY` is missing.
- Agent stops and exits with error if `sandbox_dir/notes/` is empty or missing.
- Agent stops if `read_notes` raises a `PermissionError` (path outside sandbox).
- Agent stops after 3 consecutive tool errors.

## Error Handling

| Error | Response |
|---|---|
| Missing API key | Exit immediately with a clear error message. |
| Sandbox notes dir missing | Exit with a clear error; print setup instructions. |
| Path outside sandbox | Raise PermissionError; abort the run and log the attempt. |
| File not found | Raise FileNotFoundError; log in warnings; continue. |
| Context overflow | Truncate file list to what fits; append truncation warning. |

## HITL Gates

- Gate 1: `OPERATOR_APPROVED_TO_RUN=1` must be set by a human before any live execution.
- Gate 2: A human must review the dry-run output before enabling live mode.
- Gate 3: For production deployments, a human must approve the `sandbox_dir` path before the first run.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- After each deploy: Run full eval suite against sandbox test data.
- Weekly: Spot-check 5 runs; review warning logs.
- Monthly: Re-pin `requirements.txt` dependencies and run `pip audit`.
- Quarterly: Re-run red-team suite; review sandbox path enforcement.
- On incident: Follow `INCIDENT_RESPONSE.md`.

Reference: https://github.com/openai/openai-agents-python
