# Retrieval check — v1-bm25-baseline

- time: 2026-09-29 22:13 · top_k=5 · method: BM25 keyword (rank_bm25)

## Q1: What is Sierra's pricing model?
Expected: [('Sierra', 'Step 1')] → **PASS**

| rank | score | path | section | text |
|---|---|---|---|---|
| 1 | 6.21 | raw/Sierra - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div |   - **Product Manager / Strategist, Agent Development** — SF/NY/London/Singapore/Sydney -  |
| 2 | 5.3 | raw/Sierra - company-research.md | Step 3: Competitive Landscape & Moat | - **Direct competitors:** Decagon, Intercom (Fin), Parloa, Salesforce Agentforce, Ada, Cre |
| 3 | 5.03 | raw/ClickHouse - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div | - **Macro trend:** ~167 open roles (Greenhouse) — heavy engineering, but a clear, well-def |
| 4 | 4.98 | raw/Decagon - company-research.md | Risks / Watchouts | / Risk / Why It Matters / /---/---/ / Services intensity / Large deployment strategist hir |
| 5 | 4.7 | raw/Sierra - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Enterprise conversational AI agents deployed across chat, SMS, WhatsAp |

## Q2: Where does Surge AI get its operating capital?
Expected: [('Surge AI', 'Step 1')] → **FAIL**

| rank | score | path | section | text |
|---|---|---|---|---|
| 1 | 7.43 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 2 | 6.7 | raw/Surge AI - company-research.md | Surge AI — Company Research | --- |
| 3 | 5.77 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 4 | 5.62 | raw/Decagon - company-research.md | Leadership / Culture Signals | / Signal / Interpretation / /---/---/ / Values: Just Get It Done, Invent What Customers Wa |
| 5 | 4.94 | raw/Harvey AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** Legora, Robin AI, Spellbook (contract-focused), Thomson Reuters CoCouns |

## Q3: Which AI data companies list Scale AI as a competitor?
Expected: [('David AI', 'Competitive Landscape'), ('Surge AI', 'Step 3')] → **FAIL**

| rank | score | path | section | text |
|---|---|---|---|---|
| 1 | 13.99 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 2 | 9.83 | raw/David AI - company-research.md | Sources | - David AI homepage: https://www.withdavid.ai/ - David AI jobs / YC company profile: https |
| 3 | 9.52 | raw/David AI - company-research.md | Risks / Watchouts | / Risk / Why It Matters / /---/---/ / Customer concentration / Frontier AI labs and Mag 7  |
| 4 | 9.46 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Target Audience / Key Customers / Frontier AI labs, Mag 7 / FAANG companies, and enterpr |
| 5 | 8.9 | raw/David AI - company-research.md | Sources | - Product Engineer JD: https://www.ycombinator.com/companies/david-ai/jobs/nBFCaze-product |

## Q4: What was Decagon's annual recurring revenue in 2025?
Expected: no supporting passage → **n/a (unsupported question)**

| rank | score | path | section | text |
|---|---|---|---|---|
| 1 | 4.29 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Human-data company for frontier AI — RLHF/data labeling, **RL environm |
| 2 | 3.59 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 3 | 3.38 | raw/Clay - company-research.md | Step 6: Hiring Trends & Target Roles Deep-Div | - **Where to find live reqs:** [clay.com/jobs](https://www.clay.com/jobs) + the ecosystem  |
| 4 | 3.33 | raw/Harvey AI - company-research.md | Step 2: Product Portfolio Deep-Dive | - **Recent evolution:** Shift from "assistant" to **agentic / long-horizon agents** (2025– |
| 5 | 3.29 | raw/Clay - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** GTM data + agentic-automation platform — combines 1st/3rd-party data f |
