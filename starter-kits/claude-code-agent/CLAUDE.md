# CLAUDE.md — Coding Agent Constraints

This file is read by Claude Code at session start. It defines the permitted scope, tool restrictions, and behavioral rules for this agent in this repository. Do not remove or edit this file without re-running the launch checklist.

Reference: https://code.claude.com/docs/en/setup

## Permitted Edit Scope

- You may read any file in this repository.
- You may propose or apply edits only to files under `src/`, `tests/`, and `docs/`.
- You may NOT edit: `CLAUDE.md`, `.github/workflows/`, any file containing `secrets`, `.env`, `*.key`, `*.pem`, `*.p12`, or any file outside this repository directory.
- If an edit would touch a file outside the permitted scope, stop and ask the human for explicit approval before proceeding.

## Shell Commands

- You may run: `git status`, `git diff`, `git log`, `grep`, `find`, `cat`, `ls`, test runners specified in the project README, and linters configured in the project's tool config files.
- You may NOT run: `git push`, `git commit` (without explicit human confirmation per commit), `rm -rf`, `curl`, `wget`, `pip install` (outside a virtual environment), `npm install` (outside a project-scoped node_modules), any command that writes to a path outside the repository directory, and any command that opens a network connection to an external host not explicitly listed in this file.
- If you are unsure whether a shell command is permitted, ask before running it.

## Secrets Handling

- Do not read, display, copy, or include in any output: API keys, tokens, passwords, private keys, or the contents of `.env` files.
- If you encounter a secret in a file while reading it for another purpose, do not reproduce it in your response.
- If a file appears to contain a secret that is committed to the repository, flag it to the human as a finding but do not display the secret value.

## Tool Restrictions

- Web search: permitted only when the human explicitly requests it for a specific lookup.
- File creation: permitted only under `src/`, `tests/`, or `docs/`.
- Shell execution: follow the rules above.

## HITL Requirements

- Ask for explicit confirmation before applying any edit that affects more than 10 files.
- Ask for confirmation before running any shell command that modifies state (writes, deletes, installs).
- Ask for confirmation before any network-connected command.

## Behavior on Ambiguity

When an instruction is ambiguous or seems to conflict with this file's rules, do not guess. Ask a clarifying question before taking action.
