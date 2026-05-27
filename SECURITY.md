# Security policy

## Supported versions

The site is a documentation project; there are no released versions to support. The default branch (`main`) is what is deployed to GitHub Pages.

## Reporting a vulnerability

If you discover a security issue with the site itself (XSS in code blocks, leaked secrets in repo history, vulnerable dependencies in the build, etc.):

1. **Do not file a public GitHub Issue.**
2. Open a private security advisory under the **Security** tab → **Report a vulnerability**.
3. Include a description of the issue, steps to reproduce, and your contact info.

We will acknowledge within a reasonable time and coordinate a fix.

## What is in scope

- The MkDocs Material site source under `docs/`.
- The GitHub Actions workflows under `.github/workflows/`.
- The `mkdocs.yml` and `requirements.txt` build configuration.

## What is out of scope

- Vulnerabilities in third-party platforms documented in this guide (Claude, Gemini, ChatGPT, OpenAI, Codex, GitHub Copilot, MCP servers, etc.). Report those to the respective vendors.
- Editorial disagreements about a recommendation. Open a normal GitHub Issue for those.

## Secrets

This repository should never contain real API keys, OAuth tokens, personal access tokens, patient or clinical data, or other secrets. If you find one, please report it via the private advisory flow above so we can rotate and rewrite history.
