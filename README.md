# NovaSwift Plugins

This is the list of plug-ins and total conversions that shows up in the **Plugins** screen of [NovaSwift](https://github.com/SirStig/NovaSwift). The app downloads `catalog.json` from this repo, keeps a copy for offline use, and installs things straight from the links in it.

There are no plug-in files in this repo. Every entry points at a public download: the author's own, or a community archive such as escape-velocity.games.

## Rules

- **Link to a public download.** Prefer the author's own link, or an established community archive. Don't upload a copy somewhere new.
- **Don't rehost files without the author's permission.** That goes for the plug-in, and for icons and screenshots too. Only put art in `icons/` or `screenshots/` if the author says it's fine. Otherwise link to where it already lives.
- **No EV Nova base data.** Nothing from the original game's data files, and no art ripped from it. Plug-ins that need the base game are fine; they just can't ship it.
- **The link has to be a direct file.** `downloadURLs` must open the file itself (`.zip`, `.rez`, `.ndat`, or classic Mac `.sit`, `.hqx` / `.sit.hqx`, `.sea`, `.bin`). A web page with a download button doesn't count, and neither does anything behind a login, a captcha or a click-through. The app does the download and unpacking on its own, so if it can't, the plug-in can't go in the list. Old StuffIt, BinHex and MacBinary files unpack too (resource forks are kept), but StuffIt X (`.sitx`) is proprietary and is not accepted. HTTPS links only.

## Plug-ins we host ourselves

Most of this list points at the author's own download. A few plug-ins only ever existed as StuffIt or BinHex files in the old Ambrosia add-on archive, which is now reachable only over plain http. NovaSwift won't download over http, so for those we keep a copy as a release asset on this repo (the `archive-v1` release). In the catalog they carry `"rehosted": true`.

The rule is simple: **we only host a plug-in when the author's own readme says it may be redistributed.** Entries that are rehosted must quote the exact words (`permissionQuote`), say which file they came from (`permissionSource`) and where the original download lived (`originalSource`). The checks fail if any of those are missing. If a readme is silent, vague ("freeware" alone, "use it however you want"), says "ask me first", or the plug-in leans on someone else's art we can't clear, we leave it out.

What we change: nothing in the resource data. Classic Mac files keep their resource fork, saved as a `.ndat` file with the same bytes, and the author's readme goes in the zip as written (only line endings tidied). We add one `NOVASWIFT-ARCHIVE-NOTICE.txt` with the quote and the source. Icons and screenshots for these entries are pictures taken from the plug-in's own resources.

A handful are ports of classic Escape Velocity / Override plug-ins that someone converted to Nova's format; they are tagged `ported` and, like the other ports, are not fully debugged.

**Authors:** if you made one of these and want it gone, open an issue titled with the plug-in's name and it will be removed in the next update, no questions asked. The same goes if you'd like the credit or description changed.

## Adding a plug-in

1. Fork this repo.
2. Add an object to the `plugins` array in `catalog.json`. Copy an existing one. The fields are described in `schema/catalog.schema.json`; the ones you must fill in are `id`, `name`, `author`, `version`, `summary`, `isTotalConversion` and `downloadURLs`.
3. Fill in `sizeBytes` if you can (the size of the download in bytes). A `sha256` is welcome too: `shasum -a 256 file.zip`.
4. Run the checks:
   ```
   pip install jsonschema
   python3 scripts/validate.py          # schema, duplicate ids, dependencies
   python3 scripts/validate.py --urls   # also fetches every link
   python3 scripts/validate.py --urls --pending-release   # same, but skips rehosted entries whose release files aren't uploaded yet
   ```
5. Open a pull request. The checklist in the template is short. A GitHub Action runs the same checks.

Not comfortable editing JSON? Open a "Plug-in request" issue instead and someone will add it.

### A few notes on the fields

- `id`: lowercase with dashes, e.g. `evo-facelift`. It becomes the folder name on the player's device, so don't change it later.
- `version`: any text. Numbers are compared piece by piece, so `1.10` counts as newer than `1.9`. Bump it when the author releases a new file; players with the old version see an Update button.
- `tags`: the app's filters look for `story`, `graphics`, `gameplay`, `ships` and `patch`. Use whichever apply. Total conversions are marked with `isTotalConversion`, not a tag.
- `dependencies`: ids of other entries in this list the plug-in needs. The app installs those first.
- `summary` is one or two sentences for the card. `description` is the longer text and can use Markdown.
- `popularity`: higher sorts first under Popular. Use a download count if you have one, otherwise leave a sensible rank.
- `iconURL` and `screenshotURLs`: https links. Skip them if there's nothing you're allowed to use; the app shows a placeholder.

## Updating or removing an entry

Change `version` (and `sizeBytes`, `sha256`, `updatedDate`) when a new release comes out. If an author asks to have their plug-in taken down, open a PR deleting the entry, or open an issue and it'll be removed.

## Layout

```
catalog.json              the list the app reads
schema/catalog.schema.json  what a valid catalog looks like
scripts/validate.py       the checks CI runs
icons/, screenshots/      only art whose authors allow it here
```

The app reads `https://raw.githubusercontent.com/SirStig/NovaSwift-Plugins/main/catalog.json`.
