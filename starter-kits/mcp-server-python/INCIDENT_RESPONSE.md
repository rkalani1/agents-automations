# Incident Response Runbook — MCP Server (Python)

## Overview

This runbook covers the five phases of incident response for the MCP Python server. Keep it accessible to all engineers who operate or maintain the server.

---

## 1. Detect

Signals that indicate a potential incident:

- Input validation errors logging suspicious patterns (shell metacharacters, path traversal, injection strings) in the `greet` or any other tool.
- Tool invocations for tools not in `TOOL_ALLOWLIST.md` (indicates the server was modified or a client is trying to invoke unregistered tools).
- Unexpected output patterns in tool responses.
- Process crashes or unexpected restarts.
- If HTTP transport is used: anomalous request rates or authentication failures.
- Any evidence that the server is performing filesystem access, network calls, or subprocess execution.

Monitoring:
- [ ] Alert on input validation rejections exceeding a threshold per hour.
- [ ] Alert on tool invocations for unregistered tool names.
- [ ] Alert on server process crashes.
- [ ] Alert on any filesystem or network activity from the server process (use auditd or similar).

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Stop the server process: `kill -TERM <pid>` or stop the systemd/Docker service.
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all environments.
   c. Disconnect the MCP client (e.g., restart Claude Desktop or the consuming agent).
   d. Revoke any API keys used by the server (if applicable).
2. Preserve server logs from the incident window.
3. If any files were unexpectedly accessed or modified: quarantine them and do not distribute.
4. If PII appeared in tool outputs or logs: restrict access and notify the data-protection officer.

---

## 3. Investigate

Questions to answer:

- What exact tool call triggered the incident?
- What was the input value, and why did input validation not catch it?
- Was the server modified to add new tools without updating the allowlist?
- Is the attack class documented in `RED_TEAM_CASES.jsonl`? If not, add it.
- Was the MCP client itself compromised, causing it to issue malicious tool calls?
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Patch `server.py` (input validation, tool registration, or error handling).
- Update `TOOL_ALLOWLIST.md` if the tool surface changed.
- Add a new eval and red-team case for the attack class.
- Re-run the full eval suite and confirm all cases pass.
- Run `pip audit` to check for new vulnerabilities.
- Re-issue any API keys that were active during the incident.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If PII or PHI was exposed: follow your organization's breach notification policy.
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agents-and-automations/
Reference: https://github.com/modelcontextprotocol/python-sdk
