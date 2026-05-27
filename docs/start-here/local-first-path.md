# Local-first path

> **Last verified:** 2026-05-06 · **Drift risk:** medium

This path is for anyone who wants to minimize how much data leaves their machine: researchers with sensitive datasets, engineers in regulated environments, or anyone with a strong preference for auditability and control. It describes an architecture, not a single product.

---

## What "local-first" means here

- Tool execution (MCP servers, shell commands, file access) runs on your machine.
- No remote connectors or cloud-hosted tool backends.
- All tool call logs are written to local files you control.
- Secrets and credentials are managed locally.

**The important caveat:** Unless you run a self-hosted model (which is outside the scope of this guide), the model itself still runs in the cloud. Prompts, tool arguments, and tool results are sent to and from the model provider's API. "Local-first" reduces your cloud surface area but does not eliminate it.

!!! note
    If you need fully air-gapped inference, you need a self-hosted model (e.g., via Ollama, llama.cpp, or a similar local runtime). That is a different architecture not covered here.

---

## Use stdio MCP servers only

The [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18) supports two transport modes: HTTP/SSE (remote) and stdio (local subprocess). For a local-first setup, use stdio servers only.

A stdio MCP server is a process that runs on your machine. Your CLI agent launches it as a subprocess, communicates over stdin/stdout, and kills it when the session ends. No network port is opened. No data is sent to a third-party service.

The reference [filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) uses stdio by default. Start with this one.

To add additional tools locally:
- Write your own MCP server as a Python or Node script (the MCP SDK is available for both).
- Use community stdio servers that do not require remote credentials.
- Avoid MCP servers that phone home for authentication or telemetry — read the source or the README before installing.

---

## Prefer CLI over web UI

Web UIs send your input to a server before it reaches the model. CLI agents communicate directly with the API. The difference in data handling is often small, but CLIs give you:

- Explicit control over which API key is used.
- Local logging of every request and response (if your CLI supports it — check the docs).
- Scriptable workflows that do not depend on browser sessions.

Use [Claude Code](https://code.claude.com/docs/en/setup), [Codex CLI](https://developers.openai.com/codex/cli), or [Gemini CLI](https://github.com/google-gemini/gemini-cli) rather than browser-based chat for sensitive workflows.

---

## Log all tool calls locally

Before you run any workflow with write access, set up local logging. At minimum, log:

- Timestamp
- Tool name called
- Arguments passed
- Result returned
- Whether the agent continued or stopped

Most CLI agents have a verbose or debug mode that writes this to stdout — redirect it to a file. If yours does not, wrap the MCP server in a thin logging proxy (a small script that intercepts stdio, logs it, and passes it through).

Keep logs for at least 30 days. If the agent takes an action you did not expect, the log is how you find out what happened.

---

## Manage credentials locally

Your API key and any tool credentials should never be hardcoded in a config file that lives in a project directory.

Options for local credential management:

- **Environment variables** set in your shell profile (`~/.zshrc`, `~/.bashrc`) or a sourced `.env` file that is listed in `.gitignore`. Simple, widely supported.
- **A sealed env file pattern** — a `.env.secret` file encrypted at rest and decrypted only when the agent runs. Various tools support this pattern; the right choice depends on your OS and threat model.
- **A CLI password manager** such as `pass` (GPG-based, open source) or `1Password CLI` (commercial) — both can inject secrets into environment variables at runtime without writing plaintext to disk. These are options worth evaluating; this guide does not endorse any specific product.

Whatever you use, the rule is: secrets are never in version control, never in a config file committed to a shared repo, and never logged.

---

## Restrict tool scope aggressively

For local-first work, the attack surface is whatever directories and commands you expose to the agent. Apply least-privilege:

- Point the filesystem MCP server at a dedicated working directory, not `~` or `/`.
- If you expose a shell tool, allowlist the commands it can run rather than giving unrestricted shell access.
- Review every MCP server's README for what permissions it requests before connecting it.

See [Safety baseline](safety-baseline.md) for a full pre-build checklist.

---

## Tradeoffs to accept

| What you gain | What you give up |
|--------------|-----------------|
| Reduced cloud tool surface area | Model inference still goes to the cloud |
| Full local audit log | More setup time vs. a hosted connector |
| No third-party tool auth | Fewer pre-built integrations |
| Scriptable, reproducible runs | No web UI for non-technical collaborators |

If you need to share this workflow with teammates who are not comfortable with terminals, see [Team path](team-path.md) for hybrid options.
