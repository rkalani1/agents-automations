# Changelog

All notable changes to this guide are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The repo-root mirror lives at [`/CHANGELOG.md`](https://github.com/example/agent-builder-field-guide/blob/main/CHANGELOG.md).

## [0.6.1] — 2026-05-06 — Standalone Claude site

### Changed
- Claude guidance now lives at the separate [Claude site](https://claude.ai/) instead of inside the Field Guide navigation.
- Homepage, Mastery hub, examples, source audit, and Claude redirect page now point to the standalone site.
- Removed Field Guide loading of the Claude-only CSS and JavaScript assets.

### Verified
- Claude source links were refreshed against official Anthropic docs, including the current canonical plan chooser URL.

## [0.6.0] — 2026-05-06 — Claude Mastery microsite

### Added
- **[Claude Mastery](claude-mastery/index.md)** — a beginner-first, step-by-step Claude setup and mastery microsite with a path picker, local progress checklist, copyable prompt kit, Projects walkthrough, feature map, 30-day practice plan, and safety baseline.
- Scoped `claude-mastery.css` and `claude-mastery.js` assets. The checklist persists only in the visitor's browser via `localStorage`; copy buttons use the browser Clipboard API and make no network calls.

### Changed
- Homepage now surfaces Claude Mastery as a first-class starting point for readers learning Claude specifically.
- The older `mastery/claude.md` track now points readers to the dedicated Claude Mastery microsite to avoid duplicated, drifting Claude guidance.

### Verified
- Claude feature claims rechecked against current official Anthropic sources for plans, usage limits, personalization, Projects, memory, incognito chats, Artifacts, Skills, connectors, Claude Code, and prompting best practices.

## [0.5.2] — 2026-05-06 — Audit remediation and source refresh

### Changed
- Homepage now has a "Pick the right starting point" routing table for absolute beginners, subscription maximizers, product choosers, agent builders, and team/sensitive-data owners.
- GitHub Copilot references now use the current **Copilot cloud agent** name, with "formerly Copilot coding agent" retained only where it clarifies vendor renaming.
- Copilot cloud agent availability and billing guidance now reflects the current GitHub Docs: Pro, Pro+, Business, and Enterprise availability; Business/Enterprise policy enablement; premium-request usage per cloud-agent session and steering comment.
- xAI model links now use the current canonical `docs.x.ai/developers/models` URL, and Grok API examples default to the currently documented `grok-4.3` model identifier while still reading from `XAI_MODEL`.
- The MkDocs Material header repo widget was removed to avoid unauthenticated GitHub API calls and possible 403 console errors in visitor browsers.
- OpenAI recipe snippets now use `OPENAI_MODEL` instead of stale hard-coded model IDs, and beginner setup steps include the matching env var.
- Exact live-cost claims were removed from recipes; cost sections now describe token drivers and tell readers to recalculate against current vendor pricing.
- Structured-output language now tells readers to validate returned objects locally instead of treating provider-side schema constraints as a substitute for production validation.
- Browser/computer-use comparison now marks `computer-use-preview` as legacy and reflects current OpenAI `computer` tool guidance.

### Verified
- Source refresh checked current official GitHub Copilot cloud-agent docs, GitHub Copilot requests/billing docs, xAI structured-output docs, xAI model docs, and OpenAI computer-use docs.
- Site QA now guards against stale xAI model URLs, stale Copilot cloud-agent billing language, hard-coded older OpenAI model IDs, and exact live-cost claims.

## [0.5.0] — 2026-05-06 — Subscription-first expansion (deepening pass)

### Added
- **[Capability map](capability-map/index.md)** — cross-product matrix covering 18 capability rows across Claude / ChatGPT / Gemini / Grok / Perplexity / Copilot / "any AI tool" with plan-availability tags and per-cell fallbacks.
- **[No-code automation guide](no-code-automations/index.md)** — ChatGPT Tasks, Gemini scheduled actions, Claude Cowork, calendar-driven manual fallback, plus the safety drill (3 manual runs, off-switch, cost cap).
- **[Memory & preferences guide](preferences-memory/index.md)** — portable AI profile, global vs project memory, migration playbook, 6 copy-paste templates.
- **[Examples library](examples/index.md)** — 13 beginner-to-expert guided examples, each with a 6-layer ladder (chat → project → memory → native task → custom assistant → dev/API).
- **[Universal 7-mission learning path](learning-path/index.md)** — the no-API on-ramp from "I have a subscription" to "I'm getting full value."
- **[Plain-English glossary](glossary-plain.md)** with schematic SVG diagrams for ChatGPT Project & Task, Claude Project / Skill / Cowork, Gemini Gem / Scheduled action, Grok chat.
- **Task Builder v0.5**: 4-tier mode selector (Beginner / Power User / Builder / Developer), 7 new output panels (Use this in…, Learning ladder, What good output looks like, Practice exercise, Free vs paid, Maximize my subscription, Expert expansion). Provider packages render for all 7 surfaces with the user's primary app first.
- Repo-root `SUBSCRIPTION_FIRST_EXPANSION_STATUS.md` and `USER_REQUIREMENTS_TRACEABILITY.md` extended; `docs/product-requirements/user-requirements-traceability.md` mirrors them.

### Changed
- Homepage card grid expanded with Learning path, Capability map, No-code automations, Memory, Examples.
- mkdocs.yml nav re-ordered: Task Builder → Learning path → Mastery → Capability map → Examples → No-code automations → Memory → Surface router → (rest unchanged).
- Roadmap rewritten to reflect the subscription-first strategy and what landed in v0.5.
- Source map gains a v0.5 "Subscription-first vendor surfaces" section; source audit gains a v0.5 audit entry.

### Verified
- `mkdocs build --strict` exits 0.
- Beginner / Power User / Builder modes never recommend API / CLI / MCP / local scripts.
- Task Builder JS contains no `fetch`, `XMLHttpRequest`, `WebSocket`, `sendBeacon`, dynamic script loading, or analytics calls (only commented references to those names exist as guardrails).
- All runnable scripts in starter kits remain gated behind `OPERATOR_APPROVED_TO_RUN=1`.
- All 16 user requirements and all 24 acceptance criteria are mapped to implementations in the traceability files.

## [0.4.0] — 2026-05-06 — Subscription-first expansion

### Added
- **[Mastery](mastery/index.md)** section: index plus 7 beginner-to-expert tracks for Claude, ChatGPT, Gemini, Grok, Perplexity, Coding agents, and "Any AI tool / I don't know."
- **Task Builder Beginner Mode** (the new default) plus a primary-app picker, a comfort-level picker, a 16-option job picker, and two new output panels: **Level up this workflow** and **If your plan doesn't have this**.
- A **What to click** output panel with exact step-by-step instructions per AI app.
- [User requirements traceability](product-requirements/user-requirements-traceability.md) page mapping every user requirement to its implementation.

### Changed
- Homepage opens with "No API key required. Start with the AI app you already use."
- Task Builder page rewritten with primary-app + comfort + job at the top.
- Advanced surface picker is hidden in Beginner Mode.

### Verified
- `mkdocs build --strict` exits 0.
- Beginner Mode never recommends API/CLI/MCP/local scripts.
- Task Builder JS contains no network calls.

## [0.3.0] — 2026-05-06 — Task Builder transformation

### Added
- **Task Builder** — a static, browser-local tool that turns a task description into a recommended surface plus a complete package (prompt, system instructions, memory block, setup, tool allowlist, HITL gates, evals, red-team probes, repeat-run playbook, troubleshooting, exportable JSON).
- **Surface router** — long-form decision matrix for chat vs. project vs. coding agent vs. skill vs. automation vs. agent vs. browser-use vs. MCP.
- **Grok / xAI coverage** — platform page, quickstart, two recipes (structured outputs and tool calling). Distinguishes consumer Grok, Grok on X, and the xAI API.
- **Model freshness** page — env-var pattern (`OPENAI_MODEL`, `ANTHROPIC_MODEL`, `GEMINI_MODEL`, `XAI_MODEL`) and a quarterly drift checklist.
- ADR 0004 documenting the recipe nav pattern.
- `IMPROVEMENT_PASS_STATUS.md` at the repo root.

### Changed
- Homepage rewritten as a task-to-outcome on-ramp.
- Platforms index gains an xAI / Grok row.
- Source map and source audit include xAI / Grok.

### Fixed
- **MCP starter-kit approval bypass** removed from both Python and TypeScript MCP servers; `OPERATOR_APPROVED_TO_RUN=1` is now unconditionally required.
- **Deployment claims** corrected in `DEPLOYMENT_STATUS.md`, the root `CHANGELOG.md`, and this page.
- **Link check gating** split into a gating internal-links job and an advisory external-links job.
- **Model currentness** fixed in `starter-kits/local-script-agent/script.py` (now reads `OPENAI_MODEL`).

### Verified
- `mkdocs build --strict` exits 0.
- The Task Builder JavaScript contains no network calls.
- All v0.2 work preserved.

## [0.2.0] — 2026-05-06 — Productionization pass

### Added
- **Quickstarts** — five end-to-end recipes (read-only, file-editing, coding, browser, MCP).
- **Recipe library** — 40+ complete agent recipes covering common workflows.
- **Starter kits** — nine copyable kits with specs, prompts, allowlists, eval/red-team JSONL, and launch checklists. Example scripts are inert by default.
- **Eval banks** — 100+ golden cases and 100+ red-team cases with rubrics and per-platform usage notes.
- **Agent Factory module** — a 25-candidate → 5-shipped worked example.
- **Source audit** — a record of which pages were rechecked against which official URLs.
- **Repo hygiene** — issue/PR templates, Dependabot, PR build workflow, link-check workflow.
- **Deployment docs** — `DEPLOYMENT_STATUS.md` and `PRODUCTION_DEPLOYMENT.md` at repo root.

### Changed
- Removed all "(coming soon)" labels from the Platforms index — every page exists and is linked.
- Nav label `Safety/safety-checklists` corrected to `Safety checklists`.
- Source map expanded with additional Anthropic, OpenAI, Google, GitHub, and MCP references.

### Verified
- `mkdocs build --strict` exits 0. The build emits an upstream Material for MkDocs informational banner about the future MkDocs 2.0 release (theme-level, not a project warning) and INFO-level notices for the 41 recipes accessed through the [Recipes index](recipes/index.md) — see [ADR 0004](decision-records/0004-recipe-nav-pattern.md).
- GitHub Pages production deployment succeeds.

## [0.1.0] — 2026-05-06

### Added
- Initial public release of the **AI Agent Builder Field Guide**.
- Start Here section: what an agent is, good/bad tasks, decision tree, four setup paths, safety baseline.
- Platform setup guides for Claude Desktop, Claude Code, Claude Projects, Gemini app, Gemini CLI, Antigravity, Google AI Studio, ChatGPT, Custom GPTs, OpenAI API/Agents SDK, Codex CLI, GitHub Copilot cloud agent, and local scripts/schedulers.
- MCP section: concepts, installation, writing servers, remote/custom connectors, security.
- Browser & computer use section: Anthropic, OpenAI, `browser-use`, operating boundaries.
- Orchestration section: single-agent loops, multi-agent patterns, local-first, state/memory.
- Evaluation & safety section: eval sets, red-team workflows, safety checklists, HITL, incident response.
- Templates: agent spec, prompt, eval rubric, safety checklist, agent PRD.
- Reference: glossary, source map, roadmap, decision records.
- MkDocs Material build, GitHub Actions deploy workflow, MIT license, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.

### Source verification
- All product pages verified against the official sources listed in [`source-map.md`](source-map.md) on 2026-05-06.
