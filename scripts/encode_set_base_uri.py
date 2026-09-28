#!/usr/bin/env python3
"""Print setBaseURI calldata for the live supply-7 contract.

Does not broadcast a transaction. The owner of
0x73D7b2611509C14078e16f572bE5aC7D91879DC2 sends this only after the proof
PNGs are approved. This repository's 777-card contract is not deployed.
"""
from __future__ import annotations

import sys

SELECTOR = "55f804b3"  # keccak256("setBaseURI(string)")[:4]
LIVE = "0x73D7b2611509C14078e16f572bE5aC7D91879DC2"


def encode(base: str) -> str:
    if not base.endswith("/"):
        raise SystemExit("base URI must end with /")
    raw = base.encode()
    body = raw.hex()
    if len(body) % 64:
        body = body.ljust(((len(body) + 63) // 64) * 64, "0")
    return "0x" + SELECTOR + f"{0x20:064x}" + f"{len(raw):064x}" + body


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <baseURI>", file=sys.stderr)
        return 2
    print(f"to: {LIVE}")
    print("data:")
    print(encode(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
