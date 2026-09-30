# Test results: official offline run

- **Run:** 2026-09-30 16:00–16:04 PDT, Wi‑Fi and hotspot off, `INTERNET: UNREACHABLE (offline confirmed)`.
  Full log: [`evidence/offline/offline-run-20260930-160030.log`](../evidence/offline/offline-run-20260930-160030.log) ·
  screen recording: [`evidence/offline/offline-demo.mp4`](../evidence/offline/offline-demo.mp4)
- **Model:** `gemma4:e4b` (Gemma 4 E4B, Q4_K_M) via Ollama 0.34.4, `execution: local`, thinking off, temperature 0.1
- **Retrieval:** hybrid BM25 + `embeddinggemma` (weighted RRF, dense weight 2.0), originals in `vault/raw/` only, top 5
- **Data:** 7 redacted company-research files, 197 indexed passages
- Questions and expected evidence were written before testing: [`evals/questions.md`](questions.md). They live
  outside the vault, so retrieval can never find the answer key.

## Summary

| # | Question | Expected passage retrieved? | Answer correct? | Citations check out? | Latency |
|---|---|---|---|---|---|
| 1 | What is Sierra's pricing model? | ✅ S2 = Sierra Step 1 | ✅ | ✅ | 8.0 s |
| 2 | Where does Surge AI get its operating capital? *(paraphrase)* | ✅ S3 = Surge Step 1 ("entirely bootstrapped") | ✅ | ✅ | 6.2 s |
| 3 | Which AI data companies list Scale AI as a competitor? *(2 sources)* | ✅ S1 = David AI §3, S2 = Surge Step 3 | ✅ | ✅ | 8.0 s |
| 4 | What was Decagon's annual recurring revenue in 2025? *(unsupported)* | n/a; Decagon funding/valuation passages retrieved, none mention ARR | ✅ `INSUFFICIENT EVIDENCE` | ✅ none cited | 5.6 s |

Every answer came from a fresh process with no chat history. Prompts were about 1,000–1,230 tokens (rules + 5
passages + question).

---

## Test 1: direct question, one source
**Question:** What is Sierra's pricing model?
**Expected:** `raw/Sierra - company-research.md` › Step 1: "B2B SaaS with **outcome-based pricing** ("pay for a job well done" — pay for resolved outcomes, not seats)."
**Card:** [`evidence/ask/20260930-160154-offline-test1.md`](../evidence/ask/20260930-160154-offline-test1.md)

| | Path › section | bm25 / cosine |
|---|---|---|
| S1 | raw/Sierra › Step 3 Competitive Landscape & Moat | 5.33 / 0.519 |
| **S2** | **raw/Sierra › Step 1 Company Snapshot & Business Model** | 4.69 / **0.545** |
| S3 | raw/Sierra › Step 6 Hiring Trends | 6.26 / 0.514 |
| S4 | raw/Decagon › 3. Competitive Landscape & Moat | 3.52 / 0.383 |
| S5 | raw/Decagon › Business Model Implications | 3.46 / 0.326 |

**Answer (Gemma):** "Sierra utilizes a B2B SaaS business model featuring outcome-based pricing, which means customers pay for resolved outcomes rather than for seats [S2]. This pricing model is described as "pay for a job well done" [S2]."

**Assessment: pass.** Both claims appear verbatim in S2 (Sierra Step 1). The answer adds no outside knowledge.
Retrieval note: BM25 alone ranked Step 6 higher because a job title contains "Pricing". The embedding ranked Step 1 first.

## Test 2: answerable, phrased differently from the source
**Question:** Where does Surge AI get its operating capital?
**Expected:** `raw/Surge AI - company-research.md` › Step 1: "Profitable from day one; entirely bootstrapped (no VC)" / "Zero external funding."
**Card:** [`evidence/ask/20260930-160201-offline-test2.md`](../evidence/ask/20260930-160201-offline-test2.md)

| | Path › section | bm25 / cosine |
|---|---|---|
| S1 | raw/Surge AI › Step 3 Competitive Landscape & Moat | 7.55 / 0.452 |
| S2 | raw/Surge AI › Step 1 (size & customers half) | 4.48 / 0.453 |
| **S3** | **raw/Surge AI › Step 1 (what they do / business model / funding half)** | 3.44 / **0.522** |
| S4 | raw/David AI › 3. Competitive Landscape & Moat | 4.45 / 0.390 |
| S5 | raw/David AI › 1. Company Snapshot | 5.78 / 0.372 |

**Answer (Gemma):** "Surge AI is entirely bootstrapped and has received zero external funding [S3]. The company is profitable from day one [S3]."

**Assessment: pass.** Both claims are in S3. The question's wording ("operating capital") doesn't appear in the source.
BM25 ranked the right passage only 13th. The embedding ranked it 1st, and the weighted fusion kept it in the top 5.
**Earlier failure (kept as evidence):** in the first dry run
([`dryrun-test2`](../evidence/ask/20260929-230618-dryrun-test2.md)) only the size/customers half of Step 1 was
retrieved, and Gemma correctly answered "insufficient evidence" for that input. This was a retrieval failure, not a
model failure. The fix was the dense weight of 2.0 (see the sweep in `evidence/search/retrieval-sweep-*`).

## Test 3: connects two sources
**Question:** Which AI data companies list Scale AI as a competitor?
**Expected:** `raw/David AI - company-research.md` › 3. Competitive Landscape (Scale AI row) **and** `raw/Surge AI - company-research.md` › Step 3 ("Competitors: Scale AI (Meta-backed, ~$29B) …")
**Card:** [`evidence/ask/20260930-160209-offline-test3.md`](../evidence/ask/20260930-160209-offline-test3.md)

| | Path › section | bm25 / cosine |
|---|---|---|
| **S1** | **raw/David AI › 3. Competitive Landscape & Moat** | 13.72 / 0.616 |
| **S2** | **raw/Surge AI › Step 3 Competitive Landscape & Moat** | 5.16 / 0.617 |
| S3 | raw/David AI › 3. Competitive Landscape (continued) | 5.67 / 0.524 |
| S4 | raw/Decagon › 3. Competitive Landscape & Moat | 8.71 / 0.487 |
| S5 | raw/David AI › 1. Company Snapshot | 9.37 / 0.394 |

**Answer (Gemma):** "Scale AI is listed as a competitor by David AI and Surge AI [S1][S2]. David AI differentiates itself by being audio-native and founded by former Scale operators/engineers [S1]. Surge AI lists Scale AI among its competitors, alongside Mercor, Turing, Invisible Technologies, and Appen/Labelbox [S2]."

**Assessment: pass.** Each company's claim cites that company's own file.
- The David AI differentiation matches its Scale AI row.
- Surge's competitor list matches Step 3; the source marks Appen/Labelbox as "legacy", which the answer leaves out (acceptable).

**Earlier failure (kept as evidence):** a dry run
([`dryrun2-test3`](../evidence/ask/20260929-231249-dryrun2-test3.md)) said Scale AI has "a **revenue** of approximately
$29B". The source only says "~$29B" without saying what it measures, so the citation was correct but the claim was
unsupported. The fix was a new research rule in [`instructions/wiki-instructions.md`](../instructions/wiki-instructions.md):
report numbers as written and do not name the metric unless the passage does. All four tests were rerun after the change.

## Test 4: unsupported question
**Question:** What was Decagon's annual recurring revenue in 2025?
**Expected:** no source states Decagon's ARR or revenue. The correct behavior is an explicit insufficient-evidence statement.
**Card:** [`evidence/ask/20260930-160215-offline-test4-unsupported.md`](../evidence/ask/20260930-160215-offline-test4-unsupported.md)

Retrieved (plausible but non-answering context):

| | Path › section | bm25 / cosine |
|---|---|---|
| S1 | raw/Decagon › 1. Company Snapshot (Stage & Funding: $250M Series D, $4.5B valuation) | 3.06 / 0.608 |
| S2 | raw/Decagon › Market Position | 2.54 / 0.556 |
| S3 | raw/Decagon › Broad Operations Sweep (Revenue/BizOps roles) | 2.83 / 0.531 |
| S4 | raw/David AI › 1. Company Snapshot (David AI funding rounds, ~$80M total) | 3.53 / 0.327 |
| S5 | raw/Surge AI › Step 1 (">$1B revenue" for Surge) | 4.22 / 0.284 |

**Answer (Gemma):** "INSUFFICIENT EVIDENCE: the wiki does not contain information about Decagon's annual recurring revenue in 2025."

**Assessment: pass.** This is a hard negative: the context contains Decagon's funding and valuation, plus ARR and revenue
figures for *other* companies (David AI's funding total, Surge AI's >$1B revenue). Gemma did not turn the $250M round or the
$4.5B valuation into an ARR figure, and it did not borrow another company's number.

---

## Mode checks (same offline run)

| Check | Evidence | Expected | Actual | Result |
|---|---|---|---|---|
| Search shows passages only | [`search card`](../evidence/search/20260930-160146-search.md), log step 4 | original passages + paths, no generated answer, no model call | 5 original passages with path › section and scores; no answer text | ✅ |
| Search works without the model | [`search card with Ollama stopped`](../evidence/search/20260929-231718-search.md), [`no-model log`](../evidence/offline/no-model-checks.log) | passages still returned | "BM25 keyword only (embeddings unavailable)" + passages | ✅ |
| Chat: "what can we do?" | [`offline-chat-capabilities`](../evidence/mode_checks/20260930-160253-offline-chat-capabilities.md) | capabilities, no notes search, no refusal | `retrieval: no (conversational)`; lists brainstorm, drafting, wiki search, the 7 companies, and `/save /sources /clear /exit` | ✅ |
| Chat: "what can you help me with?" | same | same | `retrieval: no`; analyze/compare, structure, synthesize, draft | ✅ |
| Chat: draft a plan "based on my notes" | [`offline-chat-followup`](../evidence/mode_checks/20260930-160403-offline-chat-followup.md) | retrieves, cites notes, labels ideas as suggestions | `retrieval: yes (mentions notes)`; 4 passages (Sierra note + raw Step 6); cites [S#] | ✅ |
| Chat: "make that shorter" | same | uses the conversation, no new search | `retrieval: no (follow-up)`; condensed version of the same 5-step plan | ✅ with caveat¹ |
| Chat: "Decagon's ARR was $300M in 2025." | same | treat as unverified, do not store as evidence | "…that detail came from you… it won't be in the wiki unless you explicitly tell me to ingest it" | ⚠️ mostly² |
| Ask after the chat claim | [`offline-chat-claim-not-evidence`](../evidence/ask/20260930-160405-offline-chat-claim-not-evidence.md) | still insufficient evidence | `INSUFFICIENT EVIDENCE…` (the $300M claim is not used) | ✅ |
| Ask with Ollama stopped | [`no-model log`](../evidence/offline/no-model-checks.log) | clear error | `error: local model unavailable … Start it with: brew services start ollama`, exit 3 | ✅ |

¹ The shortened reply reuses `[S3]`, `[S4]` from the previous turn. The labels are per-turn and the follow-up turn had no
new passages, so readers must look at the previous turn's sources (`/sources`).
² The reply opens with "I can incorporate that into our notes if you'd like", which overstates its abilities (chat cannot write to
the wiki), but it then states the correct boundary. In the earlier dry run it simply said "noted", even with the persona
rule. The small model follows this rule inconsistently. The harness boundary (ask never sees chat history) is what
actually guarantees the separation.
