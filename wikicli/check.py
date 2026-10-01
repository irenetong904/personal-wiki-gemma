"""Vault lint: every [[link]] resolves, filenames are human-readable, H1 matches filename."""
import re
from pathlib import Path

from . import config

LINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|[^\]]+)?\]\]")
MACHINE_NAME = re.compile(r"[0-9a-f]{8,}|\d{8}|--|_", re.I)


def _norm(heading: str) -> str:
    """Compare headings the way Obsidian resolves them: ignore characters links cannot contain."""
    return re.sub(r"\s+", " ", re.sub(r"[:#|^\[\]\\]", " ", heading)).strip().lower()


def run() -> int:
    files = list(config.VAULT.rglob("*"))
    by_stem = {}
    for f in files:
        if f.is_file():
            by_stem.setdefault(f.stem, []).append(f)
    rel_paths = {f.relative_to(config.VAULT).as_posix() for f in files if f.is_file()}
    problems = 0
    notes = [config.INDEX_MD] + sorted(config.WIKI_DIR.rglob("*.md"))
    for note in notes:
        text = note.read_text(encoding="utf-8")
        rel = note.relative_to(config.VAULT).as_posix()
        if note.parent != config.VAULT:
            h1 = re.search(r"^# (.+)$", text, re.M)
            if not h1 or h1.group(1).strip() != note.stem:
                print(f"HEADING  {rel}: first heading does not match filename"); problems += 1
            if MACHINE_NAME.search(note.stem) or len(note.stem.split()) > 7:
                print(f"NAME     {rel}: filename looks machine-generated"); problems += 1
        for target, anchor in LINK.findall(text):
            t = target.strip()
            ok = t in rel_paths or f"{t}.md" in rel_paths or len(by_stem.get(Path(t).name, [])) == 1
            if len(by_stem.get(t, [])) > 1:
                print(f"AMBIG    {rel}: [[{t}]] matches several files"); problems += 1
            elif not ok:
                print(f"BROKEN   {rel}: [[{t}]]"); problems += 1
            elif anchor and t.endswith(".md") and (config.VAULT / t).exists():
                heads = {_norm(h) for h in re.findall(r"^#{1,6}\s+(.+)$", (config.VAULT / t).read_text(encoding="utf-8"), re.M)}
                if _norm(anchor) not in heads:
                    print(f"ANCHOR   {rel}: [[{t}#{anchor}]] heading not found"); problems += 1
    from . import retrieval
    if not retrieval.embeddings_ready():
        print("INDEX    semantic vectors missing or stale: search/ask would use BM25 only; re-run ./wiki ingest vault/raw")
        problems += 1
    print(f"\nchecked {len(notes)} notes + retrieval index · {problems} problem(s)")
    return problems
