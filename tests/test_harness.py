"""Offline tests of the harness logic with a fake model (no Ollama needed).

Run: .venv/bin/python -m unittest tests/test_harness.py -v
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from wikicli import check, config, ingest, retrieval
from wikicli.modes import ask, chat

FAKE = {
    "a.md": {"title": "Acme Robotics", "folder": "Companies", "summary": "Acme builds robots. It sells to factories.",
             "key_points": [{"point": "Uses outcome-based pricing.", "section": "Step 1: Business Model"}],
             "concepts": [{"name": "Outcome-Based Pricing", "why": "Acme charges per task."},
                          {"name": "Factory Automation", "why": "Core market."}]},
    "b.md": {"title": "Beta Labs 2024 abcdef1234", "folder": "Companies", "summary": "Beta sells agents.",
             "key_points": [{"point": "Charges per resolution.", "section": "Pricing"}],
             "concepts": [{"name": "Outcome Based Pricing", "why": "Beta charges per resolution."}]},
}


def fake_chat(messages, temperature=0.2, json_format=False):
    user = messages[-1]["content"]
    if user.startswith("CONCEPT:"):
        return json.dumps({"summary": "Paying for results.", "details": [{"point": "Used by Acme.", "source": "S1"}]}), {}
    name = user.split("\n", 1)[0].replace("SOURCE FILE: ", "")
    return json.dumps(FAKE[name]), {"model": "fake", "execution": "local", "seconds": 0}


class HarnessTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        vault = self.tmp / "vault"
        (vault / "raw").mkdir(parents=True)
        (vault / "raw" / "a.md").write_text("# Acme\n\n## Step 1: Business Model\nAcme uses outcome-based pricing for every robot task.\n")
        (vault / "raw" / "b.md").write_text("# Beta\n\n## Pricing\nBeta Labs charges customers per resolved conversation outcome.\n")
        self.patches = [mock.patch.object(config, k, v) for k, v in {
            "VAULT": vault, "RAW_DIR": vault / "raw", "WIKI_DIR": vault / "wiki", "INDEX_MD": vault / "index.md",
            "DATA_DIR": self.tmp / "data", "CHUNKS_FILE": self.tmp / "data/chunks.jsonl",
            "EMBED_FILE": self.tmp / "data/emb.npy", "CATALOG_FILE": self.tmp / "data/catalog.json",
            "EVIDENCE_DIR": self.tmp / "evidence",
            # a 2-file corpus gives BM25 near-zero IDF, so the production floor (tuned on 7 files) is lowered
            "MIN_SCORE": 0.01}.items()]
        self.patches += [mock.patch("wikicli.llm.chat", fake_chat), mock.patch("wikicli.llm.check_model", lambda: None),
                         mock.patch("wikicli.retrieval._embed", lambda texts: None)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)

    def notes(self):
        return sorted(p.relative_to(config.WIKI_DIR).as_posix() for p in config.WIKI_DIR.rglob("*.md"))

    def test_ingest_names_links_and_idempotency(self):
        ingest.run(config.RAW_DIR)
        first = self.notes()
        # machine-style parts of the proposed title are stripped; concept shared by 2 sources gets a note
        self.assertEqual(first, ["Companies/Acme Robotics.md", "Companies/Beta Labs.md", "Concepts/Outcome-Based Pricing.md"])
        acme = (config.WIKI_DIR / "Companies/Acme Robotics.md").read_text()
        self.assertIn("# Acme Robotics", acme)
        self.assertIn("[[raw/a.md#Step 1 Business Model|§ Step 1 Business Model]]", acme)
        self.assertIn("[[Outcome-Based Pricing]] — Acme charges per task.", acme)
        self.assertIn("[[Beta Labs]] — also covers Outcome-Based Pricing", acme)
        self.assertNotIn("[[Factory Automation]]", acme)  # single-source concept: plain text, not a dead link
        self.assertEqual(check.run(), 0)
        # re-ingest (unchanged and forced) → same files, no duplicates
        ingest.run(config.RAW_DIR)
        ingest.run(config.RAW_DIR / "a.md", force=True)
        self.assertEqual(self.notes(), first)
        # a reviewed note is kept verbatim
        note = config.WIKI_DIR / "Companies/Acme Robotics.md"
        note.write_text(note.read_text().replace("reviewed: False", "reviewed: true") + "\nHuman fix.\n")
        ingest.run(config.RAW_DIR)
        self.assertIn("Human fix.", note.read_text())

    def test_search_needs_no_model_and_ask_checks_citations(self):
        ingest.run(config.RAW_DIR)
        with mock.patch("wikicli.llm.chat", side_effect=AssertionError("search must not call the model")):
            hits = retrieval.search("outcome-based pricing")
        self.assertTrue(any(h["path"].startswith("raw/") for h in hits))  # originals are retrievable
        c = ask.check_citations("Acme charges per task [S1][S9].", hits)
        self.assertEqual((c["cited"], c["invalid"]), (["S1"], ["S9"]))
        self.assertTrue(ask.check_citations("INSUFFICIENT EVIDENCE: the wiki does not contain x.", hits)["insufficient"])

    def test_chat_router(self):
        ingest.run(config.RAW_DIR)
        for msg in ["what can you help me with?", "what can we do?", "make that shorter"]:
            self.assertFalse(chat.needs_retrieval(msg)[0], msg)
        self.assertTrue(chat.needs_retrieval("what do my notes say about pricing?")[0])


if __name__ == "__main__":
    unittest.main()
