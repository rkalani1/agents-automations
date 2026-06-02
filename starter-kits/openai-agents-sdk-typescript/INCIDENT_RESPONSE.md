# Incident Response Runbook — OpenAI Agents SDK TypeScript Service

## Overview

This runbook covers the five phases of incident response for the TypeScript Agents SDK service.

---

## 1. Detect

Signals that indicate a potential incident:

- Path-outside-sandbox error thrown by `safePath()` (logged in application logs).
- Agent produced output containing content from outside the sandbox.
- API key or other secret appeared in agent output or logs.
- Unexpected API cost spike in the OpenAI usage dashboard.
- HITL gate fired but no reviewer responded within the SLA window.
- PII or PHI appeared in a summary output.
- Invocation rate anomaly (looping or abuse).

Monitoring:
- [ ] Alert on path-outside-sandbox errors in application logs.
- [ ] Alert on tokensUsed > 2x the 30-day average per run.
- [ ] Alert on invocation rate > 5x the 30-day hourly average.
- [ ] OpenAI usage dashboard alert at 150% of expected daily spend.

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Revoke the `OPENAI_API_KEY` in the OpenAI dashboard (https://platform.openai.com/api-keys).
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all deployment environments.
   c. Stop or restart the Node.js process.
   d. Issue a new API key and store in the secrets manager.
2. If PII or PHI was exposed: restrict access to that output and notify the data-protection officer.
3. Preserve all logs from the incident window.
4. If the agent wrote unexpected files: quarantine them.

---

## 3. Investigate

Questions to answer:

- What exact input or note content triggered the incident?
- Did the `safePath()` function fire? If not, was the sandbox check bypassed?
- Is the attack class in `RED_TEAM_CASES.jsonl`? If not, add it.
- Was `OPERATOR_APPROVED_TO_RUN=1` set without completing the full checklist?
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Patch `agent.ts` (sandbox enforcement, error handling, or refusal logic).
- Update `PROMPT.md` if the system prompt had a gap.
- Add a new eval and red-team case for the attack class.
- Re-run the full eval suite and confirm all cases pass.
- Run `npm audit` to check for new vulnerabilities.
- Re-issue `OPENAI_API_KEY` after rotation.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If PII or PHI was exposed: follow your organization's breach notification policy.
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agents-and-automations/
Reference: https://github.com/openai/openai-agents-python
