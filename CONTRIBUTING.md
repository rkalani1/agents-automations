# Contributing

Thanks for considering a contribution to the AI Agent Builder Field Guide. This is a living guide; the agent space changes weekly, and good PRs are very welcome.

## Ground rules

1. **Cite official sources** for any product claim. If a vendor doc disagrees with the page, the vendor doc wins — open an issue or PR.
2. **No hallucinated features.** If you can't find a feature in official docs, mark it as a "practical inference" or omit it.
3. **No secrets in examples.** Replace API keys, tokens, emails, and clinical data with placeholders.
4. **No automated job/agent code that runs on a schedule by default.** Schedulers are documented as manual examples only.
5. **Date everything.** Every product page has a `Last verified:` line at the top. Update it when you edit the page.

## Workflow

1. Fork the repo and create a branch: `git checkout -b feat/short-description`.
2. Run the site locally:
   ```bash
   pip install -r requirements.txt
   mkdocs serve
   ```
3. Make your changes, including:
   - Updating `Last verified:` on any page you edit.
   - Adding new sources to `docs/source-map.md`.
   - Adding a changelog entry to `docs/changelog.md`.
4. Open a PR. Describe what you changed, why, and which official docs you consulted.

## Style

- Use sentence case in headings.
- Prefer short paragraphs and bulleted lists.
- Code blocks should be runnable as-is by a non-expert (or clearly marked as snippets).
- Use admonitions (`!!! note`, `!!! warning`, `!!! tip`) sparingly and only when they add value.
- Avoid marketing language. Be specific about what works and what doesn't.

## Decision records

Material architecture or scope changes should land as an Architecture Decision Record under `docs/decision-records/`. Use the template at `docs/decision-records/0000-template.md`.

## Reporting issues

Use GitHub Issues. For security-sensitive issues, see [SECURITY.md](SECURITY.md).
