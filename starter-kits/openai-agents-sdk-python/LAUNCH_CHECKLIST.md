# Launch Checklist — OpenAI Agents SDK Python Service

Complete every item before setting `OPERATOR_APPROVED_TO_RUN=1` in a production environment.

---

## Scope

- [ ] [BLOCKER] Job statement in `AGENT_SPEC.md` is approved by the product owner.
- [ ] Sandbox directory path is confirmed and contains only the intended input data.
- [ ] All out-of-scope use cases are refused in `PROMPT.md`.
- [ ] A second engineer has reviewed `agent.py` and agrees with the sandbox enforcement logic.

## Tools and Permissions

- [ ] [BLOCKER] Only `read_notes` is registered in the `Agent` constructor's `tools=` parameter.
- [ ] No `WebSearchTool`, `FileSearchTool`, or `CodeInterpreterTool` is registered.
- [ ] Sandbox path enforcement in `_safe_path()` has been tested with path traversal inputs.
- [ ] Binary file handling is tested (agent skips non-text files gracefully).
- [ ] `requirements.txt` has been audited with `pip audit` for known vulnerabilities.

## Data

- [ ] Input notes are classified (e.g., internal-only, confidential) and the agent's access level matches.
- [ ] No PHI or PCI data is in `sandbox/notes/` without explicit authorization.
- [ ] PII detection tested with eval-006 (escalation case).
- [ ] Data retention policy for summary outputs and logs is defined.

## Auth

- [ ] [BLOCKER] `OPENAI_API_KEY` is stored in a secrets manager or environment variable injected by the deployment system — not hardcoded in `agent.py` or any config file.
- [ ] API key is scoped to the minimum required model access.
- [ ] Key rotation procedure is documented.
- [ ] No API key appears in version control, logs, or printed output.

## HITL

- [ ] [BLOCKER] `OPERATOR_APPROVED_TO_RUN=1` is only set after completing this checklist.
- [ ] Dry-run output has been reviewed by a human before enabling live mode.
- [ ] Gate 3 (PII detection) tested with escalation eval case.
- [ ] Human reviewer contact is configured in the alerting system.

## Logging

- [ ] Every invocation logs: timestamp, files_read, tokens_used, warnings.
- [ ] Logs do not contain PII or the contents of the OPENAI_API_KEY.
- [ ] Logs are shipped to a centralized store with retention >= 90 days.
- [ ] Log access is restricted to authorized personnel.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass against the deployed agent.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are committed to version control.
- [ ] CI pipeline runs eval suite on every pull request.

## Operations

- [ ] Kill-switch procedure in `INCIDENT_RESPONSE.md` is documented and rehearsed.
- [ ] On-call contact is listed and reachable.
- [ ] Cost cap is configured in the OpenAI usage dashboard.
- [ ] Rate limiting and retry logic are implemented and tested.
- [ ] Virtual environment is isolated from global Python packages.

## People

- [ ] Owner in `AGENT_SPEC.md` is a real person or team.
- [ ] Security review sign-off is documented.
- [ ] All engineers who will operate the service have read `INCIDENT_RESPONSE.md`.
- [ ] Review cadence is scheduled in the team calendar.

Reference: https://github.com/openai/openai-agents-python
