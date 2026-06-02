# Claude Code Agent — Starter Kit

## What This Kit Is

This starter kit configures a repo-aware coding agent that runs inside Claude Code, Anthropic's agentic coding environment. The agent reads a codebase, answers questions about it, and proposes or applies targeted edits within approved boundaries. It is scoped to a single repository and does not operate across multiple repos without explicit re-authorization.

Claude Code operates directly in your terminal and has access to the tools you grant it — including file editing, shell commands, and web search. This kit applies a principle of least-privilege configuration to reduce the risk of unintended edits, secrets leakage, or runaway shell execution. For Claude Code setup and tool-permission documentation, see the official setup guide at https://code.claude.com/docs/en/setup.

## Who This Kit Is For

- Engineers who want a guardrailed starting point for a Claude Code coding agent on a real repository.
- Team leads who need a reviewable security spec before enabling Claude Code in a shared or sensitive codebase.
- Security reviewers who want to audit the tool allowlist and HITL gates before sign-off.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `CLAUDE.md` | Claude Code memory file placed at the repo root. Constrains tool use and edit scope. |
| `AGENT_SPEC.md` | Filled agent spec: job statement, I/O, tools, stop conditions, HITL gates. |
| `PROMPT.md` | System-level instructions for the Claude Code session. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with per-tool rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list tailored to Claude Code's risk profile. |
| `INCIDENT_RESPONSE.md` | Detect / contain / investigate / remediate / communicate runbook. |

## How to Use

1. Copy `CLAUDE.md` to the root of your target repository. Claude Code reads this file automatically at session start. See https://code.claude.com/docs/en/setup for details on the `CLAUDE.md` convention.
2. Review and adapt `TOOL_ALLOWLIST.md`. Remove any tool your repository does not need.
3. Walk through `LAUNCH_CHECKLIST.md` with a second engineer before the first production session.
4. Run the eval cases in `EVALS.jsonl` against a scratch repository before enabling on production code.
5. Run the red-team cases in `RED_TEAM_CASES.jsonl` to verify refusal behavior.
6. File `INCIDENT_RESPONSE.md` where your on-call team can find it.

## A Note on Claude Code's Permission Model

Claude Code enforces tool permissions at the session level. Permissions you set in `CLAUDE.md` (such as denying shell access to production directories) are respected by the agent but are not a security boundary enforced by the OS. For sensitive repositories, pair `CLAUDE.md` constraints with OS-level file permissions and, where possible, run Claude Code in a container or sandbox environment.

Field Guide:  /agents-and-automations/
