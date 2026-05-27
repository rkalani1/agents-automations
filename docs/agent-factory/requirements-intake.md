> **Last verified:** 2026-05-06 · **Drift risk:** low

# Requirements intake

Good intake prevents two expensive problems: building the wrong agent and building the right agent in a way nobody will maintain. The intake form is a short written conversation between the requestor and the factory team. It does not need to be long, but it must answer four questions before a spec is written.

## The four intake questions

### 1. What are you trying to do?

One paragraph in plain language. Not a list of features — a description of the workflow the requestor wants to improve. "I spend three hours a week reading abstracts to decide which papers to add to our shared reading list" is better than "I want an agent that reads papers." The paragraph should describe the current state (what the person actually does today), the desired state (what they want to be able to do instead), and the threshold for "good enough" (what improvement would make this worth using?).

### 2. Who pays the cost when this fails?

One paragraph describing the downstream consequences of an agent error. This is the most important intake question and the one requestors most often underestimate. The answer should identify: who in the organization notices first when the agent produces a bad output; what they have to do to recover; and whether any of the consequences reach outside the team (customers, external partners, regulatory bodies). This paragraph determines the initial risk tier assignment.

### 3. Inputs, outputs, and tools

A checklist of what the requestor thinks the agent will need. This is not a spec — it is a starting point for the spec conversation. The requestor should list:

- [ ] Inputs: What does the agent receive? (e.g., a URL, a PDF, a search query, a calendar event)
- [ ] Outputs: What does the agent produce? (e.g., a ranked list, a draft email, a filled-in form)
- [ ] Tools: What external capabilities does the requestor expect the agent to use? (e.g., web search, a specific database, a code interpreter)
- [ ] Existing systems: What internal tools, APIs, or data sources does the agent need to interact with?
- [ ] Format constraints: Does the output need to match a specific schema or template?

The builder should not treat this checklist as final. Its purpose is to give the spec conversation a concrete starting point and to surface mismatched assumptions early (e.g., the requestor assumes the agent has access to a database that is not actually accessible).

### 4. Stop conditions

A prompt asking the requestor to describe when the agent should stop and hand off to a human rather than proceeding. Common stop conditions include: the agent reaches a decision point where the cost of a mistake is high enough to warrant human review; the agent encounters an input it was not designed to handle; the agent's confidence in its output is below a threshold the requestor finds acceptable. This question often surfaces HITL (human-in-the-loop) requirements that would otherwise be missed until red-team.

## Worked example

The following is a filled-in intake form for a literature triage agent in a research team context. All context is synthetic.

---

**What are you trying to do?**

Our team gets between 30 and 60 new preprints per week that are potentially relevant to our research area. Right now I read every abstract and decide which ones to add to our shared reading list and which ones to skip. That takes about two hours on Monday mornings. I want an agent that reads a batch of abstracts and returns a ranked list with a one-sentence justification for each ranking, so that I can spend 15 minutes confirming the top 10 rather than 2 hours reading all 50. Good enough means I trust its top-10 list enough to use it as my starting point without reading every abstract first.

**Who pays the cost when this fails?**

If the agent mislabels a highly relevant paper as low priority, I miss a paper that could have informed our research. The cost is information loss — embarrassing if a competitor cites something we missed, but not immediately harmful. The output goes only to me; nothing is sent externally without my review. The risk is low and recoverable.

**Inputs, outputs, and tools**

- [x] Inputs: A JSON array of paper metadata objects (title, authors, abstract, arXiv ID)
- [x] Outputs: A ranked list with rank, arXiv ID, title, and a one-sentence justification
- [x] Tools: No external tools needed for the first version; the agent works from the provided abstracts only
- [ ] Existing systems: None for v1; future versions might pull from the arXiv API directly
- [x] Format constraints: Output must be valid JSON matching the team's shared reading list schema

**Stop conditions**

The agent should stop and flag for human review if: (a) the batch contains fewer than 5 papers (might indicate a feed error), (b) more than 30% of the papers have abstracts shorter than 100 words (might indicate malformed input), or (c) the agent's top-ranked paper has been on the list before (might indicate a duplicate-detection failure upstream).

---

## What happens after intake

The completed intake form goes to the builder, who uses it to write the formal spec. The spec will add precision that the intake form deliberately lacks — exact input schemas, error handling behavior, tool call signatures, and eval criteria. If the builder finds that the intake form is missing information that is necessary to write the spec, they return to the requestor with specific questions rather than making assumptions.

The intake form is also the first document reviewed at the Rank stage. An intake form that describes a low-value workflow, a high-risk failure mode, or a missing data dependency may result in the candidate being deprioritized or rejected before a spec is written.

Intake forms should be stored in the factory run record alongside the spec, eval report, and launch checklist. They are useful reference documents during maintenance: if an agent starts behaving unexpectedly, the original intake form is often the clearest statement of what the agent was supposed to do.
