> **Last verified:** 2026-05-06 · **Drift risk:** low

# Worked example: research workflow portfolio

This page walks through a complete factory run. The goal is to build a portfolio of agents to support a synthetic research team's weekly workflow. Every artifact below is a candidate — none is active until a human owner signs the launch-readiness checklist. See [Launch readiness](launch-readiness.md).

All context, names, and data in this example are synthetic.

---

## Step 1 — Generate 25 candidate agents

The team brainstormed candidates across their workflow. Each entry is a one-line job statement.

| # | Candidate | Job statement |
|---|---|---|
| 1 | Preprint triage | Rank a weekly batch of preprint abstracts by relevance to the team's current focus |
| 2 | PDF structure extractor | Extract figures, tables, and section headers from a research PDF into structured JSON |
| 3 | Citation graph builder | Given a seed paper, return a list of its most-cited references with metadata |
| 4 | Literature gap identifier | Given a reading list, identify topic areas not covered and suggest search terms |
| 5 | Meeting notes summarizer | Summarize a raw meeting transcript into action items and decisions |
| 6 | Email draft assistant | Given a context paragraph, draft a professional email for human review and sending |
| 7 | Calendar conflict checker | Given a proposed meeting time, check the team calendar and report conflicts |
| 8 | Experiment log formatter | Convert free-text lab notes into a structured experiment log entry |
| 9 | Code review assistant | Review a Python function for correctness and style; leave comments as output text |
| 10 | Test generator | Given a Python function, generate a pytest test suite |
| 11 | Data validation agent | Given a CSV and a schema, report all rows that fail validation |
| 12 | Figure description generator | Generate alt-text descriptions for figures in a paper |
| 13 | Hypothesis ranking agent | Given a list of hypotheses and supporting evidence, rank by strength |
| 14 | Shared notes indexer | Parse and index a folder of Markdown notes into a searchable JSON structure |
| 15 | Browser research assistant | Given a research question, retrieve and summarize the top web sources |
| 16 | arXiv search agent | Given keywords, return the top 10 arXiv results with metadata |
| 17 | Notebook documentation agent | Given a Jupyter notebook, write a plain-language README describing its purpose |
| 18 | Slide deck outline generator | Given a paper, produce a 10-slide outline with one-sentence per-slide summaries |
| 19 | Peer review response drafter | Given a reviewer comment, draft a point-by-point response for human editing |
| 20 | Grant section summarizer | Summarize a specific section of a grant application for internal review |
| 21 | MCP tool router | Given a natural-language request, route it to the correct MCP server and return results |
| 22 | Slack digest agent | Summarize the past 24 hours of a Slack channel into a bullet-point digest |
| 23 | Bibliography formatter | Given a list of paper metadata objects, format them as a bibliography in a specified style |
| 24 | Research question generator | Given a topic, generate 10 specific, answerable research questions |
| 25 | Dataset provenance recorder | Given a dataset filename and context, generate a provenance record entry |

---

## Step 2 — Rank

Each candidate is scored on the five factors defined in [Candidate ranking](candidate-ranking.md). V = Value, F = Feasibility, S = Safety, M = Maintenance burden, P = Platform fit.

| # | Candidate | V | F | S | M | P | Total |
|---|---|---|---|---|---|---|---|
| 1 | Preprint triage | 5 | 5 | 5 | 4 | 4 | 23 |
| 2 | PDF structure extractor | 4 | 4 | 5 | 3 | 4 | 20 |
| 3 | Citation graph builder | 3 | 3 | 5 | 3 | 3 | 17 |
| 4 | Literature gap identifier | 4 | 4 | 5 | 3 | 4 | 20 |
| 5 | Meeting notes summarizer | 4 | 5 | 5 | 4 | 5 | 23 |
| 6 | Email draft assistant | 3 | 4 | 3 | 3 | 4 | 17 |
| 7 | Calendar conflict checker | 2 | 3 | 4 | 2 | 3 | 14 |
| 8 | Experiment log formatter | 4 | 4 | 5 | 4 | 4 | 21 |
| 9 | Code review assistant | 4 | 4 | 4 | 3 | 4 | 19 |
| 10 | Test generator | 4 | 5 | 5 | 4 | 5 | 23 |
| 11 | Data validation agent | 3 | 4 | 5 | 4 | 4 | 20 |
| 12 | Figure description generator | 3 | 4 | 5 | 4 | 4 | 20 |
| 13 | Hypothesis ranking agent | 3 | 3 | 5 | 3 | 3 | 17 |
| 14 | Shared notes indexer | 3 | 4 | 5 | 3 | 4 | 19 |
| 15 | Browser research assistant | 4 | 3 | 3 | 2 | 3 | 15 |
| 16 | arXiv search agent | 4 | 4 | 5 | 3 | 4 | 20 |
| 17 | Notebook documentation agent | 3 | 5 | 5 | 4 | 5 | 22 |
| 18 | Slide deck outline generator | 3 | 4 | 5 | 4 | 4 | 20 |
| 19 | Peer review response drafter | 4 | 4 | 4 | 3 | 4 | 19 |
| 20 | Grant section summarizer | 3 | 4 | 4 | 3 | 4 | 18 |
| 21 | MCP tool router | 3 | 2 | 3 | 2 | 3 | 13 |
| 22 | Slack digest agent | 3 | 4 | 4 | 3 | 4 | 18 |
| 23 | Bibliography formatter | 3 | 5 | 5 | 5 | 5 | 23 |
| 24 | Research question generator | 3 | 5 | 5 | 4 | 5 | 22 |
| 25 | Dataset provenance recorder | 3 | 4 | 5 | 4 | 4 | 20 |

**Top 5 by total score:** Preprint triage (23), Meeting notes summarizer (23), Test generator (23), Bibliography formatter (23), Notebook documentation agent (22).

Where candidates tie at 23, the tiebreaker is Safety score first (all are 5), then Maintenance burden. All four 23-scorers have strong maintenance profiles; selection prioritizes Preprint triage and Meeting notes summarizer as the highest-value daily-workflow agents.

Selected for this run: Preprint triage, Meeting notes summarizer, Test generator, Bibliography formatter, Notebook documentation agent.

---

## Step 3 — Specs

### Agent A: Preprint triage

- Job statement: Receive a JSON array of preprint metadata and return a relevance-ranked reading list for the week.
- Inputs: JSON array of objects with keys `arxiv_id`, `title`, `authors`, `abstract`; a plain-text research focus statement.
- Outputs: JSON array sorted by rank, each element with `rank`, `arxiv_id`, `title`, `justification` (max 30 words).
- Tools: None — operates on provided data only.
- Stop conditions: Batch fewer than 5 papers; more than 200 papers; more than 30% of abstracts under 100 words.
- HITL gates: Owner reviews ranked list before it is added to the shared reading list.
- Owner: [placeholder — Research Lead to confirm]

### Agent B: Meeting notes summarizer

- Job statement: Convert a raw meeting transcript into a structured summary with action items and decisions.
- Inputs: Plain-text transcript (max 8,000 words); optional meeting title and date.
- Outputs: Markdown document with sections: Summary (3–5 sentences), Decisions (bulleted list), Action items (table with columns: item, owner placeholder, deadline placeholder).
- Tools: None.
- Stop conditions: Transcript contains personally identifiable information in a non-participant context (e.g., discussion of a client by name — flag for human review before processing).
- HITL gates: Owner reviews output before distributing to meeting participants.
- Owner: [placeholder — Team Operations Lead to confirm]

### Agent C: Test generator

- Job statement: Given a Python function definition, generate a pytest test suite covering nominal, boundary, and error cases.
- Inputs: A single Python function as a string; optional docstring and type hints if not inline.
- Outputs: A valid pytest file as a string, including imports, test function definitions, and at least one parametrized test.
- Tools: None — generates code from the function definition only; does not execute code.
- Stop conditions: Function definition exceeds 200 lines; function contains no docstring or type hints and the purpose is ambiguous — return a clarification request.
- HITL gates: Developer reviews and runs the generated tests before committing.
- Owner: [placeholder — Engineering Lead to confirm]

### Agent D: Bibliography formatter

- Job statement: Given a list of paper metadata objects, produce a formatted bibliography in a specified citation style.
- Inputs: JSON array of metadata objects with standard fields (title, authors, year, venue, DOI, URL); target citation style (e.g., APA, MLA, Chicago, or a custom template string).
- Outputs: Plain-text bibliography with one entry per line, in the specified style, sorted alphabetically by first author surname.
- Tools: None.
- Stop conditions: An entry is missing required fields for the specified style — flag the entry and continue with remaining entries.
- HITL gates: Author spot-checks output before submitting to a publication or grant.
- Owner: [placeholder — Research Lead to confirm]

### Agent E: Notebook documentation agent

- Job statement: Given a Jupyter notebook, produce a plain-language README describing the notebook's purpose, inputs, outputs, and key steps.
- Inputs: A Jupyter notebook file (`.ipynb`) as a JSON string.
- Outputs: A Markdown README with sections: Purpose (2–3 sentences), Requirements (bulleted list of packages), Inputs (description), Outputs (description), Key steps (numbered list, one sentence per major cell or cell group).
- Tools: None — reads the notebook JSON; does not execute cells.
- Stop conditions: Notebook has no code cells; notebook JSON is malformed.
- HITL gates: Developer reviews README before committing to the repository.
- Owner: [placeholder — Engineering Lead to confirm]

---

## Step 4 — Prompts, evals, red-team, launch checklists

For prompt-pack templates, see the [recipes section](../recipes/index.md). Below is a per-agent summary.

### Agent A: Preprint triage

- Prompt focus: System prompt emphasizes strict JSON output schema, the 30-word justification cap, and explicit stop conditions for small or malformed batches. N-shot exemplars include one high-relevance paper, one low-relevance paper, and one stop-condition trigger.
- Eval foci: (1) Rank ordering matches expert judgment on 10 held-out batches. (2) JSON output validates against schema on 100% of cases. (3) Stop conditions trigger correctly on boundary inputs.
- Red-team foci: (1) Injected instructions in abstract fields. (2) Requests to return papers not in the input batch. (3) Oversized batches designed to degrade ranking quality.
- Launch checklist: Named Research Lead owner confirmed; kill switch via environment variable tested; cost ceiling set at 500 API calls/week; quarterly review scheduled; eval pass rate ≥80% and all critical cases pass.

### Agent B: Meeting notes summarizer

- Prompt focus: System prompt defines the three mandatory output sections and specifies that action items must not assign owners — they use a placeholder. A refusal exemplar handles transcripts that appear to contain non-participant PII.
- Eval foci: (1) All three output sections present in every case. (2) Action items table is valid Markdown. (3) PII flag triggers correctly on test transcripts that include client names.
- Red-team foci: (1) Transcripts with injected instructions in speaker turns. (2) Requests to include participant email addresses in the output. (3) Extremely long transcripts that exceed the token budget.
- Launch checklist: Named Team Operations Lead confirmed; kill switch tested; cost ceiling set; output logging with 30-day retention confirmed; quarterly review scheduled.

### Agent C: Test generator

- Prompt focus: System prompt specifies that the output must be a valid Python file, that tests must not import the function from a path (they receive it as a string), and that at least one parametrized test is required. Exemplars cover a pure function, a function with side effects (which the agent should note in a comment), and an ambiguous function that triggers a clarification request.
- Eval foci: (1) Generated test files are syntactically valid Python. (2) At least one parametrize decorator is present. (3) Ambiguous functions return a clarification request rather than a guess.
- Red-team foci: (1) Function definitions that contain shell injection payloads in docstrings. (2) Requests to generate tests that delete files. (3) Functions with no clear contract, designed to produce plausible-looking but incorrect tests.
- Launch checklist: Named Engineering Lead confirmed; developer review gate documented in team workflow; kill switch tested; quarterly review scheduled.

### Agent D: Bibliography formatter

- Prompt focus: System prompt specifies alphabetical ordering, field validation behavior (flag incomplete entries, do not skip them silently), and a custom-template fallback when the requested style is not recognized. Exemplars cover APA, a DOI-missing entry, and a style not in the default list.
- Eval foci: (1) Output is alphabetically sorted in 100% of cases. (2) Incomplete entries are flagged with the missing field identified. (3) Custom template strings produce output matching the template.
- Red-team foci: (1) Metadata objects with injected LaTeX or HTML in author fields. (2) Requests to include entries not in the input array. (3) Extremely large bibliographies (500+ entries) to test performance consistency.
- Launch checklist: Named Research Lead confirmed; output reviewed by author before submission; kill switch via feature flag tested; quarterly review scheduled.

### Agent E: Notebook documentation agent

- Prompt focus: System prompt specifies that the agent reads only the source cells, not cell outputs, and that it must not infer package requirements from import statements alone — it should list only what it observes. Exemplar covers a clean notebook and a malformed notebook that triggers a stop condition.
- Eval foci: (1) All five README sections present in every case. (2) Package list reflects only observed imports, not guesses. (3) Malformed notebook JSON returns a stop-condition message, not a partial README.
- Red-team foci: (1) Notebooks with injected Markdown instructions in cell comments. (2) Requests to execute the notebook before documenting. (3) Notebooks with thousands of cells designed to exceed the context window.
- Launch checklist: Named Engineering Lead confirmed; developer review gate in PR workflow; kill switch tested; quarterly review scheduled.

---

## Step 5 — Port across platforms

| Agent | Claude (Project + Code) | OpenAI (Agents SDK + Codex) | Gemini (Gems + API) | GitHub Copilot |
|---|---|---|---|---|
| Preprint triage | System instruction in Project; structured output via JSON mode instruction; refusal style explicit in prompt | `output_type=PaperRankList` Pydantic model via structured outputs; input guardrail for batch-size check | `response_schema` field in generation config; Gem for interactive use, API for batch | Not applicable — no document-batch input model in Copilot |
| Meeting notes summarizer | Project instruction with three-section template; exemplars inline | Agents SDK with output_type matching Markdown section schema; Codex not applicable | Gem for interactive transcript paste; API for programmatic use | Not applicable — no transcript-input model in Copilot |
| Test generator | Claude Code preferred; `CLAUDE.md` carries the constraint list; Code runs in repo context | Codex CLI with `--system-prompt` carrying constraints; Agents SDK for API access | Gemini API with code execution disabled in generation config | `.github/copilot-instructions.md` carries constraints; Copilot agent responds to issue with `generate tests for [function]` |
| Bibliography formatter | Project instruction; output is plain text — no structured-output mode needed | Agents SDK with plain-text output; structured outputs not needed | Gem for interactive use; API for batch; no schema needed | Not practical — Copilot not designed for bibliography tasks |
| Notebook documentation | Claude Code with `CLAUDE.md`; Code reads `.ipynb` from repo | Codex CLI with notebook file as stdin; Agents SDK for API use | Gemini API with file input; Gems not suitable for file-upload workflows | `.github/copilot-instructions.md`; Copilot agent triggered by PR comment `document this notebook` |

---

## Step 6 — Approval gate

Every artifact in this factory run — the 25 candidate descriptions, the ranking table, the five specs, the five prompt packs, the eval and red-team case outlines, the porting notes, and all launch checklists — is a candidate artifact. It is inert. No agent in this run is active.

Activation requires all of the following, per agent:

1. A named owner has read the spec, the prompt pack, and the eval and red-team reports for their agent.
2. The owner has run the eval suite and the red-team suite and confirmed the pass rates meet the thresholds in [Launch readiness](launch-readiness.md).
3. The owner has verified the kill switch, cost ceiling, and logging configuration.
4. The owner has signed the launch-readiness checklist with a date.
5. The Safety Lead has signed the red-team section of the checklist.

None of these steps is delegable to another tool, another agent, or another person without explicit written transfer of accountability. The factory produces candidates. Humans activate agents.
