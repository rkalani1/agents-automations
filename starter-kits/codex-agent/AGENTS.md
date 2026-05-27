# AGENTS.md — Codex CLI Agent Constraints

This file is read by the Codex CLI agent at session start. It defines permitted scope, tool restrictions, and behavioral rules for this agent in this repository. Do not remove or modify this file without re-running the launch checklist.

Reference: https://developers.openai.com/codex/cli

## Permitted Edit Scope

- You may read any file in this repository.
- You may propose or apply edits only to files under `src/`, `tests/`, and `docs/`.
- You may NOT edit: `AGENTS.md`, `.github/workflows/`, infrastructure configuration files, any file whose name contains `secret`, `.env`, `*.key`, `*.pem`, or any file outside this repository directory.
- If a requested edit would touch a file outside the permitted scope, stop and ask the human for explicit approval.

## Shell Commands

- Permitted: `git status`, `git diff`, `git log`, `grep`, `find`, `cat`, `ls`, test runners defined in the project README, and linters configured in the project's tool config files.
- Forbidden without explicit human confirmation: `git push`, `git commit`, `rm -rf`, `curl`, `wget`, `pip install` (outside a virtual environment), `npm install` (outside project-scoped node_modules), any command writing outside the repository directory, any command opening a network connection to an external host.
- If uncertain whether a shell command is permitted, ask before running it.
- Before running any shell command, state what you are about to run and why.

## Secrets Handling

- Do not read, display, copy, or include in any output the contents of files matching: `.env`, `*.key`, `*.pem`, `*secret*`, `*token*`, `*password*`, `*credentials*`.
- If you encounter a secret in a file while reading it for another purpose, do not reproduce it in your response.
- If a secret appears to be committed to the repository, flag it to the human as a security finding without displaying its value.

## HITL Requirements

- Ask for explicit confirmation before applying edits affecting more than 10 files.
- Ask for confirmation before running any state-modifying shell command.
- Ask for confirmation before any network-connected command.
- Ask for confirmation before any git operation that modifies history or pushes to a remote.

## Behavior on Ambiguity

When an instruction is ambiguous or conflicts with this file, ask a clarifying question. Do not guess.
