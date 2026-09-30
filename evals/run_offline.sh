#!/bin/bash
# Offline demonstration: run with Wi-Fi OFF. Everything is tee'd to evidence/offline/.
# Usage: evals/run_offline.sh "<raw file to re-ingest>"
set -u
cd "$(dirname "$0")/.."
OUT="evidence/offline/offline-run-$(date +%Y%m%d-%H%M%S).log"
mkdir -p evidence/offline
source evals/questions.env   # defines Q1..Q4 and SEARCH_TOPIC, FOLLOWUP_FILE
{
  echo "=== network status ==="
  date
  networksetup -getairportpower en0
  ping -c 1 -t 3 google.com >/dev/null 2>&1 && echo "INTERNET: REACHABLE (not offline!)" || echo "INTERNET: UNREACHABLE (offline confirmed)"
  echo; echo "=== device / runtime ==="
  sysctl -n machdep.cpu.brand_string; echo "RAM: $(( $(sysctl -n hw.memsize) / 1073741824 )) GB"
  ollama --version; ollama show gemma4:e4b | head -12
  echo; echo "=== help ==="; ./wiki --help
  echo; echo "=== ingest one source (offline) ==="; /usr/bin/time -l ./wiki ingest "${1:-vault/raw}" --force 2>&1
  echo; echo "=== check ==="; ./wiki check
  echo; echo "=== search (no model) ==="; ./wiki search "$SEARCH_TOPIC" --save
  echo; echo "=== ask tests ==="
  ./wiki ask "$Q1" --name test1
  ./wiki ask "$Q2" --name test2
  /usr/bin/time -l ./wiki ask "$Q3" --name test3 2>&1
  ./wiki ask "$Q4" --name test4-unsupported
  echo; echo "=== chat: capabilities ==="; ./wiki chat --script evals/chat_capabilities.txt --name chat-capabilities
  echo; echo "=== chat: follow-up ==="; ./wiki chat --script "$FOLLOWUP_FILE" --name chat-followup
  echo; echo "=== ask: chat claim is not evidence ==="; ./wiki ask "$CHAT_CLAIM_Q" --name chat-claim-not-evidence
  echo; echo "=== model memory ==="; ollama ps
} 2>&1 | tee "$OUT"
echo "saved → $OUT"
