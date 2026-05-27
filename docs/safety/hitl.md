# Human-in-the-loop patterns

> **Last verified:** 2026-05-06 · **Drift risk:** low

A human-in-the-loop (HITL) gate is a point in an agent's execution where it pauses and asks a human to confirm, review, or approve before continuing. HITL gates are not a sign that your agent is not autonomous enough — they are a deliberate design choice that limits the blast radius of mistakes.

This page covers the three main HITL patterns, defines what counts as an irreversible action (the key decision in deciding when a gate is required), and gives concrete implementation guidance.

---

## The three HITL patterns

### Approve-before-act

The agent constructs a proposed action, presents it to the human in plain language, and waits for an explicit approval before executing.

**When to use it.** Any time the action is irreversible or has significant external effects. This is the highest-friction pattern and should be reserved for actions where the cost of a mistake is high.

**What it looks like in practice.**

```
Agent: I am about to send the following email on your behalf:
  To: vendor@example.com
  Subject: PO cancellation notice
  Body: [...]

Type "confirm" to send, or "cancel" to abort.
```

The agent must not proceed until it receives an explicit confirmation signal — not a timeout, not silence, not a follow-up message that could be interpreted ambiguously.

**Implementation notes.**
- Present the full content of the proposed action, not a summary. Users should be able to catch errors in the detail.
- Include a cancel path that is at least as easy as the confirm path.
- Do not pre-select "confirm" as the default. If the user closes the window, the action should not execute.

---

### Dry-run mode

The agent simulates an action — executing all the logic except the final write or send — and shows the user what would have happened. The user can then approve a live run or adjust their request.

**When to use it.** Actions that are reversible but expensive to undo (bulk record updates, large data imports), or any time the user is unfamiliar with what the agent will do and would benefit from seeing the output before it is committed.

**What it looks like in practice.**

```
Agent: Dry-run complete. Here is what would happen if I executed this now:
  - 47 records in the "contacts" table would be updated
  - 3 records would be marked inactive
  - 0 records would be deleted
  
Run for real? (yes/no)
```

**Implementation notes.**
- Dry-run mode must be a first-class feature of your tool integrations, not just a prompt-level instruction. The tool itself needs to support a preview or simulation mode.
- Make it clear that the dry-run output is a prediction, not a guarantee. If the underlying data changes between the dry run and the live run, the results will differ.

---

### Confirm-on-irreversible

The agent proceeds autonomously for reversible actions but automatically surfaces a gate whenever it is about to take an action that has been classified as irreversible.

**When to use it.** Most production agents benefit from this pattern as a baseline. It keeps friction low for read-heavy workflows while providing a safety net for the actions that matter most.

**What it looks like in practice.**

The agent classifies each action before executing it. Actions on the irreversible list trigger a confirmation prompt; all others execute without interruption.

---

## What counts as irreversible

The following categories of action should be treated as irreversible by default unless your specific context provides a reliable undo mechanism:

**Writes to external systems**
- Creating, updating, or deleting records in a database or data store that is not exclusively under your agent's control.
- Writing to a file system path that other systems depend on.
- Updating configuration in an infrastructure system (DNS, load balancer rules, IAM policies).

**Sending messages**
- Sending email, SMS, Slack messages, or any push notification.
- Posting to a public forum, social platform, or shared channel.
- Triggering a webhook that delivers a payload to an external service.

**Financial transactions**
- Charging a payment method.
- Creating, modifying, or canceling an invoice or subscription.
- Initiating a wire transfer, ACH payment, or cryptocurrency transaction.
- Placing or canceling an order with a vendor.

**Code changes**
- Merging a branch to a protected branch (main, production).
- Deploying a build to a production environment.
- Publishing a package to a public registry.

**Actions affecting other people**
- Any action that creates a commitment on behalf of another person or organization.
- Scheduling a meeting, sending a calendar invite, or canceling an appointment.
- Submitting a form or application in another person's name.
- Sharing or publishing data that another person provided in confidence.

---

## When HITL is not enough

HITL gates reduce risk but do not eliminate it. A user can confirm a bad action if the agent's description of the action is unclear or if the user is fatigued by too many confirmation prompts.

To keep HITL effective:

- Keep the number of gates low. If every action requires approval, users will approve without reading. Reserve gates for genuinely high-stakes actions.
- Write confirmation prompts in plain language. Avoid jargon, IDs, and technical detail that users cannot evaluate.
- Log every gate: what was proposed, what the user decided, and when. This creates an audit trail.
- Review confirmation patterns in production. If users are approving actions and then immediately reporting problems, the gate description needs improvement.

HITL is one layer in a defense-in-depth approach. It works alongside narrow tool permissions, eval-driven development, and the logging practices described in [Incident response](incidents.md).
