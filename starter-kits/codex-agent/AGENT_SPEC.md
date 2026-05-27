# Agent Spec — Codex CLI Coding Agent

## Job Statement

Given a repository and a task description from a human developer, propose or apply targeted code changes — including edits, new files, and test updates — within the approved edit scope defined in `AGENTS.md`, without modifying secrets, CI/CD configuration, or files outside the approved directories.

## Inputs

| Field | Type | Description |
|---|---|---|
| `task_description` | string | Plain-language description of the coding task. |
| `context_files` | list[path] | Optional specific files to read for context. |
| `target_branch` | string | The git branch to work on. Must not be `main` or `master` without explicit human approval. |

Validation rules:
- `task_description` must be provided; the agent does not initiate work autonomously.
- `target_branch` defaults to the current branch; must not be a protected branch without HITL approval.

## Outputs

| Field | Type | Description |
|---|---|---|
| `proposed_changes` | list[diff] | Unified diffs of proposed edits. |
| `new_files` | list[path] | Paths of new files created. |
| `shell_commands_run` | list[string] | Log of every shell command executed. |
| `test_results` | string | Output of test runners invoked. |
| `open_questions` | list[string] | Clarifying questions for the human. |

## Tools

See `TOOL_ALLOWLIST.md` for the complete list. Primary tools: `read_file`, `edit_file`, `create_file`, `bash` (restricted per `AGENTS.md`). For the full Codex CLI tool model, see https://developers.openai.com/codex/cli.

## Stop Conditions

- Stop and request human confirmation before edits affecting > 10 files.
- Stop and report an error if a secret-matching file pattern is encountered.
- Stop if a shell command would write outside the repository directory.
- Stop after 3 consecutive tool errors.
- Stop and escalate if the task requests actions outside the permitted edit scope.

## Error Handling

| Error | Response |
|---|---|
| Edit outside permitted scope requested | Refuse, explain the restriction, ask if human wants to update `AGENTS.md`. |
| Test failure after edit | Report failure and propose fix; do not auto-apply without confirmation. |
| Secret detected in file | Flag the location; do not display secret value; stop processing the file. |
| Ambiguous instruction | Ask a clarifying question. |
| Network command requested | State the command, ask for confirmation, do not run autonomously. |

## HITL Gates

- Gate 1: Human must confirm before any stateful git operation (commit, push, branch creation).
- Gate 2: Human must confirm before edits affecting > 10 files.
- Gate 3: Human must confirm before any network-connected shell command.
- Gate 4: Human must confirm before any edit to CI/CD or infrastructure configuration files.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- After each major task: Review `shell_commands_run` log for anomalies.
- Weekly: Spot-check five random session transcripts.
- Monthly: Re-review `AGENTS.md` constraints against current repository structure.
- Quarterly: Re-run full red-team suite against a scratch repository.
- On incident: Follow `INCIDENT_RESPONSE.md`.

Reference: https://developers.openai.com/codex/cli
