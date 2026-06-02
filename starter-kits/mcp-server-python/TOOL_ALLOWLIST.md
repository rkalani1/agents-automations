# Tool Allowlist — MCP Server (Python)

Every tool listed here is permitted with the restrictions noted. Adding a new tool to the server requires updating this document, the `AGENT_SPEC.md`, the `PROMPT.md`, and re-running the launch checklist.

Reference: https://github.com/modelcontextprotocol/python-sdk

## Allowed Tools

- `greet(name: str) -> str`
  Why this is needed: This tool is a minimal, side-effect-free example for demonstrating the MCP server pattern. It returns a greeting string. It reads no files, makes no network calls, and has no persistent state.
  Input validation: Name is validated for length (<= 100 chars), non-emptiness, and absence of shell metacharacters and injection-prone characters before use.
  Side effects: None.
  Data access: None.

## Explicitly Forbidden Tools (for this starter kit)

- Any tool that reads filesystem paths — add filesystem access only after defining sandbox boundaries and updating this document.
- Any tool that makes HTTP requests or calls external APIs.
- Any tool that executes shell commands, subprocesses, or evaluates code.
- Any tool that reads or writes environment variables and returns their values.
- Any tool that persists state to a database or file system.

## Guidelines for Adding New Tools

When you are ready to expand this server beyond the `greet` example, apply these principles for each new tool:

1. Define the minimum input set. Accept only what is necessary for the tool's function.
2. Validate all inputs at the tool boundary before using them.
3. Scope data access to the minimum required (e.g., read-only, specific directory).
4. Document side effects explicitly in the tool's docstring.
5. Add the tool to this allowlist with a "why this is needed" rationale.
6. Update `PROMPT.md` with the tool's name, signature, description, and usage rules.
7. Add at least two eval cases and two red-team cases for the new tool.
8. Re-run the launch checklist before deploying.

## Why a Minimal Tool Surface Matters

Each tool exposed by an MCP server becomes an action the AI client can take. A prompt injection in any data the agent processes could cause it to invoke any registered tool. Keeping the tool surface minimal limits the blast radius of a successful injection.

Field Guide:  /agents-and-automations/
