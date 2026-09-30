"""Read source files and split them into passages that keep their path and section heading."""
import re
from pathlib import Path

from . import config

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)


def read_text(path: Path) -> list[tuple[str, str]]:
    """Return [(section_label, text)] for a file. PDFs are split per page, Markdown per heading."""
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return [(f"page {i + 1}", p.extract_text() or "") for i, p in enumerate(PdfReader(str(path)).pages)]
    text = FRONTMATTER.sub("", path.read_text(encoding="utf-8", errors="replace"))
    sections, current, buf = [], "(top)", []
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            if "".join(buf).strip():
                sections.append((current, "\n".join(buf).strip()))
            current, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    if "".join(buf).strip():
        sections.append((current, "\n".join(buf).strip()))
    return sections


def full_text(path: Path) -> str:
    return "\n\n".join(f"## {s}\n{t}" for s, t in read_text(path))


def _split(text: str, size: int, overlap: int) -> list[str]:
    """Pack paragraphs into ~size-char windows; hard-split very long paragraphs."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, cur = [], ""
    for p in paras:
        if len(p) > size and "\n" in p:  # tables / long lists: split on row boundaries, not mid-row
            rows, p = p.split("\n"), ""
            for row in rows:
                if len(p) + len(row) + 1 > size and p:
                    out.append(p)
                    p = ""
                p = f"{p}\n{row}" if p else row
        while len(p) > size:
            out.append(p[:size])
            p = p[size - overlap:]
        if len(cur) + len(p) + 2 > size and cur:
            out.append(cur)
            cur = cur[-overlap:] + "\n\n" + p if overlap else p
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        out.append(cur)
    return out


def chunk_file(path: Path, kind: str) -> list[dict]:
    rel = path.resolve().relative_to(config.VAULT.resolve()).as_posix()
    chunks = []
    for section, text in read_text(path):
        for i, piece in enumerate(_split(text, config.CHUNK_CHARS, config.CHUNK_OVERLAP)):
            chunks.append({
                "id": f"{rel}#{section}#{i}",
                "path": rel,
                "section": section,
                "kind": kind,  # "raw" = original evidence, "wiki" = generated summary
                "text": piece,
            })
    return chunks
