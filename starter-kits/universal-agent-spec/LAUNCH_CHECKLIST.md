# Launch Checklist — Universal Summarization Agent

Complete every item before promoting the agent to production. Items marked with [BLOCKER] must be resolved; others are strongly recommended.

---

## Scope

- [ ] [BLOCKER] Job statement is approved by the product owner and matches what is in `AGENT_SPEC.md`.
- [ ] Scope boundaries (read-only, sandbox-only) have been reviewed by at least one engineer who did not write the spec.
- [ ] All out-of-scope use cases are documented and explicitly refused in `PROMPT.md`.
- [ ] A clear non-goals list exists and has been communicated to stakeholders.

## Tools and Permissions

- [ ] [BLOCKER] Tool list in the platform's tool registry matches `TOOL_ALLOWLIST.md` exactly — no extra tools.
- [ ] `read_file` is scoped to the sandbox directory at the platform/runtime level, not just in the prompt.
- [ ] Symbolic link traversal outside the sandbox is blocked at the OS or runtime layer.
- [ ] No code interpreter, shell, or network tool is registered for this agent.
- [ ] Tool permissions have been reviewed by a security engineer.

## Data

- [ ] [BLOCKER] Input data classification is documented (e.g., internal-only, confidential).
- [ ] PII detection logic has been tested against the PII eval cases in `EVALS.jsonl`.
- [ ] Data retention policy for summaries and logs is defined and implemented.
- [ ] No production data was used during development or eval runs without authorization.

## Auth

- [ ] API key for the LLM provider is stored in a secrets manager, not in source code or environment files checked into version control.
- [ ] The API key is scoped to minimum required model access (no fine-tuning, no image generation, no admin endpoints).
- [ ] Key rotation procedure is documented.
- [ ] Access to the agent endpoint (if any) is authenticated and rate-limited.

## HITL

- [ ] [BLOCKER] All three HITL gates from `AGENT_SPEC.md` are implemented and tested.
- [ ] Gate 1 (sandbox directory approval) fires on first invocation in a new environment.
- [ ] Gate 2 (file count > 100) has been tested with a folder of 101 files.
- [ ] Gate 3 (PII detection) has been tested with the escalation eval case (eval-008).
- [ ] Human reviewer contact information is configured in the alerting system.

## Logging

- [ ] Every invocation is logged with: timestamp, `notes_dir` (sanitized), `files_read`, `tokens_consumed`, `warnings`.
- [ ] Logs are shipped to a centralized store with retention >= 90 days.
- [ ] PII is not written to logs in plaintext.
- [ ] Log access is restricted to authorized personnel.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass against the deployed agent.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are committed to version control alongside this checklist.
- [ ] A regression eval run is wired into CI (or documented as a manual step with a schedule).

## Operations

- [ ] Kill-switch procedure is documented in `INCIDENT_RESPONSE.md` and tested.
- [ ] On-call rotation or responsible-party contact is listed.
- [ ] Runbook for common failures (directory not found, context overflow) is published.
- [ ] Cost cap and alerting threshold are configured with the LLM provider.
- [ ] Rate limit behavior under load has been tested.

## People

- [ ] Owner field in `AGENT_SPEC.md` is set to a real person or team, not a placeholder.
- [ ] Security and privacy review sign-off is documented.
- [ ] Team members who will operate the agent have read `INCIDENT_RESPONSE.md`.
- [ ] Stakeholders have been notified of the launch date and rollback plan.
- [ ] Review cadence from `AGENT_SPEC.md` is scheduled in the team calendar.
