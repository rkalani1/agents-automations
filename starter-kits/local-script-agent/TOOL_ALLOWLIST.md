# Tool Allowlist — Local Script Agent

This agent makes a single non-agentic API call. It does not use an agentic tool-call loop, so there are no LLM-invokable tools to list. This document describes the Python-level operations the script performs.

## Permitted Python Operations

- `pathlib.Path.read_text()` — scoped to `./sandbox/` via `safe_read()`. Used to read note files.
  Why this is needed: The script must read notes to send them to the API.
  Scope: `./sandbox/notes/` only. Any path resolving outside `./sandbox/` raises `PermissionError`.

- `openai.OpenAI.chat.completions.create()` — one API call to the OpenAI chat completions endpoint.
  Why this is needed: This is the model inference call that produces the summary.
  Scope: One call per script invocation. The model receives no tools in the API call.

- `pathlib.Path.write_text()` — scoped to `./sandbox/output/`.
  Why this is needed: Persisting the summary to disk for downstream use.
  Scope: `./sandbox/output/summary.md` only. The script does not write outside this path.

## Explicitly Forbidden Operations

- Reading files outside `./sandbox/` — enforced by `safe_read()`.
- Writing files outside `./sandbox/output/` — enforced by the hardcoded output path.
- Executing subprocess or shell commands — not used in the script.
- Making additional HTTP calls beyond the single OpenAI inference call.
- Reading environment variables and including them in the API call payload — `OPENAI_API_KEY` is passed to the OpenAI client only, never sent in the user message.

## LLM-Level Tool Restrictions

No tools are passed to the `client.chat.completions.create()` call. The model receives only `system` and `user` messages. This means:

- The model cannot perform file reads, network calls, or any external action.
- Prompt injection attacks can cause the model to produce a misleading summary, but cannot cause it to take external actions.
- Red-team coverage for injection attacks is provided in `RED_TEAM_CASES.jsonl`.

Field Guide:  /agents-automations/
