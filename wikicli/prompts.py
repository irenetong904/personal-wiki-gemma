"""Prompt assembly. Instructions are loaded from files so the rules stay explicit and editable."""
from . import config


def load(name: str) -> str:
    return (config.INSTRUCTIONS_DIR / name).read_text(encoding="utf-8")


def format_passages(passages: list[dict]) -> str:
    blocks = []
    for i, p in enumerate(passages, 1):
        blocks.append(f'[S{i}] ({p["path"]} > {p["section"]})\n{p["text"]}')
    return "\n\n".join(blocks)


def ask_messages(question: str, passages: list[dict]) -> list[dict]:
    """Ask mode: research rules + evidence + question. No persona, no history."""
    sources = format_passages(passages) if passages else "(no passages matched)"
    return [
        {"role": "system", "content": load("wiki-instructions.md")},
        {"role": "user", "content": f"SOURCES:\n{sources}\n\nQUESTION: {question}"},
    ]


def chat_messages(history: list[dict], user_msg: str, passages: list[dict] | None) -> list[dict]:
    """Chat mode: persona + recent turns + (optional) retrieved notes for this turn only."""
    msgs = [{"role": "system", "content": load("persona.md")}]
    msgs += history[-2 * config.CHAT_HISTORY_TURNS:]
    if passages:
        content = (f"Notes retrieved from Irene's wiki for this message:\n{format_passages(passages)}\n\n"
                   f"Message: {user_msg}")
    else:
        content = user_msg
    msgs.append({"role": "user", "content": content})
    return msgs


def ingest_messages(source_name: str, text: str) -> list[dict]:
    return [
        {"role": "system", "content": load("ingest-instructions.md")},
        {"role": "user", "content": f"SOURCE FILE: {source_name}\n\n{text[:config.INGEST_MAX_CHARS]}"},
    ]


def concept_messages(name: str, passages: list[dict]) -> list[dict]:
    return [
        {"role": "system", "content": (
            "Write a short wiki note about one concept using ONLY the numbered passages. "
            'Return JSON: {"summary": "2-3 sentences", "details": [{"point": "...", "source": "S#"}]} '
            "with 2-5 details. Do not add outside knowledge.")},
        {"role": "user", "content": f"CONCEPT: {name}\n\nPASSAGES:\n{format_passages(passages)}"},
    ]


def theme_messages(listing: str, existing: list[str]) -> list[dict]:
    reuse = ("Existing theme names (reuse them exactly when they still fit): " + ", ".join(existing)) if existing else ""
    return [
        {"role": "system", "content": (
            "You organize a personal wiki about companies. Group the companies' topics into 4-8 shared THEMES. "
            "Each theme must apply to at least 2 companies, be a general idea (not a company or product name), "
            "and have a 2-4 word Title Case name. For each member, write one sentence on how that company relates "
            "to the theme, using only the topics given. "
            'Return JSON: {"themes": [{"name": "...", "members": [{"company": "<exact company name>", "why": "..."}]}]}')},
        {"role": "user", "content": f"{reuse}\n\nCOMPANIES AND THEIR TOPICS:\n{listing}"},
    ]


def assign_messages(company: str, topics: str, theme_names: list[str]) -> list[dict]:
    return [
        {"role": "system", "content": (
            "Decide which EXISTING wiki themes a company clearly belongs to, using only its topics. "
            "Never invent new theme names. For each match write one sentence on how the company relates to it. "
            'Return JSON: {"themes": [{"name": "<exact existing theme name>", "why": "..."}]} (empty list if none).')},
        {"role": "user", "content": f"THEMES: {', '.join(theme_names)}\n\nCOMPANY: {company}\nTOPICS: {topics}"},
    ]
