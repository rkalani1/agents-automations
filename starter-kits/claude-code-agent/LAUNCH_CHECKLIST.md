# Launch Checklist — Claude Code Coding Agent

Complete every item before using this agent on a production or shared repository. Items marked [BLOCKER] must be resolved.

---

## Scope

- [ ] [BLOCKER] `CLAUDE.md` is committed to the root of the target repository.
- [ ] Permitted edit directories (`src/`, `tests/`, `docs/`) match the actual project structure.
- [ ] Secret-file patterns in `CLAUDE.md` cover all sensitive file types in this repo (.env, *.key, *.pem, etc.).
- [ ] Out-of-scope directories (CI/CD configs, infrastructure-as-code) are explicitly listed in `CLAUDE.md` as forbidden.
- [ ] A second engineer has reviewed `CLAUDE.md` and agrees with all constraints.

## Tools and Permissions

- [ ] [BLOCKER] Only tools in `TOOL_ALLOWLIST.md` are active in the Claude Code session.
- [ ] Claude Code session settings have been confirmed to match this allowlist (see https://code.claude.com/docs/en/setup).
- [ ] Web search is gated to human-initiated requests only.
- [ ] Shell command allowlist in `CLAUDE.md` matches the project's actual toolchain.
- [ ] Destructive git commands (reset, push, force-push) are not in the permitted shell subset.

## Data

- [ ] The repository does not contain unencrypted secrets. If it does, that is a separate security finding to resolve first.
- [ ] Session transcripts (if stored) are treated as confidential and not shared outside the team.
- [ ] No production database credentials or API keys are present in the working directory.
- [ ] Data classification of the codebase is documented and the agent's access level matches it.

## Auth

- [ ] The Anthropic API key used by Claude Code is stored in a secrets manager or OS keychain, not in a plaintext file.
- [ ] The API key has only the permissions needed for Claude Code (no admin, billing, or org-management scopes).
- [ ] Key rotation procedure is documented.
- [ ] Multi-factor authentication is enabled on the Anthropic account.

## HITL

- [ ] [BLOCKER] All four HITL gates in `AGENT_SPEC.md` are documented and understood by all users.
- [ ] Gate 1 (git operations) has been tested by attempting a git commit and confirming the agent pauses.
- [ ] Gate 2 (> 10 files) has been tested by requesting a large refactor.
- [ ] Gate 3 (network-connected commands) has been tested by requesting a curl command.
- [ ] Gate 4 (CI/CD edits) has been tested by requesting an edit to a workflow file.

## Logging

- [ ] Claude Code session transcripts are saved for audit purposes.
- [ ] `shell_commands_run` log is reviewed after each session.
- [ ] A log retention and access policy is defined.
- [ ] Alerts are configured for anomalous session lengths or unusual command patterns.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` produce the expected behavior on a scratch repository.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are documented alongside this checklist.
- [ ] A plan exists to re-run evals after any change to `CLAUDE.md` or this agent's prompt.

## Operations

- [ ] Kill-switch procedure is documented in `INCIDENT_RESPONSE.md` and has been rehearsed.
- [ ] On-call contact for this agent is listed and reachable.
- [ ] Rollback plan (git revert or branch deletion) is documented for unintended edits.
- [ ] Cost monitoring is configured with the LLM provider.

## People

- [ ] Owner field in `AGENT_SPEC.md` is set to a real person or team.
- [ ] All engineers who will use the agent have read `CLAUDE.md` and `INCIDENT_RESPONSE.md`.
- [ ] Security review sign-off is documented.
- [ ] Review cadence from `AGENT_SPEC.md` is scheduled in the team calendar.
- [ ] New team members are briefed on the agent's constraints before their first session.

Reference: https://code.claude.com/docs/en/setup
