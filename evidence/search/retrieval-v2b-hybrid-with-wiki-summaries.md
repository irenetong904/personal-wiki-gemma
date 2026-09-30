# Retrieval check — v2-hybrid-embeddinggemma

- time: 2026-09-29 23:05 · top_k=5 · method: hybrid: BM25 + embeddinggemma cosine, reciprocal rank fusion

## Q1: What is Sierra's pricing model?
Expected: [('Sierra', 'Step 1')] → **FAIL**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 5.21 / 0.675 | wiki/Companies/Sierra.md | Sierra | Sierra provides enterprise conversational AI agents deployed across multiple channels to r |
| 2 | 6.32 / 0.604 | wiki/Concepts/AI Customer Service Agents.md | Details | - Sierra's moat includes outcome-based pricing and deep compliance certifications such as  |
| 3 | 5.13 / 0.67 | wiki/Companies/Sierra.md | Key points | - Deploys conversational AI agents across chat, SMS, WhatsApp, email, voice, and ChatGPT.  |
| 4 | 6.86 / 0.554 | wiki/Concepts/Pricing and Business Models.md | Details | - Clay utilizes credit-based usage pricing for its self-serve + enterprise SaaS model. ([[ |
| 5 | 4.57 / 0.581 | wiki/Concepts/AI Customer Service Agents.md | Details | - Sierra offers enterprise conversational AI agents deployed across multiple channels incl |

## Q2: Where does Surge AI get its operating capital?
Expected: [('Surge AI', 'Step 1')] → **FAIL**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 5.27 / 0.623 | wiki/Companies/Surge AI.md | Surge AI | Surge AI is a human-data company focused on providing intelligence for frontier AI, offeri |
| 2 | 5.19 / 0.517 | wiki/Companies/Surge AI.md | Sources | - Original: [[raw/Surge AI - company-research.md]] (unchanged copy in `raw/`) |
| 3 | 7.04 / 0.452 | raw/Surge AI - company-research.md | Step 3: Competitive Landscape & Moat | - **Competitors:** **Scale AI** (Meta-backed, ~$29B), Mercor, Turing, Invisible Technologi |
| 4 | 5.05 / 0.463 | wiki/Concepts/AI Training Data.md | Where it appears in my notes | - [[David AI]] — Designs, collects and evaluates audio datasets for frontier AI labs, and  |
| 5 | 4.79 / 0.465 | wiki/Concepts/AI Training Data.md | Details | - David AI creates audio datasets for speech recognition, translation, synthesis, and conv |

## Q3: Which AI data companies list Scale AI as a competitor?
Expected: [('David AI', 'Competitive Landscape'), ('Surge AI', 'Step 3')] → **FAIL**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 11.72 / 0.644 | wiki/Concepts/AI Training Data.md | Where it appears in my notes | - [[David AI]] — Designs, collects and evaluates audio datasets for frontier AI labs, and  |
| 2 | 16.37 / 0.611 | wiki/Concepts/AI Training Data.md | AI Training Data | Two companies in my notes sell training and evaluation data to frontier AI labs. David AI  |
| 3 | 11.62 / 0.616 | raw/David AI - company-research.md | 3. Competitive Landscape & Moat | / Competitor / Category / Why They Compete / David AI Differentiation Angle / /---/---/--- |
| 4 | 10.1 / 0.565 | wiki/Companies/Surge AI.md | Related | - [[AI Evaluation and Testing]] — Sells evaluations and benchmarks and critiques leaderboa |
| 5 | 8.3 / 0.555 | wiki/Companies/David AI.md | Related | - [[AI Evaluation and Testing]] — Evaluates whether its data improves model capabilities,  |

## Q4: What was Decagon's annual recurring revenue in 2025?
Expected: no supporting passage → **n/a (unsupported question)**

| rank | bm25 / cosine | path | section | text |
|---|---|---|---|---|
| 1 | 3.34 / 0.608 | raw/Decagon - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series D. Decagon announced $250M led by Coatue and Index Ventures in  |
| 2 | 3.31 / 0.531 | raw/Decagon - company-research.md | Broad Operations Sweep | / Revenue / BizOps / Yes / Revenue Strategy & Operations Manager; BizOps & Strategy, Prici |
| 3 | 4.24 / 0.327 | raw/David AI - company-research.md | 1. Company Snapshot & Business Model | / Stage & Funding / Series B. Public company announcements show $5M seed in Jan 2025, $25M |
| 4 | 4.95 / 0.284 | raw/Surge AI - company-research.md | Step 1: Company Snapshot & Business Model | - **What they do:** Human-data company for frontier AI — RLHF/data labeling, **RL environm |
| 5 | 2.19 / 0.48 | wiki/Companies/Decagon.md | Key points | - The company values include Just Get It Done, Invent What Customers Want, Winner's Mindse |
