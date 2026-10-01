"""Ask mode: standalone RAG. Question -> retrieve -> prompt with evidence -> local Gemma -> check citations."""
import re

from rich.console import Console
from rich.markdown import Markdown

from .. import config, evidence, llm, prompts, retrieval

CITE = re.compile(r"\[S(\d+)\]")


def check_citations(answer: str, passages: list[dict]) -> dict:
    nums = sorted({int(n) for n in CITE.findall(answer)})
    valid = [n for n in nums if 1 <= n <= len(passages)]
    insufficient = answer.strip().upper().startswith("INSUFFICIENT EVIDENCE")
    return {
        "cited": [f"S{n}" for n in valid],
        "invalid": [f"S{n}" for n in nums if n not in valid],
        "insufficient": insufficient,
        "uncited_answer": not insufficient and not valid,
        "cited_sources": [f"S{n} → {passages[n-1]['path']} › {passages[n-1]['section']}" for n in valid],
    }


def answer(question: str) -> dict:
    """Core ask workflow, shared by the CLI and the eval runner. No chat history is used."""
    # retrieval.search already drops passages below the relevance floor, so an empty list is possible
    # and lets Gemma say "insufficient" instead of forcing an answer from noise.
    passages = retrieval.search(question, k=config.TOP_K, kinds=config.EVIDENCE_KINDS)
    text, stats = llm.chat(prompts.ask_messages(question, passages), temperature=config.TEMPERATURE_ASK)
    check = check_citations(text, passages)
    return {"question": question, "passages": passages, "retrieval": retrieval.describe(),
            "answer": text.strip(), "citation_check": check, "stats": stats}


def run(question: str, name: str | None = None) -> dict:
    console = Console()
    console.print(f"[bold]ask[/bold] · model [cyan]{config.MODEL}[/cyan] · execution [green]local[/green]\n")
    with console.status("[dim]retrieving passages and asking local Gemma…[/dim]"):
        result = answer(question)
    console.print(Markdown(result["answer"]))
    c = result["citation_check"]
    console.print()
    for s in c["cited_sources"]:
        console.print(f"  [dim]{s}[/dim]")
    if c["invalid"]:
        console.print(f"[red]⚠ cites passages that were not provided: {c['invalid']}[/red]")
    if c["uncited_answer"]:
        console.print("[yellow]⚠ answer has no citations — treat as unsupported[/yellow]")
    if "BM25 keyword only" in result["retrieval"]:
        console.print("[bold red]⚠ semantic search unavailable: retrieval fell back to keywords only; "
                      "re-run ./wiki ingest vault/raw[/bold red]")
    console.print(f"\n[dim]{result['stats']['seconds']} s · {len(result['passages'])} passages · "
                  f"retrieval: {result['retrieval']}[/dim]")
    path = evidence.save("ask", result, name=name or "ask")
    console.print(f"[dim]saved → {path}[/dim]")
    return result
