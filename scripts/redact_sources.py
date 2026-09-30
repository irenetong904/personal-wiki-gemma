"""One-time redaction: private company-research files -> shareable copies in vault/raw/.

The private originals stay outside the repo. Only personal job-search content is removed
(resume metrics, fit assessments, cold pitches, outreach contacts); company facts are untouched.
Usage: python scripts/redact_sources.py <private_dir> vault/raw
"""
import re
import sys
from pathlib import Path

DROP_SECTIONS = re.compile(r"best role targets|relevance assessment|positioning narrative|outreach angles|"
                           r"suggested next actions|step 7|step 8", re.I)
DROP_LINES = re.compile(r"^Prepared for |^\*\*Tier: |/Users/")
PERSONAL = re.compile(r"\bIrene\b|\bher\b|\bshe\b|fit for a candidate|strongest targets", re.I)
CLAUSES = [
    (re.compile(r"\s*—\s*\*\*best operator/GTME outreach contact\.\*\*"), ""),
    (re.compile(r"\s*—\s*\*\*key GTM/RevOps outreach target\.\*\*"), ""),
    (re.compile(r"\s*Outreach entry = [^*]*"), ""),
    (re.compile(r"\s*Best path: [^*]*"), ""),
    (re.compile(r"\s*Series A post lists direct outreach to \S+ at \S+\."), ""),
    (re.compile(r"\s*\((?:[^()]*\bher\b[^()]*)\)"), ""),
    (re.compile(r"Open roles for Irene"), "Open GTM/ops roles"),
]


def redact(text: str) -> str:
    out, skipping, drop_col = [], False, None
    for line in text.splitlines():
        heading = re.match(r"^#{1,6}\s+(.*)", line)
        if heading:
            skipping = bool(DROP_SECTIONS.search(heading.group(1)))
        elif line.strip() == "---":
            skipping = False  # footer separator before the Sources line
        if skipping or DROP_LINES.search(line):
            continue
        # Leadership tables: drop the "Relevance for Outreach" column
        if line.startswith("|"):
            cells = line.strip().strip("|").split("|")
            if any("Relevance for Outreach" in c for c in cells):
                drop_col = [i for i, c in enumerate(cells) if "Relevance for Outreach" in c][0]
            if drop_col is not None and len(cells) > drop_col:
                del cells[drop_col]
                line = "|" + "|".join(cells) + "|"
        else:
            drop_col = None
        for pat, rep in CLAUSES:
            line = pat.sub(rep, line)
        # Executive-read paragraphs: drop only the sentences about personal fit
        if PERSONAL.search(line) and not line.startswith(("|", "#", "-")):
            line = " ".join(s for s in re.split(r"(?<=[.!?])\s+", line) if not PERSONAL.search(s))
        out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    for f in sorted(src.glob("*.md")):
        clean = redact(f.read_text(encoding="utf-8"))
        (dst / f.name).write_text(clean, encoding="utf-8")
        left = [l for l in clean.splitlines() if re.search(r"\bIrene\b|\bher\b|\bshe\b|cold-pitch|@", l, re.I)]
        print(f"{f.name}: {len(f.read_text().splitlines())} -> {len(clean.splitlines())} lines; review: {len(left)}")
        for l in left:
            print("   ?", l[:130])
