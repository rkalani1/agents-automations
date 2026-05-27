# Platforms Overview

> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [Claude overview](https://claude.ai), [Gemini overview](https://gemini.google.com), [OpenAI overview](https://openai.com), [GitHub Copilot overview](https://github.com/features/copilot)

This section maps the landscape of surfaces where you can build, run, or embed AI agents. Each page covers what a platform is for, how to set it up, and where its limits are. The goal is to help you choose the right surface for a given task and get something working without guessing.

---

## Platform Pages

### Anthropic / Claude

| Page | Purpose |
|------|---------|
| [Claude Desktop](claude-desktop.md) | The installable macOS/Windows app for Claude. The primary surface for adding local MCP servers and desktop extensions that connect Claude to files, apps, and local tools. |
| [Claude Code](claude-code.md) | Anthropic's terminal-based coding agent. Install it once, point it at a repository, and drive code changes, tests, commits, and refactors from a shell prompt. |
| [Claude Projects](claude-projects.md) | Persistent project workspaces on claude.ai. Attach files, write system instructions, and give Claude long-running context for a specific domain or workflow. |

### Google / Gemini

| Page | Purpose |
|------|---------|
| [Gemini App](gemini-app.md) | The gemini.google.com web app. Includes Gems, which are saved custom personas, and integration with Google Workspace data for document-aware conversations. |
| [Gemini CLI](gemini-cli.md) | An open-source terminal agent from Google. Authenticate with a Google account or an AI Studio API key, then drive file edits, code changes, and tool calls from the command line. |
| [Google Antigravity](antigravity.md) | An agent-first IDE built on VS Code that orchestrates autonomous agents capable of planning, coding, browsing, and iterating with minimal hand-holding. |
| [Google AI Studio](ai-studio.md) | A browser-based workbench for the Gemini API. Design prompts, set system instructions, test structured output, and export working code—all before writing a single line of application code. |

### OpenAI / ChatGPT

| Page | Purpose |
|------|---------|
| [ChatGPT](chatgpt.md) | The chatgpt.com web app, including Projects and custom instructions. Suitable for ad-hoc tasks, iterative conversation, and document-aware Projects with attached files. |
| [Custom GPTs](custom-gpts.md) | GPT Builder lets you create persistent GPT personas with custom instructions, uploaded knowledge files, and optional Actions backed by HTTPS endpoints. |
| [OpenAI API & Agents SDK](openai-api.md) | The core REST API plus the Agents SDK. The foundation for programmatic agents, tool calling, structured outputs, guardrails, handoffs, and tracing. |
| [Codex](codex.md) | OpenAI's terminal coding agent (Codex CLI) and cloud Codex surface. Reads repositories, runs tests, and opens pull requests against GitHub branches. |

### xAI / Grok

| Page | Purpose |
|------|---------|
| [Grok / xAI](grok.md) | Three distinct surfaces: Grok consumer chat (grok.com), Grok on X (X subscription), and the xAI API for programmatic agents. Tool calling and structured outputs require API access. |

### Microsoft

| Page | Purpose |
|------|---------|
| [GitHub Copilot](copilot.md) | Copilot cloud agent. Assign issues to Copilot and review the resulting pull request — distinct from the in-editor Copilot integrations. |

### Local

| Page | Purpose |
|------|---------|
| [Local scripts & schedulers](local-scripts.md) | Patterns for lightweight agents in Python or shell, with manual-only schedulers (cron / launchd / Task Scheduler) gated behind explicit opt-in. |

---

## How to Use This Section

Start with the platform you already have access to. If you have a Claude Pro subscription, begin with [Claude Desktop](claude-desktop.md) or [Claude Code](claude-code.md). If you have a Google account, [Google AI Studio](ai-studio.md) is free-tier accessible and requires no subscription. If you want a terminal-first workflow without vendor lock-in, [Gemini CLI](gemini-cli.md) is open source.

Each page is self-contained. You do not need to read them in order, but if you are new to agents entirely, reading [Claude Desktop](claude-desktop.md) first gives you a concrete mental model of how local tool access works, which transfers to most other platforms.

All pages note drift risk. Check the linked official sources if you notice UI discrepancies—these products ship updates frequently.
