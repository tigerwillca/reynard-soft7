#!/usr/bin/env python3
"""Serve Soft7 token JSON and the proof files. Does not deploy or mint."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from token_metadata import ROOT, collection_document, token_document

PROOFS = (ROOT / "proofs").resolve()
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
}


def canonical_token_id(stem: str) -> int | None:
    if not stem.isdigit():
        return None
    if stem != str(int(stem)):
        return None
    return int(stem)


class MetadataHandler(BaseHTTPRequestHandler):
    server_version = "Soft7Metadata/1.0"

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in ("/collection.json", "/meta/collection.json"):
            self._send(200, "application/json; charset=utf-8", _json(collection_document()))
            return
        if path in ("/waves", "/waves.html"):
            self.send_response(302)
            self.send_header("Location", "/proofs/waves.html")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        token_id = _token_path(path)
        if token_id is not None:
            try:
                document = token_document(token_id)
            except KeyError:
                self._send(
                    404,
                    "application/json; charset=utf-8",
                    _json({"error": "token is outside the 777 supply"}),
                )
                return
            self._send(200, "application/json; charset=utf-8", _json(document))
            return

        static = _proof_file(path)
        if static is None:
            self._send(404, "text/plain; charset=utf-8", b"not found\n")
            return
        kind = CONTENT_TYPES.get(static.suffix, "application/octet-stream")
        self._send(200, kind, static.read_bytes())

    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def _json(document: object) -> bytes:
    return (json.dumps(document, indent=2) + "\n").encode("utf-8")


def _token_path(path: str) -> int | None:
    for prefix in ("/meta/", "/"):
        if not path.startswith(prefix) or path == prefix:
            continue
        name = path[len(prefix):]
        if "/" in name or not name.endswith(".json") or name == "collection.json":
            continue
        return canonical_token_id(name[: -len(".json")])
    return None


def _proof_file(path: str) -> pathlib.Path | None:
    if not path.startswith("/proofs/") or path.endswith("/"):
        return None
    candidate = (ROOT / path.lstrip("/")).resolve()
    if PROOFS not in candidate.parents or not candidate.is_file():
        return None
    return candidate


def serve(bind: str, port: int) -> None:
    httpd = ThreadingHTTPServer((bind, port), MetadataHandler)
    print(f"metadata server on http://{bind}:{port}", flush=True)
    httpd.serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve Soft7 metadata locally")
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    serve(args.bind, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
