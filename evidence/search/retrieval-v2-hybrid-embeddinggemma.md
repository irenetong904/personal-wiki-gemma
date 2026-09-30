# Retrieval check — v2-hybrid-embeddinggemma

- time: 2026-09-29 23:05 · top_k=5 · method: hybrid: BM25 + embeddinggemma cosine, reciprocal rank fusion

## Q1: What is Sierra's pricing model?
Expected: [('Sierra', 'Step 1')] → **FAIL**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 6.26 / 0.514 | raw/Sierra - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div |   - **Product Manager / Strategist, Agent Development** — SF/NY/London/Singapore/Sydney -  |
| 2 | 5.33 / 0.519 | raw/Sierra - company-research.md | Step 3: Competitive Landscape & Moat | - **Direct competitors:** Decagon, Intercom (Fin), Parloa, Salesforce Agentforce, Ada, Cre |
| 3 | 3.52 / 0.383 | raw/Decagon - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / Decagon Differentiation Angle / /---/---/---/ |
| 4 | 3.46 / 0.326 | raw/Decagon - company-research.md | Business Model Implications | / Signal / What It Means / /---/---/ / Enterprise logos and case studies / Sales motion is |
| 5 | 2.62 / 0.364 | raw/Clay - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** GTM data + agentic-automation platform — combines 1st/3rd-party data f |

## Q2: Where does Surge AI get its operating capital?
Expected: [('Surge AI', 'Step 1')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 7.55 / 0.452 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 2 | 4.48 / 0.453 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **Size & Location:** Lean — **~100–120 employees** at the $1B milestone (getlatka lists  |
| 3 | 5.78 / 0.372 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 4 | 4.45 / 0.39 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 5 | 3.49 / 0.298 | raw/Harvey AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Domain-specific ("professional-class") AI for legal & professional ser |

## Q3: Which AI data companies list Scale AI as a competitor?
Expected: [('David AI', 'Competitive Landscape'), ('Surge AI', 'Step 3')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 13.72 / 0.616 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 2 | 5.67 / 0.524 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Appen / TELUS International AI / Indirect incumbent / Established contributor networks a |
| 3 | 5.16 / 0.617 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 4 | 8.71 / 0.487 | raw/Decagon - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / Decagon Differentiation Angle / /---/---/---/ |
| 5 | 4.78 / 0.378 | raw/Harvey AI - company-research.md | Step 4: Future Goals & Growth Opportunities | - **Strategic focus:** Scale the number of agents customers run; expand embedded legal-eng |

## Q4: What was Decagon's annual recurring revenue in 2025?
Expected: no supporting passage → **n/a (unsupported question)**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 3.06 / 0.608 | raw/Decagon - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series D. Decagon announced $250M led by Coatue and Index Ventures in  |
| 2 | 2.83 / 0.531 | raw/Decagon - company-research.md | Broad Operations Sweep | / Revenue / BizOps / Yes / Revenue Strategy & Operations Manager; BizOps & Strategy, Prici |
| 3 | 3.53 / 0.327 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 4 | 4.22 / 0.284 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Human-data company for frontier AI — RLHF/data labeling, **RL environm |
| 5 | 3.07 / 0.289 | raw/Sierra - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Enterprise conversational AI agents deployed across chat, SMS, WhatsAp |
