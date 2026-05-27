# Safety baseline

> **Last verified:** 2026-05-06 · **Drift risk:** low

This is a short, opinionated checklist. Work through it before you build anything that takes real actions or processes real data. It does not replace domain-specific risk assessment — it is the floor, not the ceiling.

---

## 1. Name the agent's job in one sentence

Write it down. "This agent reads PDFs from the `inbox/` folder, extracts structured fields into a CSV, and stops." If you cannot write this sentence, you are not ready to build.

The sentence becomes the first line of your system prompt and the first thing you check when something goes wrong.

---

## 2. Define stop conditions before the first run

Every agent needs at least two stop conditions:

- **Success:** what output or state means the task is complete?
- **Failure:** what error, count, or condition causes the agent to halt and alert rather than continue?

Document both. Hard-code a maximum step count as a circuit breaker even if you expect the agent to finish earlier. An agent with no step limit will run (and bill) until something crashes.

---

## 3. Restrict tools to least-privilege

Give the agent access to exactly the tools it needs for its named job. Nothing more.

- If it only needs to read files, do not give it write access.
- If it needs to call one API endpoint, do not give it a credential with broader scope.
- If it needs to search the web, do not also give it email access.

Revisit this list every time you expand the agent's task scope.

---

## 4. Require HITL for irreversible actions

If the agent can send messages, delete records, submit forms, transfer funds, or take any other action that cannot be undone, it must pause and request human confirmation before executing. No exceptions.

Implement a dry-run mode that describes what the agent would do without doing it. Run dry-run first on any new workflow.

!!! warning
    "The agent will probably get it right" is not an acceptable reason to skip HITL on irreversible actions. Agents fail at unexpected times on unexpected inputs.

---

## 5. Log everything

Log every tool call: timestamp, tool name, arguments, result, and whether the agent continued or stopped. Write logs to a location the agent cannot modify.

If you cannot answer "what exactly did the agent do at 14:32 yesterday?" from your logs, your logging is insufficient.

---

## 6. Build an eval set before scaling

Before running an agent on more than a handful of real inputs, build an eval set of at least 5 representative cases (see [Power-user path](power-user-path.md) for how). Run the eval set before any change to prompts, models, or tool configuration.

An agent you have not evaluated is a system you do not understand.

---

## 7. Plan for prompt injection from untrusted inputs

If the agent reads any content from outside your control — web pages, user-submitted files, email bodies, third-party APIs — that content can contain instructions designed to redirect the agent's behavior.

Mitigations:

- Treat all external content as data, not instructions. Use a system prompt that explicitly states this.
- Validate tool outputs before passing them back into context.
- Run agents that process untrusted input in read-only mode where possible.
- Do not give agents that process untrusted input access to write or send tools.

---

## 8. Rotate keys and plan for exposure

API keys in environment variables, config files, or logs can be exposed through accidents, misconfiguration, or compromise. Before you go beyond a personal experiment:

- Store keys in a secrets manager or an encrypted env file, not in plaintext.
- Set up key rotation so you can replace a key in under 15 minutes.
- Know which services use which key so you can scope an incident if one is compromised.

---

## 9. Plan a kill switch

Before a workflow runs in production, know how to stop it immediately:

- Which process do you kill?
- Which API key do you revoke?
- Who needs to be notified?
- How do you verify it has stopped?

Write this down and share it with at least one other person. An agent you cannot stop quickly is a risk you have not managed.

---

## Baseline checklist

- [ ] Agent's job named in one sentence
- [ ] Stop conditions (success and failure) defined
- [ ] Tools restricted to least-privilege
- [ ] HITL required for all irreversible actions
- [ ] Tool call logging enabled, logs protected from agent writes
- [ ] Eval set of ≥5 cases built and run before scaling
- [ ] Prompt injection risk assessed for all external inputs
- [ ] API keys in a secrets manager, rotation procedure documented
- [ ] Kill switch procedure written and shared

This checklist takes 30–60 minutes to work through for a new workflow. That time is cheaper than the first incident.
