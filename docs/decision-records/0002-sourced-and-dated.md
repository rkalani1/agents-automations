# 0002 — Vendor-neutral, sourced-and-dated content model

- **Status:** Accepted
- **Date:** 2026-05-06
- **Deciders:** maintainers

## Context

Vendor docs in this space change weekly. Product names get renamed (Bard → Gemini, Anthropic Claude.ai connectors getting renamed/repositioned, Codex repackaged across CLI and cloud surfaces, etc.). Most third-party guides go stale within months and silently mislead readers.

## Decision

Every product page must include, at the top:

```
Last verified: YYYY-MM-DD
Official sources: <links>
Drift risk: low | medium | high
```

And every product claim in the page body must be one of:

- **Confirmed by docs** with a link, or
- **Practical inference** clearly labeled as such, or
- **Known drift risk** explicitly called out.

## Consequences

- **Pros**
  - Readers can quickly tell whether a page is current.
  - Drift becomes a normal maintenance task, not an emergency.
  - Reduces the amount of vendor PR copy that creeps into the guide.
- **Cons**
  - More overhead per edit (date update, source check).
  - Pages that go un-touched for long periods need scheduled re-verification.

## Alternatives considered

- **Single global "last updated" stamp** — too coarse; doesn't help readers spot a page that's specifically stale.
- **No dating** — what most third-party guides do, and the reason most third-party guides are unreliable.
