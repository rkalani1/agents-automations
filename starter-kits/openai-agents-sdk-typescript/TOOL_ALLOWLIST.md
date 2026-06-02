# Tool Allowlist — OpenAI Agents SDK TypeScript Service

Every tool listed here is permitted with the restrictions noted. Tools not listed are forbidden. SDK reference: https://github.com/openai/openai-agents-python (npm: `@openai/agents`).

## Allowed Tools

- `read_notes(path: string) -> string`
  Why this is needed: The agent's only job is to read note files and produce a summary. Without this tool the agent cannot read any input.
  Scope enforcement: The tool resolves the path using `path.resolve()` and throws an error if the resolved path does not start with the absolute sandbox directory path. This check is implemented in TypeScript, not just in the prompt.
  File types: `.txt` and `.md` only. Binary files are not opened.

## Explicitly Forbidden Tools

- Any tool that writes files — the agent produces its summary as a return value only.
- Any tool that executes shell commands, child processes, or `eval()`.
- Any tool that makes HTTP requests, calls external APIs, or opens network connections outside the OpenAI API inference call.
- Any code interpreter or REPL tool.
- Any tool that reads environment variables and returns them to the model — the model must not observe `OPENAI_API_KEY` or any other secret.
- Any bundled SDK tools (web search, file search, code interpreter) — do not register them for this agent.

## Registration in Code

Only `readNotesTool` is passed to the Agent constructor. This is the authoritative list for production:

```typescript
// In agent.ts — only readNotesTool is registered
const agent = new Agent({
  name: "NotesSummarizer",
  instructions: SYSTEM_PROMPT,
  tools: [readNotesTool],  // ONLY this tool
});
```

## Dependency Security

Run `npm audit` against `package.json` before each deployment. Pin all dependency versions in `package.json` for production deployments. See the monthly review cadence in `AGENT_SPEC.md`.

Field Guide:  /agents-automations/
