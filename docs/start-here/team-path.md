# Team path

> **Last verified:** 2026-05-06 · **Drift risk:** medium

Building with AI agents as a team introduces problems that do not exist for individual users: shared resources that drift, credentials that get embedded in scripts, data that should not cross team boundaries, and no one person who knows what the agent is doing. This page covers the organizational and technical practices that keep a team-level deployment from becoming a liability.

---

## Start with authentication and identity

Before sharing any AI resource with a team, answer:

- Who can access the agent and its tools?
- Can access be revoked instantly when someone leaves?
- Is access tied to individual identity (SSO) or a shared password?

All major platforms — OpenAI, Anthropic, Google — offer enterprise or team tiers with SSO support. Personal plan credentials shared via a group chat are not a team deployment. If your organization has an SSO provider (Okta, Azure AD, Google Workspace), connect the AI platform to it before onboarding anyone else.

!!! note
    Enterprise tier availability and pricing change frequently. Check each platform's current pricing page directly. This guide does not enumerate pricing.

---

## Shared Custom GPTs vs. shared Projects

These are different things:

- **[Custom GPTs](https://help.openai.com/en/articles/8554397)** are published assistants with a system prompt, optional tools, and an optional knowledge base. You can share them with a team (within a ChatGPT Team or Enterprise org). They are designed to be consumed by many users but configured by few.
- **[Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)** in ChatGPT organize conversations and files for a single user or a shared workspace. They are more flexible but less governed.

For team deployment, Custom GPTs are usually the right unit: one person (or a small ops team) owns the configuration; everyone else uses it. This separates the people who tune the assistant from the people who use it.

The same principle applies on Claude.ai: a shared Project with governed custom instructions, owned by a named admin, is more maintainable than individual projects each team member configures on their own.

---

## Define knowledge boundaries before uploading anything

"What can the agent see?" is a question with compliance implications. Before attaching any files or data sources to a shared assistant:

- Classify the data: is it internal, confidential, or public?
- Establish who is allowed to see model outputs derived from that data.
- Do not attach data to a shared assistant that not all users of that assistant are authorized to see.

For workflows involving PII or PHI (personal health information), consult your organization's legal and compliance teams before proceeding. This guide does not give legal or compliance advice. Data handling requirements vary by jurisdiction, industry, and contract.

!!! warning
    Attaching a file to a shared AI project may make its content accessible to all users of that project, depending on how the platform handles retrieval. Verify the platform's data isolation guarantees before sharing sensitive files.

---

## Audit logs

Before deploying any agent that takes actions (sends messages, writes files, calls APIs), verify that you have an audit trail:

- What action was taken?
- What input triggered it?
- When did it happen?
- Which user or system invoked it?

Most enterprise tiers include audit log exports. If you are using the API directly, instrument your own logging at the application layer. Logs should be write-once (append only, not editable) and retained long enough to support your incident response process.

---

## Centralize API key management

Shared API keys embedded in scripts, environment files, or Slack messages are a security incident waiting to happen. For team deployments:

- Use a secrets vault (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or equivalent) to store and rotate API keys.
- Grant access to the vault per-service and per-environment, not per-person.
- Rotate keys on a schedule and immediately after any suspected exposure.
- Audit which services and people have accessed which keys.

Do not use a single shared API key for all team members. If a key is compromised, you need to know which workloads used it.

---

## Evaluation as a team practice

Individual evals (see [Beginner path](beginner-path.md) and [Power-user path](power-user-path.md)) become a shared artifact at team scale:

- Store the eval set in version control alongside the prompt configuration.
- Run the eval set before any change to system prompts, model versions, or tool configuration goes to production.
- Assign an owner to the eval set — someone who updates it when the task scope changes.
- Review eval results as a team, not just as an individual. Different people catch different failure modes.

A shared eval set is also the primary tool for onboarding new team members: "here are 10 representative tasks and what good output looks like."

---

## Governance checklist before team launch

- [ ] SSO configured; access reviewable and revocable
- [ ] Named owner for each shared assistant or project
- [ ] Data classification done for all attached files and data sources
- [ ] Legal/compliance reviewed for any PII or regulated data
- [ ] Audit logging enabled and retention period set
- [ ] API keys in a vault, not in scripts or chat
- [ ] Eval set created, versioned, and documented
- [ ] Incident response plan: what happens if the agent takes an unexpected action?
- [ ] Offboarding process: what happens to shared resources when the owner leaves?
