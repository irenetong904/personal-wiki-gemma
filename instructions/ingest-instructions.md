# Ingestion instructions (sent to Gemma once per source file)

You turn ONE source document into a wiki note for a personal knowledge base.

Rules:
- Use only facts stated in the source. Do not add outside knowledge, guesses, or dates that are not in the text.
- `title`: the subject of the document in 2-6 words, Title Case, no dates, no file names, no punctuation except hyphens. For a company profile use just the company name, e.g. "Decagon", "Harvey AI".
- `company_name`: if the document profiles one company, its name exactly as written in the first heading (e.g. "Sierra", "Harvey AI"); otherwise "".
- `folder`: exactly one of: Companies, Concepts.
  - Companies = the document is mainly about one company. Concepts = the document is mainly about an idea.
- `summary`: 2-3 plain sentences.
- `key_points`: 4-8 short factual bullets. Each has `point` and `section` (the `## heading` in the source where it appears).
- `concepts`: 3-6 important general ideas this document discusses (e.g. "Outcome-Based Pricing", "AI Customer Service Agents", "Human Data for AI"), each with `name` (2-4 words, Title Case) and `why` (one sentence on how THIS document uses the idea).

Return ONLY JSON with this shape:
{"title": "...", "company_name": "...", "folder": "...", "summary": "...",
 "key_points": [{"point": "...", "section": "..."}],
 "concepts": [{"name": "...", "why": "..."}]}
