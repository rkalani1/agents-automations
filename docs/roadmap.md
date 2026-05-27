# Roadmap

This roadmap is a living document. Items are not promises; they reflect the maintainers' current intent.

The strategy is **subscription-first**: anyone with a normal AI subscription should get full value from this site without API keys, CLIs, or code. Developer Mode is a real path, but it is a path users opt into.

## Done in v0.5 (subscription-first expansion)

- Beginner / Power User / Builder / Developer mode selector in the Task Builder.
- Provider-specific packages ("Use this in Claude / ChatGPT / Gemini / Grok / Perplexity / Copilot / Other").
- Practice exercise + "what good output looks like" + Plans + Maximize-my-subscription + Expert-expansion outputs.
- New top-level sections: Capability map, No-code automations, Memory & preferences, Examples, Learning path.
- 13 beginner examples + the universal 7-mission learning path.
- Plain-English glossary with schematic diagrams for ChatGPT Project / Task, Claude Project / Skill / Cowork, Gemini Gem / Scheduled action, Grok chat.
- Traceability files updated; all 16 user requirements + the 24 acceptance criteria mapped.

## Now (next ~30 days)

- Replace schematic SVG diagrams with annotated screenshots on a quarterly cadence (auth-redacted).
- Add 5 more beginner examples driven by reader requests.
- Verify every product page against current vendor docs and refresh the `Last verified:` line.
- Add a per-page Plan-availability shorthand legend at the top of every Mastery page (consistency pass).

## Next (~30–90 days)

- Localization: a parallel French + Spanish track for the homepage, learning path, and capability map.
- Add a chapter on **observability for subscription users** — what each app surfaces about a chat (logs, share links, audit trails), without API access.
- Expand the No-code automation guide with platform-specific cost-cap guidance (token caps, message caps, runs-per-day).
- Add an "AI for non-knowledge-work" examples track (parents, drivers, tradespeople, students at any age).

## Later

- A self-graded eval set per provider that users can run by hand to score their AI on their own work.
- An offline / disconnected mode page for users in low-bandwidth or air-gapped contexts.
- A self-hosted alternative to GitHub Pages for organisations that cannot publish externally.

## Out of scope (for now)

- Vendor-specific deep dives that duplicate official docs. We summarise and link.
- Reviews of unreleased products. We wait for GA + a public doc page.
- Anything that requires running code on a schedule by default. Schedulers stay opt-in and manual; native scheduled actions are documented but never recommended without a 3-run drill.
- Recommending API keys or developer tooling to users who said they're beginners.

## Contributing to the roadmap

Open a GitHub Issue with the label `roadmap` and a short proposal. Material changes land as Architecture Decision Records under [`decision-records/`](decision-records/index.md).
