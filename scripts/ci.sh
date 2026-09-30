#!/usr/bin/env bash
# Run the 777-card checks. Compiles the proof contract. Does not deploy.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 scripts/check_waves.py
python3 scripts/check_contract.py
python3 scripts/supply.py --check
python3 scripts/check_metadata.py
python3 - << 'PY'
import pathlib, sys
sys.path.insert(0, "scripts")
from encode_set_base_uri import encode
data = encode("https://example.com/meta/")
assert data.startswith("0x55f804b3")
assert "example.com" in bytes.fromhex(data[2:]).decode("latin1")
print("PASSED: setBaseURI calldata encodes and is not sent")
PY
bash scripts/compile_proof.sh
git diff --exit-code -- contracts/compiler-input.json
bash scripts/test_contract.sh
echo "PASSED: overall build"
