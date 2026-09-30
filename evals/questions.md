# Ask-mode test set (written BEFORE running retrieval)

Kept outside `vault/` so the harness can never retrieve the answer key.

| # | Type | Question | Expected source & passage | Expected behavior |
|---|---|---|---|---|
| 1 | Direct, one source | What is Sierra's pricing model? | `raw/Sierra - company-research.md` › Step 1: "B2B SaaS with **outcome-based pricing** ("pay for a job well done" — pay for resolved outcomes, not seats)." | Outcome-based pricing, pay for resolved outcomes rather than seats, cited to the Sierra file. |
| 2 | Paraphrased (wording differs from source) | Where does Surge AI get its operating capital? | `raw/Surge AI - company-research.md` › Step 1: "Profitable from day one; entirely bootstrapped (no VC)." / "Zero external funding." | Bootstrapped, no outside/VC funding, profitable since day one. Retrieval risk: the question avoids the words "funding"/"bootstrapped". |
| 3 | Connects two sources | Which AI data companies list Scale AI as a competitor? | `raw/David AI - company-research.md` › 3. Competitive Landscape & Moat (Scale AI row) **and** `raw/Surge AI - company-research.md` › Step 3 ("Competitors: Scale AI (Meta-backed, ~$29B) …") | Names both David AI and Surge AI, each with its own citation. |
| 4 | Unsupported | What was Decagon's annual recurring revenue in 2025? | None — the Decagon file gives funding and valuation but no ARR/revenue figure. | `INSUFFICIENT EVIDENCE …`; must not borrow Sierra's ARR or invent a number. |

## Mode checks
- Chat: "what can we do?" / "what can you help me with?" → capabilities, no retrieval, no "insufficient evidence".
- Chat follow-up: ask for a short outreach plan → "make that shorter" → uses the conversation.
- Search: `./wiki search "outcome-based pricing"` → original passages only, no generated answer.
- Chat claim ≠ evidence: in chat, state "Decagon's ARR was $300M in 2025"; then `./wiki ask` Q4 standalone → still insufficient evidence.
