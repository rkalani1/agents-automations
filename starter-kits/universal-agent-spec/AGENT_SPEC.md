# Agent Spec — Universal Summarization Agent

## Job Statement

Given a folder of plain-text notes, produce a single-page summary (300-500 words) that captures the key themes, decisions, and open questions without adding information that is not present in the source files.

## Inputs

| Field | Type | Description |
|---|---|---|
| `notes_dir` | string (path) | Absolute or relative path to the folder containing `.txt` or `.md` files. |
| `max_files` | integer | Maximum number of files to read. Default: 50. |
| `output_format` | enum | `markdown` or `plaintext`. Default: `markdown`. |

Validation rules:
- `notes_dir` must exist and be readable.
- `notes_dir` must not resolve outside a pre-approved sandbox directory.
- `max_files` must be between 1 and 200 inclusive.

## Outputs

| Field | Type | Description |
|---|---|---|
| `summary` | string | The one-pager text in the requested format. |
| `files_read` | integer | Count of files actually read. |
| `tokens_consumed` | integer | Approximate token count for cost tracking. |
| `warnings` | list[string] | Non-fatal issues (e.g., skipped binary files). |

## Tools

The agent is permitted to use exactly one tool: `read_file(path)`. See `TOOL_ALLOWLIST.md` for rationale and restrictions.

## Stop Conditions

- The agent stops after producing one summary output.
- The agent stops and escalates if `notes_dir` resolves to a path outside the approved sandbox.
- The agent stops and reports an error if no readable `.txt` or `.md` files are found.
- The agent stops after 3 consecutive tool errors.
- The agent stops if total input tokens would exceed the model's context window.

## Error Handling

| Error | Response |
|---|---|
| Directory not found | Return a structured error; do not hallucinate a summary. |
| File read permission denied | Log the file path in `warnings`; continue with remaining files. |
| Context window exceeded | Summarize files processed so far; include a warning that input was truncated. |
| Output exceeds 500 words | Truncate to 500 words and append `[truncated]`. |

## HITL Gates

- Gate 1: A human must approve `notes_dir` before the agent is invoked for the first time in a new environment.
- Gate 2: If `files_read` exceeds 100, pause and ask a human to confirm before continuing.
- Gate 3: If any file contains apparent PII (email addresses, phone numbers, SSNs), pause and ask a human before including that file in the summary.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- Weekly: Spot-check 5 random runs against the golden eval cases in `EVALS.jsonl`.
- Monthly: Re-run full eval suite; review any new warning patterns in logs.
- Quarterly: Re-assess tool allowlist and HITL gates against current threat model.
- On incident: Follow `INCIDENT_RESPONSE.md`; update this spec with root-cause findings.
