# Capability map

> **Last verified:** 2026-05-06 · **Drift risk:** medium (vendor product names and plan tiers change quarterly — see [Model freshness](../model-freshness.md))

This is the cross-product matrix for picking — and switching — AI tools. Each cell labels availability with one of:

- **Free** — works on the free plan with no payment.
- **Paid** — requires a paid consumer subscription (e.g., Plus / Pro / Advanced / SuperGrok / Pro).
- **Team / Ent** — requires a Team or Enterprise plan, or admin enablement.
- **Dev / API** — requires API keys, a developer console, CLI, or SDK access.
- **Not primary** — the product technically allows it but it is not a strength; prefer a fallback.
- **N/A** — not offered.

Every row also lists a **fallback** — the manual or saved-prompt workflow that imitates the capability when your plan does not include it.

## Legend at a glance

| Tag | Meaning |
|---|---|
| `Free` | Anyone with the product can do this without paying. |
| `Paid` | Standard paid consumer subscription unlocks it. |
| `Team / Ent` | Requires Team / Business / Enterprise tier or admin toggle. |
| `Dev / API` | Requires API key, developer console, or SDK — not a normal subscription path. |
| `Not primary` | The capability technically works but is not the right tool — prefer the fallback. |
| `N/A` | Genuinely not offered today. |

## How to read this map

1. Find the row for the capability you want.
2. Look at the column for the AI you already pay for.
3. If the cell is `Free` or `Paid`, follow the linked Mastery section.
4. If the cell is `Team / Ent`, `Dev / API`, `Not primary`, or `N/A`, use the **fallback** in the rightmost column.
5. If two products both qualify, the [Surface router](../surface-router/index.md) and the [When to switch tools](../mastery/index.md#when-to-switch-tools) section in Mastery help you pick.

## Capability table

The table below uses short labels per cell. Click the capability name in the first column to jump to the deep dive. Anything labelled `Dev / API` is hidden in Beginner Mode of the [Task Builder](../task-builder/index.md).

### Core conversational

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **One-off chat** | Free | Free | Free | Free | Free | Free (in editor / on github.com) | Free | Use whatever chat box your product offers; save the prompt as a note. |
| **Reusable prompt** (saved/pinned) | Paid (Project + saved instructions) | Free / Paid (Custom Instructions; saved messages) | Paid (Saved info; Gem) | Paid (saved chats; persona on plans that have it) | Paid (Space system prompt) | Free (`.github/prompts/*.md` in repo, slash-prompts) | Free (paste from a notes app) | Maintain a plain-text **Prompt vault** in your notes app and paste before every run. |
| **Project / workspace** | Paid (Projects) | Paid (Projects) | Paid (Gems are the closest) | Paid (Spaces / Workspaces where available) | Paid (Spaces) | Free (`.github/copilot-instructions.md`) | N/A | Use a single chat thread per topic; pin the system prompt at the top of each thread. |

### Memory and context

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Memory / saved preferences** | Paid (profile preferences; project memory) | Paid (Memory; Custom Instructions) | Paid (Saved info) | Paid (where rolled out) | Paid (profile personalisation) | Free (`copilot-instructions.md` is the equivalent; per-repo) | Varies | Maintain a portable [AI profile](../preferences-memory/index.md#portable-ai-profile) in a `.md` file and paste at the start of new chats. |
| **Uploaded files / sources** | Paid (Project knowledge; chat attachments) | Paid (chat & Project files; canvas) | Paid (Drive integration; chat upload) | Paid (image + file upload on consumer) | Paid (Space sources; per-search files) | Free (the repo *is* the context) | Varies | If file upload is missing, paste the relevant excerpt inline (chunk it under ~10k chars). |
| **Long-context citation reading** | Paid | Paid | Paid | Paid (image OCR + file) | Paid (built-in for web) | Not primary | Varies | Summarise to bullets manually before pasting into the chat with weaker context handling. |

### Reusable assistants

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Custom assistant** (named, instructions + knowledge) | Paid (Project ≈ assistant) | Paid (Custom GPT) | Paid (Gem) | Paid (custom persona on plans that have it; otherwise saved chat) | Paid (Space ≈ assistant) | Free (Copilot Extensions on enabled plans; otherwise repo prompts) | N/A | Save a "system prompt + 3 examples + output format" doc and paste it as the first message of any chat. |
| **Skill** (packaged instructions + templates + resources) | Paid (Claude Skills, `SKILL.md`) | Paid (Custom GPT with Knowledge files) | Paid (Gem with attached files) | Not primary | Not primary | Free / Team (custom slash-prompts; Copilot Extensions) | N/A | Author a folder with `INSTRUCTIONS.md` + templates + examples; paste contents on demand. |
| **Sharing assistants with others** | Team / Ent (Project sharing) | Paid (Custom GPT public/link share); Team/Ent (workspace) | Paid (Gem share by link); Workspace plans for org sharing | Limited (chat link share) | Paid (Space share) | Team / Ent (organization Extensions) | Varies | Share the assistant's source-of-truth doc in your team drive and ask people to paste it. |

### Native automations

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Native task / scheduled action** | Paid (Cowork scheduled tasks where rolled out) | Paid (Tasks where rolled out) | Paid (Scheduled actions on Advanced where rolled out) | Not primary | Not primary | Not primary (use GitHub Actions in Dev / API) | Varies | Calendar reminder + saved prompt; run it manually each morning. See the [No-code automation guide](../no-code-automations/index.md). |
| **Connectors** (Email, Calendar, Drive, etc.) | Paid (selected connectors) | Paid (selected connectors) | Paid (Workspace integration) | Limited | Limited | N/A (uses repo + GitHub APIs) | Varies | Copy the email / calendar text manually into the chat; paste back into the source app. |

### Agent and computer-use modes

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Coworker / agent mode** | Paid (Claude with computer use, Cowork) | Paid (agent / browser modes where available) | Paid (Agent / Cowork on Advanced where rolled out) | Limited | Paid (Comet browser) | Paid (Copilot cloud agent on Pro, Pro+, Business, Enterprise) | Limited | Manual repeat-run playbook: human runs each step in the chat. See [No-code automations](../no-code-automations/index.md). |
| **Desktop / computer-use** | Paid (Claude Desktop with computer-use tool, sandbox) | Paid (where available) | Paid (where available) | N/A | Paid (Comet for browsing) | N/A | N/A | Use a screenshot + describe-and-click pattern in chat: paste a screenshot, ask the AI to tell you what to click. |

### Coding and developer

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Coding agent** | Dev / API (Claude Code CLI) | Dev / API (Codex CLI / cloud) | Dev / API (Gemini CLI / Antigravity) | Dev / API (xAI tool calling) | Not primary | **Free / Paid editor chat; Paid cloud agent** (Copilot cloud agent on issues) | N/A | In Beginner / Power-User mode: paste code into chat, ask for a unified diff, apply manually. |
| **API / SDK** | Dev / API | Dev / API | Dev / API | Dev / API | Dev / API | Dev / API (GitHub Models) | N/A | The Task Builder hides this entirely in Beginner Mode. Use the chat product instead. |

### Research and sharing

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Research / search with citations** | Paid (web search where enabled) | Paid (web search; Deep Research where rolled out) | Paid (Deep Research) | Paid (web search on consumer) | **Free / Paid** (this is its core) | Not primary | Limited | When the AI cannot cite, ask it to *list assumptions* and you verify each separately in a search engine. |
| **Shareable reports / pages** | Paid (Artifacts; Project export) | Paid (canvas export; share link) | Paid (Gem export; share link) | Limited (chat share) | Paid (Pages: research-as-article) | Free (commit a report.md to the repo) | Varies | Copy the chat into a Google Doc or Notion page and share that. |

### Audience and depth

| Capability | Claude | ChatGPT | Gemini | Grok | Perplexity | GitHub Copilot | Other / any AI chat | Fallback if missing |
|---|---|---|---|---|---|---|---|---|
| **Collaboration / team use** | Team / Ent (Project sharing, audit) | Team / Ent (Workspaces, Custom GPT sharing) | Team / Ent (Workspace integration, Gem org-share) | Team / Ent (limited) | Team / Ent (Spaces sharing) | Team / Ent (organisation policies) | Varies | Maintain a shared prompt-and-preferences doc in your team drive; everyone pastes it. |
| **Beginner-friendly no-code** | Free (chat) → Paid (Project) | Free (chat) → Paid (Project / Custom GPT / Tasks) | Free (chat) → Paid (Gem / scheduled action) | Free (chat) → Paid (persona) | Free (ask) → Paid (Space) | Free (Chat) | Varies | Stick to chat; save prompts to your notes app. |
| **Intermediate reusable workflow** | Paid (Projects + memory + Skills) | Paid (Projects + memory + Custom GPT + Tasks) | Paid (Gems + Scheduled actions) | Paid (Spaces + persona) | Paid (Spaces) | Free / Paid (repo prompts; Copilot Chat) | Varies | Build a prompt vault + checklist; iterate weekly. |
| **Expert / developer extensibility** | Dev / API (Claude Code, MCP, API) | Dev / API (OpenAI Agents SDK, Codex, MCP) | Dev / API (Gemini API, AI Studio, CLI) | Dev / API (xAI API) | Dev / API (Perplexity API / sonar) | Dev / API (GitHub Models, MCP via VS Code) | N/A | Stay in subscription mode if you do not need automation — most people do not. |

## How to use this map to choose

- **Choose ChatGPT** when you need a Custom GPT or Tasks, you live in OpenAI's Mac/Windows app, or you want a single tool that does most things well.
- **Choose Claude** when you need long-document reading, careful writing, Project knowledge, or Skills.
- **Choose Gemini** when you live in Google Workspace and want Drive/Docs/Calendar context.
- **Choose Grok** when you want personality, X integration, or a different second opinion.
- **Choose Perplexity** when the job is research with citations and shareable Pages.
- **Choose GitHub Copilot** when the job is in a code editor or a GitHub repo.
- **Choose "any AI tool"** if you do not know what you have, or you have something else (Mistral Le Chat, DeepSeek, Pi, Poe, Le Chat, Llama-based apps, your phone's built-in assistant, etc.). Use the [universal method](../mastery/any-ai-tool.md).

## When to switch mid-workflow

| Situation | Switch to | Why |
|---|---|---|
| You need many cited sources | Perplexity | Built-in retrieval and Pages output. |
| You're drafting a long document or report | Claude (Project) | Long context, careful style, Artifacts. |
| You want a custom assistant your team can use | ChatGPT (Custom GPT) or Gemini (Gem) | Easiest sharing surface today. |
| You're in a code repo | GitHub Copilot or Claude Code | Repo-aware tools. |
| You need email / calendar context | Gemini (Workspace) or ChatGPT (connectors) | Native connectors today. |
| You want a quick second opinion | Grok | Distinct personality + alternative model. |

## Plan-availability shorthand

The same shorthand is used on every Mastery page and in the Task Builder output:

> `Free` &nbsp;·&nbsp; `Sub` (paid consumer) &nbsp;·&nbsp; `Team / Ent` &nbsp;·&nbsp; `Dev / API` &nbsp;·&nbsp; `Not primary` &nbsp;·&nbsp; `N/A`

If a feature you want is `Team / Ent` or `Dev / API` and you do not have access, use the fallback in this map and check the matching Mastery page section for the manual workflow.

## See also

- [Mastery hub](../mastery/index.md) — provider-by-provider tracks.
- [No-code automation guide](../no-code-automations/index.md) — native tasks and safe fallbacks.
- [Memory and preferences guide](../preferences-memory/index.md) — portable AI profile and migration.
- [Surface router](../surface-router/index.md) — the prose decision tree behind this matrix.
- [Examples library](../examples/index.md) — guided beginner examples for every workflow shape.
