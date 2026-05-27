# Tool Allowlist — MCP Server (TypeScript)

Every tool listed here is permitted with the restrictions noted. Adding a new tool requires updating this document, `AGENT_SPEC.md`, `PROMPT.md`, and re-running the launch checklist.

Reference: https://github.com/modelcontextprotocol/typescript-sdk

## Allowed Tools

- `greet(name: string) -> string`
  Why this is needed: This is a minimal, side-effect-free example tool for demonstrating the MCP TypeScript server pattern. It returns a greeting string and serves as a verified baseline for adding real tools.
  Input validation: Enforced in `validateName()` in `server.ts` — checks for non-empty string, max length 100 characters, and absence of shell metacharacters via regex.
  Side effects: None.
  Data access: None.
  Network calls: None.

## Explicitly Forbidden Tools (for this starter kit)

- Any tool that reads from or writes to the filesystem.
- Any tool that makes HTTP requests or calls external APIs.
- Any tool that executes shell commands or child processes.
- Any tool that reads environment variables and returns their values to the caller.
- Any tool that persists state to a database or file.

## Guidelines for Adding New Tools

When expanding this server for real use cases:

1. Define the minimum input set. Accept only what is strictly necessary.
2. Validate all inputs at the tool boundary. Use the `validateName` pattern or a schema validator like Zod.
3. Scope data access to the minimum required.
4. Document side effects explicitly in the tool's description field.
5. Add the tool to this allowlist with a "why this is needed" rationale.
6. Update `PROMPT.md` with the tool's name, signature, and usage rules.
7. Add at least two eval cases and two red-team cases for the new tool.
8. Re-run the launch checklist before deploying.

## Why Minimal Tool Surface Matters

Each registered tool is a potential action an AI client can invoke. A prompt injection in any data the agent processes could cause it to call any registered tool. Keeping the surface minimal limits the blast radius of a successful injection to the tools that are actually needed.

Field Guide:  /agent-builder-field-guide/
