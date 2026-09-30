"""Command-line entry point. The harness picks a mode from argv and wires it to retrieval + local Gemma."""
import argparse
import sys
from pathlib import Path

from . import config

EPILOG = f"""
modes:
  ingest   read vault/raw, have local Gemma write linked notes in vault/wiki, rebuild index.md + search index
  search   show original matching passages and paths (retrieval only, no model — works with Ollama stopped)
  ask      standalone factual answer from retrieved evidence, with [S#] citations or INSUFFICIENT EVIDENCE
  chat     personal assistant 'Sage' with conversation memory; searches notes only when useful
  check    verify every [[link]] in the vault resolves and note names are readable

configuration:
  model     {config.MODEL}   (override with WIKI_MODEL=...)
  runtime   Ollama at {config.OLLAMA_HOST}   (start: brew services start ollama)
  vault     {config.VAULT.relative_to(config.ROOT)}/   · machine data in {config.DATA_DIR.relative_to(config.ROOT)}/

examples:
  ./wiki ingest vault/raw
  ./wiki search "workshop location"
  ./wiki ask "Where is the workshop?"
  ./wiki chat
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wiki", description="Personal wiki CLI: local Gemma + RAG over your own notes.",
                                epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", metavar="{ingest,search,ask,chat,check,help}")

    s = sub.add_parser("ingest", help="build/update wiki pages from raw sources")
    s.add_argument("path", nargs="?", default=str(config.RAW_DIR), help="a file or folder inside vault/raw")
    s.add_argument("--force", action="store_true", help="regenerate even unchanged or reviewed notes")

    s = sub.add_parser("search", help="show matching original passages (no model)")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=config.TOP_K, help="number of passages")
    s.add_argument("--save", action="store_true", help="save results under evidence/search/")

    s = sub.add_parser("ask", help="grounded factual answer with citations")
    s.add_argument("question")
    s.add_argument("--mode", choices=["local", "online"], default="local", help="where the model runs (default local)")
    s.add_argument("--name", help="label for the saved evidence card")

    s = sub.add_parser("chat", help="talk with your personal assistant")
    s.add_argument("--mode", choices=["local", "online"], default="local")
    s.add_argument("--script", help="text file with one message per line (non-interactive run)")
    s.add_argument("--name", help="label for the saved transcript")

    sub.add_parser("check", help="lint vault links and note names")
    sub.add_parser("help", help="show this help")
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd in (None, "help"):
        parser.print_help()
        return 0
    if getattr(args, "mode", "local") == "online":
        print("Online mode is not configured in this project. Local mode is the default: omit --mode.", file=sys.stderr)
        return 2

    from .llm import ModelUnavailable
    try:
        if args.cmd == "ingest":
            from . import ingest
            ingest.run(Path(args.path), force=args.force)
        elif args.cmd == "search":
            from .modes import search
            search.run(args.query, k=args.k, save=args.save)
        elif args.cmd == "ask":
            from .modes import ask
            ask.run(args.question, name=args.name)
        elif args.cmd == "chat":
            from .modes import chat
            script = None
            if args.script:
                script = [l.strip() for l in Path(args.script).read_text().splitlines() if l.strip()]
            chat.run(script=script, name=args.name)
        elif args.cmd == "check":
            from . import check
            return 1 if check.run() else 0
    except ModelUnavailable as e:
        print(f"error: local model unavailable\n{e}", file=sys.stderr)
        return 3
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
