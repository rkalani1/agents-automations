# MCP Server — TypeScript Starter Kit

## What This Kit Is

This starter kit provides a minimal Model Context Protocol (MCP) server implemented with the official MCP TypeScript SDK. The server exposes one trivial `greet` tool as a working example. It is inert by default — the server does not start unless `OPERATOR_APPROVED_TO_RUN=1` is set in the launching environment. There is no stdio / pipe bypass: when an MCP client auto-launches this server, the operator must add `OPERATOR_APPROVED_TO_RUN=1` to the client's `env` block for that server (see `server.ts` docstring for an example).

The MCP TypeScript SDK is the reference implementation for building MCP servers in Node.js/TypeScript. Source and documentation are at https://github.com/modelcontextprotocol/typescript-sdk.

## Who This Kit Is For

- TypeScript/Node.js engineers building custom tool servers for MCP-compatible AI clients.
- Teams who need a reviewed starting point before exposing custom tools to an AI agent.
- Security reviewers auditing the tool surface of an MCP server.

## Files Included

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `server.ts` | Inert MCP server. Exposes one `greet` tool. |
| `package.json` | NPM dependencies and scripts. |
| `tsconfig.json` | TypeScript compiler configuration. |
| `AGENT_SPEC.md` | Filled agent spec. |
| `PROMPT.md` | System prompt for agents consuming this server. |
| `TOOL_ALLOWLIST.md` | Least-privilege tool list with rationale. |
| `EVALS.jsonl` | Eight golden eval cases. |
| `RED_TEAM_CASES.jsonl` | Eight red-team adversarial cases. |
| `LAUNCH_CHECKLIST.md` | Pre-launch task list. |
| `INCIDENT_RESPONSE.md` | Incident response runbook. |

## How to Use

1. Install dependencies: `npm install`
2. Review `server.ts` to understand the tool surface.
3. Run in dry-run mode: `npx ts-node server.ts` (without `OPERATOR_APPROVED_TO_RUN=1`).
4. Complete the launch checklist.
5. Start the server: `OPERATOR_APPROVED_TO_RUN=1 npx ts-node server.ts`
6. Connect an MCP-compatible client to the server's stdio transport.

## MCP Security Model

MCP servers run as local processes communicating with AI clients over stdio or HTTP. Every tool you expose becomes part of the agent's reachable action surface. A successful prompt injection in the AI client could invoke any registered tool. This is why the tool allowlist and red-team suite in this kit focus on what `greet` can and cannot do, and on input validation at the tool boundary.

Reference: https://github.com/modelcontextprotocol/typescript-sdk

Field Guide:  /agents-automations/
