# NovaSwift Plugins

This is the list of plug-ins and total conversions that shows up in the **Plugins** screen of [NovaSwift](https://github.com/SirStig/NovaSwift). The app downloads `catalog.json` from this repo, keeps a copy for offline use, and installs things straight from the links in it.

There are no plug-in files in this repo. Every entry points at a public download: the author's own, or a community archive such as escape-velocity.games.

## Rules

- **Link to a public download.** Prefer the author's own link, or an established community archive. Don't upload a copy somewhere new.
- **Don't rehost files without the author's permission.** That goes for the plug-in, and for icons and screenshots too. Only put art in `icons/` or `screenshots/` if the author says it's fine. Otherwise link to where it already lives.
- **No EV Nova base data.** Nothing from the original game's data files, and no art ripped from it. Plug-ins that need the base game are fine; they just can't ship it.
- **The link has to be a direct file.** `downloadURLs` must open the file itself (`.zip`, `.rez` or `.ndat`). A web page with a download button doesn't count, and neither does anything behind a login, a captcha or a click-through. The app does the download and unpacking on its own, so if it can't, the plug-in can't go in the list. Formats like StuffIt (`.sit`) and BinHex (`.hqx`) aren't supported yet.

## Adding a plug-in

1. Fork this repo.
2. Add an object to the `plugins` array in `catalog.json`. Copy an existing one. The fields are described in `schema/catalog.schema.json`; the ones you must fill in are `id`, `name`, `author`, `version`, `summary`, `isTotalConversion` and `downloadURLs`.
3. Fill in `sizeBytes` if you can (the size of the download in bytes). A `sha256` is welcome too: `shasum -a 256 file.zip`.
4. Run the checks:
   ```
   pip install jsonschema
   python3 scripts/validate.py          # schema, duplicate ids, dependencies
   python3 scripts/validate.py --urls   # also fetches every link
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
