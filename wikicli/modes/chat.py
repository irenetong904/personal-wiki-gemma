"""Chat mode: personal assistant with persona, rolling conversation memory, and retrieval only when useful."""
import re
from datetime import datetime

from rich.console import Console
from rich.markdown import Markdown

from .. import config, evidence, llm, prompts, retrieval

# Turns that are about the assistant itself or about the previous reply never need a notes lookup.
NO_RETRIEVE = re.compile(
    r"^(hi|hello|hey|thanks|thank you|ok|cool)\b|what can (you|we)|help me with|who are you|"
    r"make (it|that|this)|shorter|longer|rewrite|rephrase|more (formal|casual)|bullet|"
    r"translate|fix (the )?(tone|grammar)", re.I)
# Explicit signals that the user is asking about their own material.
RETRIEVE = re.compile(
    r"\b(my notes?|wiki|class|course|lecture|assignment|professor|syllabus|according to|"
    r"remind me|what did (i|we)|in (my|our) )", re.I)
STRONG_MATCH = 6.0  # BM25 score that suggests a question is about the notes even without cue words


def needs_retrieval(msg: str) -> tuple[bool, str]:
    if NO_RETRIEVE.search(msg):
        return False, "conversational / follow-up"
    if RETRIEVE.search(msg):
        return True, "mentions notes/course"
    if msg.rstrip().endswith("?"):
        hits = retrieval.search(msg, k=1, kinds=("raw",))
        if hits and hits[0]["score"] >= STRONG_MATCH:
            return True, f"strong keyword match ({hits[0]['score']})"
    return False, "no need for notes"


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
        reply, stats = llm.chat(prompts.chat_messages(self.history, msg, passages),
                                temperature=config.TEMPERATURE_CHAT)
        reply = reply.strip()
        self.history += [{"role": "user", "content": msg}, {"role": "assistant", "content": reply}]
        self.transcript += [{"role": "user", "content": msg, "retrieved": f"{use} ({why})"},
                            {"role": "assistant", "content": reply,
                             "sources": [f"{p['path']} › {p['section']}" for p in passages]}]
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
        reply, used, why, stats = s.turn(msg)
        console.print(f"[dim]retrieval: {'yes' if used else 'no'} ({why}) · {stats['seconds']} s[/dim]")
        console.print("[bold green]Sage ›[/bold green]")
        console.print(Markdown(reply))
        console.print()
    if s.transcript:
        path = evidence.save("mode_checks", {"transcript": s.transcript,
                                             "stats": {"model": config.MODEL, "execution": "local"}},
                             name=name or "chat")
        console.print(f"[dim]transcript saved → {path}[/dim]")
