#!/usr/bin/env bash
# Run Soft7MascotCards against its compiled bytecode. Does not deploy.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SOLC="${SOLC:-$ROOT/.tools/solc-0.8.24}"
if [[ ! -x "$SOLC" ]]; then
  bash scripts/compile_proof.sh
fi

if command -v forge >/dev/null 2>&1; then
  FORGE="$(command -v forge)"
elif [[ -x "$ROOT/.tools/forge" ]]; then
  FORGE="$ROOT/.tools/forge"
else
  mkdir -p "$ROOT/.tools"
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/foundry.tar.gz" \
    "https://github.com/foundry-rs/foundry/releases/download/v1.8.3/foundry_v1.8.3_linux_amd64.tar.gz"
  tar -xzf "$tmp/foundry.tar.gz" -C "$tmp" forge
  mv "$tmp/forge" "$ROOT/.tools/forge"
  chmod +x "$ROOT/.tools/forge"
  rm -rf "$tmp"
  FORGE="$ROOT/.tools/forge"
fi

"$FORGE" test
echo "PASSED: Soft7MascotCards execution"
