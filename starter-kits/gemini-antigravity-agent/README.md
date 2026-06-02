# Gemini Antigravity Agent — Starter Kit

Last verified: 2026-05-06
Drift risk: high

## What This Kit Is

This starter kit configures a project agent built on Google's Antigravity platform, using Gemini as the underlying model. Antigravity is Google's agentic project execution environment, designed for multi-step tasks that span files, tools, and web resources within a structured project workspace.

The agent modeled here reads a project's documents and notes, answers questions about them, and produces summaries or structured outputs on demand. It is scoped to the project's designated workspace and does not operate across project boundaries without explicit re-authorization.

Because Antigravity is an actively developed platform with a high rate of change, verify the codelab and API documentation against the current state of the platform before deploying. See the official getting-started guide at https://codelabs.developers.google.com/getting-started-google-antigravity.

## Who This Kit Is For

- Engineers and product managers building project-scoped agents on the Antigravity platform.
- Teams who need a reviewable security spec before enabling an Antigravity agent in a shared workspace.
- Security reviewers auditing the tool allowlist and HITL gates.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `PROJECT_README.md` | Describes the Antigravity project layout and workspace structure. |
| `AGENT_SPEC.md` | Filled agent spec: job statement, I/O, tools, stop conditions, HITL gates. |
| `PROMPT.md` | System-level instructions for the Antigravity agent session. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with per-tool rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list tailored to Antigravity's risk profile. |
| `INCIDENT_RESPONSE.md` | Detect / contain / investigate / remediate / communicate runbook. |

## How to Use

1. Read `PROJECT_README.md` to understand the Antigravity project layout.
2. Review `AGENT_SPEC.md` and adapt job statement, inputs, and outputs for your project.
3. Adapt `PROMPT.md` for your Antigravity project's configuration.
4. Walk through `LAUNCH_CHECKLIST.md` before the first production session.
5. Run eval cases from `EVALS.jsonl` before enabling on production data.
6. Run red-team cases from `RED_TEAM_CASES.jsonl` to verify refusal behavior.

## Important Caveat on Platform Drift

Antigravity is a rapidly evolving Google platform. Tool names, configuration keys, and API shapes may have changed since this kit was last verified. Always cross-reference against the current codelab at https://codelabs.developers.google.com/getting-started-google-antigravity before deploying. The patterns in this kit (least-privilege tools, HITL gates, eval cases) remain valid regardless of API changes; the specific tool names and configuration syntax may need updating.

Field Guide:  /agents-and-automations/
