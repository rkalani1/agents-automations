# Tool Allowlist — Codex CLI Coding Agent

Every tool listed here is permitted with the restrictions noted. Tools not listed are forbidden. The Codex CLI tool model is described at https://developers.openai.com/codex/cli.

## Allowed Tools

- `read_file(path)`
  Why this is needed: The agent must read source, test, and configuration files to understand the codebase before proposing changes. Scope: any file in the repository directory except secret-matching patterns listed in `AGENTS.md`.

- `edit_file(path, edits)`
  Why this is needed: Code changes are the agent's primary output. Scope: restricted to `src/`, `tests/`, and `docs/` per `AGENTS.md`. Human confirmation required for changes to > 10 files.

- `create_file(path, content)`
  Why this is needed: New features require new source or test files. Scope: `src/`, `tests/`, `docs/` only.

- `bash(command)` — restricted subset
  Why this is needed: Running tests, linters, and read-only git commands is necessary to verify correctness. Permitted commands are enumerated in `AGENTS.md`. All commands are logged in `shell_commands_run`.

- `web_search(query)` — gated
  Why this is needed: Occasional lookups for API docs, error messages, or dependency versions. Gated: human must explicitly request a web search. The agent does not initiate searches autonomously.

## Explicitly Forbidden Tools

- `git push`, `git commit` without human confirmation — require HITL gate approval.
- Any write operation outside the repository directory — must be enforced at OS/container level in addition to the prompt.
- Any command reading or displaying secret-matching files.
- Any tool making autonomous network calls (curl, wget, fetch, requests) — require human confirmation.
- Package installers (pip, npm, cargo) targeting global or system-level locations.

## Container-Level Enforcement

Because Codex CLI runs in your local terminal, model-level constraints alone are not sufficient for high-security environments. Where possible, run Codex CLI in a container with:
- Filesystem access restricted to the repository directory.
- Network egress blocked except for the OpenAI API endpoint.
- No root or sudo access inside the container.

This defense-in-depth approach ensures that even if the model is manipulated, the blast radius is limited.

Field Guide:  /agent-builder-field-guide/
Reference: https://developers.openai.com/codex/cli
