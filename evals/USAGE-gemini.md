# Running Evals with Gemini

This guide covers running eval cases manually in the Gemini web app (gemini.google.com) and programmatically via the Google Gemini API.

---

## Gemini Web App: Manual Spot-Check

The Gemini web app is suitable for individual case review and small batches. Gemini Advanced (with Gemini 1.5 Pro or later) is recommended for eval use because it has a longer context window and supports system instructions via Gems.

### Step-by-Step

1. Open any JSONL file in a text editor. Select a case.

2. If the case has a system field in its input object, use a Gem (a Gemini custom persona) to set the system instruction. Create a Gem at gemini.google.com/gems/create with the system text in the instructions field.

3. Paste the input value into the conversation. If the input is a JSON object, format it clearly (e.g., paste the JSON and describe which field is the user message).

4. Compare the response to expected_behavior. Check every must_not_do item.

5. Record your score in your scoring sheet using the appropriate rubric.

### Creating a Gem for System-Prompted Cases

For refusal, escalation, and tool-choice cases that include a system prompt:

1. Go to gemini.google.com/gems/create.
2. Name the Gem (e.g., "Billing Support Agent Eval").
3. Paste the system instruction from the case's input.system field into the instructions box.
4. Save and use this Gem for all cases that share that system context.

---

## Gemini API: Programmatic Batch

The Gemini API (via google-generativeai Python SDK) enables automated batch runs. A full programmatic runner is in USAGE-programmatic.md. This section covers Gemini-specific configuration.

### Installation

```bash
pip install google-generativeai
```

### Model Selection

Recommended models for eval:
- gemini-1.5-pro — best reasoning, suitable for all eval categories
- gemini-1.5-flash — faster and cheaper, suitable for summarization, classification, and extraction
- gemini-2.0-flash-exp — if available in your region, tests the newest capability tier

### System Instruction Support

Gemini 1.5 and later support a system_instruction parameter in the GenerativeModel constructor:

```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")  # Do not commit real keys

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="You are a billing support agent. Only answer billing questions."
)
response = model.generate_content("Write me a poem about autumn.")
print(response.text)
```

This is the correct way to replicate cases that include a system field.

### Multimodal Input

Some extraction cases could be adapted for Gemini's multimodal capabilities (e.g., passing an image of an invoice). The current eval cases use text-only inputs; multimodal adaptation is left as an extension exercise.

---

## Tips for Specific Categories

**Citation-faithfulness:** Gemini 1.5 Pro supports long contexts, making it well-suited for multi-source citation cases. Paste all sources in the input and instruct the model to cite using the provided source IDs.

**Format-compliance:** Gemini tends to include markdown formatting by default. For cases that require plain JSON or CSV output with no surrounding prose, add an explicit instruction: "Return only the requested format. Do not include any explanation or markdown formatting outside the requested output."

**Red-team cases:** Run each red-team case in a new API call (no conversation history). Gemini's multi-turn history can suppress or amplify jailbreak resistance depending on prior turns.

**Tool-choice cases:** Gemini supports function calling via the tools parameter. For tool-choice cases, define the available_tools from the case as function declarations and observe which function (if any) Gemini calls. This tests actual function-selection behavior rather than stated intent.

---

## Platform Coverage

Cases tagged gemini in platform_tags are prioritized for this platform. Gemini is especially relevant for: summarization (long context), extraction (structured output), citation-faithfulness (grounded generation), and tool-choice (function calling API).
