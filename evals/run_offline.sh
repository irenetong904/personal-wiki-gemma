#!/bin/bash
# Offline demonstration. Turn Wi-Fi / hotspot OFF first, then run:  evals/run_offline.sh
# Everything printed here is also saved to evidence/offline/offline-run-<time>.log
set -u
cd "$(dirname "$0")/.."
OUT="evidence/offline/offline-run-$(date +%Y%m%d-%H%M%S).log"
mkdir -p evidence/offline
source evals/questions.env   # Q1..Q4, SEARCH_TOPIC, FOLLOWUP_FILE, CHAT_CLAIM_Q
INGEST_SOURCE="vault/raw/Clay - company-research.md"

step() { echo; echo "================================================================"; echo "=== $*"; echo "================================================================"; }
{
  step "0. Network status (must be offline)"
  date
  networksetup -getairportpower en0
  if curl -s --max-time 5 -o /dev/null https://www.google.com; then echo "INTERNET: REACHABLE  <-- NOT OFFLINE"; else echo "INTERNET: UNREACHABLE (offline confirmed)"; fi

  step "1. Device, runtime, model"
  sysctl -n machdep.cpu.brand_string; echo "RAM: $(( $(sysctl -n hw.memsize) / 1073741824 )) GB"; sw_vers -productVersion
  ollama --version
  ollama list
  ollama show gemma4:e4b | sed -n '1,8p'

  step "2. Restart: fresh CLI process, model unloaded"
  ollama stop gemma4:e4b 2>/dev/null; ollama ps
  ./wiki --help

  step "3. CLI ingestion offline: ./wiki ingest \"$INGEST_SOURCE\" --force"
  /usr/bin/time -l ./wiki ingest "$INGEST_SOURCE" --force 2>&1
  ollama ps
  ./wiki check

  step "4. Search mode (retrieval only, no answer generated)"
  ./wiki search "$SEARCH_TOPIC" --save

  step "5. Ask mode: four tests (standalone, no chat history)"
  ./wiki ask "$Q1" --name offline-test1
  ./wiki ask "$Q2" --name offline-test2
  /usr/bin/time -l ./wiki ask "$Q3" --name offline-test3 2>&1
  ./wiki ask "$Q4" --name offline-test4-unsupported

  step "6. Chat mode: capability questions (should not search notes)"
  ./wiki chat --script evals/chat_capabilities.txt --name offline-chat-capabilities

  step "7. Chat mode: draft, follow-up, and an unsupported claim"
  ./wiki chat --script "$FOLLOWUP_FILE" --name offline-chat-followup

  step "8. Ask after the chat claim: chat is not evidence"
  ./wiki ask "$CHAT_CLAIM_Q" --name offline-chat-claim-not-evidence

  step "9. Model memory while loaded"
  ollama ps
  ps -axo rss,comm | grep -i "[o]llama" | awk '{s+=$1} END {printf "ollama processes RSS total: %.0f MB\n", s/1024}'
  date
} 2>&1 | tee "$OUT"
echo "saved → $OUT"
