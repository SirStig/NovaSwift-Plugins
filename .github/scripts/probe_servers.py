#!/usr/bin/env python3
"""Probe every server in servers/servers.json with the NovaSwift UDP status query and write status.json.

The website (sirstig.github.io/NovaSwift servers page) reads status/status.json from the `status` branch.
Browsers can't send UDP, so this job does it on a schedule. Stdlib only.
Query: "NSQ1" + version byte 0x01 + zero padding to 1200 bytes (anti-amplification format); servers that
predate it answer only the bare 4-byte "NSQ1", so that is tried as a fallback.
"""
import json, socket, sys, time, datetime

TIMEOUT = 3.0

def query(host, port, payload):
    status_port = 53736 if port == 53735 else port + 1
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT)
        t0 = time.monotonic()
        s.sendto(payload, (host, status_port))
        data, _ = s.recvfrom(65535)
        ms = int((time.monotonic() - t0) * 1000)
    if not data.startswith(b"NSB1"):
        raise ValueError("unexpected reply")
    info = json.loads(data[4:].decode("utf-8", "replace"))
    return info, ms

def probe(entry):
    host, port = entry["host"], int(entry.get("port", 53735))
    padded = b"NSQ1" + b"\x01" + b"\x00" * (1200 - 5)
    for payload in (padded, b"NSQ1"):
        for _attempt in range(2):
            try:
                info, ms = query(host, port, payload)
                if info.get("upgrade") and payload == b"NSQ1":
                    break
                players = int(info.get("players", 0))
                if info.get("dedicated") and "pcount" in info:
                    players = int(info.get("pcount", players))
                return {"online": True, "players": max(0, players), "max": int(info.get("max", entry.get("maxPlayers", 0))),
                        "pw": bool(info.get("pw", False)), "ver": str(info.get("ver", ""))[:32],
                        "proto": int(info.get("proto", 0)), "rules": str(info.get("rules", ""))[:16], "ms": ms}
            except Exception:
                continue
    return {"online": False}

def main():
    servers = json.load(open(sys.argv[1]))["servers"]
    out = {"updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "servers": {}}
    for e in servers:
        out["servers"][e["id"]] = probe(e)
        print(e["id"], out["servers"][e["id"]])
    json.dump(out, open(sys.argv[2], "w"), indent=2)

if __name__ == "__main__":
    main()
