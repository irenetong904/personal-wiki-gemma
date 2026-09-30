# Wiki review log (generated notes checked against vault/raw originals)

Rule: corrections go into the wiki notes; the originals in `vault/raw/` are never edited.
Edited notes are marked `reviewed: true` so re-ingestion cannot overwrite the correction.

## Ingest run 1: rejected (see `evidence/measurements/ingest-run1.log`)
- Titles ignored the "company name only" rule: `Harvey AI Company Research.md`, `ClickHouse Database Company Profile.md`.
  **Fix (harness):** ingest prompt now returns `company_name`, which the harness uses for company notes.
- 0 concept notes: every source named the same idea differently ("Outcome-Based Pricing" / "Usage-Based Pricing" /
  "Credit-Based Pricing"), so exact matching found no shared concepts.
  **Fix (harness):** Gemma consolidation step groups topics from all sources into themes with 2+ members.

## Ingest run 2: themes reviewed (before: `concepts-before-review/`, `catalog-before-review.json`)
| Problem found | Action |
|---|---|
| "Advanced AI Capabilities": vague name; 3 members but the text covered only David AI (evidence query used the vague name alone, so the other members matched nothing) | Removed. Harness fix: the evidence query is now `theme + member reason`, so every member contributes passages |
| "Data Infrastructure Focus" overlapped with the above | Merged into **AI Training Data** / **AI Evaluation and Testing** |
| Missing obvious relations: Sierra ↔ Decagon name each other as direct competitors; David AI ↔ Surge AI both sell data to labs and list Scale AI | New themes **AI Customer Service Agents** and **AI Training Data** |
| "Business Model Innovation", "Enterprise Market Strategy", "Agentic System Design": generic names | Renamed **Pricing and Business Models**, **Enterprise Trust and Compliance**, **Agent Building Platforms**; membership re-checked |

The reviewed theme map (names, members, and a one-line reason per member, each traceable to the original) is stored in
`data/source_catalog.json` → `concepts`. Gemma then regenerated the six concept notes from retrieved raw passages.

## Statement-level corrections after reading every note against its source
| Note | Generated text | Problem | Corrected to |
|---|---|---|---|
| Concepts/AI Training Data | Summary described only David AI | Misleading: the theme covers David AI and Surge AI | Summary now covers both and notes that both list Scale AI as a competitor |
| Concepts/AI Evaluation and Testing | "Decagon offers a category around ongoing agent QA…" | Overstated: the source says these tools *could create a potential* category | Wording now matches the source |
| Companies/Harvey AI | "Raised over $1B, reaching $200M at an $11B valuation" | Conflates the round size with total funding | "Raised $200M at an $11B valuation in March 2026; total funding raised exceeds $1B." |

Checked and supported (no change): all key points in Clay, ClickHouse, David AI (including the Growth Ops "A/B testing" and
"channel experiments" points → raw lines 151–152), Decagon (the "repeatable systems" point → raw line 153), Sierra, and
Surge AI; the remaining concept notes.

## After the forced re-ingest of Sierra (duplicate check)
Re-ingesting Sierra with `--force` regenerated the four unreviewed concept notes that include Sierra. Re-reading them
found a **new error that the earlier version did not have**:

| Note | Generated text | Problem | Corrected to |
|---|---|---|---|
| Concepts/Enterprise Trust and Compliance | Harvey AI certifications "…GDPR, and HIPAA" | **Cross-passage contamination**: HIPAA appears only in Sierra's passage, not Harvey's | "…GDPR, and AIUC-1" (matches the Harvey original) |
| Concepts/Agent Building Platforms | "certified AI agents in legal, such as AIUC-1" | Reads as if AIUC-1 were an agent | "launched the first certified AI agents in legal (AIUC-1 certification)" |

Lesson: regeneration is not idempotent in content (same prompt, temperature 0.2, different details), so every
regenerated note needs review, and corrected notes must be marked `reviewed: true`.
