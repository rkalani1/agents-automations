# OpenAI Agents SDK — Python Starter Kit

## What This Kit Is

This starter kit provides a guardrailed starting point for a Python service built with the OpenAI Agents SDK. The agent reads plain-text notes from a sandbox directory and produces a summary. It demonstrates the `@function_tool` decorator pattern for tool registration and applies sandbox path enforcement at the Python level.

The OpenAI Agents SDK is the official Python framework for building multi-step, tool-using agents on top of OpenAI models. It provides primitives for tool definition, agent orchestration, and guardrail attachment. Source and documentation are at https://github.com/openai/openai-agents-python.

## Who This Kit Is For

- Python engineers building a production agent service using the OpenAI Agents SDK.
- Teams who need a reviewable security spec and eval suite before shipping.
- Security reviewers auditing the tool allowlist, sandbox enforcement, and HITL gates.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `agent.py` | Inert example agent script. Exits unless `OPERATOR_APPROVED_TO_RUN=1`. |
| `requirements.txt` | Python dependencies with pinned versions. |
| `AGENT_SPEC.md` | Filled agent spec. |
| `PROMPT.md` | System prompt for the agent. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list. |
| `INCIDENT_RESPONSE.md` | Incident response runbook. |

## How to Use

1. Review `agent.py` — understand the sandbox enforcement and tool definition pattern.
2. Set `OPENAI_API_KEY` in your environment from a secrets manager. Never hardcode it.
3. Create a `./sandbox/notes/` directory and populate it with test notes.
4. Set `OPERATOR_APPROVED_TO_RUN=1` only after completing the launch checklist.
5. Run: `python agent.py`
6. Review the dry-run output (printed when `OPERATOR_APPROVED_TO_RUN` is not set) before enabling live mode.

## SDK Reference

- GitHub: https://github.com/openai/openai-agents-python
- Install: `pip install openai-agents`
- The SDK uses `@function_tool` from the `agents` package to register Python functions as tools available to the agent.

## Security Notes

- `agent.py` enforces sandbox path restrictions by resolving the real path and rejecting anything outside `./sandbox/`. This check must be present in production code — do not remove it.
- The API key is read from the environment. If it is missing, the script exits with a clear error. Never pass the key as a command-line argument.
- No network calls are made in the default inert mode.

Field Guide:  /agents-and-automations/
