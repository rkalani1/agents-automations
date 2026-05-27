# Agent Spec — Claude Code Coding Agent

## Job Statement

Given a repository and a task description from a human developer, propose or apply targeted code changes — including edits, new files, and test updates — within the approved edit scope defined in `CLAUDE.md`, without modifying secrets, CI/CD configuration, or files outside the approved directories.

## Inputs

| Field | Type | Description |
|---|---|---|
| `task_description` | string | A plain-language description of the coding task (e.g., "add pagination to the /users endpoint"). |
| `context_files` | list[path] | Optional list of specific files to read for context. |
| `target_branch` | string | The git branch to work on. Must not be `main` or `master` without explicit human approval. |

## Outputs

| Field | Type | Description |
|---|---|---|
| `proposed_changes` | list[diff] | Unified diffs of all proposed file edits. |
| `new_files` | list[path] | Paths of any new files created. |
| `shell_commands_run` | list[string] | Log of every shell command executed. |
| `test_results` | string | Output of any test runner invoked. |
| `open_questions` | list[string] | Clarifying questions for the human before finalizing. |

## Tools

See `TOOL_ALLOWLIST.md` for the complete list. Primary tools: `read_file`, `edit_file`, `create_file`, `bash` (restricted per `CLAUDE.md`). Web search is available but gated. For the full Claude Code tool model, see https://code.claude.com/docs/en/setup.

## Stop Conditions

- The agent stops and asks for human confirmation before applying edits to more than 10 files.
- The agent stops and reports an error if it encounters a file that matches a secret-containing pattern.
- The agent stops if a shell command would write outside the repository directory.
- The agent stops after 3 consecutive tool errors.
- The agent stops and escalates if the task description requests actions outside the permitted edit scope.

## Error Handling

| Error | Response |
|---|---|
| Attempted edit outside permitted scope | Refuse, explain the restriction, ask if human wants to update `CLAUDE.md` with approval. |
| Test failure after edit | Report the failure and proposed fix; do not auto-apply the fix without confirmation. |
| Secret detected in file | Flag the finding; do not display the secret value; stop processing the file. |
| Ambiguous instruction | Ask a clarifying question rather than guessing. |

## HITL Gates

- Gate 1: Human must confirm before the agent applies any stateful git operation (commit, push, branch creation).
- Gate 2: Human must confirm before edits affecting > 10 files are applied.
- Gate 3: Human must confirm before any network-connected shell command is run.
- Gate 4: Human must confirm before any edit to CI/CD configuration files, even if later added to permitted scope.

## Owner

`OWNER: REPLACE_WITH_TEAM_OR_PERSON`

## Review Cadence

- After each major task: Review `shell_commands_run` log for anomalies.
- Weekly: Spot-check five random session transcripts.
- Monthly: Re-review `CLAUDE.md` constraints against current repository structure.
- Quarterly: Re-run full red-team suite against a scratch repository.
- On incident: Follow `INCIDENT_RESPONSE.md`; update this spec with root-cause findings.

Reference: https://code.claude.com/docs/en/setup
