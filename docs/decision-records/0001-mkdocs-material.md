# 0001 — Use MkDocs Material on GitHub Pages

- **Status:** Accepted
- **Date:** 2026-05-06
- **Deciders:** maintainers

## Context

The guide needs a public, low-friction documentation site that:

- builds reproducibly from Markdown,
- has good search and code-block UX out of the box,
- has zero runtime dependencies once deployed,
- and can be hosted on GitHub Pages without paid services.

We considered Docusaurus, plain Jekyll, Astro Starlight, and MkDocs Material.

## Decision

Use **MkDocs Material** with a GitHub Actions workflow that publishes to GitHub Pages via `actions/deploy-pages@v4`.

## Consequences

- **Pros**
  - Mature, low-maintenance, batteries-included theme.
  - Excellent code blocks, admonitions, and content tabs — well suited to a setup-guide format.
  - Pure Python toolchain; one `requirements.txt` line.
  - First-party guidance for GitHub Pages publishing exists in the [MkDocs Material docs](https://squidfunk.github.io/mkdocs-material/publishing-your-site/).
- **Cons**
  - Themed React components (e.g. interactive widgets) are harder than in Docusaurus.
  - Heavy custom theming requires CSS overrides rather than a component model.

## Alternatives considered

- **Docusaurus** — more flexible component model, but heavier toolchain (Node, Yarn, MDX) and overkill for static reference docs.
- **Jekyll (default GH Pages)** — extremely simple, but the default themes are dated and search is poor.
- **Astro Starlight** — promising, but more moving parts than we need.
