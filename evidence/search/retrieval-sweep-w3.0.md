# Retrieval check — sweep-w3.0

- time: 2026-09-29 23:12 · top_k=5 · method: hybrid: BM25 + embeddinggemma cosine, reciprocal rank fusion

## Q1: What is Sierra's pricing model?
Expected: [('Sierra', 'pay for resolved outcomes')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 4.69 / 0.545 | raw/Sierra - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Enterprise conversational AI agents deployed across chat, SMS, WhatsAp |
| 2 | 5.33 / 0.519 | raw/Sierra - company-research.md | Step 3: Competitive Landscape & Moat | - **Direct competitors:** Decagon, Intercom (Fin), Parloa, Salesforce Agentforce, Ada, Cre |
| 3 | 6.26 / 0.514 | raw/Sierra - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div |   - **Product Manager / Strategist, Agent Development** — SF/NY/London/Singapore/Sydney -  |
| 4 | 3.52 / 0.383 | raw/Decagon - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / Decagon Differentiation Angle / /---/---/---/ |
| 5 | 3.46 / 0.326 | raw/Decagon - company-research.md | Business Model Implications | / Signal / What It Means / /---/---/ / Enterprise logos and case studies / Sales motion is |

## Q2: Where does Surge AI get its operating capital?
Expected: [('Surge AI', 'entirely bootstrapped')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 7.55 / 0.452 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 2 | 4.48 / 0.453 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **Size & Location:** Lean — **~100–120 employees** at the $1B milestone (getlatka lists  |
| 3 | 3.44 / 0.522 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Human-data company for frontier AI — RLHF/data labeling, **RL environm |
| 4 | 4.45 / 0.39 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 5 | 5.78 / 0.372 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |

## Q3: Which AI data companies list Scale AI as a competitor?
Expected: [('David AI', '| Scale AI |'), ('Surge AI', '**Scale AI** (Meta-backed')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 13.72 / 0.616 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 2 | 5.16 / 0.617 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 3 | 5.67 / 0.524 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Appen / TELUS International AI / Indirect incumbent / Established contributor networks a |
| 4 | 8.71 / 0.487 | raw/Decagon - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / Decagon Differentiation Angle / /---/---/---/ |
| 5 | 9.37 / 0.394 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Target Audience / Key Customers / Frontier AI labs, Mag 7 / FAANG companies, and enterpr |

## Q4: What was Decagon's annual recurring revenue in 2025?
Expected: no supporting passage → **n/a (unsupported question)**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 3.06 / 0.608 | raw/Decagon - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series D. Decagon announced $250M led by Coatue and Index Ventures in  |
| 2 | 2.54 / 0.556 | raw/Decagon - company-research.md | Market Position | Decagon appears to be an enterprise leader / category disruptor in AI customer experience  |
| 3 | 2.28 / 0.566 | raw/Decagon - company-research.md | 4. Future Goals & Growth Opportunities | **Strategic Focus:** Decagon's next big milestone is scaling from high-touch enterprise wi |
| 4 | 3.53 / 0.327 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 5 | 4.22 / 0.284 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Human-data company for frontier AI — RLHF/data labeling, **RL environm |
