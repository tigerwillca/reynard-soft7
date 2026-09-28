#!/usr/bin/env python3
"""Build and check the 777-card supply map.

Tokens 1–7 are the approval proofs. Tokens 8–777 are unpainted slots.
Nothing in the map is minted.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "supply" / "catalog.json"
META_DIR = ROOT / "proofs" / "meta"
ART_DIR = ROOT / "proofs" / "art"
PAGE_PATH = ROOT / "proofs" / "index.html"
COLLECTION_PATH = ROOT / "proofs" / "collection.json"
SUMS_PATH = ART_DIR / "SHA256SUMS"

CANON = (
    "reynard-soft7 mascot cards on robinhood chain. ten percent of every mint "
    "routes back to soft7 holders proportional to what they hold. stake your card, "
    "feed the treasury, pull when you're ready."
)
TRAITS = ("tier", "color", "eyes", "signature", "globe")
PAYOUT = "0xe53bdb2118585d5B2cD06a117d3A036AFA70677a"
FOX_IDS = {1, 4, 5}
TIGER_IDS = {3}

# Face paint, eyes, and globe for the seven proofs. Copied from the approval
# set; not redrawn here.
LOCKED = (
    ("Crimson", "Amber Lock", "Brow Line", "Root Stone"),
    ("Amber", "Coal Lock", "Cheek Marks", "Sacral Clay"),
    ("Gold", "Pale Lock", "Solar Tick", "Solar Dust"),
    ("Green", "Amber Lock", "Heart Band", "Heart Moss"),
    ("Blue", "Amber Lock", "Throat Outline", "Throat Tide"),
    ("Indigo", "Ink Lock", "Layered Contour", "Brow Night"),
    ("Violet", "Band Lock", "Crown Glyphs", "Crown Gate"),
)


def wave_cap(weeks_elapsed: int) -> int:
    cap = 7 + weeks_elapsed * 77
    return 777 if cap > 777 else cap


def token_wave(token_id: int) -> int:
    previous = 0
    for week in range(0, 11):
        cap = wave_cap(week)
        if previous < token_id <= cap:
            return week
        previous = cap
    raise ValueError(f"token {token_id} is outside the 777 supply")


def attributes(token_id: int) -> list[dict[str, object]]:
    color, eyes, signature, globe = LOCKED[token_id - 1]
    return [
        {"trait_type": "tier", "value": token_id},
        {"trait_type": "color", "value": color},
        {"trait_type": "eyes", "value": eyes},
        {"trait_type": "signature", "value": signature},
        {"trait_type": "globe", "value": globe},
    ]


def proof_entry(token_id: int) -> dict[str, object]:
    entry: dict[str, object] = {
        "id": token_id,
        "wave": 0,
        "status": "proof",
        "name": f"Reynard Soft7 Proof Tier {token_id}",
        "description": CANON,
        "image": f"proofs/art/{token_id:02d}.png",
        "attributes": attributes(token_id),
    }
    if token_id in FOX_IDS:
        entry["mascot"] = "fox"
    elif token_id in TIGER_IDS:
        entry["mascot"] = "tiger"
    return entry


def catalog() -> dict[str, object]:
    tokens: list[dict[str, object]] = []
    for token_id in range(1, 778):
        if token_id <= 7:
            tokens.append(proof_entry(token_id))
        else:
            tokens.append(
                {
                    "id": token_id,
                    "wave": token_wave(token_id),
                    "status": "unpainted",
                }
            )
    return {
        "name": "Reynard Soft7",
        "symbol": "SOFT7",
        "chainId": 4663,
        "maxSupply": 777,
        "firstWave": 7,
        "weeklyWave": 77,
        "mint": "closed",
        "payout": PAYOUT,
        "royaltyBps": 750,
        "tokens": tokens,
    }


def proof_metadata(token_id: int) -> dict[str, object]:
    entry = proof_entry(token_id)
    return {
        "name": entry["name"],
        "description": CANON,
        "image": entry["image"],
        "external_url": "https://tigerwillca.github.io/",
        "attributes": entry["attributes"],
    }


def collection() -> dict[str, object]:
    return {
        "name": "Reynard Soft7",
        "description": CANON,
        "image": "proofs/art/01.png",
        "banner_image": "proofs/art/banner.png",
        "external_link": "https://tigerwillca.github.io/",
        "discord_url": "https://discord.gg/tigerwillca",
        "twitter_username": "tigerwillca",
        "seller_fee_basis_points": 750,
        "fee_recipient": PAYOUT,
    }


def render_page() -> str:
    cards = []
    for token_id in range(1, 8):
        attrs = attributes(token_id)
        rows = "\n".join(
            f"        <li>{attr['trait_type']}: {attr['value']}</li>" for attr in attrs
        )
        cards.append(
            f"""    <article>
      <img src="art/{token_id:02d}.png" alt="Reynard Soft7 proof tier {token_id}" width="420">
      <h2>Tier {token_id}</h2>
      <ul>
{rows}
      </ul>
    </article>"""
        )
    body = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Reynard Soft7 proofs</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; font: 18px/1.45 Georgia, serif; background: #14120e; color: #f3efe4; }}
    main {{ max-width: 920px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    h1 {{ font-weight: normal; letter-spacing: 0.02em; }}
    .banner {{ width: 100%; height: auto; display: block; }}
    .grid {{ display: grid; gap: 2.5rem; }}
    article img {{ width: min(100%, 420px); height: auto; background: #000; }}
    h2 {{ font-weight: normal; margin-bottom: 0.25rem; }}
    ul {{ margin: 0; padding-left: 1.1rem; }}
  </style>
</head>
<body>
  <main>
    <h1>Reynard Soft7 proofs</h1>
    <p>Seven paintings for the first wave. Supply is 777. Mint is closed until these proofs are approved.</p>
    <p>{CANON}</p>
    <img class="banner" src="art/banner.png" alt="Purple-lime banner with Reynard and the seventh-gate potion orb">
    <p>The banner proof clips the fox at the shins.</p>
    <div class="grid">
{body}
    </div>
  </main>
</body>
</html>
"""


def dump(path: pathlib.Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def write_outputs() -> None:
    dump(CATALOG_PATH, catalog())
    dump(COLLECTION_PATH, collection())
    for token_id in range(1, 8):
        dump(META_DIR / f"{token_id}.json", proof_metadata(token_id))
    PAGE_PATH.write_text(render_page())


def load_json(path: pathlib.Path) -> object:
    return json.loads(path.read_text())


def check_art() -> list[str]:
    errors: list[str] = []
    sums: dict[str, str] = {}
    for line in SUMS_PATH.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, name = line.split()
        sums[name] = digest
    expected = [f"{i:02d}.png" for i in range(1, 8)] + ["banner.png"]
    if set(sums) != set(expected):
        errors.append(f"SHA256SUMS names are {sorted(sums)}, expected {expected}")
    for name, digest in sums.items():
        path = ART_DIR / name
        if not path.is_file():
            errors.append(f"missing {name}")
            continue
        raw = path.read_bytes()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append(f"{name} is not a PNG")
        got = hashlib.sha256(raw).hexdigest()
        if got != digest:
            errors.append(f"{name} sha256 is {got}")
    return errors


def check_outputs() -> list[str]:
    errors = check_art()
    if load_json(CATALOG_PATH) != catalog():
        errors.append("supply/catalog.json does not match the generator")
    if load_json(COLLECTION_PATH) != collection():
        errors.append("proofs/collection.json does not match the generator")
    for token_id in range(1, 8):
        path = META_DIR / f"{token_id}.json"
        if load_json(path) != proof_metadata(token_id):
            errors.append(f"{path.name} does not match the generator")
    if PAGE_PATH.read_text() != render_page():
        errors.append("proofs/index.html does not match the generator")

    data = catalog()
    tokens = data["tokens"]
    if not isinstance(tokens, list) or len(tokens) != 777:
        errors.append("catalog must list 777 tokens")
        return errors
    signatures: list[str] = []
    colors: list[str] = []
    previous = 0
    for week in range(0, 11):
        cap = wave_cap(week)
        width = cap - previous
        expect = 7 if week == 0 else 77
        if width != expect:
            errors.append(f"week {week} has {width} tokens, expected {expect}")
        previous = cap
    for token in tokens:
        token_id = int(token["id"])
        if token["wave"] != token_wave(token_id):
            errors.append(f"token {token_id} is in the wrong wave")
        if token_id <= 7:
            attrs = token["attributes"]
            found = tuple(attr["trait_type"] for attr in attrs)
            if found != TRAITS:
                errors.append(f"token {token_id} traits are {found}")
            by_type = {attr["trait_type"]: attr["value"] for attr in attrs}
            if by_type["tier"] != token_id:
                errors.append(f"token {token_id} tier drifted")
            if token_id in FOX_IDS and by_type["eyes"] != "Amber Lock":
                errors.append(f"token {token_id} fox eyes must stay Amber Lock")
            if token_id in TIGER_IDS and token.get("mascot") != "tiger":
                errors.append("tier 3 is the tiger proof")
            signatures.append(str(by_type["signature"]))
            colors.append(str(by_type["color"]))
            if token["status"] != "proof":
                errors.append(f"token {token_id} is not a proof")
        else:
            if token["status"] != "unpainted":
                errors.append(f"token {token_id} must stay unpainted")
            if "attributes" in token or "image" in token or "name" in token:
                errors.append(f"token {token_id} has invented art fields")
    if len(signatures) != len(set(signatures)):
        errors.append("proof signatures are not unique")
    if len(colors) != len(set(colors)):
        errors.append("proof colors are not unique")
    page = PAGE_PATH.read_text()
    for name in [f"{i:02d}.png" for i in range(1, 8)] + ["banner.png"]:
        if f"art/{name}" not in page:
            errors.append(f"proof page is missing art/{name}")
    return errors


def main() -> int:
    if "--write" in sys.argv:
        write_outputs()
        print("wrote supply/catalog.json, proofs/meta, proofs/collection.json, proofs/index.html")
        return 0
    errors = check_outputs()
    if errors:
        for err in errors:
            print(f"FAIL {err}", file=sys.stderr)
        return 1
    print("PASSED: 777 slots, 7 proofs, 770 unpainted, week 10 closes the supply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
