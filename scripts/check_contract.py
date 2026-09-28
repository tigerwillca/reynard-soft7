#!/usr/bin/env python3
"""The Solidity constants match the 777-card brief."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "contracts" / "Soft7MascotCards.sol"

EXPECT = {
    "name": "Reynard Soft7",
    "symbol": "SOFT7",
    "MAX_SUPPLY": "777",
    "FIRST_WAVE": "7",
    "WEEKLY_WAVE": "77",
    "WAVE_PERIOD": "7 days",
    "ROYALTY_BPS": "750",
    "PAYOUT": "0xe53bdb2118585d5B2cD06a117d3A036AFA70677a",
}


def main() -> int:
    text = SOURCE.read_text()
    errors: list[str] = []
    for name, value in EXPECT.items():
        if name in ("name", "symbol"):
            pattern = rf'{name} = "{re.escape(value)}"'
        elif name == "PAYOUT":
            pattern = rf"{name} = {value}"
        else:
            pattern = rf"{name} = {re.escape(value)}"
        if not re.search(pattern, text):
            errors.append(f"missing {name} = {value}")
    if "block.chainid != 4663" not in text:
        errors.append("mint is not locked to chain 4663")
    if "proofsApproved" not in text or "openWaves" not in text:
        errors.append("proof gate is missing")
    if errors:
        for err in errors:
            print(f"FAIL {err}", file=sys.stderr)
        return 1
    print("PASSED: Soft7MascotCards constants match the brief")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
