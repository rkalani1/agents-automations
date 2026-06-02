# Codex CLI Agent — Starter Kit

## What This Kit Is

This starter kit configures a repo-aware coding agent that runs inside the OpenAI Codex CLI. The agent reads a codebase, answers questions about it, and proposes targeted edits within approved boundaries. It is scoped to a single repository and operates in the terminal environment where Codex CLI is invoked.

Codex CLI is OpenAI's terminal-based coding assistant. It reads an `AGENTS.md` file from the repository root to understand task-specific instructions and constraints. For documentation on the CLI and its configuration model, see https://developers.openai.com/codex/cli.

## Who This Kit Is For

- Engineers who want a guardrailed starting point for a Codex CLI coding agent on a real repository.
- Team leads who need a reviewable security spec before enabling Codex CLI in a shared or sensitive codebase.
- Security reviewers who want to audit the tool allowlist and HITL gates before sign-off.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `AGENTS.md` | Codex CLI agent memory file. Constrains tool use and edit scope. Placed at repo root. |
| `AGENT_SPEC.md` | Filled agent spec: job statement, I/O, tools, stop conditions, HITL gates. |
| `PROMPT.md` | System-level instructions for the Codex CLI session. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with per-tool rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list tailored to Codex CLI's risk profile. |
| `INCIDENT_RESPONSE.md` | Detect / contain / investigate / remediate / communicate runbook. |

## How to Use

1. Copy `AGENTS.md` to the root of your target repository. Codex CLI reads this file automatically. See https://developers.openai.com/codex/cli for the `AGENTS.md` convention.
2. Review and adapt `TOOL_ALLOWLIST.md`. Remove tools your repository does not need.
3. Walk through `LAUNCH_CHECKLIST.md` with a second engineer before the first production session.
4. Run all eval cases from `EVALS.jsonl` on a scratch repository before production use.
5. Run all red-team cases from `RED_TEAM_CASES.jsonl` to verify refusal behavior.
6. File `INCIDENT_RESPONSE.md` where your on-call team can access it.

## A Note on Codex CLI's Execution Model

Codex CLI executes in your local terminal environment. It has access to your filesystem and can run shell commands unless explicitly restricted. This means the `AGENTS.md` constraints and this kit's tool allowlist are behavioral guardrails enforced by the model, not by the OS. For sensitive repositories, run Codex CLI in a container or virtual machine where filesystem access and network egress are restricted at the infrastructure level.

Field Guide:  /agents-and-automations/
Reference: https://developers.openai.com/codex/cli
