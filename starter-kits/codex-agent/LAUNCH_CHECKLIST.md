# Launch Checklist — Codex CLI Coding Agent

Complete every item before using this agent on a production or shared repository. Items marked [BLOCKER] must be resolved.

---

## Scope

- [ ] [BLOCKER] `AGENTS.md` is committed to the root of the target repository.
- [ ] Permitted edit directories match the actual project structure.
- [ ] Secret-file patterns in `AGENTS.md` cover all sensitive file types in this repo.
- [ ] CI/CD and infrastructure files are explicitly listed as forbidden in `AGENTS.md`.
- [ ] A second engineer has reviewed `AGENTS.md` and agrees with all constraints.
- [ ] Non-goals are documented and communicated to all users of the agent.

## Tools and Permissions

- [ ] [BLOCKER] Only tools listed in `TOOL_ALLOWLIST.md` are used by the agent.
- [ ] Shell command allowlist in `AGENTS.md` matches the project's actual toolchain.
- [ ] Destructive git operations are not in the permitted shell subset.
- [ ] Network-connected commands require explicit human confirmation.
- [ ] If running in a container, filesystem and network restrictions are verified.

## Data

- [ ] Repository does not contain unencrypted committed secrets. (Resolve first if it does.)
- [ ] Session transcripts are treated as confidential and stored securely.
- [ ] No production credentials are present in the working directory.
- [ ] Data classification of the codebase is documented.

## Auth

- [ ] The OpenAI API key used by Codex CLI is stored in a secrets manager or OS keychain, not in a dotfile committed to version control.
- [ ] The API key is scoped to the minimum required capabilities.
- [ ] Key rotation procedure is documented.
- [ ] Multi-factor authentication is enabled on the OpenAI account.

## HITL

- [ ] [BLOCKER] All four HITL gates in `AGENT_SPEC.md` are understood by all users.
- [ ] Gate 1 (git operations) tested by attempting git commit without confirmation.
- [ ] Gate 2 (> 10 files) tested by requesting a large-scope change.
- [ ] Gate 3 (network commands) tested by requesting a curl command.
- [ ] Gate 4 (CI/CD edits) tested by requesting a workflow file change.

## Logging

- [ ] Session transcripts are saved for audit purposes.
- [ ] `shell_commands_run` log is reviewed after every session.
- [ ] Log retention and access policy is defined.
- [ ] Alerts are configured for anomalous session length or command patterns.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass on a scratch repository.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are documented.
- [ ] A plan exists to re-run evals after changes to `AGENTS.md` or the system prompt.

## Operations

- [ ] Kill-switch procedure in `INCIDENT_RESPONSE.md` is documented and rehearsed.
- [ ] On-call contact for this agent is listed and reachable.
- [ ] Rollback plan (git revert) for unintended edits is documented.
- [ ] Cost monitoring is configured with the OpenAI dashboard.

## People

- [ ] Owner in `AGENT_SPEC.md` is a real person or team.
- [ ] All engineers using the agent have read `AGENTS.md` and `INCIDENT_RESPONSE.md`.
- [ ] Security review sign-off is documented.
- [ ] Review cadence is scheduled in the team calendar.

Reference: https://developers.openai.com/codex/cli
