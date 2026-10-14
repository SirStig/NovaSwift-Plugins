#!/usr/bin/env python3
"""Checks servers/servers.json against servers.schema.json plus a few extra rules.
Standard library + jsonschema:  pip install jsonschema && python3 servers/validate.py"""
import ipaddress
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

here = Path(__file__).resolve().parent
doc = json.loads((here / "servers.json").read_text())
schema = json.loads((here / "servers.schema.json").read_text())
errors = [f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message}" for e in Draft202012Validator(schema).iter_errors(doc)]
seen_ids, seen_addr = set(), set()
for s in doc.get("servers", []):
    if s.get("id") in seen_ids:
        errors.append(f"duplicate id {s.get('id')}")
    seen_ids.add(s.get("id"))
    addr = (str(s.get("host", "")).lower(), s.get("port"))
    if addr in seen_addr:
        errors.append(f"duplicate address {addr[0]}:{addr[1]}")
    seen_addr.add(addr)
    h = str(s.get("host", ""))
    try:
        ip = ipaddress.ip_address(h.strip("[]"))
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            errors.append(f"{s.get('id')}: host {h} is not a public address")
    except ValueError:
        if h.lower() in ("localhost",) or h.endswith(".local") or h.endswith(".lan"):
            errors.append(f"{s.get('id')}: host {h} is not public")
for e in errors:
    print("ERROR:", e)
print("OK" if not errors else f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)
