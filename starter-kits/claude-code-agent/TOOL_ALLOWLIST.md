# Tool Allowlist — Claude Code Coding Agent

Every tool listed here is permitted with the restrictions noted. Tools not listed are forbidden. Claude Code's tool model is described at https://code.claude.com/docs/en/setup.

## Allowed Tools

- `read_file(path)`
  Why this is needed: The agent must read source files, test files, and configuration files to understand the codebase before proposing changes. Scope: any file in the repository directory. Exception: files matching secret patterns (see `CLAUDE.md`).

- `edit_file(path, edits)`
  Why this is needed: The agent's primary output is code changes. Scope: restricted to `src/`, `tests/`, and `docs/` as defined in `CLAUDE.md`. Requires human confirmation for changes affecting > 10 files.

- `create_file(path, content)`
  Why this is needed: New feature work requires creating new source or test files. Scope: `src/`, `tests/`, `docs/` only.

- `bash(command)` — restricted subset
  Why this is needed: Running tests, linters, and `git status`/`git diff`/`git log` is necessary to verify correctness. The permitted command list is enumerated in `CLAUDE.md`. Every command is logged in `shell_commands_run`.

- `web_search(query)` — gated
  Why this is needed: Occasionally the agent needs to look up an API, library version, or error message. Gated: the human must explicitly request a web search. The agent does not initiate searches autonomously.

## Explicitly Forbidden Tools

- `git push` / `git commit` without human confirmation — state-modifying git operations require HITL gate approval.
- Any tool that writes outside the repository directory — enforced by `CLAUDE.md` and should also be enforced at the OS/container level.
- Any tool that reads or displays secret-matching file patterns — `CLAUDE.md` rule applies.
- Any tool that makes autonomous network calls (e.g., `curl`, `wget`) — network-connected commands require human confirmation per session.

## Notes on Claude Code's Built-in Tools

Claude Code bundles several tools by default. Use the `CLAUDE.md` file to restrict which tools are active in a given session. Per the setup docs at https://code.claude.com/docs/en/setup, tool permissions can be configured at the project level. Confirm that your session settings match this allowlist before starting a production session.

Field Guide:  /agent-builder-field-guide/
