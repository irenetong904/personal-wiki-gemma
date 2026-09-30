"""Ingestion: raw source -> local Gemma (JSON) -> readable, linked wiki note + source catalog + index.

Idempotency: every raw file gets a stable source_id (its path under raw/). The catalog maps
source_id -> note path, so re-ingesting a source rewrites the SAME note and never creates a new name.
Notes marked `reviewed: true` in their frontmatter are never overwritten unless --force is given.
"""
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from rich.console import Console

from . import config, llm, prompts, retrieval
from .chunker import full_text, read_text

console = Console()
BAD_CHARS = re.compile(r'[\\/:*?"<>|#^\[\]{}()!@$%&=+;,.`~]')


# ---------- catalog ----------
def load_catalog() -> dict:
    if config.CATALOG_FILE.exists():
        return json.loads(config.CATALOG_FILE.read_text(encoding="utf-8"))
    return {"sources": {}, "concepts": {}}


def save_catalog(cat: dict) -> None:
    config.DATA_DIR.mkdir(exist_ok=True)
    config.CATALOG_FILE.write_text(json.dumps(cat, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------- helpers ----------
def clean_title(title: str, max_words: int = 6) -> str:
    """Turn a model-proposed title into a short, filesystem-safe, human filename."""
    t = BAD_CHARS.sub(" ", title or "").replace("_", " ")
    words = [w for w in t.split() if not re.fullmatch(r"\d{4,}|[0-9a-f]{8,}", w, re.I)]
    words = words[:max_words] or ["Untitled Note"]
    return " ".join(w if w.isupper() else w[:1].upper() + w[1:] for w in words)


def concept_key(name: str) -> str:
    k = " ".join(re.sub(r"[^a-z0-9]", " ", name.lower()).split())  # "Outcome-Based" == "Outcome Based"
    return re.sub(r"s\b", "", k)  # crude singularization: "LLMs" == "LLM"


def is_reviewed(note: Path) -> bool:
    return note.exists() and re.search(r"^reviewed:\s*true", note.read_text(encoding="utf-8"), re.M) is not None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_call(messages) -> dict:
    for attempt in range(2):
        text, _ = llm.chat(messages, temperature=config.TEMPERATURE_INGEST, json_format=True)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            if attempt:
                raise
    return {}


def summarize_source(path: Path) -> dict:
    """Call Gemma on the source. Long files are summarized per segment and merged (map-reduce)."""
    text = full_text(path)
    segments = [text[i:i + config.INGEST_MAX_CHARS] for i in range(0, len(text), config.INGEST_MAX_CHARS)]
    parts = [_json_call(prompts.ingest_messages(path.name, seg)) for seg in segments]
    first = parts[0]
    merged = {"title": first.get("title", path.stem), "folder": first.get("folder", "Concepts"),
              "summary": first.get("summary", ""), "key_points": [], "concepts": []}
    seen = set()
    for p in parts:
        merged["key_points"] += [kp for kp in p.get("key_points", []) if isinstance(kp, dict)]
        for c in p.get("concepts", []):
            if isinstance(c, dict) and c.get("name") and concept_key(c["name"]) not in seen:
                seen.add(concept_key(c["name"]))
                merged["concepts"].append(c)
    merged["key_points"] = merged["key_points"][:10]
    if merged["folder"] not in config.TOPIC_FOLDERS:
        merged["folder"] = "Concepts"
    return merged


def section_link(raw_rel: str, section: str, headings: list[str]) -> str:
    """Link to the exact heading in the original when it exists, else to the file itself."""
    want = (section or "").strip().lower()
    match = next((h for h in headings if h.lower() == want), None) or \
        next((h for h in headings if want and (want in h.lower() or h.lower() in want)), None)
    if match and match != "(top)":
        # Obsidian heading links cannot contain : # | ^ [ ] \ ; its autocomplete drops them the same way
        anchor = re.sub(r"\s+", " ", re.sub(r"[:#|^\[\]\\]", " ", match)).strip()
        return f"[[{raw_rel}#{anchor}|§ {anchor}]]"
    return f"[[{raw_rel}|source]]"


# ---------- rendering ----------
def frontmatter(fields: dict) -> str:
    lines = ["---"]
    for k, v in fields.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines += [f"  - {json.dumps(x, ensure_ascii=False)}" for x in v]
        else:
            lines.append(f"{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, str) else v}")
    lines.append("---")
    return "\n".join(lines)


def render_source_note(entry: dict, cat: dict, concept_titles: dict) -> str:
    raw_rel = entry["original_file"]
    headings = [s for s, _ in read_text(config.VAULT / raw_rel)]
    fm = frontmatter({"type": "source-note", "source_id": entry["source_id"], "original_file": raw_rel,
                      "sha256": entry["sha256"], "generated_by": entry["model"],
                      "ingested_at": entry["ingested_at"], "reviewed": False,
                      "tags": [entry["folder"].lower()]})
    out = [fm, "", f"# {entry['title']}", "", entry["summary"], "", "## Key points"]
    for kp in entry["key_points"]:
        out.append(f"- {kp.get('point', '').strip()} ({section_link(raw_rel, kp.get('section', ''), headings)})")
    out += ["", "## Sources", f"- Original: [[{raw_rel}]] (unchanged copy in `raw/`)", "", "## Related"]
    related, mentioned = [], []
    for c in entry["concepts"]:
        key = concept_key(c["name"])
        if key in concept_titles:
            related.append(f"- [[{concept_titles[key]}]] — {c.get('why', '').strip()}")
        else:
            mentioned.append(c["name"])
    # Other sources that share at least one concept with this one
    mine = {concept_key(c["name"]) for c in entry["concepts"]} & set(concept_titles)
    for sid, other in cat["sources"].items():
        if sid == entry["source_id"]:
            continue
        shared = mine & {concept_key(c["name"]) for c in other["concepts"]}
        if shared:
            names = ", ".join(concept_titles[s] for s in sorted(shared))
            related.append(f"- [[{other['title']}]] — also covers {names}")
    out += related or ["- _(no related notes yet)_"]
    if mentioned:
        out += ["", "## Also mentioned", ", ".join(mentioned)]
    return "\n".join(out) + "\n"


def render_concept_note(title: str, info: dict, gen: dict, passages: list[dict], cat: dict) -> str:
    fm = frontmatter({"type": "concept-note", "concept_id": info["key"], "generated_by": config.MODEL,
                      "ingested_at": datetime.now().isoformat(timespec="seconds"), "reviewed": False,
                      "tags": ["concept"]})
    out = [fm, "", f"# {title}", "", gen.get("summary", "").strip(), "", "## Details"]
    for d in gen.get("details", []):
        m = re.search(r"S(\d+)", str(d.get("source", "")))
        ref = ""
        if m and 1 <= int(m.group(1)) <= len(passages):
            p = passages[int(m.group(1)) - 1]
            ref = f" ([[{p['path']}|{Path(p['path']).name}]])"
        out.append(f"- {d.get('point', '').strip()}{ref}")
    out += ["", "## Where it appears in my notes"]
    for sid in info["sources"]:
        s = cat["sources"][sid]
        why = next((c.get("why", "") for c in s["concepts"] if concept_key(c["name"]) == info["key"]), "")
        out.append(f"- [[{s['title']}]] — {why}")
    out += ["", "## Sources"] + [f"- [[{p}]]" for p in sorted({p['path'] for p in passages})]
    return "\n".join(out) + "\n"


def render_index(cat: dict, concept_titles: dict) -> str:
    groups = defaultdict(list)
    for s in cat["sources"].values():
        groups[s["folder"]].append((s["title"], s["summary"]))
    for key, title in concept_titles.items():
        groups["Concepts"].append((title, cat["concepts"][key].get("summary", "")))
    out = ["# Personal Wiki Index", "",
           "Landing page for my AI-startup company research (Haas MBA, Fall 2026 targeting). Notes are grouped by topic; each note links "
           "back to its unchanged original in `raw/`.", ""]
    for folder in config.TOPIC_FOLDERS:
        if groups.get(folder):
            out += [f"## {folder}", ""]
            for title, summ in sorted(groups[folder]):
                first = re.split(r"(?<=[.!?])\s", summ.strip(), maxsplit=1)[0] if summ else ""
                out.append(f"- [[{title}]] — {first}")
            out.append("")
    out += ["## Source catalog", "", "| Original file | Wiki note |", "|---|---|"]
    for s in sorted(cat["sources"].values(), key=lambda s: s["original_file"]):
        out.append(f"| [[{s['original_file']}]] | [[{s['title']}]] |")
    return "\n".join(out) + "\n"


# ---------- main entry ----------
def run(target: Path, force: bool = False) -> None:
    target = target.resolve()
    if not target.exists():
        raise FileNotFoundError(f"{target} does not exist")
    files = [target] if target.is_file() else sorted(
        p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in config.SUPPORTED_EXT)
    files = [f for f in files if config.RAW_DIR.resolve() in f.parents]
    if not files:
        raise FileNotFoundError(f"No .md/.txt/.pdf sources found under {config.RAW_DIR}. Add files to vault/raw/ first.")
    llm.check_model()
    cat = load_catalog()
    changed_sources = set()

    # 1) one note per source (stable name via catalog)
    for f in files:
        raw_rel = f.relative_to(config.VAULT.resolve()).as_posix()
        sid = raw_rel
        digest = sha256(f)
        prev = cat["sources"].get(sid)
        note_path = config.WIKI_DIR / prev["folder"] / f"{prev['title']}.md" if prev else None
        if prev and prev["sha256"] == digest and not force and note_path.exists():
            console.print(f"[dim]unchanged[/dim]  {raw_rel} → {prev['folder']}/{prev['title']}.md (re-rendering links)")
            continue
        if prev and is_reviewed(note_path) and not force:
            console.print(f"[yellow]reviewed, kept[/yellow]  {raw_rel} (use --force to regenerate)")
            continue
        console.print(f"[cyan]gemma[/cyan]  summarizing {raw_rel} ...")
        gen = summarize_source(f)
        if prev:  # keep the established human-readable name and folder
            title, folder = prev["title"], prev["folder"]
        else:
            title, folder = clean_title(gen["title"]), gen["folder"]
            taken = {s["title"] for s in cat["sources"].values()}
            if title in taken:  # meaningful qualifier instead of a random suffix
                title = f"{title} - {clean_title(f.stem, 3)}"
        cat["sources"][sid] = {"source_id": sid, "original_file": raw_rel, "sha256": digest,
                               "title": title, "folder": folder, "summary": gen["summary"],
                               "key_points": gen["key_points"], "concepts": gen["concepts"],
                               "model": config.MODEL, "ingested_at": datetime.now().isoformat(timespec="seconds")}
        changed_sources.add(sid)
        console.print(f"  → wiki/{folder}/{title}.md")

    # 2) concepts shared by >= 2 sources become their own notes
    shared = defaultdict(set)
    names = {}
    for sid, s in cat["sources"].items():
        for c in s["concepts"]:
            k = concept_key(c["name"])
            shared[k].add(sid)
            names.setdefault(k, clean_title(c["name"], 4))
    source_titles = {s["title"].lower() for s in cat["sources"].values()}
    concept_titles = {}
    retrieval.build_index()  # concept notes are written from retrieved raw passages
    for k, sids in shared.items():
        if len(sids) < 2 or names[k].lower() in source_titles:
            continue
        prev = cat["concepts"].get(k)
        title = prev["title"] if prev else names[k]
        concept_titles[k] = title
        note = config.WIKI_DIR / "Concepts" / f"{title}.md"
        info = {"key": k, "sources": sorted(sids)}
        stale = force or not prev or prev["sources"] != info["sources"] or (sids & changed_sources) or not note.exists()
        if stale and not (is_reviewed(note) and not force):
            console.print(f"[cyan]gemma[/cyan]  concept note: {title}")
            passages = retrieval.search(title, k=4, kinds=("raw",))
            gen = _json_call(prompts.concept_messages(title, passages))
            note.parent.mkdir(parents=True, exist_ok=True)
            cat["concepts"][k] = {"title": title, "sources": info["sources"], "summary": gen.get("summary", "")}
            note.write_text(render_concept_note(title, info, gen, passages, cat), encoding="utf-8")
    # drop concept notes that no longer have two sources
    for k in list(cat["concepts"]):
        if k not in concept_titles:
            old = config.WIKI_DIR / "Concepts" / f"{cat['concepts'][k]['title']}.md"
            if old.exists() and not is_reviewed(old):
                old.unlink()
            del cat["concepts"][k]

    # 3) render source notes (links depend on the final concept set) + index + retrieval index
    for s in cat["sources"].values():
        note = config.WIKI_DIR / s["folder"] / f"{s['title']}.md"
        if is_reviewed(note) and not force:
            continue
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(render_source_note(s, cat, concept_titles), encoding="utf-8")
    config.INDEX_MD.write_text(render_index(cat, concept_titles), encoding="utf-8")
    save_catalog(cat)
    n = retrieval.build_index()
    notes = sorted(p.relative_to(config.VAULT).as_posix() for p in config.WIKI_DIR.rglob("*.md"))
    console.print(f"\n[green]done[/green] · {len(cat['sources'])} sources · {len(notes)} wiki notes · {n} passages indexed")
    for p in notes:
        console.print(f"  {p}")
