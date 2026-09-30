"""Central settings for the personal wiki harness. Everything path- or model-related lives here."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent

# Vault (the only folder opened in Obsidian)
VAULT = ROOT / "vault"
RAW_DIR = VAULT / "raw"
WIKI_DIR = VAULT / "wiki"
INDEX_MD = VAULT / "index.md"

# Machine files live OUTSIDE the vault
DATA_DIR = ROOT / "data"
CHUNKS_FILE = DATA_DIR / "chunks.jsonl"
EMBED_FILE = DATA_DIR / "embeddings.npy"   # one EmbeddingGemma vector per line of chunks.jsonl
CATALOG_FILE = DATA_DIR / "source_catalog.json"
CHAT_SAVES = DATA_DIR / "chat_saves"
EVIDENCE_DIR = ROOT / "evidence"

INSTRUCTIONS_DIR = ROOT / "instructions"

# Model / runtime
MODEL = os.environ.get("WIKI_MODEL", "gemma4:e4b")
EMBED_MODEL = os.environ.get("WIKI_EMBED_MODEL", "embeddinggemma")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
THINK = False             # Gemma 4 "thinking" mode; measured 15.5 s vs 2.4 s for the same answer
NUM_CTX = 8192            # context window we ask Ollama to allocate
TEMPERATURE_ASK = 0.1     # near-deterministic for factual answers
TEMPERATURE_CHAT = 0.7    # a bit of personality for chat
TEMPERATURE_INGEST = 0.2

# Chunking / retrieval
CHUNK_CHARS = 800         # ~150-200 tokens per passage
CHUNK_OVERLAP = 150
EVIDENCE_KINDS = ("raw",)  # ask/search cite originals only; generated wiki summaries outranked them (retrieval-v2b)
TOP_K = 5                 # passages handed to Gemma in ask mode (~1k tokens of evidence)
MIN_SCORE = 1.0           # BM25 floor ...
DENSE_WEIGHT = float(os.environ.get("WIKI_DENSE_WEIGHT", 2.0))  # embedding vote vs BM25 vote in RRF; smallest weight passing all checks (evidence/search/retrieval-sweep-*)
MIN_COSINE = 0.45        # ... or embedding floor; a passage must clear one of them to count as relevant
INGEST_MAX_CHARS = 16000  # ~4k tokens of source text per ingestion call (fits num_ctx 8192)
CHAT_HISTORY_TURNS = 6    # user+assistant pairs kept as conversation context

TOPIC_FOLDERS = ["Companies", "Concepts"]  # fits a company-research corpus
SUPPORTED_EXT = {".md", ".txt", ".pdf"}
