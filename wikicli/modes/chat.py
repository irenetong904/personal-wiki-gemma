"""Chat mode: personal assistant with persona, rolling conversation memory, and retrieval only when useful."""
import re
from datetime import datetime

from rich.console import Console
from rich.markdown import Markdown

from .. import config, evidence, llm, prompts, retrieval

# Explicit signals that the user is asking about their own material. Checked FIRST: an interactive test
# ("Give me a 3-bullet summary of Sierra from my notes") was misrouted because "bullet" matched the edit rule.
RETRIEVE = re.compile(
    r"\b(my notes?|wiki|class|course|lecture|assignment|professor|syllabus|according to|"
    r"remind me|what did (i|we)|in (my|our) )", re.I)
# Edits of the previous reply: no new search, the previous turn's passages are reused so [S#] stays valid.
EDIT = re.compile(
    r"make (it|that|this)|shorter|longer|rewrite|rephrase|more (formal|casual)|bullet|"
    r"translate|fix (the )?(tone|grammar)", re.I)
# Small talk and questions about the assistant itself never need a notes lookup.
SMALL_TALK = re.compile(
    r"^(hi|hello|hey|thanks|thank you|ok|cool)\b|what can (you|we)|help me with|who are you", re.I)
STRONG_MATCH = 6.0  # BM25 score that suggests a question is about the notes even without cue words
CITE = re.compile(r"\[S(\d+)")


def _companies() -> list[str]:
    try:
        from ..ingest import load_catalog
        return [s["title"] for s in load_catalog()["sources"].values()]
    except Exception:
        return []


def needs_retrieval(msg: str) -> tuple[bool, str]:
    """Returns (retrieve?, reason). Reason 'follow-up' means: reuse the previous turn's passages."""
    if RETRIEVE.search(msg):
        return True, "mentions notes/course"
    named = [c for c in _companies() if re.search(rf"\b{re.escape(c)}\b", msg, re.I)]
    if named and not EDIT.search(msg):
        return True, f"mentions {', '.join(named)}"
    if EDIT.search(msg):
        return False, "follow-up"
    if SMALL_TALK.search(msg):
        return False, "conversational"
    if msg.rstrip().endswith("?"):
        hits = retrieval.search(msg, k=1, kinds=("raw",))
        if hits and hits[0]["score"] >= STRONG_MATCH:
            return True, f"strong keyword match ({hits[0]['score']})"
    return False, "no need for notes"


def citation_warning(reply: str, passages: list[dict]) -> str | None:
    """Harness-level guard: [S#] markers must point at passages actually given to the model this turn."""
    nums = {int(n) for n in CITE.findall(reply)}
    if nums and not passages:
        return "reply contains [S#] citations but no notes were given to the model: treat them as unsupported"
    bad = sorted(n for n in nums if n > len(passages))
    if bad:
        return f"reply cites passages that do not exist: {', '.join(f'S{n}' for n in bad)}"
    return None


class ChatSession:
    def __init__(self):
        self.history: list[dict] = []   # plain user/assistant turns (no passages) = conversation context
        self.transcript: list[dict] = []
        self.last_passages: list[dict] = []

    def turn(self, msg: str) -> tuple[str, bool, str, dict]:
        use, why = needs_retrieval(msg)
        passages = []
        if use:
            passages = retrieval.search(msg, k=4)
            self.last_passages = passages
        elif why == "follow-up" and self.last_passages:
            passages = self.last_passages  # same labels as the reply being edited
            why = "follow-up, reusing previous notes"
        else:
            self.last_passages = []
        reply, stats = llm.chat(prompts.chat_messages(self.history, msg, passages),
                                temperature=config.TEMPERATURE_CHAT)
        reply = reply.strip()
        warning = citation_warning(reply, passages)
        self.history += [{"role": "user", "content": msg}, {"role": "assistant", "content": reply}]
        self.transcript += [{"role": "user", "content": msg, "retrieved": f"{use} ({why})"},
                            {"role": "assistant", "content": reply + (f"\n\n⚠ HARNESS: {warning}" if warning else ""),
                             "sources": [f"{p['path']} › {p['section']}" for p in passages]}]
        stats["citation_warning"] = warning
        return reply, use, why, stats


def run(script: list[str] | None = None, name: str | None = None):
    """Interactive REPL. `script` feeds fixed messages (used for the recorded mode checks)."""
    console = Console()
    llm.check_model()
    console.print(f"[bold]chat[/bold] · Sage · model [cyan]{config.MODEL}[/cyan] · execution [green]local[/green]")
    console.print("[dim]/save  /sources  /clear  /exit[/dim]\n")
    s = ChatSession()
    queue = list(script) if script else None
    while True:
        if queue is not None:
            if not queue:
                break
            msg = queue.pop(0)
            console.print(f"[bold magenta]you ›[/bold magenta] {msg}")
        else:
            try:
                msg = console.input("[bold magenta]you ›[/bold magenta] ").strip()
            except (EOFError, KeyboardInterrupt):
                break
        if not msg:
            continue
        if msg in ("/exit", "/quit"):
            break
        if msg == "/clear":
            s.history.clear()
            console.print("[dim]conversation cleared[/dim]")
            continue
        if msg == "/sources":
            for i, p in enumerate(s.last_passages, 1):
                console.print(f"[S{i}] {p['path']} › {p['section']}\n{p['text']}\n")
            if not s.last_passages:
                console.print("[dim]no notes were retrieved last turn[/dim]")
            continue
        if msg == "/save":
            if s.history:
                config.CHAT_SAVES.mkdir(parents=True, exist_ok=True)
                f = config.CHAT_SAVES / f"draft-{datetime.now():%Y%m%d-%H%M%S}.md"
                f.write_text(f"<!-- chat draft, NOT source evidence -->\n\n{s.history[-1]['content']}\n")
                console.print(f"[dim]saved draft → {f.relative_to(config.ROOT)}[/dim]")
            continue
        # A cold model load takes ~30 s; show that the harness is working instead of a frozen prompt
        with console.status("[dim]Sage is thinking… (first reply loads the model, ~30 s)[/dim]"):
            reply, used, why, stats = s.turn(msg)
        console.print(f"[dim]retrieval: {'yes' if used else 'no'} ({why}) · {stats['seconds']} s[/dim]")
        console.print("[bold green]Sage ›[/bold green]")
        console.print(Markdown(reply))
        if stats.get("citation_warning"):
            console.print(f"[bold red]⚠ {stats['citation_warning']}[/bold red]")
        elif s.last_passages and CITE.search(reply):
            console.print("[dim]" + " · ".join(f"S{i} {p['path'][4:]} › {p['section'][:40]}"
                                               for i, p in enumerate(s.last_passages, 1)) + "[/dim]")
        console.print()
    if s.transcript:
        path = evidence.save("mode_checks", {"transcript": s.transcript,
                                             "stats": {"model": config.MODEL, "execution": "local"}},
                             name=name or "chat")
        console.print(f"[dim]transcript saved → {path}[/dim]")
