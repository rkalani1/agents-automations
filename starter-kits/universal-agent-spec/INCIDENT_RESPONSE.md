# Incident Response Runbook — Universal Summarization Agent

## Overview

This runbook covers the five phases of incident response for this agent. Keep this document accessible to anyone on the on-call rotation. Review it quarterly or after any incident.

---

## 1. Detect

Signals that indicate a potential incident:

- The agent reads files outside the configured sandbox directory (visible in logs as a path mismatch).
- The agent produces a summary that contains content not present in any source file (hallucination or injection).
- The agent invokes a tool that is not in `TOOL_ALLOWLIST.md` (visible in tool-call logs).
- Token consumption spikes unexpectedly (denial-of-wallet pattern).
- A HITL gate fires but no human reviewer responds within the SLA window.
- A user or downstream system reports that PII appeared in a summary output.
- Anomalous invocation frequency (potential looping or abuse).

Monitoring checklist:
- [ ] Log-based alert on path-outside-sandbox errors.
- [ ] Alert on `tokens_consumed` > 2x the 30-day average per invocation.
- [ ] Alert on invocation rate > 5x the 30-day average per hour.
- [ ] Alert on unanswered HITL gate requests older than 30 minutes.

---

## 2. Contain

Immediate steps when an incident is confirmed or strongly suspected:

1. Kill switch: Rotate the LLM API key immediately. This stops all in-flight and future agent invocations. Steps:
   a. Go to your LLM provider's API key management console.
   b. Revoke the current key.
   c. Issue a new key and store it in the secrets manager.
   d. Set `OPERATOR_APPROVED_TO_RUN=0` in all deployment environments.
   e. Restart any long-running agent processes.
2. If the agent has a network-accessible endpoint, take it offline or block traffic at the load balancer.
3. Preserve all logs from the incident window. Do not rotate or delete them.
4. If PII was exposed in output, immediately restrict access to that output and notify the data-protection officer.

---

## 3. Investigate

Questions to answer during investigation:

- What was the exact invocation (inputs, tool calls, model response) that triggered the incident?
- Did the incident originate from injected content in a note file?
- Was the attack class one of the documented red-team scenarios in `RED_TEAM_CASES.jsonl`? If not, add it.
- Was the sandbox path restriction enforced at the runtime level or only in the prompt?
- Were all HITL gates functioning correctly at the time of the incident?
- Which eval or red-team case, if added earlier, would have caught this?

---

## 4. Remediate

Steps to fix the root cause before re-enabling the agent:

- Patch the code, configuration, or prompt that allowed the incident.
- Add a new eval or red-team case that covers the incident's attack class.
- Re-run the full eval suite and confirm all cases pass.
- Repeat the affected red-team case against the patched agent.
- Update `AGENT_SPEC.md` and `TOOL_ALLOWLIST.md` if the root cause was a spec gap.
- Re-issue API credentials after rotation is complete.

---

## 5. Communicate

- Within 1 hour of detection: Notify the owner listed in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to all stakeholders. Include: what happened, what was contained, current status.
- If PII was exposed: Follow your organization's breach notification policy. This may include regulatory reporting obligations depending on jurisdiction and data type.
- After remediation: Publish a post-mortem with a timeline, root cause, and a list of changes made. File a copy alongside this document.

Field Guide:  /agents-automations/
