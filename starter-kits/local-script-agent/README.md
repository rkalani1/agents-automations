# Local Script Agent — Starter Kit

## What This Kit Is

This starter kit configures a local Python script agent: a single-file Python script that calls an LLM API to summarize a folder of notes. It is the simplest possible agent deployment — no frameworks, no orchestration layer, just a Python script you can read end-to-end in five minutes.

This kit is the reference implementation for the local-scripts platform described in `docs/platforms/local-scripts.md` of the Agents and Automations.

The script is inert by default. It exits immediately unless `OPERATOR_APPROVED_TO_RUN=1` is set, and it prints a dry-run description of what it would do before doing anything.

## Who This Kit Is For

- Developers who want to understand agent mechanics without a framework abstraction.
- Teams building lightweight automation that does not justify a full service deployment.
- Engineers who need a fully auditable, dependency-minimal starting point.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `script.py` | Inert local agent script. Gated by `OPERATOR_APPROVED_TO_RUN=1`. |
| `requirements.txt` | Python dependencies. |
| `AGENT_SPEC.md` | Filled agent spec. |
| `PROMPT.md` | System prompt used in the script's API call. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list. |
| `INCIDENT_RESPONSE.md` | Incident response runbook. |

## How to Use

1. Install dependencies: `pip install -r requirements.txt`
2. Set `OPENAI_API_KEY` in your environment from a secrets manager.
3. Create `./sandbox/notes/` and add `.txt` files.
4. Run `python script.py` without `OPERATOR_APPROVED_TO_RUN=1` to see the dry-run.
5. Complete the launch checklist.
6. Run: `OPERATOR_APPROVED_TO_RUN=1 python script.py`

## Scheduling

This script can be scheduled with cron, but NEVER enable a cron job without first completing the full launch checklist. A commented-out example crontab line is included in `script.py` for reference only.

Field Guide:  /agents-and-automations/

