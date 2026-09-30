#!/usr/bin/env bash
# Serve /1.json through /777.json. Idempotent. Does not deploy or mint.
set -euo pipefail

PORT="${METADATA_SERVER_PORT:-8000}"
LOG="/tmp/soft7-metadata-server.log"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

metadata_ready() {
  local body
  body="$(curl -sf "http://127.0.0.1:${PORT}/1.json" 2>/dev/null)" || return 1
  python3 -c 'import json,sys; data=json.loads(sys.argv[1]); attrs=data.get("attributes"); ok=data.get("name")=="Reynard Soft7 Proof Tier 1" and isinstance(attrs, list) and len(attrs)==5 and data.get("image")=="proofs/art/01.png"; raise SystemExit(0 if ok else 1)' "$body"
}

if metadata_ready; then
  echo "metadata server already listening on :${PORT}"
  exit 0
fi

cd "$ROOT"
nohup python3 scripts/metadata_server.py --bind 0.0.0.0 --port "$PORT" >"$LOG" 2>&1 &
server_pid=$!

for _ in $(seq 1 40); do
  if metadata_ready; then
    echo "metadata server ready on :${PORT} (pid ${server_pid})"
    exit 0
  fi
  sleep 0.25
done

echo "metadata server failed to become ready on :${PORT}; see ${LOG}" >&2
exit 1
