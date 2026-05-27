# Launch Checklist — MCP Server (TypeScript)

Complete every item before exposing this server to an AI agent or MCP client.

---

## Scope

- [ ] [BLOCKER] Tool surface matches `TOOL_ALLOWLIST.md` exactly.
- [ ] Every tool has a documented "why this is needed" rationale.
- [ ] Input validation is implemented and tested for every tool parameter.
- [ ] A second engineer has reviewed `server.ts` and agrees with the tool definitions.

## Tools and Permissions

- [ ] [BLOCKER] Only tools in `TOOL_ALLOWLIST.md` are registered in `server.ts`.
- [ ] No filesystem, shell, or network tools are registered.
- [ ] `validateName` tested with: empty string, 101-char string, shell metacharacters, newline injection.
- [ ] `npm audit` has been run with no high or critical findings.
- [ ] All dependencies are pinned to specific versions in `package.json`.

## Data

- [ ] Server handles no user PII. If extended to do so, add a PII handling section to `AGENT_SPEC.md`.
- [ ] Server has no persistent state. If state is added, data retention policy must be defined.
- [ ] Server logs do not contain sensitive input values in full.

## Auth

- [ ] If HTTP transport is used: authentication and authorization are implemented.
- [ ] For stdio: server process is only started by the authorized MCP client process.
- [ ] Any API keys required by tools are stored in a secrets manager.

## HITL

- [ ] [BLOCKER] `OPERATOR_APPROVED_TO_RUN=1` is only set after completing this checklist.
- [ ] Gate 2: New tools require full review before adding.
- [ ] Human reviewer contact is defined for HITL-gated actions.

## Logging

- [ ] Every tool invocation is logged with: timestamp, tool name, input summary, result status.
- [ ] Logs do not contain full user input values if they could contain PII.
- [ ] Log retention policy is defined.
- [ ] Log access is restricted to authorized personnel.

## Evals

- [ ] [BLOCKER] All 8 eval cases in `EVALS.jsonl` pass.
- [ ] All 8 red-team cases in `RED_TEAM_CASES.jsonl` produce the desired response.
- [ ] Automated test suite runs on every commit.

## Operations

- [ ] Kill-switch procedure in `INCIDENT_RESPONSE.md` is documented and tested.
- [ ] Process restart procedure is documented.
- [ ] Transport type (stdio vs HTTP) matches the intended deployment.
- [ ] TypeScript build output (`dist/`) is not committed to version control.

## People

- [ ] Owner in `AGENT_SPEC.md` is a real person or team.
- [ ] Security review sign-off is documented.
- [ ] All engineers who will operate the server have read `INCIDENT_RESPONSE.md`.
- [ ] Review cadence is scheduled.

Reference: https://github.com/modelcontextprotocol/typescript-sdk
