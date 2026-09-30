# MODE_CHECKS evidence card

- **Time:** 2026-09-30T16:42:02
- **Interaction mode:** mode_checks
- **Execution:** local
- **Model:** gemma4:e4b
- **Latency:** n/a s

## Transcript

**user** _(retrieved: False (conversational))_

what can you help me with?

**assistant**

Hey Irene! I'm Sage, your study buddy and personal wiki assistant for your Haas MBA research on those AI startups (Clay, ClickHouse, David AI, Decagon, Harvey AI, Sierra, Surge AI). 😊

Basically, I can help you with:

*   **Brainstorming & Drafting:** Outlining, rewriting, or drafting emails and project ideas.
*   **Summarizing & Organizing:** Condensing notes or creating study plans.
*   **Wiki Lookups:** I can search your personal research notes (in your wiki) to pull up info on any of those companies or concepts!

If you need me to check your notes, just tell me what you're looking for. If I use your notes, I'll always cite where the info came from!

Also, remember you can use commands like `/save` to draft replies or `/sources` to see what I pulled from your notes!

What part of the research are you tackling today?

**user** _(retrieved: True (mentions notes/course))_

Give me a 3-bullet summary of Sierra from my notes

**assistant**

Here is a 3-bullet summary of Sierra based on your notes:

*   **Offering:** Sierra provides enterprise conversational AI agents that are deployed across various channels (chat, SMS, voice, etc.) to resolve customer issues and drive revenue [S2, S4].
*   **Business Model & Moat:** They operate on a B2B SaaS model featuring outcome-based pricing, which aligns vendor incentives with actual achieved customer outcomes [S2, S4]. Their moat is further supported by deep compliance certifications like SOC 2 and HIPAA [S3].
*   **Strategy:** The company is focused on becoming a global standard for AI-powered Customer Experience (CX) and is strategically expanding its capabilities to include internal enterprise agents [S1, S4].

Does this summary capture the main points you were looking for, or should we dive deeper into their product modules like Agent Studio?

**user** _(retrieved: False (follow-up, reusing previous notes))_

make that shorter

**assistant**

Got it. Let's condense that into a super sharp summary.

**Sierra Snapshot:**

*   **What they do:** Provide enterprise conversational AI agents for customer service across channels like chat, voice, and SMS [S4].
*   **How they make money:** They use a B2B SaaS model with outcome-based pricing, meaning they get paid based on resolved customer issues [S4, S2].
*   **Key strengths:** Their moat includes deep compliance (like HIPAA) and a platform designed to become the global standard for CX, now expanding to internal enterprise use [S3, S1, S4].

How does this shorter version feel for your outline?

## Assessment
**PASS (re-test after the fix).** Same three messages: capability question `retrieval: no`; notes summary `retrieval: yes` with 4 real passages, every [S#] maps to a passage and the claims match the Sierra note; 'make that shorter' reuses the previous passages so the labels stay valid.
