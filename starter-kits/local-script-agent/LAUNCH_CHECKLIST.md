# Launch Checklist — Local Script Agent

Complete every item before setting `OPERATOR_APPROVED_TO_RUN=1` in any environment. Items marked [BLOCKER] must be resolved.

---

## Scope

- [ ] [BLOCKER] Job statement in `AGENT_SPEC.md` is approved by the product owner.
- [ ] `./sandbox/notes/` contains only the intended input data.
- [ ] Output path `./sandbox/output/` is writable by the script user.
- [ ] Out-of-scope use cases are documented and refused in `PROMPT.md`.
- [ ] A second engineer has reviewed `script.py` and agrees with the sandbox enforcement.

## Tools and Permissions

- [ ] [BLOCKER] `safe_read()` is present and untouched in `script.py`.
- [ ] `safe_read()` tested with path traversal inputs (e.g., `../../etc/passwd`).
- [ ] No tools are passed to the `client.chat.completions.create()` call.
- [ ] Script does not execute any subprocess or shell commands.
- [ ] `pip audit` has been run with no high or critical findings.
- [ ] Dependencies pinned to specific versions in `requirements.txt` for production.

## Data

- [ ] Input notes are classified (e.g., internal-only, confidential).
- [ ] No PHI or PCI data is in `./sandbox/notes/` without explicit authorization.
- [ ] PII detection tested with eval-006 (escalation case).
- [ ] Data retention policy for `./sandbox/output/summary.md` is defined.

## Auth

- [ ] [BLOCKER] `OPENAI_API_KEY` is stored in a secrets manager or environment injected by the deployment system — not hardcoded in `script.py` or committed to version control.
- [ ] API key is scoped to the minimum required model access.
- [ ] Key rotation procedure is documented.
- [ ] API key does not appear in any log file, printed output, or error message.

## HITL

- [ ] [BLOCKER] `OPERATOR_APPROVED_TO_RUN=1` is only set after completing this checklist.
- [ ] Dry-run output has been reviewed by a human before enabling live mode.
- [ ] Gate 3: Any cron job scheduling this script requires sign-off on the crontab entry. The commented-out example in `script.py` is labeled "manual-only example" and must not be uncommented without completing this checklist.

## Logging

- [ ] Script output (stdout and stderr) is redirected to a log file in production.
- [ ] Log file is not world-readable.
- [ ] Log does not contain the full note contents if they could include PII.
- [ ] Log retention policy is defined (rotate after N days).

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are committed to version control.
- [ ] Plan to re-run evals after any change to `PROMPT.md` or `script.py`.

## Operations

- [ ] Kill-switch procedure in `INCIDENT_RESPONSE.md` is documented and rehearsed.
- [ ] On-call contact is listed.
- [ ] Cost monitoring is configured in the OpenAI usage dashboard.
- [ ] Virtual environment is isolated from global Python packages.
- [ ] Cron scheduling (if planned) has been explicitly authorized and documented.

## People

- [ ] Owner in `AGENT_SPEC.md` is a real person or team.
- [ ] Security review sign-off is documented.
- [ ] All engineers who run the script have read `INCIDENT_RESPONSE.md`.
- [ ] Review cadence is scheduled.

Field Guide:  /agents-automations/
