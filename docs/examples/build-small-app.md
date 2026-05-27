# Example: build a small app

> **Last verified:** 2026-05-06 · **Time:** 1–3 hours for a working prototype · **No API key required for chat**

A small single-purpose app you actually use — a habit tracker, a vocabulary trainer, a packing-list generator. The chat-only path produces a real working app you can run locally; the developer path turns it into something maintainable.

## Layer 1 — Chat only `Free`

```
Help me build a small browser-based habit tracker.

What it does:
- 7-day grid of habits I define.
- Click to mark a day done. Persist in localStorage. No login.
- Reset button. Export-to-JSON button.

Constraints:
- Single `index.html` with inlined CSS + vanilla JS.
- No frameworks. No external CDNs. No tracking.
- Mobile-friendly. Keyboard-accessible.

After the code, give me a 5-line plain-English explanation of where data is saved (localStorage) and how to delete it.
```

Save as `tracker.html`, double-click, use.

## Layer 2 — Project `Sub`

"Small apps" Project. Knowledge file = your "always" rules (no trackers, no CDNs, accessible, mobile-friendly). Each chat = one app.

**Best surface:** Claude (Artifacts) or ChatGPT (Canvas) for iteration; Copilot if you'll run a real dev loop.

## Layer 3 — Memory `Sub`

```
- For small apps: vanilla JS, no frameworks, no external CDNs, no trackers, accessible, mobile-friendly.
- Always inline CSS unless I ask otherwise.
- Always include an export-to-JSON and a reset button for stateful apps.
```

## Layer 4 — Scheduled action

N/A. Closest: a "review usage" reminder once a month.

## Layer 5 — Custom assistant `Sub`

Custom GPT / Gem "Small apps coach": packs your style rules, gives you a prompt scaffold for each new app idea.

## Layer 6 — Developer / API (advanced) `Dev`

For real apps you'll maintain:

- **GitHub Copilot** in a real repo: `.github/copilot-instructions.md` with your conventions. See [Mastery — Coding agents](../mastery/coding-agents.md).
- **Claude Code / Codex CLI**: `CLAUDE.md` / `AGENTS.md` at repo root. Coding agents work well for small, well-scoped apps.
- **MCP**: when the app needs filesystem or repo access. See [docs/mcp/index.md](../mcp/index.md).

This Task Builder hides the developer path in Beginner Mode for a reason: most users are better served by a single-file chat-built app.

## Make it reusable

- Commit the file to a GitHub repo (free). Re-prompt for upgrades.
- Keep a `CHANGELOG.md`.

## Make it robust

- **Eval**: 5 user stories you walk through manually. Each must pass.
- **Red-team**: paste an "import" of malformed JSON. The app must not crash.
- **Drift check**: quarterly, ask the AI for one accessibility improvement.

## What good output looks like

- Works without an internet connection.
- Saves data locally only.
- Loads in under a second.
- Reads cleanly enough that you can hand-edit.

## If your plan doesn't have this feature

- No Artifacts / Canvas → ask for the file in a code block.
- No Project → paste rules each time.
- No Custom GPT → save the prompt.

## See also

- [Mastery — Coding agents](../mastery/coding-agents.md)
- [Examples — Build a simple website](build-simple-website.md)
