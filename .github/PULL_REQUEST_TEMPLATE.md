# Pull request

## What does this change?

<!-- Short summary. One paragraph. -->

## Why?

<!-- What problem does this solve? Link any related issue. -->

## Type of change

- [ ] New page or section
- [ ] Edit to an existing page
- [ ] Source/drift refresh (vendor docs changed)
- [ ] New recipe or starter kit
- [ ] Eval / red-team additions
- [ ] Repo hygiene (workflows, templates, deps)
- [ ] Other (describe)

## Sourcing checklist

- [ ] Every product claim links an **official vendor doc**.
- [ ] Each affected page has an updated **`Last verified:`** date.
- [ ] Non-doc claims are explicitly labeled **"practical inference"**.
- [ ] New canonical URLs were added to [`docs/source-map.md`](../docs/source-map.md).

## Safety checklist

- [ ] No real API keys, tokens, or secrets in any example.
- [ ] No real PII, PHI, or personal data in examples (synthetic only).
- [ ] No new background automations, schedulers, or recurring agents.
- [ ] Any runner scripts are **inert by default** and require an explicit env var to run.

## Build & links

- [ ] `mkdocs build --strict` passes locally.
- [ ] Internal links resolve.
- [ ] If you added pages, they appear in the `nav` section of [`mkdocs.yml`](../mkdocs.yml).

## Notes for reviewers

<!-- Anything reviewers should pay extra attention to. -->
