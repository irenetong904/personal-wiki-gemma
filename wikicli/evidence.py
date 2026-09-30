"""Save every run as JSON (machine-readable) + Markdown card (human-readable) under evidence/."""
import json
import platform
from datetime import datetime

from . import config


def save(kind: str, record: dict, name: str | None = None) -> str:
    out_dir = config.EVIDENCE_DIR / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = f"{stamp}-{name}" if name else stamp
    record = {"timestamp": datetime.now().isoformat(timespec="seconds"),
              "device": f"{platform.machine()} {platform.system()} {platform.mac_ver()[0]}", **record}
    (out_dir / f"{base}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / f"{base}.md").write_text(_card(kind, record), encoding="utf-8")
    return str((out_dir / f"{base}.md").relative_to(config.ROOT))


def _card(kind: str, r: dict) -> str:
    lines = [f"# {kind.upper()} evidence card", "",
             f"- **Time:** {r['timestamp']}", f"- **Interaction mode:** {kind}",
             f"- **Execution:** {r.get('stats', {}).get('execution', 'n/a (no model call)')}",
             f"- **Model:** {r.get('stats', {}).get('model', 'none')}",
             f"- **Latency:** {r.get('stats', {}).get('seconds', 'n/a')} s", ""]
    if "question" in r:
        lines += ["## Question", r["question"], ""]
    if "passages" in r:
        lines += ["## Retrieved passages", f"_Method: {r.get('retrieval', 'n/a')}_", ""]
        for i, p in enumerate(r["passages"], 1):
            lines += [f"**[S{i}]** `{p['path']}` › {p['section']} (bm25 {p['score']}{', cosine ' + str(p['cosine']) if 'cosine' in p else ''})", "",
                      "> " + p["text"].replace("\n", "\n> "), ""]
    if "answer" in r:
        lines += ["## Answer", r["answer"], ""]
    if "citation_check" in r:
        c = r["citation_check"]
        lines += ["## Citation check",
                  f"- cited: {c['cited']}", f"- invalid: {c['invalid']}",
                  f"- insufficient evidence: {c['insufficient']}", ""]
        for s in c.get("cited_sources", []):
            lines.append(f"- {s}")
        lines.append("")
    if "transcript" in r:
        lines += ["## Transcript", ""]
        for t in r["transcript"]:
            lines += [f"**{t['role']}**" + (f" _(retrieved: {t['retrieved']})_" if "retrieved" in t else ""),
                      "", t["content"], ""]
    lines += ["## Assessment", r.get("assessment", "_(to be filled in by reviewer)_"), ""]
    return "\n".join(lines)
