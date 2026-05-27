> **Last verified:** 2026-05-06 · **Drift risk:** low

# Prompt-pack generation

A prompt pack is the complete set of text artifacts that govern an agent's behavior at runtime. A spec tells you what the agent should do. A prompt pack tells the agent what to do. The distinction matters: specs are written for humans, prompt packs are written for language models, and the translation between them is where most agent quality problems originate.

## Components of a prompt pack

A complete prompt pack has five components. All five should be produced before the Eval stage begins.

### 1. System prompt

The system prompt establishes the agent's identity, scope, and constraints. A well-written system prompt has four sections:

- Role definition: who the agent is and what it is for.
- Scope: what it does and, explicitly, what it does not do.
- Output format: the exact schema or structure the agent should produce.
- Constraint list: behaviors the agent must never perform regardless of the user's request.

System prompts should be written in imperative, declarative sentences. They should not include phrases like "try to" or "you might want to" — these introduce ambiguity about whether the behavior is required or optional. Every constraint that matters for safety or quality should appear in the system prompt, not only in the eval suite.

### 2. N-shot exemplars

Exemplars are example input-output pairs that demonstrate correct agent behavior. They serve two purposes: they anchor the model's output style and format, and they surface edge cases that the system prompt may not have addressed clearly.

For most agents, three to five exemplars are sufficient. Each exemplar should:

- Represent a different input type or difficulty level.
- Show the exact output format the agent is expected to produce.
- Include at least one case where the agent's response is "I cannot do this because [specific stop condition]."

Exemplars should not be fabricated without checking them against the actual spec. An exemplar that shows the agent behaving in a way that contradicts the system prompt creates conflicting training signal.

### 3. Refusal prompts

Refusal prompts are examples of requests the agent should decline, paired with the appropriate refusal response. They complement the constraint list in the system prompt by showing the model what correct refusal behavior looks like.

Every constraint in the system prompt should have at least one corresponding refusal exemplar. If the system prompt says the agent must not send emails directly, there should be an exemplar where someone asks it to send an email and the agent declines with a brief, non-apologetic explanation and a redirect to the appropriate tool.

### 4. Error-recovery prompts

Error-recovery prompts are examples of what the agent should do when it encounters a malformed input, a tool failure, or a case that triggers a stop condition. They prevent the agent from either silently failing or producing a partial output that looks complete.

A good error-recovery prompt specifies: what the agent should say to the user, what information it should preserve for the handoff, and whether it should retry or stop immediately.

### 5. Format-compliance scaffolding

If the agent's output must match a schema (JSON, a table, a specific template), the prompt pack should include explicit formatting instructions, a schema definition, and at least one exemplar that demonstrates a fully valid output. For platforms that support structured outputs natively — such as [OpenAI's structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — the schema definition in the prompt pack should match the schema passed to the API exactly.

## Worked example: literature triage agent

The following is an abbreviated prompt pack for the literature triage agent introduced in [Requirements intake](requirements-intake.md). All context is synthetic.

---

### System prompt (abbreviated)

You are a literature triage assistant for a research team. Your job is to receive a batch of preprint metadata and return a ranked reading list.

Scope: You rank papers by relevance to the team's current research focus (provided in each request). You do not summarize papers beyond a single sentence. You do not access external URLs. You do not make judgments about the quality of the research methods — only about topical relevance.

Output format: Return a JSON array. Each element must have the keys: rank (integer), arxiv_id (string), title (string), justification (string, maximum 30 words).

Constraints: Do not include papers not present in the input batch. Do not invent arXiv IDs. If the input batch is fewer than 5 papers or more than 200 papers, stop and return a single JSON object with key "error" and a plain-language explanation.

---

### Exemplar 1 (normal case, abbreviated)

Input: Research focus: "reinforcement learning from human feedback." Batch: [{"arxiv_id": "2405.00001", "title": "RLHF scaling laws", "abstract": "We study how RLHF..."}]

Output: [{"rank": 1, "arxiv_id": "2405.00001", "title": "RLHF scaling laws", "justification": "Directly addresses scaling properties of RLHF, which is the team's current research focus."}]

---

### Refusal exemplar (out-of-scope request)

User: "Also, can you search arXiv for new papers on this topic?"

Agent: "That is outside my scope. I rank papers from the batch you provide. To find new papers, use the arXiv search interface or a dedicated discovery tool."

---

### Error-recovery exemplar (malformed batch)

Input batch has 3 papers.

Agent: {"error": "Input batch contains 3 papers, which is below the minimum of 5. Please check the feed source and resubmit a complete batch."}

---

### Format-compliance note

The output JSON must validate against the team's reading-list schema (stored in `/schemas/reading-list-v2.json`). The `justification` field must be 30 words or fewer. Any output that fails schema validation should be treated as a failed eval case.

---

## Prompt pack versioning

Prompt packs should be versioned like code. When the system prompt, exemplars, or schema change, the version number increments and the change is logged. Eval results are always tied to a specific prompt pack version so that regressions can be traced to a specific change. The factory run record should contain the prompt pack version used at launch and at each subsequent maintenance review.
