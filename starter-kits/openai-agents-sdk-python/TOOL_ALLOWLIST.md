# Tool Allowlist — OpenAI Agents SDK Python Service

Every tool listed here is permitted with the restrictions noted. Tools not on this list are forbidden. The SDK's tool registration model is described at https://github.com/openai/openai-agents-python.

## Allowed Tools

- `read_notes(path: str) -> str`
  Why this is needed: The agent's only job is to read note files and produce a summary. Without this tool the agent cannot read any file.
  Scope enforcement: The tool resolves the full path using `pathlib.Path.resolve()` and raises `PermissionError` if the resolved path does not start with the sandbox directory absolute path. This check is implemented in Python, not just in the prompt.
  File types: `.txt` and `.md` only. Binary files are not opened.

## Explicitly Forbidden Tools

- Any tool that writes files — the agent produces its summary as a return value; it never writes to disk.
- Any tool that executes shell commands or subprocesses.
- Any tool that makes HTTP requests or calls external APIs. The `openai` library calls for model inference are the only outbound network calls permitted; all others are blocked by design.
- The OpenAI Agents SDK's built-in `WebSearchTool`, `FileSearchTool`, and `CodeInterpreterTool` — these are not registered for this agent. Do not add them without updating this document, the AGENT_SPEC, and the launch checklist.
- Any tool that reads environment variables and returns them to the model — the model must not be able to observe the `OPENAI_API_KEY` or any other secret.

## Registration in Code

Tools are registered by passing them to the `tools=` parameter of the `Agent` constructor. Only `read_notes` is passed. This is the authoritative list for production deployments — the prompt alone is not sufficient to prevent tool use.

```python
# In agent.py — only read_notes is registered
summarizer_agent = Agent(
    name="NotesSummarizer",
    instructions=SYSTEM_PROMPT,
    tools=[read_notes],  # ONLY this tool
)
```

## Dependency Security

Run `pip audit` against `requirements.txt` before each deployment to check for known vulnerabilities in the dependency chain. See the monthly review cadence in `AGENT_SPEC.md`.

Field Guide:  /agents-and-automations/
Reference: https://github.com/openai/openai-agents-python
