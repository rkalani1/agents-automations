# Surface router

> **Last verified:** 2026-05-06 · **Drift risk:** low (this page is about shapes, not specific products)

Most "should I build an agent?" decisions actually decompose into a different question: **what shape should this work take?** This page is the long-form decision matrix that the [Task Builder](../task-builder/index.md) uses under the hood.

The shapes in scope are:

- **One-shot chat** — the cheapest, fastest, most under-used shape. Often it's all you need.
- **Reusable prompt** — a saved prompt you paste into a chat surface.
- **Project** (Claude Project / ChatGPT Project / Gemini Gem) — a named workspace with persistent instructions and files.
- **Custom GPT / Gem / Grok persona** — a configurable personality + knowledge files + optional Actions, shareable.
- **Coding agent** (Claude Code / Codex CLI / Copilot cloud agent / Antigravity) — a process that edits a repo, runs tests, and opens PRs.
- **Skill** — a small, named, reusable unit of behavior — usually a prompt + a tool definition + a few examples.
- **Automation** — a script or workflow that runs on a schedule or trigger. Manual-first, by policy.
- **Agent** — a model-driven loop with tools, memory, and stop conditions. The most expensive shape.
- **Browser / computer-use workflow** — an agent that drives a sandboxed browser or VM.
- **MCP server / local script** — a programmatic substrate the AI talks to, not the AI itself.

## The 30-second decision

```
Does the work happen once?                       → One-shot chat
Will I redo this exact thing every week?         → Reusable prompt or Project
Does it touch a code repo?                       → Coding agent
Does it touch logged-in services?                → Project + connectors (or local scripts with SDKs)
Does it need browser / external sites?           → Browser-use workflow (sandbox)
Does it need real tool execution + decisions?    → Agent (programmatic SDK or coding agent)
Does it need to expose tools to other AIs?       → MCP server
Should it run while I'm asleep?                  → Stop. Promote later. Default is manual.
```

## The longer matrix

| Question | Answer | Recommended shape |
|---|---|---|
| Frequency | one-time | One-shot chat |
| Frequency | repeated manually | Reusable prompt → Project / Custom GPT / Gem |
| Frequency | scheduled / event-triggered | Manual-first; only after clean dry runs, promote to a small automation with an explicit gate |
| Touches | local files only | MCP filesystem (Claude Desktop) or local script |
| Touches | a code repo | Coding agent (Claude Code, Codex CLI, Copilot cloud agent, Antigravity) |
| Touches | email / calendar | Project + read-only connectors (draft-only by default) |
| Touches | a browser / external sites | Browser-use workflow inside a sandbox VM |
| Touches | a database | Programmatic SDK (OpenAI Agents SDK / Gemini / Grok function calling) with a SELECT-only tool |
| Touches | documents (PDF, DOCX, sheets) | Project (Claude / ChatGPT) or Custom GPT / Gem with knowledge files |
| Authority | draft only | Any chat surface; Project is best |
| Authority | act with approval | Programmatic agent with HITL gates, OR coding agent with strict approval mode |
| Authority | act within allowlist | Programmatic agent with strict tool allowlist + audit log |
| Sensitivity | none | Any consumer surface |
| Sensitivity | confidential | Enterprise tier or local scripts |
| Sensitivity | clinical / financial / legal | Local scripts or approved enterprise tier; never put PHI/PCI into consumer products |

## Six shape pitfalls

1. **Building an agent when a Project would do.** Projects are stateful, persistent, and free of orchestration code. Try one first.
2. **Building an automation before a clean manual run.** Schedulers turn small bugs into recurring failures. Run manually 3+ times first.
3. **Using a chat for actions.** Chats can pretend to take actions. Use a programmatic SDK or a coding agent if you actually need actions to fire.
4. **Letting an agent loose on a logged-in browser.** Computer-use needs a sandbox VM. Always.
5. **Skipping HITL for "just one quick thing."** That's how you accidentally email customers. Default to draft-only.
6. **Forgetting maintenance.** Every shape needs a `Last verified:` date and a maintenance cadence. See [Model freshness](../model-freshness.md).

## Shape × surface examples

| Shape | Example surfaces | Best for |
|---|---|---|
| One-shot chat | Claude / ChatGPT / Gemini / Grok / Perplexity | "Read this and summarize." |
| Reusable prompt | Any chat | "I do this exact thing every Monday." |
| Project | Claude Projects, ChatGPT Projects, Gemini Gems | "Same domain, many tasks, persistent files and style." |
| Custom GPT | ChatGPT Custom GPTs | "Sharable persona + knowledge + small Actions." |
| Coding agent (local) | Claude Code, Codex CLI | "Edit my repo while I watch." |
| Coding agent (cloud) | GitHub Copilot cloud agent, Codex cloud | "Open a PR for this issue." |
| Skill | Custom GPT Action, MCP tool, OpenAI Agents SDK tool | "One reusable capability across many agents." |
| Automation | Local Python + cron / launchd / GitHub Actions | "Run this exact recipe on Mondays — after I've run it manually 3 times." |
| Agent | OpenAI Agents SDK, Gemini SDK, Grok SDK, Claude SDK | "Decide between tools, loop, observe, stop." |
| Browser-use workflow | `browser-use`, Anthropic computer-use, OpenAI computer-use | "Drive a sandbox browser to extract structured data." |
| MCP server | Python / TypeScript SDKs | "Expose tools to whatever AI client the user picks." |

## When a shape is wrong, the symptom usually looks like

| Symptom | Likely wrong shape | Better shape |
|---|---|---|
| "I keep retyping the same setup at the top of every chat." | Chat | Project / Custom GPT / Gem |
| "It said it sent the email — but it didn't." | Chat | Programmatic agent + email tool, with HITL |
| "It rewrote files I didn't ask it to touch." | Open coding agent | Coding agent on a feature branch + diff review |
| "It opened a tab and got stuck on a CAPTCHA." | Browser-use against the public web | Use a public API instead, or a sandbox with explicit allowlist |
| "It started costing real money overnight." | Automation enabled too early | Manual-first; cap tokens; review logs daily for first 14 days |

## Where this lives in the guide

- [Task Builder](../task-builder/index.md) uses this matrix automatically.
- [Recipes](../recipes/index.md) are organized by the same shapes.
- [Templates](../template-library/index.md) gives you the blank spec for each shape.
- [Agent Factory](../agent-factory/index.md) walks the full lifecycle for a portfolio of agents.

## Source notes

- This page is intentionally vendor-neutral. Vendor specifics live in [`/platforms/`](../platforms/index.md).
- Specific model names and prices drift fast — see [Model freshness](../model-freshness.md).
