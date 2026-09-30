"""Evaluate retrieval alone (no model): does the expected passage appear in the top-k?

Usage: .venv/bin/python evals/retrieval_check.py <label>
Writes evidence/search/retrieval-<label>.md so each retrieval change keeps its before/after record.
"""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from wikicli import config, retrieval  # noqa: E402

# (source file, phrase that must appear in a retrieved passage). Matching only the section was too lenient:
# a long section is split into several passages, and the right section can come back without the answer (dry run Q2).
TESTS = [
    ("Q1", "What is Sierra's pricing model?", [("Sierra", "pay for resolved outcomes")]),
    ("Q2", "Where does Surge AI get its operating capital?", [("Surge AI", "entirely bootstrapped")]),
    ("Q3", "Which AI data companies list Scale AI as a competitor?",
     [("David AI", "| Scale AI |"), ("Surge AI", "**Scale AI** (Meta-backed")]),
    ("Q4", "What was Decagon's annual recurring revenue in 2025?", []),  # nothing should support it
]


def main(label: str) -> None:
    lines = []
    for qid, q, expected in TESTS:
        hits = retrieval.search(q, k=config.TOP_K, kinds=config.EVIDENCE_KINDS)  # same call as ask mode
        found = [any(src in h["path"] and phrase in h["text"] for h in hits) for src, phrase in expected]
        verdict = "n/a (unsupported question)" if not expected else ("PASS" if all(found) else "FAIL")
        lines += [f"## {qid}: {q}", f"Expected: {expected or 'no supporting passage'} → **{verdict}**", "",
                  "| rank | bm25 / cosine | path | section | text |", "|---|---|---|---|---|"]
        for i, h in enumerate(hits, 1):
            text = h["text"][:90].replace("\n", " ").replace("|", "/")
            lines.append(f"| {i} | {h['score']}{' / ' + str(h['cosine']) if 'cosine' in h else ''} | {h['path']} | {h['section'][:45]} | {text} |")
        lines.append("")
        print(f"{qid} {verdict:28} {[h['path'][4:20] + ' › ' + h['section'][:22] for h in hits]}")
    lines = [f"# Retrieval check — {label}", "",
             f"- time: {datetime.now():%Y-%m-%d %H:%M} · top_k={config.TOP_K} · method: {retrieval.describe()}", ""] + lines
    out = config.EVIDENCE_DIR / "search" / f"retrieval-{label}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"saved → {out.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "run")
