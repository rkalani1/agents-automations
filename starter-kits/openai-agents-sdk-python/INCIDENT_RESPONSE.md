# Incident Response Runbook — OpenAI Agents SDK Python Service

## Overview

This runbook covers the five phases of incident response for the Python Agents SDK service.

---

## 1. Detect

Signals that indicate a potential incident:

- `PermissionError` logged from `read_notes` (path traversal attempt detected).
- Agent produced a summary containing content from outside the sandbox.
- Agent returned content resembling secrets (API keys, tokens) in its output.
- Unexpected API cost spike in the OpenAI usage dashboard.
- A HITL gate fired but no reviewer responded within the SLA window.
- PII or PHI appeared in a summary output.
- Invocation rate anomaly (looping or abuse).

Monitoring:
- [ ] Alert on `PermissionError` in application logs.
- [ ] Alert on tokens_used > 2x the 30-day average per run.
- [ ] Alert on invocation rate > 5x the 30-day hourly average.
- [ ] OpenAI usage dashboard alert at 150% of expected daily spend.

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Revoke the `OPENAI_API_KEY` in the OpenAI dashboard (https://platform.openai.com/api-keys).
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all deployment environments.
   c. Restart or stop the agent process.
   d. Issue a new API key and store in the secrets manager.
2. If PII or PHI was exposed in output: restrict access to that output and notify the data-protection officer.
3. Preserve all logs from the incident window (do not rotate).
4. If the agent wrote files outside `sandbox/`: quarantine those files.

---

## 3. Investigate

Questions to answer:

- What exact input or note content triggered the incident?
- Did the sandbox path enforcement in `_safe_path()` fire? If not, why?
- Is the attack class documented in `RED_TEAM_CASES.jsonl`? If not, add it.
- Was `OPERATOR_APPROVED_TO_RUN=1` set without completing the full launch checklist?
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Patch `agent.py` (sandbox enforcement, error handling, or refusal logic).
- Update `PROMPT.md` if the system prompt had a gap.
- Add a new eval and red-team case for the attack class.
- Re-run the full eval suite and confirm all cases pass.
- Run `pip audit` against `requirements.txt` to check for new vulnerabilities.
- Re-issue `OPENAI_API_KEY` after rotation.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If PII or PHI was exposed: follow your organization's breach notification policy.
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agents-and-automations/
Reference: https://github.com/openai/openai-agents-python
