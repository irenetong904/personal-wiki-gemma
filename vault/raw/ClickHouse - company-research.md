# ClickHouse — Company Research

---

### Step 1: Company Snapshot & Business Model
- **What they do:** The leading open-source, column-oriented **OLAP database** for real-time analytics at petabyte scale, now positioned as "the leading database for AI" (millisecond queries for agentic systems). Spans real-time analytics, data warehousing, observability (ClickStack), and ML/GenAI.
- **Business Model:** Open-source core (49k+ GitHub stars) + commercial **ClickHouse Cloud** (managed, **usage/consumption-based** pricing, from ~$50/mo) on AWS/GCP/Azure. Classic OSS-to-cloud PLG + enterprise sales.
- **Stage & Funding:** **Series D — $400M at ~$15B valuation (Jan 16, 2026)**, led by **Dragoneer** (Bessemer, GIC, Index, Khosla, Lightspeed, T. Rowe, WCM). Up ~2.5x from $6.35B (May 2025). Concurrent: **acquired Langfuse** (LLM observability) + launched native **Postgres**. 4,000+ customers; ARR grown >250% YoY. Founded 2021 (project created 2016 at Yandex).
- **Size & Location:** HQ **Portola Valley / Bay Area, CA**; distributed across 20+ countries.
- **Customers:** Meta, Microsoft, Sony, Tesla, Lyft, Spotify, eBay, Cisco, IBM, GitLab, **Anthropic** ("instrumental in helping us ship Claude 4"), Cursor, Sierra, Vercel, Ramp, Deutsche Bank, Instacart, HubSpot.

### Step 2: Product Portfolio Deep-Dive
- **Core products:** ClickHouse (OSS), ClickHouse Cloud (managed), ClickHouse Local (query local files), **ClickStack** (OSS observability: logs/metrics/traces), **ClickPipes** (ingestion/CDC/streaming), + **Langfuse** (LLM observability/evals) + native **Postgres** (transactional + analytical unification).
- **Use cases:** Real-time analytics/dashboards, observability at scale (Anthropic, Character.AI GPU fleets), warehousing (BigQuery/Elasticsearch migrations), ML/GenAI (vector search, aggregations, training data).
- **Recent evolution:** Aggressive AI pivot (2025–26): "database for AI," Langfuse acquisition (Jan 2026), Postgres launch, wave of AI/ML + GTM-automation hiring.

### Step 3: Competitive Landscape & Moat
- **Competitors:** **Snowflake** & **Databricks** (cloud data platforms — the "challenger" framing), Elasticsearch/OpenSearch (observability/log migrations), Apache Druid/Pinot/StarRocks (real-time OLAP), Datadog/Grafana (observability, via ClickStack).
- **Moat:** Extreme query speed + compression (100x on OLAP), open-source adoption flywheel, cost-efficiency vs. warehouses, first-mover "speed layer for AI" positioning; strong migration story (cheaper/faster than Elastic/BigQuery).
- **Position:** Category leader in real-time/OLAP; credible Snowflake/Databricks challenger at $15B.

### Step 4: Future Goals & Growth Opportunities
- **Strategic focus:** Become the default database layer for AI/agentic apps + observability; monetize consumption at scale; integrate Langfuse + Postgres into a unified stack.
- **Scale next:** LLM observability (Langfuse), transactional+analytical convergence (Postgres), enterprise/financial-services, international (APAC/EMEA hiring).

### Step 5: Leadership Team (Targeted)
- **Aaron Katz — CEO & Co-founder.** Former CRO at Elastic; ex-Salesforce.
- **Alexey Milovidov — CTO & Co-founder.** Creator of ClickHouse at Yandex (2016).
- **Yury Izrailevsky — President, Product & Engineering (Co-founder).** Ex-Google VP Engineering, ex-Netflix VP Cloud.
- **Krithika Balagurunathan — Head of Product, ClickHouse Cloud.**
- **Dorota Szeremeta — VP, Operations** (ex-Salesforce). **VP, Revenue Operations** (unnamed publicly) owns the Commercial Strategy & Ops reqs; **Mike Hayes — VP, Sales.**

### Step 6: Hiring Trends & Target Roles Deep-Dive
- **Macro trend:** ~167 open roles (Greenhouse) — heavy engineering, but a clear, well-defined **RevOps / commercial-systems build-out** driven by the consumption model; professionalizing GTM/commercial infrastructure post-$400M raise.
- **Open roles most relevant (US; links live):**
  - **Director, Commercial Strategy & Operations** — $225–300K. Owns pricing strategy/packaging for a usage-based model, discount governance, CPQ/Q2C automation, marketplace ops (AWS/GCP/Azure). Requires SQL + pricing modeling. *(Senior, 10+ yrs — aspirational, but the clearest S&O charter.)*
  - **GTM Engineer, AI & Automation** — $145–225K. Builds AI/agents/automation across GTM (enrichment, routing, outbound, expansion signals) in RevOps; stack Salesforce/Gong/Clay/n8n/Python/TS/dbt/LLM APIs/Langfuse/ClickHouse. **Best GTM-Engineer match, though BS in engineering required.**
  - **Sr Finance Analyst, Product & GTM** (BizOps/FP&A × GTM).
  - **Marketing Operations Manager**; **Data Scientist, Finance Forecasting** (SF hybrid); **AR & Billing Operations Manager**; **Head of Website Growth**.

---
*Sources: clickhouse.com (site, /company/careers, /our-story), Series D blog + BusinessWire (Jan 16 2026), TechCrunch (Jan 16 2026), live Greenhouse board (job-boards.greenhouse.io/clickhouse), Forbes. Caveat: VP RevOps name not public; employee count not officially disclosed.*
