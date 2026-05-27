# Example: build a simple website

> **Last verified:** 2026-05-06 · **Time:** 30–60 minutes · **No API key required for chat**

A one-page personal site (about me, projects, contact) using only an AI chat product — no installs, no terminal.

## Layer 1 — Chat only `Free`

```
Help me build a one-page personal website.

About me: <2 lines>
Sections: About / Projects / Contact / Links
Style: minimal, sentence-case headers, no animations, accessible.
Output: a single file `index.html` with inlined CSS. No external scripts. Mobile-friendly.
Constraints: no tracking, no third-party fonts, no forms that collect data.
After the file, give me 5 lines of plain English explaining how to host it for free on GitHub Pages.
```

How to tell whether it worked: paste the HTML into a `.html` file, double-click to open it locally, see your site.

Hosting: drag `index.html` into a GitHub Pages repo (per the AI's instructions). No code editor required.

## Layer 2 — Project `Sub`

Build a "Personal site" Project. Knowledge files: your bio doc, a list of projects with 1-line descriptions, your headshot. Each iteration = one chat in the Project.

**Best surface:** Claude or ChatGPT with their canvas/Artifacts feature. You can iterate on the HTML side-by-side.

## Layer 3 — Memory `Sub`

Add to memory:

```
- For website work: minimal, accessible (WCAG AA), no third-party trackers, no auto-loaded fonts, no animations.
- Mobile-friendly defaults. Inlined CSS unless I ask otherwise.
```

## Layer 4 — Scheduled action

Not a typical scheduled task. Closest: a quarterly "review my site" reminder.

## Layer 5 — Custom assistant `Sub`

Custom GPT / Gem / Skill "Personal site":

- **Knowledge file**: your bio, projects list, design preferences.
- **Sample prompts**: "draft an About update," "add a Projects entry," "add a Now page."

## Layer 6 — Developer / API (optional, advanced)

For a real codebase: GitHub Copilot or Claude Code, with a static site generator (e.g., MkDocs Material like this very site, or 11ty). See [Mastery — Coding agents](../mastery/coding-agents.md). Only worth it if you'll iterate weekly.

## Make it reusable

- Save the project HTML in a GitHub repo. Re-prompt for incremental changes.
- Keep a `CHANGELOG.md` in the repo.

## Make it robust

- **Eval**: validate HTML at the W3C validator. Check colour contrast (Lighthouse).
- **Red-team**: ask the AI to add tracking. It should refuse per your memory rules.
- **Drift check**: yearly, ask the AI for one improvement.

## What good output looks like

- One file, mobile-friendly, accessible.
- No external requests.
- HTML you can read and edit by hand.

## If your plan doesn't have this feature

- No canvas / Artifacts → ask for the file in a code block; paste into a `.html`.
- No Project → paste bio + preferences each time.
- No Custom GPT → save the prompt.

## See also

- [Mastery — Coding agents](../mastery/coding-agents.md)
- [Examples — Build a small app](build-small-app.md)
