# Universal Agent Spec — Starter Kit

## What This Kit Is

This is the vendor-neutral baseline starter kit from the Agents and Automations. It contains everything you need to define, evaluate, and safely operate a simple summarization agent before you write a single line of code. The agent task modeled here is: summarize a folder of plain-text notes into a one-pager. That task is intentionally narrow so that every field in the spec feels concrete and reachable.

This kit is not tied to any runtime, cloud provider, or orchestration framework. The files here translate directly into any platform — Claude Code, Codex CLI, OpenAI Agents SDK, LangChain, AutoGen, or a bare API call in a shell script.

## Who This Kit Is For

- Builders defining an agent for the first time who want a complete blueprint before choosing a platform.
- Team leads who need a reviewable artifact to socialize with security, legal, or product partners.
- Anyone who wants to stress-test their agent design against red-team scenarios before deployment.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. Overview, usage, and context. |
| `AGENT_SPEC.md` | Filled spec: job statement, I/O contracts, tools, stop conditions, error handling, HITL gates, owner, review cadence. |
| `PROMPT.md` | A complete system prompt ready to paste into any inference call. |
| `TOOL_ALLOWLIST.md` | Least-privilege enumeration of every tool the agent may use, with rationale. |
| `EVALS.jsonl` | Eight golden evaluation cases covering key behavioral categories. |
| `RED_TEAM_CASES.jsonl` | Eight adversarial test cases across nine attack classes. |
| `LAUNCH_CHECKLIST.md` | Pre-launch, launch-day, and post-launch task checklist tailored to this agent's risk profile. |
| `INCIDENT_RESPONSE.md` | Detect, contain, investigate, remediate, and communicate runbook. |

## How to Use

1. Read `AGENT_SPEC.md` first. Confirm every field makes sense for your context.
2. Adapt `PROMPT.md` for your target platform. The prompt is written in neutral language; add platform-specific header syntax as needed.
3. Review `TOOL_ALLOWLIST.md` and remove any tool that your deployment does not require.
4. Run every case in `EVALS.jsonl` against your implementation before going live.
5. Run every case in `RED_TEAM_CASES.jsonl` and confirm the agent produces the desired response.
6. Walk through `LAUNCH_CHECKLIST.md` with at least one other person.
7. File `INCIDENT_RESPONSE.md` somewhere your on-call team can reach it at 2 AM.

## Links

- Field Guide home:  /agents-and-automations/
- Platform-specific kits live alongside this one in the `starter-kits/` directory.

## A Note on Scope

This kit models a read-only, single-purpose agent. It reads files; it never writes them. If your agent needs write access, update `AGENT_SPEC.md` and `TOOL_ALLOWLIST.md` accordingly and re-run the full launch checklist before deploying.

