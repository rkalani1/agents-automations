# Example: trip planning

> **Last verified:** 2026-05-06 · **Time:** 15 minutes · **No API key required**

Plan a trip end-to-end with the AI as your scheduler, fact-checker, and packing list.

## Layer 1 — Chat only `Free`

```
Help me plan a trip.

Destination(s): <e.g., Lisbon then Porto>
Dates: <e.g., 2026-09-12 to 2026-09-19>
Travelers: <e.g., 2 adults>
Pace: <e.g., one major thing per day, evenings unbooked>
Budget tier: <e.g., mid>
Things I care about: <bullet list — food, museums, walks, etc.>
Constraints: <e.g., I'm vegetarian; partner has knee issues; no late nights>

Output:
- Day-by-day itinerary in a markdown table (date | morning | afternoon | evening).
- A 1-paragraph "why this order" rationale.
- A short "neighbourhood by neighbourhood" lodging hint per stop.
- A 3-bullet "watch out for" list (scams, transit gotchas, holiday closures).
- A packing list grouped by category.
- Drafts only. Cite anything time-sensitive (festival dates, hours).
```

How to tell whether it worked: the itinerary respects pace + constraints. Time-sensitive claims are cited. The "watch out for" list is specific to the destination.

## Layer 2 — Project / Space `Sub`

Build a "Trips" Project / Space:

- System prompt: the format above + your default travel preferences.
- Project Knowledge: 1-pager "how we travel" (allergies, mobility, partner preferences).

Each new trip is a one-message paste.

Perplexity Spaces are particularly good here for cited time-sensitive info (hours, holidays).

## Layer 3 — Memory `Sub`

Global memory:

```
- Trip planning: one major thing/day, evenings unbooked, mid budget, vegetarian, partner has knee issues, no late nights.
- Always cite time-sensitive info (hours, holiday closures, festival dates).
```

## Layer 4 — Scheduled action `Sub`

Not a typical scheduled task. Closest: a weekly "trip prep" reminder at T-30, T-14, T-7, T-1 days that asks the AI to re-check time-sensitive facts.

Manual fallback: 4 calendar reminders.

## Layer 5 — Custom assistant `Sub`

Custom GPT / Gem / Skill "Trip planner":

- **Knowledge files**: your travel preferences doc, a packing template, a "good lodging vs not" rubric.
- **Sample prompts**: a real prior trip's brief and the itinerary it produced.

## Layer 6 — Developer / API (optional)

Not a great fit. Trip planning involves volatile real-world facts; subscription tools with web access are the better surface.

## Make it reusable

- Save the Project / Gem.
- After each trip, add 5 lines to the Knowledge file: what worked, what didn't.

## Make it robust

- **Eval**: take a past trip you remember well; run the prompt with that input; compare.
- **Red-team**: include a constraint the AI might miss (e.g., "no flights with layovers >2h"). Verify it respected it.
- **Drift check**: hours and prices change. Always re-verify the day before a booking.

## What good output looks like

- Itinerary respects pace + constraints + budget tier.
- Time-sensitive claims are cited.
- "Watch out for" entries are destination-specific, not generic travel platitudes.

## If your plan doesn't have this feature

- No Project → paste preferences and prompt each time.
- No web access in your AI → switch to Perplexity for cited facts.
- No Custom GPT → save the prompt; same effect.

## See also

- [Mastery — Perplexity](../mastery/perplexity.md)
- [Memory and preferences](../preferences-memory/index.md)
