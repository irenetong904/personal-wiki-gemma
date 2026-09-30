# Retrieval check — v2a-bm25-diversity

- time: 2026-09-29 22:18 · top_k=5 · method: BM25 keyword only (embeddings unavailable)

## Q1: What is Sierra's pricing model?
Expected: [('Sierra', 'Step 1')] → **FAIL**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 6.26 | raw/Sierra - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div |   - **Product Manager / Strategist, Agent Development** — SF/NY/London/Singapore/Sydney -  |
| 2 | 5.33 | raw/Sierra - company-research.md | Step 3: Competitive Landscape & Moat | - **Direct competitors:** Decagon, Intercom (Fin), Parloa, Salesforce Agentforce, Ada, Cre |
| 3 | 4.86 | raw/ClickHouse - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div | - **Macro trend:** ~167 open roles (Greenhouse) — heavy engineering, but a clear, well-def |
| 4 | 4.84 | raw/Decagon - company-research.md | Risks / Watchouts | / Risk / Why It Matters / /---/---/ / Services intensity / Large deployment strategist hir |
| 5 | 3.79 | raw/Decagon - company-research.md | 1. Company Snapshot & Business Model | / Category / Details / /---/---/ / Website / https://decagon.ai/ / / What They Do / Decago |

## Q2: Where does Surge AI get its operating capital?
Expected: [('Surge AI', 'Step 1')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 7.55 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 2 | 5.78 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 3 | 5.66 | raw/Decagon - company-research.md | Leadership / Culture Signals | / Signal / Interpretation / /---/---/ / Values: Just Get It Done, Invent What Customers Wa |
| 4 | 4.96 | raw/Harvey AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** Legora, Robin AI, Spellbook (contract-focused), Thomson Reuters CoCouns |
| 5 | 4.48 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **Size & Location:** Lean — **~100–120 employees** at the $1B milestone (getlatka lists  |

## Q3: Which AI data companies list Scale AI as a competitor?
Expected: [('David AI', 'Competitive Landscape'), ('Surge AI', 'Step 3')] → **PASS**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 13.72 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 2 | 9.64 | raw/David AI - company-research.md | Sources | - David AI homepage: https://www.withdavid.ai/ - David AI jobs / YC company profile: https |
| 3 | 8.71 | raw/Decagon - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / Decagon Differentiation Angle / /---/---/---/ |
| 4 | 7.41 | raw/Surge AI - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div |   - **Data Science, Growth**; **AI Programs Analyst (Finance Domain)**; **Business Analyst |
| 5 | 5.16 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |

## Q4: What was Decagon's annual recurring revenue in 2025?
Expected: no supporting passage → **n/a (unsupported question)**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 4.22 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Human-data company for frontier AI — RLHF/data labeling, **RL environm |
| 2 | 3.53 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 3 | 3.33 | raw/Clay - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div | - **Where to find live reqs:** [clay.com/jobs](https://www.clay.com/jobs) + the ecosystem  |
| 4 | 3.28 | raw/Harvey AI - company-research.md | Step 2: Product Portfolio Deep-Dive | - **Recent evolution:** Shift from "assistant" to **agentic / long-horizon agents** (2025– |
| 5 | 3.25 | raw/Clay - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** GTM data + agentic-automation platform — combines 1st/3rd-party data f |
