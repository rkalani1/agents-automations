# OpenAI Agents SDK — TypeScript Starter Kit

## What This Kit Is

This starter kit provides a guardrailed starting point for a TypeScript service built with the OpenAI Agents SDK. The agent reads plain-text notes from a sandbox directory and produces a summary. It demonstrates the tool definition pattern from the `@openai/agents` package and applies sandbox path enforcement at the Node.js level.

The `@openai/agents` package is the official TypeScript/JavaScript SDK for building multi-step, tool-using agents on top of OpenAI models. For source, installation, and API reference, see https://github.com/openai/openai-agents-python (the TypeScript SDK ships as `@openai/agents` on npm; verify the current npm package name against the repository before installing).

## Who This Kit Is For

- TypeScript/Node.js engineers building a production agent service with the OpenAI Agents SDK.
- Teams who need a reviewable security spec and eval suite before shipping.
- Security reviewers auditing sandbox enforcement, tool allowlist, and HITL gates.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `agent.ts` | Inert example agent script. Exits unless `OPERATOR_APPROVED_TO_RUN=1`. |
| `package.json` | NPM dependencies and scripts. |
| `tsconfig.json` | TypeScript compiler configuration. |
| `AGENT_SPEC.md` | Filled agent spec. |
| `PROMPT.md` | System prompt for the agent. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list. |
| `INCIDENT_RESPONSE.md` | Incident response runbook. |

## How to Use

1. Run `npm install` to install dependencies.
2. Set `OPENAI_API_KEY` in your environment from a secrets manager. Never hardcode it.
3. Create a `./sandbox/notes/` directory and add `.txt` note files.
4. Run `npx ts-node agent.ts` (without `OPERATOR_APPROVED_TO_RUN=1`) to see the dry-run output.
5. Complete the launch checklist.
6. Set `OPERATOR_APPROVED_TO_RUN=1` and run again for live execution.

## Security Notes

- `agent.ts` enforces sandbox path restrictions by resolving the real path with `path.resolve()` and rejecting anything outside `./sandbox/`.
- The API key is read from `process.env.OPENAI_API_KEY`. The script exits with a clear error if it is missing.
- No network calls are made in the default inert mode.

Field Guide:  /agents-automations/
