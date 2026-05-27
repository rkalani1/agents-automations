# Agent Spec — Local Script Agent

## Job Statement

Read a folder of plain-text notes from a local sandbox directory and produce a 300-500 word structured summary via a single OpenAI chat completions API call, writing the output to a sandbox output file.

## Inputs

| Field | Type | Description |
|---|---|---|
| `NOTES_DIR` | path | `./sandbox/notes/` — hardcoded in `script.py`. |
| `MAX_FILES` | integer | Maximum files to read. Default: 50. |
| `OPENAI_API_KEY` | env var | Read from environment. Script exits if missing. |
| `OPERATOR_APPROVED_TO_RUN` | env var | Must be `"1"` for live execution. |

Validation:
- `NOTES_DIR` must exist and be inside `./sandbox/`.
- All file reads are checked against the sandbox boundary in `safe_read()`.

## Outputs

| Field | Type | Description |
|---|---|---|
| `summary` | string | 300-500 word markdown summary. Printed to stdout. |
| `output_file` | path | `./sandbox/output/summary.md` — written after the API call. |
| `warnings` | list[string] | Non-fatal issues printed to stderr. |

## Tools

This agent uses no agentic tool-call loop. It makes one HTTP call to the OpenAI chat completions endpoint using the model named in `OPENAI_MODEL`. File reads are performed by the Python script directly, not by the model.

## Stop Conditions

- Script exits if `OPERATOR_APPROVED_TO_RUN != "1"`.
- Script exits if `OPENAI_API_KEY` is missing.
- Script exits if `./sandbox/notes/` is empty or missing.
- Script raises `PermissionError` and skips any file resolving outside the sandbox.

## Error Handling

| Error | Response |
|---|---|
| Missing API key | Exit immediately with clear error. |
| Notes dir missing | Exit with clear error and setup instructions. |
| File outside sandbox | Log warning; skip file; continue. |
| API error | Let the openai library raise; print error to stderr; exit non-zero. |
| Context too large | openai library raises; consider reducing MAX_FILES. |

## HITL Gates

- Gate 1: `OPERATOR_APPROVED_TO_RUN=1` must be set by a human before any live execution.
- Gate 2: Dry-run output must be reviewed by a human before enabling live mode.
- Gate 3: Cron scheduling (if ever enabled) requires explicit sign-off on the crontab entry and completion of the full launch checklist. The commented-out example in `script.py` is labeled "manual-only example."

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- After each run: Review output for quality and any warnings.
- Weekly: Spot-check 5 runs.
- Monthly: Run `pip audit`; re-pin dependencies.
- Quarterly: Re-run red-team suite.
- On incident: Follow `INCIDENT_RESPONSE.md`.
