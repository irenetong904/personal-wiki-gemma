"""Retrieval tool: hybrid search over vault/raw (evidence) and vault/wiki (summaries).

v1 was BM25 keywords only; it missed paraphrased questions (see evidence/search/retrieval-v1-*.md).
v2 fuses two local rankings with Reciprocal Rank Fusion:
  - BM25 keyword scores (rank_bm25) - always available, no model needed
  - cosine similarity of EmbeddingGemma vectors (served by the local Ollama) - optional
If Ollama or the embedding model is unavailable, search silently degrades to BM25 only,
so `wiki search` still works with the language model stopped. Nothing leaves the machine.
"""
import json
import re

import numpy as np
from rank_bm25 import BM25Okapi

from . import config

STOPWORDS = set("""a an and are as at be by did do does for from has have how i in is it its of on or
that the this to was were what when where which who why will with my me you your we our about can""".split())
RRF_K = 60           # standard Reciprocal Rank Fusion constant
MAX_PER_SOURCE = 3   # diversity: one long file cannot fill every slot (v1 Q3); 2 was too strict (v2 Q1)
MIN_CHARS = 40       # drop separator-only passages such as "---"


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


# ---------- local embeddings (optional) ----------
EMBED_BATCH = 32  # small batches + retries: one 197-passage request failed transiently under memory pressure


def _embed(texts: list[str], retries: int = 3) -> np.ndarray | None:
    import time
    import ollama
    client = ollama.Client(host=config.OLLAMA_HOST)
    out = []
    for start in range(0, len(texts), EMBED_BATCH):
        batch = texts[start:start + EMBED_BATCH]
        for attempt in range(retries):
            try:
                out += client.embed(model=config.EMBED_MODEL, input=batch)["embeddings"]
                break
            except Exception:
                if attempt == retries - 1:
                    return None
                time.sleep(2 * (attempt + 1))
    v = np.array(out, dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def embeddings_ready() -> bool:
    """True when every passage in chunks.jsonl has a stored EmbeddingGemma vector."""
    if not (config.EMBED_FILE.exists() and config.CHUNKS_FILE.exists()):
        return False
    n = sum(1 for l in config.CHUNKS_FILE.read_text(encoding="utf-8").splitlines() if l.strip())
    return len(np.load(config.EMBED_FILE)) == n


def _doc_text(c: dict) -> str:
    # EmbeddingGemma's recommended document prompt format
    return f'title: {c["path"]} > {c["section"]} | text: {c["text"]}'


# ---------- index ----------
def build_index() -> int:
    from .chunker import chunk_file
    chunks = []
    for kind, folder in (("raw", config.RAW_DIR), ("wiki", config.WIKI_DIR)):
        for p in sorted(folder.rglob("*")):
            if p.is_file() and p.suffix.lower() in config.SUPPORTED_EXT:
                chunks += [c for c in chunk_file(p, kind) if len(re.sub(r"\W", "", c["text"])) >= MIN_CHARS]
    config.DATA_DIR.mkdir(exist_ok=True)
    with config.CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    vecs = _embed([_doc_text(c) for c in chunks]) if chunks else None
    if vecs is not None:
        np.save(config.EMBED_FILE, vecs)
    else:
        if config.EMBED_FILE.exists():
            config.EMBED_FILE.unlink()  # never keep vectors that no longer match chunks.jsonl
        # Offline run 2 degraded silently here; say it loudly instead.
        print(f"WARNING: could not build {config.EMBED_MODEL} vectors; search/ask will use BM25 keywords only "
              "(paraphrased questions may fail). Re-run ./wiki ingest vault/raw once Ollama is healthy.")
    return len(chunks)


def load_chunks() -> list[dict]:
    if not config.CHUNKS_FILE.exists():
        raise FileNotFoundError("No retrieval index yet. Run:  ./wiki ingest vault/raw")
    return [json.loads(l) for l in config.CHUNKS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]


_last_method = "BM25 keyword (rank_bm25)"


def describe() -> str:
    return _last_method


def search(query: str, k: int = config.TOP_K, kinds=("raw", "wiki"), paths: set | None = None) -> list[dict]:
    global _last_method
    all_chunks = load_chunks()
    idx = [i for i, c in enumerate(all_chunks) if c["kind"] in kinds and (paths is None or c["path"] in paths)]
    chunks = [all_chunks[i] for i in idx]
    q = tokenize(query)
    if not chunks or not q:
        return []
    # Heading + path words are indexed too, so "pricing" finds a section titled "Pricing".
    bm25 = BM25Okapi([tokenize(f'{c["path"]} {c["section"]} {c["text"]}') for c in chunks])
    kw = bm25.get_scores(q)

    cos = None
    if config.EMBED_FILE.exists():
        doc_vecs = np.load(config.EMBED_FILE)
        if len(doc_vecs) == len(all_chunks):
            qv = _embed([f"task: search result | query: {query}"])
            if qv is not None:
                cos = (doc_vecs[idx] @ qv[0])

    if cos is None:
        _last_method = "BM25 keyword only (embeddings unavailable)"
        fused = kw
    else:
        _last_method = f"hybrid: BM25 + {config.EMBED_MODEL} cosine, reciprocal rank fusion"
        fused = np.zeros(len(chunks))
        for scores, weight in ((kw, 1.0), (cos, config.DENSE_WEIGHT)):
            for rank, i in enumerate(np.argsort(-scores)):
                fused[i] += weight / (RRF_K + rank + 1)

    results, per_source = [], {}
    for i in np.argsort(-fused):
        c = chunks[i]
        relevant = kw[i] >= config.MIN_SCORE or (cos is not None and cos[i] >= config.MIN_COSINE)
        if not relevant or per_source.get(c["path"], 0) >= MAX_PER_SOURCE:
            continue
        per_source[c["path"]] = per_source.get(c["path"], 0) + 1
        hit = dict(c, score=round(float(kw[i]), 2))
        if cos is not None:
            hit["cosine"] = round(float(cos[i]), 3)
        results.append(hit)
        if len(results) == k:
            break
    return results
