"""Search mode: expose the retrieval tool directly. No language model is involved."""
from rich.console import Console
from rich.panel import Panel

from .. import config, evidence, retrieval


def run(query: str, k: int = config.TOP_K, save: bool = False) -> list[dict]:
    console = Console()
    hits = retrieval.search(query, k=k)
    console.print(f"[bold]search[/bold] · retrieval only, no answer generated · {retrieval.describe()}")
    console.print(f"query: [cyan]{query}[/cyan]\n")
    if not hits:
        console.print("[yellow]No matching passages.[/yellow]")
    for i, h in enumerate(hits, 1):
        tag = "original" if h["kind"] == "raw" else "wiki summary"
        console.print(Panel(h["text"], title=f"[S{i}] {h['path']} › {h['section']}",
                            subtitle=f"bm25 {h['score']}" + (f" · cosine {h['cosine']}" if "cosine" in h else "") + f" · {tag}", title_align="left"))
    if save:
        path = evidence.save("search", {"question": query, "retrieval": retrieval.describe(), "passages": hits}, name="search")
        console.print(f"[dim]saved → {path}[/dim]")
    return hits
