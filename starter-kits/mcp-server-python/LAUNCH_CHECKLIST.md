# Launch Checklist — MCP Server (Python)

Complete every item before exposing this server to an AI agent or MCP client. Items marked [BLOCKER] must be resolved.

---

## Scope

- [ ] [BLOCKER] Tool surface is limited to what is in `TOOL_ALLOWLIST.md`.
- [ ] Every tool has a documented "why this is needed" rationale.
- [ ] Input validation is implemented and tested for every tool parameter.
- [ ] Out-of-scope capabilities are explicitly not registered.
- [ ] A second engineer has reviewed `server.py` and agrees with the tool definitions.

## Tools and Permissions

- [ ] [BLOCKER] Only `greet` (or approved tools) is registered via `@mcp.tool()`.
- [ ] No filesystem-access, shell-execution, or network-call tools are registered.
- [ ] Input validation for `greet` tested with: empty string, 101-char string, shell metacharacters, newline injection, null bytes.
- [ ] `pip audit` has been run against `requirements.txt` with no high/critical findings.
- [ ] Dependencies pinned to specific versions for production.

## Data

- [ ] Server handles no user PII. If it is extended to do so, add a PII handling section to `AGENT_SPEC.md`.
- [ ] Server has no persistent state. If state is added, data retention policy must be defined.
- [ ] Server logs do not contain sensitive input values.

## Auth

- [ ] If the server exposes an HTTP transport (not stdio): authentication and authorization are implemented.
- [ ] For stdio transport: the server process is only started by the authorized MCP client process.
- [ ] If an API key is needed for any tool: stored in a secrets manager, not hardcoded.

## HITL

- [ ] [BLOCKER] `OPERATOR_APPROVED_TO_RUN=1` is only set after completing this checklist.
- [ ] Gate 2: New tools require review before adding to the server.
- [ ] Human reviewer contact is defined for any HITL-gated actions.

## Logging

- [ ] Server logs every tool invocation with: timestamp, tool name, input summary (not full value if PII-risk), result status.
- [ ] Log access is restricted to authorized personnel.
- [ ] Log retention policy is defined.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Eval results are committed to version control.
- [ ] Automated test suite runs on every commit.

## Operations

- [ ] Kill-switch procedure in `INCIDENT_RESPONSE.md` is documented and tested.
- [ ] On-call contact is listed.
- [ ] Process restart procedure is documented (e.g., systemd unit file or Docker restart policy).
- [ ] Transport type (stdio vs HTTP) is documented and matches the intended deployment.

## People

- [ ] Owner in `AGENT_SPEC.md` is a real person or team.
- [ ] Security review sign-off is documented.
- [ ] All engineers who will operate the server have read `INCIDENT_RESPONSE.md`.
- [ ] Review cadence is scheduled.

Reference: https://github.com/modelcontextprotocol/python-sdk
