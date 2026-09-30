#!/usr/bin/env python3
"""Check the 777 metadata documents and serve them once on a free port."""
from __future__ import annotations

import json
import pathlib
import sys
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from metadata_server import MetadataHandler
from supply import CANON, proof_metadata
from token_metadata import (
    SHELL_KEYS,
    WAVES_PATH,
    collection_document,
    render_waves_page,
    token_document,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
META_DIR = ROOT / "proofs" / "meta"
PAGE_PATH = ROOT / "proofs" / "index.html"


def _get(base: str, path: str) -> tuple[int, bytes, str, str]:
    request = urllib.request.Request(base + path)
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=5) as response:
            raw = response.read()
            return (
                response.status,
                raw,
                response.headers.get("Content-Type", ""),
                response.headers.get("Location", ""),
            )
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.headers.get("Content-Type", ""), exc.headers.get("Location", "")


class _NoRedirect(urllib.request.HTTPErrorProcessor):
    def http_response(self, request, response):  # noqa: ARG002
        return response

    https_response = http_response


def check_documents() -> list[str]:
    errors: list[str] = []
    page = render_waves_page()
    if "Mint is closed" not in page:
        errors.append("wave page does not say mint is closed")
    if WAVES_PATH.read_text() != page:
        errors.append("proofs/waves.html does not match the generator")
    if 'href="waves.html"' not in PAGE_PATH.read_text():
        errors.append("proof page is missing the wave schedule link")

    collection = collection_document()
    on_disk = json.loads((ROOT / "proofs" / "collection.json").read_text())
    if collection != on_disk:
        errors.append("collection document drifted from proofs/collection.json")
    if collection.get("seller_fee_basis_points") != 750:
        errors.append("collection royalty is not 750")

    for token_id in range(1, 8):
        document = token_document(token_id)
        stored = json.loads((META_DIR / f"{token_id}.json").read_text())
        if document != stored or document != proof_metadata(token_id):
            errors.append(f"token {token_id} metadata drifted")
        image = document.get("image")
        if not isinstance(image, str) or not image.startswith("proofs/art/"):
            errors.append(f"token {token_id} image is not a proofs/art path")
            continue
        raw = (ROOT / image).read_bytes()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append(f"token {token_id} image is not a PNG")
        traits = document.get("attributes")
        if not isinstance(traits, list) or len(traits) != 5:
            errors.append(f"token {token_id} must keep five traits")

    for token_id in (8, 84, 85, 700, 701, 777):
        document = token_document(token_id)
        if tuple(document) != SHELL_KEYS:
            errors.append(f"token {token_id} shell keys are {tuple(document)}")
        if document["description"] != CANON:
            errors.append(f"token {token_id} description drifted")
        if document["name"] != f"Reynard Soft7 #{token_id}":
            errors.append(f"token {token_id} name drifted")
        if "image" in document or "attributes" in document:
            errors.append(f"token {token_id} invented art fields")

    for token_id in (0, 778, -1):
        try:
            token_document(token_id)
        except KeyError:
            continue
        errors.append(f"token {token_id} should be outside the supply")
    return errors


def check_server() -> list[str]:
    errors: list[str] = []
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), MetadataHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    port = httpd.server_address[1]
    base = f"http://127.0.0.1:{port}"
    try:
        status, raw, content_type, _ = _get(base, "/1.json")
        if status != 200 or "application/json" not in content_type:
            errors.append(f"/1.json returned {status} {content_type}")
        else:
            body = json.loads(raw)
            if body != token_document(1):
                errors.append("/1.json body drifted")

        status, raw, _, _ = _get(base, "/meta/8.json")
        if status != 200:
            errors.append(f"/meta/8.json returned {status}")
        else:
            body = json.loads(raw)
            if tuple(body) != SHELL_KEYS or "image" in body or "attributes" in body:
                errors.append("/meta/8.json is not an unpainted shell")

        status, raw, content_type, _ = _get(base, "/meta/778.json")
        if status != 404 or "application/json" not in content_type:
            errors.append(f"/meta/778.json returned {status} {content_type}")

        status, _, _, _ = _get(base, "/meta/01.json")
        if status != 404:
            errors.append(f"/meta/01.json returned {status}")

        status, raw, content_type, _ = _get(base, "/proofs/art/01.png")
        if status != 200 or content_type != "image/png" or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append(f"proof png returned {status} {content_type}")

        status, _, _, _ = _get(base, "/proofs/../scripts/ci.sh")
        if status != 404:
            errors.append("metadata server leaked a file outside proofs/")

        status, _, _, location = _get(base, "/waves")
        if status != 302 or location != "/proofs/waves.html":
            errors.append(f"/waves returned {status} location {location}")

        status, raw, content_type, _ = _get(base, "/proofs/waves.html")
        if status != 200 or "text/html" not in content_type or b"Mint is closed" not in raw:
            errors.append(f"/proofs/waves.html returned {status} {content_type}")
        if status == 200 and raw != render_waves_page().encode("utf-8"):
            errors.append("/proofs/waves.html does not match the generator")

        status, raw, _, _ = _get(base, "/collection.json")
        if status != 200 or json.loads(raw).get("seller_fee_basis_points") != 750:
            errors.append("collection.json royalty drifted")
    finally:
        httpd.shutdown()
    return errors


def main() -> int:
    if "--write" in sys.argv:
        WAVES_PATH.write_text(render_waves_page())
        print("wrote proofs/waves.html")
        return 0
    errors = check_documents() + check_server()
    if errors:
        for err in errors:
            print(f"FAIL {err}", file=sys.stderr)
        return 1
    print("PASSED: metadata for 7 proofs and 770 unpainted shells, wave page, local server")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
