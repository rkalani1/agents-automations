# Launch Checklist — Gemini Antigravity Project Agent

Last verified: 2026-05-06. Platform drift risk: high — verify checklist items against current Antigravity docs before launch.

Complete every item before enabling this agent on production data. Items marked [BLOCKER] must be resolved.

---

## Scope

- [ ] [BLOCKER] Job statement in `AGENT_SPEC.md` is approved by the project owner.
- [ ] `notes_dir` is confirmed to contain only the intended data.
- [ ] Workspace path is scoped correctly in `antigravity.yaml` (see `PROJECT_README.md`).
- [ ] Out-of-scope use cases are documented and refused in `PROMPT.md`.
- [ ] A second engineer has reviewed the agent definition YAML.

## Tools and Permissions

- [ ] [BLOCKER] `read_file` is scoped to `notes_dir` only in the project manifest.
- [ ] `write_file` is either disabled or scoped to `data/outputs/` with HITL required.
- [ ] No shell, code interpreter, web search, or network tool is enabled.
- [ ] Tool permissions are verified against `TOOL_ALLOWLIST.md`.
- [ ] Tool scoping has been tested by attempting a read of a path outside `notes_dir`.

## Data

- [ ] Input data classification is documented.
- [ ] PII detection tested against eval-006.
- [ ] Data retention policy for summaries and logs is defined.
- [ ] No PHI or PCI data is present in the notes directory without authorization.

## Auth

- [ ] Google/Gemini API credentials are stored in a secrets manager, not in plaintext files.
- [ ] Credentials are scoped to the minimum required API access.
- [ ] Key rotation procedure is documented.
- [ ] Access to the Antigravity project is restricted to authorized team members.

## HITL

- [ ] [BLOCKER] All four HITL gates in `AGENT_SPEC.md` are implemented.
- [ ] Gate 1 (workspace approval) fires on first invocation in a new environment.
- [ ] Gate 2 (file count > 100) has been tested.
- [ ] Gate 3 (PII detection) tested with the escalation eval case (eval-006).
- [ ] Gate 4 (write_file) tested by attempting to write an output file.

## Logging

- [ ] Every invocation is logged with timestamp, `notes_dir`, `files_read`, `tokens_consumed`, `warnings`.
- [ ] Logs are shipped to a centralized store with retention >= 90 days.
- [ ] PII is not written to logs in plaintext.
- [ ] Log access is restricted to authorized personnel.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are committed to version control.
- [ ] A regression eval schedule is documented.

## Operations

- [ ] Kill-switch procedure in `INCIDENT_RESPONSE.md` is documented and tested.
- [ ] On-call contact is listed and reachable.
- [ ] Cost cap is configured with Google Cloud billing alerts.
- [ ] Platform changelog for Antigravity is monitored for breaking changes.

## People

- [ ] Owner in `AGENT_SPEC.md` is a real person or team.
- [ ] Security and privacy review sign-off is documented.
- [ ] Team members have read `INCIDENT_RESPONSE.md`.
- [ ] Review cadence is scheduled in the team calendar.
- [ ] "Last verified" dates in all kit files are updated before each launch.

Reference: https://codelabs.developers.google.com/getting-started-google-antigravity
