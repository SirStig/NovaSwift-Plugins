#!/usr/bin/env python3
"""Checks catalog.json: schema, duplicate ids, dependencies, and that every
download link is a direct file (not an HTML page).

  python3 scripts/validate.py              # schema + ids only (offline)
  python3 scripts/validate.py --urls       # also hit every download URL
  python3 scripts/validate.py --urls --hash  # also download and check sha256
"""
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
FILE_EXTS = (".zip", ".rez", ".ndat", ".sit", ".hqx", ".sea", ".bin")  # no .sitx: StuffIt X is unsupported
errors = []


def err(msg):
    errors.append(msg)
    print("ERROR:", msg)


def check_schema(doc):
    schema = json.loads((ROOT / "schema" / "catalog.schema.json").read_text())
    for e in sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in e.path) or "(root)"
        err(f"schema: {where}: {e.message}")


def check_ids(doc):
    ids = [p.get("id") for p in doc.get("plugins", [])]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        err(f"duplicate id: {i}")
    known = set(ids)
    for p in doc.get("plugins", []):
        for d in p.get("dependencies", []):
            if d not in known:
                err(f"{p.get('id')}: dependency '{d}' is not in the catalog")
        if p.get("id") in p.get("dependencies", []):
            err(f"{p.get('id')}: depends on itself")


def open_url(url, ranged):
    headers = {"User-Agent": "NovaSwift-Plugins-CI"}
    if ranged:
        headers["Range"] = "bytes=0-1023"
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60)


def check_download(pid, url, sha256, full):
    if not url.lower().split("?")[0].endswith(FILE_EXTS):
        err(f"{pid}: {url} does not end in {', '.join(FILE_EXTS)}")
    try:
        r = open_url(url, ranged=not full)
    except (urllib.error.URLError, TimeoutError) as ex:
        err(f"{pid}: {url} not reachable: {ex}")
        return
    ctype = (r.headers.get("Content-Type") or "").lower()
    if ctype.startswith("text/html"):
        err(f"{pid}: {url} returned an HTML page, not a file")
        return
    h = hashlib.sha256()
    first = b""
    while True:
        chunk = r.read(1 << 20)
        if not chunk:
            break
        if not first:
            first = chunk[:4]
        h.update(chunk)
    if url.lower().split("?")[0].endswith(".zip") and first[:2] != b"PK":
        err(f"{pid}: {url} does not look like a zip (starts {first!r})")
    if full and sha256 and h.hexdigest() != sha256.lower():
        err(f"{pid}: sha256 mismatch for {url}: got {h.hexdigest()}")


def check_image(pid, url):
    try:
        r = open_url(url, ranged=True)
    except (urllib.error.URLError, TimeoutError) as ex:
        err(f"{pid}: image {url} not reachable: {ex}")
        return
    ctype = (r.headers.get("Content-Type") or "").lower()
    if not ctype.startswith("image/"):
        err(f"{pid}: image {url} has content-type '{ctype}', not an image")


def main():
    urls = "--urls" in sys.argv
    full = "--hash" in sys.argv
    doc = json.loads((ROOT / "catalog.json").read_text())
    check_schema(doc)
    check_ids(doc)
    if urls and not errors:
        for p in doc["plugins"]:
            for u in p["downloadURLs"]:
                check_download(p["id"], u, p.get("sha256") if u == p["downloadURLs"][0] else None,
                               full and bool(p.get("sha256")))
            for u in [p.get("iconURL"), *p.get("screenshotURLs", [])]:
                if u:
                    check_image(p["id"], u)
    print(f"{len(doc.get('plugins', []))} plug-ins checked, {len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
