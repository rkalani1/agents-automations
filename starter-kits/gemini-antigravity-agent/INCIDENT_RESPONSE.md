# Incident Response Runbook — Gemini Antigravity Project Agent

Last verified: 2026-05-06. Platform drift risk: high.

## Overview

This runbook covers the five phases of incident response for the Gemini Antigravity project agent. Keep it accessible to all project team members.

---

## 1. Detect

Signals that indicate a potential incident:

- Agent attempted to read or write files outside the configured workspace.
- Agent produced a summary containing information not present in the source notes (hallucination or injection).
- Agent attempted to call a tool not in `TOOL_ALLOWLIST.md`.
- Unexpected token consumption spike (potential denial-of-wallet).
- A HITL gate fired but no human reviewer responded within the SLA window.
- PII or PHI appeared in a summary output.
- Google Cloud billing alert fired unexpectedly.

Monitoring:
- [ ] Alert on file access outside `notes_dir`.
- [ ] Alert on `tokens_consumed` > 2x the 30-day average.
- [ ] Alert on HITL gate requests unanswered for > 30 minutes.
- [ ] Google Cloud billing alert at 150% of expected daily spend.

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Revoke the Google/Gemini API key in Google Cloud Console.
   b. Disable the Antigravity project or agent definition in the project manifest.
   c. Set `OPERATOR_APPROVED_TO_RUN=0` in all environments.
   d. Restart any long-running agent processes.
   e. Issue a new API key and store it in the secrets manager.
2. If PII or PHI was exposed in output: restrict access to that output immediately and notify the data-protection officer.
3. Preserve all invocation logs from the incident window.
4. If the agent wrote unexpected files to `data/outputs/` or elsewhere: quarantine those files and do not distribute them.

---

## 3. Investigate

Questions to answer:

- What exact input or file content triggered the behavior?
- Was it a prompt injection from a note file or a direct instruction?
- Which HITL gate was bypassed or malfunctioned?
- Is the attack class in `RED_TEAM_CASES.jsonl`? If not, add it.
- Did the Antigravity platform change a behavior since the "Last verified" date?
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Update `PROMPT.md` and `antigravity.yaml` to close the gap.
- Update `TOOL_ALLOWLIST.md` if tool scoping was insufficient.
- Add a new eval and red-team case for the incident's attack class.
- Re-run the full eval and red-team suite.
- Re-issue API credentials after rotation.
- Update the "Last verified" date in all kit files after verifying against current Antigravity docs.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If PHI or PII was exposed: follow your organization's breach notification policy (which may include regulatory obligations under HIPAA, GDPR, or CCPA depending on data type and jurisdiction).
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agents-and-automations/
Reference: https://codelabs.developers.google.com/getting-started-google-antigravity
