# Agent Spec — Gemini Antigravity Project Agent

Last verified: 2026-05-06
Drift risk: high

## Job Statement

Given a project workspace containing plain-text notes and documents, produce a structured summary of key themes, decisions, and action items without adding information not present in the source files.

## Inputs

| Field | Type | Description |
|---|---|---|
| `notes_dir` | string (path) | Path to the notes subdirectory within the project workspace (e.g., `data/notes/`). |
| `max_files` | integer | Maximum number of files to read. Default: 50. Range: 1-200. |
| `output_format` | enum | `markdown` or `plaintext`. Default: `markdown`. |

Validation:
- `notes_dir` must resolve inside the project workspace directory.
- `notes_dir` must not escape the workspace via path traversal or symlinks.

## Outputs

| Field | Type | Description |
|---|---|---|
| `summary` | string | Structured summary (300-500 words) in the requested format. |
| `files_read` | integer | Count of files read. |
| `tokens_consumed` | integer | Approximate token count for cost tracking. |
| `warnings` | list[string] | Non-fatal issues (e.g., skipped binary files, PII detections). |

## Tools

See `TOOL_ALLOWLIST.md`. Primary tool: `read_file` scoped to `notes_dir`. Optionally `write_file` scoped to `data/outputs/` if output persistence is needed (requires HITL gate). For current Antigravity tool definitions, see https://codelabs.developers.google.com/getting-started-google-antigravity.

## Stop Conditions

- Stop after producing one summary output.
- Stop and escalate if `notes_dir` resolves outside the project workspace.
- Stop and report an error if no readable files are found.
- Stop after 3 consecutive tool errors.
- Stop if total input tokens would exceed the Gemini model's context window.

## Error Handling

| Error | Response |
|---|---|
| Directory not found | Return structured error; do not hallucinate a summary. |
| File read denied | Log in `warnings`; continue with remaining files. |
| Context overflow | Summarize files processed so far; append truncation warning. |
| PII detected | Omit the PII, add warning, trigger HITL Gate 3. |

## HITL Gates

- Gate 1: Human must approve `notes_dir` before first invocation in a new environment.
- Gate 2: If `files_read` > 100, pause and request human confirmation.
- Gate 3: If any file contains apparent PII, pause before including that file.
- Gate 4: If `write_file` is used, human must confirm the output path before writing.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- Weekly: Spot-check 5 random runs against eval cases.
- Monthly: Re-run full eval suite; review warning patterns.
- Quarterly: Re-assess tool allowlist and HITL gates. Re-verify against current Antigravity docs.
- On incident: Follow `INCIDENT_RESPONSE.md`.

Reference: https://codelabs.developers.google.com/getting-started-google-antigravity
