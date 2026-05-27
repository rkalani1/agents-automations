# Incident Response Runbook — MCP Server (TypeScript)

## Overview

This runbook covers the five phases of incident response for the MCP TypeScript server.

---

## 1. Detect

Signals that indicate a potential incident:

- `validateName` rejecting inputs with shell metacharacters at a high rate (injection attempt).
- Tool invocations for unregistered tools (client trying to invoke tools not on the allowlist).
- Unexpected output patterns in tool responses.
- Process crashes or unexpected exits.
- If HTTP transport is used: anomalous request rates or auth failures.
- Any evidence of filesystem, network, or subprocess activity from the server process.

Monitoring:
- [ ] Alert on validation rejection rate exceeding a threshold per hour.
- [ ] Alert on unknown-tool invocation attempts.
- [ ] Alert on server process crashes.
- [ ] Alert on any unexpected network or filesystem activity (use auditd or similar).

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Stop the server: `kill -TERM <pid>` or stop the Docker/systemd service.
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all environments.
   c. Disconnect or restart the MCP client.
   d. Revoke any API keys if applicable.
2. Preserve server logs from the incident window.
3. If any unexpected files were written or read: quarantine them.
4. If PII appeared in tool outputs or logs: restrict access and notify the data-protection officer.

---

## 3. Investigate

Questions to answer:

- What exact tool call triggered the incident?
- Did `validateName` fire? If not, why was the input not rejected?
- Was the server modified to add unreviewed tools?
- Is the attack class in `RED_TEAM_CASES.jsonl`? If not, add it.
- Was the MCP client compromised, causing malicious tool calls?
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Patch `server.ts` (validation logic, tool registration, or error handling).
- Update `TOOL_ALLOWLIST.md` if the tool surface changed.
- Add new eval and red-team cases for the attack class.
- Re-run the full eval suite.
- Run `npm audit` to check for new vulnerabilities.
- Re-issue any API keys active during the incident.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If PII or PHI was exposed: follow your organization's breach notification policy.
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agent-builder-field-guide/
Reference: https://github.com/modelcontextprotocol/typescript-sdk
