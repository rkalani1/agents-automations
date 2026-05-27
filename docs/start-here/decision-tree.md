# Decision tree: which surface?

> **Last verified:** 2026-05-06 · **Drift risk:** medium

There are four broad categories of surface for building with AI agents: chat apps (subscription-tier), custom assistants built on top of those apps, desktop/CLI clients, and the raw API/SDK. This page helps you pick the right starting point.

---

## The core questions

Work through these questions in order. Stop at the first recommendation that fits.

---

### 1. Do you just need a better chat experience today, with no custom tooling?

**Yes** → Start with a chat app.

- Use [ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) to organize conversations by topic, share custom instructions, and keep files in scope across sessions.
- Use Claude.ai for long-context work and conversational analysis.
- Use Gemini app + [Google AI Studio](https://ai.google.dev/aistudio) when you need deep integration with Google Workspace data.

**No** → Continue to question 2.

---

### 2. Do you have a coding workflow — editing code, running tests, refactoring a repo?

**Yes** → Use a coding-focused agent surface.

- [Claude Code](https://code.claude.com/docs/en/setup) runs in your terminal and has direct filesystem and shell access. Best if you work primarily in Claude.
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli) is a terminal-native coding agent for OpenAI models.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) provides a similar terminal experience for Gemini models.
- [GitHub Copilot's coding agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) operates inside GitHub, handling issues and pull requests without leaving the GitHub UI.

**No** → Continue to question 3.

---

### 3. Do you need to connect external tools (databases, APIs, file systems, SaaS products)?

**Yes** → You need MCP or a connector layer.

- **With a desktop client:** Claude Desktop + one or more [MCP servers](https://modelcontextprotocol.io/specification/2025-06-18) is the most common local MCP setup. Anthropic also provides [connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) for common SaaS tools.
- **With a CLI:** Gemini CLI, Claude Code, and Codex CLI all support MCP servers via configuration files.
- **With a custom assistant:** [Custom GPTs](https://help.openai.com/en/articles/8554397) can call external APIs via Actions. Claude.ai Projects work with connectors.

**No** → Continue to question 4.

---

### 4. Do you need long-running tasks, custom logic, or a multi-agent pipeline?

**Yes** → You need the API or an SDK.

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) provides primitives for agents, tools, handoffs between agents, and tracing. Start here for Python-based multi-agent systems on OpenAI models.
- Anthropic's API supports tool use and multi-turn conversations natively. Combine with the [MCP spec](https://modelcontextprotocol.io/specification/2025-06-18) for standardized tool definitions.
- Google AI Studio provides access to Gemini models with function calling for code-based workflows.

**No** → You are likely in "better chat" territory. Go back to question 1.

---

### 5. Do you need everything to run locally (data residency, air-gap, or privacy)?

**Yes** → Read the [Local-first path](local-first-path.md). Use stdio MCP servers, CLI tools, and local file access. Note that the model itself typically still runs in the cloud unless you run a self-hosted model.

---

### 6. Are you building for a team or org?

**Yes** → Read the [Team path](team-path.md). This changes the surface choice: you need SSO, shared resources, audit logs, and key management that personal subscriptions do not provide.

---

## Summary table

| Your situation | Recommended starting point |
|----------------|---------------------------|
| Better chat, no tooling | ChatGPT Projects or Claude.ai |
| Coding and terminal work | Claude Code, Codex CLI, or Gemini CLI |
| Connect external tools, no code | Claude Desktop + MCP or Claude connectors |
| Connect external tools, some code | Custom GPT Actions or Claude Projects + connectors |
| Custom pipeline, Python | OpenAI Agents SDK or Anthropic API |
| Everything local | CLI tools + stdio MCP servers |
| Team or org | Enterprise tier on whichever platform fits above |

---

## What to do next

- Beginner, no prior experience: [Beginner path](beginner-path.md)
- Already using ChatGPT/Claude daily: [Power-user path](power-user-path.md)
- Privacy or air-gap requirements: [Local-first path](local-first-path.md)
- Building for a team: [Team path](team-path.md)
