# Public NovaSwift servers

`servers.json` is the directory behind the **Public** tab of NovaSwift's multiplayer screen. The app downloads it from

`https://raw.githubusercontent.com/SirStig/NovaSwift-Plugins/main/servers/servers.json`

then pings every entry itself (a UDP status query) to show whether it is online, how many players are in, its version, whether it has a password, and your latency. **Nothing here runs a server for you** and the list is never trusted for live data: an entry that doesn't answer is shown offline.

## List your server

1. Run a dedicated server (see "Host a public server in 5 minutes" in NovaSwift's `docs/MULTIPLAYER.md`). Make sure UDP **53735** (your game port) and **53736** (game port + 1, for the status query) are reachable from the internet.
2. Start it once with `--public`. It prints a ready-to-paste JSON entry for your server, including the content hash of every plug-in players need.
3. Fork this repo, paste the entry into the `servers` array of `servers/servers.json`.
4. Check it: `pip install jsonschema && python3 servers/validate.py`
5. Open a pull request titled `Add server: <name>`.

To update or remove your server, open a PR changing or deleting the entry. Servers that stay offline for a month or two may be pruned.

## Rules

- **Public address only.** A DNS name or public IP. No `192.168.x.x`, no `localhost`.
- **No passwords in the listing.** A password-protected server may be listed (players are asked for it), but the password itself must never appear here.
- **Be honest.** `rules` must describe what the server really does: `safe` (visitors' PvP damage and death aren't real), `full` (real stakes) or `custom`.
- **Plug-ins must be obtainable.** List required plug-ins by `id` from this repo's `catalog.json` where possible, so players can install them from the Plugins screen. No EV Nova base data, ever.
- **Family-friendly names and descriptions.**
- **Give a contact** (`owner.contact`: Discord, GitHub user or email) so players and maintainers can reach you.

## Entry fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | lowercase-with-dashes, unique, stable |
| `name` | yes | up to 40 characters |
| `host` | yes | DNS name or public IP |
| `port` | yes | UDP game port, default `53735` |
| `region` | yes | `na-east`, `na-west`, `sa`, `eu`, `af`, `me`, `as`, `oc`, `global` |
| `description` | yes | up to 300 characters |
| `owner` | yes | `{ "name": "...", "contact": "..." }` |
| `rules` | yes | `safe`, `full`, `custom` |
| `plugins` | no | `[{ "id", "name", "version", "contentHash" }]` players must have enabled |
| `maxPlayers` | yes | 2 to 64 |
| `added` | yes | `YYYY-MM-DD` |
| `website` | no | https only |

Example:

```json
{
  "id": "example-eu",
  "name": "Example Sector",
  "host": "nova.example.com",
  "port": 53735,
  "region": "eu",
  "description": "Friendly 24/7 server, safe rules, vanilla EV Nova.",
  "owner": { "name": "Jane", "contact": "discord: jane#0001" },
  "rules": "safe",
  "plugins": [],
  "maxPlayers": 12,
  "added": "2026-10-13",
  "website": "https://example.com/nova"
}
```

The full schema is `servers.schema.json`.
