# When not to use an agent

> **Last verified:** 2026-05-06 · **Drift risk:** low

Agent architecture adds complexity, latency, cost, and failure modes that do not exist in a simple prompt or a script. Use this page as a checklist before you commit to building an agent loop.

---

## You cannot articulate success criteria

If you cannot finish the sentence "The agent is done when ___," you do not have a stop condition. Without one, the loop either runs forever, stops arbitrarily, or produces output you cannot evaluate.

**Do instead:** Spend 30 minutes writing acceptance criteria before writing any code. If you cannot, the task is not ready to automate.

---

## The action is irreversible and there is no human in the loop

Sending emails, posting to social media, deleting records, submitting forms, transferring money — these cannot be undone. An agent that can take irreversible actions without a confirmation step is a liability, not a feature.

**Do instead:** Design a dry-run mode that shows what the agent would do. Require explicit human approval before execution. This is non-negotiable for production systems.

!!! warning
    "It will probably be right" is not a HITL strategy. Agents make mistakes at unexpected times.

---

## The UX requires low latency

A loop that calls tools 5–10 times takes seconds to minutes. If your user is waiting for a response in a chat interface or a real-time dashboard, an agent loop will feel broken.

**Do instead:** Use a single-shot prompt with a well-engineered system prompt. If you need tool use, limit it to one or two fast calls with timeouts.

---

## The workflow is regulated and you have no evaluation harness

Clinical decision support, financial advice, legal analysis, HR decisions — these domains have compliance requirements that go beyond "the model seemed confident." An agent operating in these areas without a documented eval set, human review, and audit log is a compliance risk.

**Do instead:** Build the eval harness first. Get compliance sign-off on the architecture before the first production run. See [Team path](team-path.md) and [Safety baseline](safety-baseline.md).

!!! note
    This guide does not give legal or compliance advice. Consult your legal and compliance teams.

---

## A 10-line script would do it

If the task is deterministic — parse this CSV, rename these files, call this API with these parameters — a script is faster, cheaper, more auditable, and more reliable than an agent.

**Do instead:** Write the script. Use an LLM to help you write it if you want, but the output should be code, not an agent.

---

## The input data is untrusted and you have not addressed prompt injection

If the agent reads content from the web, user-submitted files, emails, or any source outside your control, that content can contain instructions designed to hijack the agent's behavior (prompt injection). An agent with write access to files or the ability to send messages is a high-value injection target.

**Do instead:** Either scope the agent to read-only trusted sources, or implement explicit input validation and treat all external content as untrusted. See [Safety baseline](safety-baseline.md).

---

## You need novelty or genuine judgment in safety-critical decisions

Agents inherit the model's tendency to be confidently wrong. For decisions where a wrong answer causes serious harm — medical triage, structural engineering checks, security incident response — the agent should present options and evidence, not act autonomously.

**Do instead:** Use the agent to gather and summarize information, then route to a human for the final decision. Build the routing into the workflow, not as an afterthought.

---

## A quick reference

| Situation | Recommended alternative |
|-----------|------------------------|
| Can't define done | Clarify requirements first |
| Irreversible actions | Add HITL dry-run mode |
| Need sub-second response | Single-shot prompt |
| Regulated domain, no eval | Build eval + get compliance review |
| Deterministic data transform | Write a script |
| Untrusted input | Sandbox and validate inputs |
| Safety-critical judgment | Human-in-the-loop for final decision |

Building an agent for the right task is straightforward. Building one for the wrong task is expensive in time, money, and trust. Use this checklist before you start.
