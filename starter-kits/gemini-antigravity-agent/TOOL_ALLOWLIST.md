# Tool Allowlist — Gemini Antigravity Project Agent

Last verified: 2026-05-06. Platform drift risk: high — verify tool names and scoping syntax against current Antigravity docs at https://codelabs.developers.google.com/getting-started-google-antigravity.

## Allowed Tools

- `read_file(path: string) -> string`
  Why this is needed: The agent's job is to read notes. Scope: paths under the configured `notes_dir` only. Any path that resolves outside the project workspace must produce an error.

- `write_file(path: string, content: string)` — conditionally permitted, HITL-gated
  Why this is needed: Persisting summaries to `data/outputs/` is useful for downstream consumers. This tool is only enabled if output persistence is required by the project. It must be scoped to `data/outputs/` only and requires HITL gate approval before each write.

## Explicitly Forbidden Tools

- `execute_command` / `bash` / `shell` — No code execution is required or permitted.
- `http_request` / `fetch_url` / `web_search` — Summarization operates on local workspace files only.
- `list_directory` beyond workspace scope — If bundled, scope to the project workspace only.
- `send_email` / `post_message` — No communication actions are required.
- Any code interpreter or REPL — Not needed and significantly increases attack surface.
- Any tool that reads or modifies files outside `notes_dir` (for reads) or `data/outputs/` (for writes).

## Antigravity-Specific Scoping

Configure tool permissions in `antigravity.yaml` using the project manifest's `tool_permissions` section. Example:

```yaml
tool_permissions:
  read_file:
    scope: "data/notes/"
  write_file:
    scope: "data/outputs/"
    requires_hitl: true
```

Do not grant project-wide or filesystem-wide tool access. Scope every tool to the minimum directory required.

## Rationale for Minimal Footprint

A summarization agent with read-only access to a bounded directory has a small blast radius if manipulated by a prompt injection in a note file. Removing write access (or HITL-gating it) and blocking all network tools means a successful injection still cannot exfiltrate data or cause lasting harm beyond a misleading summary.

Field Guide:  /agents-and-automations/
