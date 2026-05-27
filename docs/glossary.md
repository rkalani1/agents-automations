# Glossary

A working vocabulary for this guide. When a term has a vendor-specific meaning that differs from common usage, both are noted.

**Agent.** A system that uses a model in a loop to plan, take actions through tools, observe results, and decide what to do next, until a goal is reached or a stop condition fires. In practice this guide treats anything that runs a model with tool use across more than one step as an "agent."

**Tool / Tool use / Function calling.** A structured way to let a model call code, an API, or a connector. ChatGPT and OpenAI APIs use the term "tool calling" / "function calling" (see the [OpenAI docs](https://developers.openai.com/api/docs/guides/tools)). Claude uses "tool use" (see the [Anthropic docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). Gemini uses "function calling" / "tools" (see the [Gemini API docs](https://ai.google.dev/gemini-api/docs)).

**MCP (Model Context Protocol).** An open protocol — primarily driven by Anthropic and adopted by other vendors — for connecting LLM clients to data sources and tools through standardized servers. See the [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18).

**MCP server.** A process that exposes resources, prompts, and tools over MCP. Can be local (stdio) or remote (HTTP/SSE).

**MCP client.** A host application that talks to MCP servers. Examples include Claude Desktop, Claude Code, and various IDE plugins.

**Connector (Claude).** Anthropic's user-facing name for an integration. Custom connectors use remote MCP under the hood. See [Claude support: connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities).

**Project (Claude / ChatGPT).** A workspace concept that bundles instructions, files, and conversation history. Distinct from a "Custom GPT" in ChatGPT. See [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) and Anthropic's project surfaces.

**Custom GPT (ChatGPT).** A configurable variant of ChatGPT with custom instructions, knowledge files, and actions. Distinct from a "Project." See [Creating and editing GPTs](https://help.openai.com/en/articles/8554397).

**Custom instructions.** Persistent instructions applied to all conversations on a given surface. ChatGPT, Claude, and Gemini all expose a version.

**Codex CLI.** OpenAI's local terminal coding agent. See <https://developers.openai.com/codex/cli> and <https://github.com/openai/codex>.

**Codex (cloud).** OpenAI's cloud-side coding agent surface, accessed from ChatGPT.

**Agents SDK (OpenAI).** A Python framework for building agents that orchestrate models, tools, handoffs, and guardrails. See <https://github.com/openai/openai-agents-python>.

**Antigravity (Google).** An agent-first IDE from Google built around Gemini. See [Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity).

**Gemini CLI.** Google's open-source command-line agent for Gemini. See <https://github.com/google-gemini/gemini-cli>.

**Google AI Studio.** Google's web playground and API key management surface for the Gemini API. See <https://ai.google.dev/aistudio>.

**Computer use.** A capability where a model controls a virtual computer (mouse, keyboard, screen). Anthropic's tool: [computer-use-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool). OpenAI's tool: [Computer-Using Agent](https://openai.com/index/computer-using-agent/).

**browser-use (library).** An open-source Python library for letting LLMs drive a real browser. See <https://github.com/browser-use/browser-use>.

**GitHub Copilot cloud agent.** A cloud agent that opens PRs against your repo, distinct from the in-editor Copilot. It was formerly called Copilot coding agent. See [About GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent).

**Eval / Eval set.** A reproducible set of inputs + expected behaviors used to measure agent quality across changes.

**Red team.** A deliberate effort to find failure modes — prompt injection, data exfiltration, unsafe tool use — before users do.

**Human-in-the-loop (HITL).** A pattern where the agent pauses for human review before high-impact tool calls.

**Drift risk.** A subjective rating in this guide for how quickly a page is likely to go stale. *Low* = stable for ≥1 year. *Medium* = re-check quarterly. *High* = re-check monthly.
