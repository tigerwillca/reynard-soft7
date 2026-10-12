# Developers

Product rules live in `BRIEF.md`. This page is the local metadata server in `scripts/metadata_server.py`, the token JSON from `scripts/token_metadata.py`, and the wave page `proofs/waves.html`.

Nothing here deploys, mints, or calls a chain. The server is not a base URI for the live supply-7 contract `0x73D7b2611509C14078e16f572bE5aC7D91879DC2`. `scripts/encode_set_base_uri.py` only prints calldata. `BRIEF.md` says not to send it.

## Setup

`bash scripts/ci.sh` runs the metadata check with the rest of the build. It needs `bash`, `python3`, and `git`. The metadata scripts use the Python standard library only. `.github/workflows/build.yml` runs that script on every push and pull request, with Python 3.12.

```bash
python3 scripts/check_metadata.py
bash scripts/start_metadata_server.sh
```

`check_metadata.py` checks the documents, then serves once on `127.0.0.1` and a free port. It shuts that server down before it exits. It does not use port 8000.

`start_metadata_server.sh` is the long-running server. `METADATA_SERVER_PORT` overrides the port (default `8000`). The process binds `0.0.0.0`, logs to `/tmp/soft7-metadata-server.log`, and is left running. The script does not stop it.

The ready check is `GET /1.json`. The body must be JSON whose `name` is `Reynard Soft7 Proof Tier 1`, whose `attributes` is a list of five traits, and whose `image` is `proofs/art/01.png`. When that already succeeds, the script prints that the server is listening and exits 0. It does not restart the process, so a later edit to a shell is invisible until that process is killed.

If the port is taken by something that fails the ready check, the new process cannot bind. The script then exits 1 after about ten seconds (40 polls, 0.25 seconds apart). The traceback is in the log.

## What the check runs

`python3 scripts/check_metadata.py` is the metadata step inside `scripts/ci.sh`, after `scripts/supply.py --check` and before the compiler. It proves:

| Check | What is locked |
| --- | --- |
| `proofs/waves.html` | Byte-for-byte match with `render_waves_page()`, and the page contains `Mint is closed`. |
| `proofs/index.html` | Contains `href="waves.html"`. |
| `proofs/collection.json` | Matches `collection()`, and `seller_fee_basis_points` is 750. |
| `proofs/meta/1.json`–`7.json` | Match `token_document` and `proof_metadata`. Each image is a `proofs/art/` PNG, and each proof has five traits. |
| Shells 8, 84, 85, 700, 701, and 777 | Keys are exactly `name`, `description`, `external_url`, in that order. No `image` and no `attributes`. |
| Ids 0, 778, and −1 | `token_document` raises `KeyError`. |
| `GET /1.json` | 200 JSON equal to `token_document(1)`. |
| `GET /meta/8.json` | 200 unpainted shell. |
| `GET /meta/778.json` | 404 JSON. |
| `GET /meta/01.json` | 404. Leading zeros are not a token id. |
| `GET /proofs/art/01.png` | 200 `image/png` starting with the PNG signature. |
| `GET /proofs/../scripts/ci.sh` | 404. Paths outside `proofs/` are not served. |
| `GET /waves` | 302 to `/proofs/waves.html`. |
| `GET /proofs/waves.html` | 200 HTML equal to the generator. |
| `GET /collection.json` | 200, royalty 750. |

`python3 scripts/check_metadata.py --write` rewrites `proofs/waves.html` and nothing else. `python3 scripts/supply.py --write` rewrites the catalog, `proofs/collection.json`, `proofs/meta/1.json` through `7.json`, and `proofs/index.html`. Shells for tokens 8–777 are not files. The server builds them on request.

## Routes

The handler reads `GET` only. The query string is ignored. Every response from `_send` sets `Access-Control-Allow-Origin: *` and `Cache-Control: no-store`. The 302 does not set those two headers. `Server` identifies as `Soft7Metadata/1.0`.

| Path | Status | Body |
| --- | --- | --- |
| `/{id}.json` | 200 | Token document for id 1–777. |
| `/meta/{id}.json` | 200 | The same document. |
| `/collection.json` | 200 | Collection document. |
| `/meta/collection.json` | 200 | The same collection document. |
| `/waves`, `/waves.html` | 302 | `Location: /proofs/waves.html`, empty body. |
| `/proofs/<file>` | 200 | A file whose resolved path is under `proofs/`. |
| Canonical id outside 1–777 | 404 | JSON `{"error": "token is outside the 777 supply"}`. |
| Anything else | 404 | Plain text `not found`. |

A canonical id is a decimal stem with no leading zeros: `1.json` is token 1, and `01.json` is not a token path. `GET /1.json` is the generator. `GET /proofs/meta/1.json` is the committed file. The check requires them to match.

Static files must start with `/proofs/`, must not end in `/`, and must be a file. `proofs/` has to be a parent of the resolved path, so a `..` segment cannot leave that directory. HTML is `text/html; charset=utf-8`, JSON is `application/json; charset=utf-8`, and PNG is `image/png`. Any other suffix under `proofs/` is `application/octet-stream`.

On the 777-card contract, `tokenURI` is the base, the decimal id, and `.json`. A base of `http://127.0.0.1:8000/` requests `/1.json`. PNG filenames are zero-padded (`01.png`). Token URLs are not.

```bash
curl -sS http://127.0.0.1:8000/1.json
curl -sS http://127.0.0.1:8000/8.json
curl -sS -D - -o /dev/null http://127.0.0.1:8000/waves
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/meta/01.json
curl -sS http://127.0.0.1:8000/meta/778.json
```

## Token JSON

Tokens 1–7 repeat the proof files. Token 1:

```json
{
  "name": "Reynard Soft7 Proof Tier 1",
  "description": "reynard-soft7 mascot cards on robinhood chain. ten percent of every mint routes back to soft7 holders proportional to what they hold. stake your card, feed the treasury, pull when you're ready.",
  "image": "proofs/art/01.png",
  "external_url": "https://tigerwillca.github.io/",
  "attributes": [
    { "trait_type": "tier", "value": 1 },
    { "trait_type": "color", "value": "Crimson" },
    { "trait_type": "eyes", "value": "Amber Lock" },
    { "trait_type": "signature", "value": "Brow Line" },
    { "trait_type": "globe", "value": "Root Stone" }
  ]
}
```

The `image` value is a path under `proofs/art/`, served at `/proofs/art/01.png`. It is not an `https` URL. Traits stay the five names in `BRIEF.md`, in the order `tier`, `color`, `eyes`, `signature`, `globe`. Proof names are `Reynard Soft7 Proof Tier N`.

Tokens 8–777 are shells. Token 8:

```json
{
  "name": "Reynard Soft7 #8",
  "description": "reynard-soft7 mascot cards on robinhood chain. ten percent of every mint routes back to soft7 holders proportional to what they hold. stake your card, feed the treasury, pull when you're ready.",
  "external_url": "https://tigerwillca.github.io/"
}
```

The description is the canon string in `scripts/supply.py`. Adding `image` or `attributes` to a shell fails the check. Those slots stay unpainted.

`GET /collection.json` returns `name`, `description`, `image` (`proofs/art/01.png`), `banner_image` (`proofs/art/banner.png`), `external_link` (`https://tigerwillca.github.io/`), `discord_url`, `twitter_username` (`tigerwillca`), `seller_fee_basis_points` (750), and `fee_recipient` (`0xe53bdb2118585d5B2cD06a117d3A036AFA70677a`). Token documents use `external_url`. The collection document uses `external_link`.

## Wave page

`proofs/waves.html` is generated. Hand-editing it fails the check. The page states that mint is closed, the seven proofs are unapproved, and `openWaves` has not been sent. It links to `index.html` as “The seven proofs”. The proof page links back with `href="waves.html"`.

`/waves` redirects to `/proofs/waves.html` so that proof link stays inside `proofs/`. Opening `/waves.html` at the server root does the same redirect. Opening the file directly from disk uses the relative link and does not need the redirect.

The table is weeks 0 through 10. The cap is `7 + week * 77`, and it stops at 777. The page does not add a row for later weeks. Its prose says later weeks stay at 777. “What that week adds” is `7 proofs` in week 0 and `77 cards` after that.

| Week | Cap | Token ids | What that week adds |
| --- | --- | --- | --- |
| 0 | 7 | 1–7 | 7 proofs |
| 1 | 84 | 8–84 | 77 cards |
| 2 | 161 | 85–161 | 77 cards |
| 3 | 238 | 162–238 | 77 cards |
| 4 | 315 | 239–315 | 77 cards |
| 5 | 392 | 316–392 | 77 cards |
| 6 | 469 | 393–469 | 77 cards |
| 7 | 546 | 470–546 | 77 cards |
| 8 | 623 | 547–623 | 77 cards |
| 9 | 700 | 624–700 | 77 cards |
| 10 | 777 | 701–777 | 77 cards |

The catalog `wave` for an id comes from `token_wave()` in `scripts/supply.py`. Token 8 stays wave 1 there even if it is minted in a later week. This page lists the cap, not a mint.

## When a check fails

| Failure | What to fix |
| --- | --- |
| `proofs/waves.html does not match the generator` | Regenerate with `python3 scripts/check_metadata.py --write`. Do not hand-edit the table. |
| `wave page does not say mint is closed` | `render_waves_page()` in `scripts/token_metadata.py` must keep the sentence `Mint is closed.` |
| `proof page is missing the wave schedule link` | `proofs/index.html` has to contain `href="waves.html"`. `python3 scripts/supply.py --write` restores the generated page. |
| `token N metadata drifted` | `proofs/meta/N.json` no longer matches `proof_metadata`. Restore it with `python3 scripts/supply.py --write`. |
| `token N invented art fields` | A shell gained `image` or `attributes`. Tokens 8–777 stay name, description, and `external_url`. |
| `token N image is not a PNG` or `is not a proofs/art path` | Proof images stay the committed files under `proofs/art/`. Do not redraw them. |
| `collection royalty is not 750` or `collection.json royalty drifted` | `seller_fee_basis_points` stays 750, on disk and on `GET /collection.json`. |
| `metadata server leaked a file outside proofs/` | `_proof_file` only serves a file under `proofs/`. |
| `/meta/01.json returned` something other than 404 | Token stems are not zero-padded. `01` is not token 1. |
| `metadata server failed to become ready` | Read `/tmp/soft7-metadata-server.log`. A process already bound to the port, or `/1.json` is not the tier-1 proof. Kill the old pid before starting again after a code change. |
