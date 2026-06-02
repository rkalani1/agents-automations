# Tool Allowlist — Universal Summarization Agent

This document enumerates every tool this agent is permitted to invoke. Any tool not listed here is forbidden. The principle is least privilege: grant only what is necessary for the job statement, nothing more.

## Allowed Tools

- `read_file(path: string) -> string`
  Why this is needed: The agent's entire job is reading notes. Without this tool the agent cannot do anything. Restricted to paths under the configured sandbox directory; any path that resolves outside the sandbox must produce an error rather than content.

## Explicitly Forbidden Tools (illustrative, not exhaustive)

- `write_file` / `create_file` / `delete_file` — The agent produces a summary as a return value; it never writes to disk.
- `execute_command` / `bash` / `shell` — No code execution is required or permitted.
- `http_request` / `fetch_url` / `web_search` — Summarization is performed on local files only; no network access is needed.
- `list_directory` — The caller provides the directory; the agent does not need to enumerate filesystem structure beyond reading individual files. If your platform bundles `list_directory` with `read_file`, scope it to the sandbox directory only.
- `send_email` / `post_message` / `create_calendar_event` — No communication or scheduling actions are required.
- Any code interpreter or REPL tool — Not needed and significantly widens the attack surface.

## Rationale for Minimal Footprint

An agent that can only read files inside a sandbox directory has a very small blast radius if it is manipulated by a prompt injection attack embedded in one of the notes. An adversary who controls a note's content could attempt to convince the agent to exfiltrate data or modify files. Removing every tool except `read_file` means a successful injection still cannot cause harm beyond producing a misleading summary, which is detectable by the HITL gate and eval suite.

## Notes on Implementation

When configuring your platform's tool registry, pass only `read_file` in the tools array. If the platform uses a default tool set (e.g., a code interpreter is bundled by default), explicitly disable it for this agent. See the platform-specific starter kits in this repository for concrete configuration examples.

Field Guide:  /agents-and-automations/
