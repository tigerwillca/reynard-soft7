#!/usr/bin/env python3
"""Token JSON for the 777-card set.

Tokens 1–7 repeat the proof files. Tokens 8–777 are shells: a name, the canon
description, and external_url. No image and no traits. Nothing here is minted.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from supply import CANON, collection, proof_metadata, wave_cap

ROOT = pathlib.Path(__file__).resolve().parent.parent
WAVES_PATH = ROOT / "proofs" / "waves.html"
EXTERNAL_URL = "https://tigerwillca.github.io/"
SHELL_KEYS = ("name", "description", "external_url")


def token_document(token_id: int) -> dict[str, object]:
    if isinstance(token_id, bool) or not isinstance(token_id, int):
        raise KeyError(token_id)
    if token_id < 1 or token_id > 777:
        raise KeyError(token_id)
    if token_id <= 7:
        return proof_metadata(token_id)
    return {
        "name": f"Reynard Soft7 #{token_id}",
        "description": CANON,
        "external_url": EXTERNAL_URL,
    }


def collection_document() -> dict[str, object]:
    return collection()


def render_waves_page() -> str:
    rows: list[str] = []
    previous = 0
    for week in range(0, 11):
        cap = wave_cap(week)
        start = previous + 1
        kind = "7 proofs" if week == 0 else "77 cards"
        rows.append(
            f'      <tr><th scope="row">{week}</th><td>{cap}</td>'
            f"<td>{start}–{cap}</td><td>{kind}</td></tr>"
        )
        previous = cap
    body = "\n".join(rows)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reynard Soft7 wave schedule</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; font: 18px/1.45 Georgia, serif; background: #14120e; color: #f3efe4; }}
    main {{ max-width: 920px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    h1 {{ font-weight: normal; letter-spacing: 0.02em; }}
    a {{ color: #f0e0a8; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1.5rem; }}
    th, td {{ text-align: left; padding: 0.45rem 0.6rem; border-bottom: 1px solid #3a3428; vertical-align: top; }}
    th {{ font-weight: normal; color: #f0e0a8; white-space: nowrap; }}
  </style>
</head>
<body>
  <main>
    <h1>Wave schedule</h1>
    <p>Mint is closed. The seven proofs are unapproved, and openWaves has not been sent.</p>
    <p>{CANON}</p>
    <p><a href="index.html">The seven proofs</a></p>
    <p>Caps after the waves open. Later weeks stay at 777.</p>
    <table>
      <thead>
        <tr><th scope="col">Week</th><th scope="col">Cap</th><th scope="col">Token ids</th><th scope="col">What that week adds</th></tr>
      </thead>
      <tbody>
{body}
      </tbody>
    </table>
  </main>
</body>
</html>
"""
