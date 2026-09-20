# Swedish Translation Memory

**688 242 unique English–Swedish translation pairs** in 16 ecosystem exports
(790 331 entries before deduplicating across ecosystems). These counts describe
the files shipped in this repository, exported on 2026-09-19.

## Release 1.1.0

Release 1.1.0 publishes the validated 2026-09-19 exports. It contains 790 331
active entries and 688 224 distinct English–Swedish pairs across 15 ecosystems.
The Translation Project review has individually checked 88 125 of 127 367
source entries and made 21 181 confirmed corrections; its scope and remaining
work are recorded in [TP-REVIEW.md](TP-REVIEW.md). The review is ongoing, so
every match remains a suggestion to be evaluated in its destination context.

All 16 PO files and 15 corresponding TMX files are checked in CI for gettext
validity, XML safety, format agreement and statistics consistency.

## Contents

| Ecosystem | Pairs in export | TMX | PO compendium |
|-----------|----------------:|-----|---------------|
| GNOME | 70 026 | [sv-gnome.tmx](sv-gnome.tmx) | [sv-gnome.po](sv-gnome.po) |
| KDE | 35 507 | [sv-kde.tmx](sv-kde.tmx) | [sv-kde.po](sv-kde.po) |
| Mozilla | 19 293 | [sv-mozilla.tmx](sv-mozilla.tmx) | [sv-mozilla.po](sv-mozilla.po) |
| Ubuntu | 50 525 | [sv-ubuntu.tmx](sv-ubuntu.tmx) | [sv-ubuntu.po](sv-ubuntu.po) |
| Fedora | 14 237 | [sv-fedora.tmx](sv-fedora.tmx) | [sv-fedora.po](sv-fedora.po) |
| LibreOffice | 44 495 | [sv-libreoffice.tmx](sv-libreoffice.tmx) | [sv-libreoffice.po](sv-libreoffice.po) |
| XFCE | 3 182 | [sv-xfce.tmx](sv-xfce.tmx) | [sv-xfce.po](sv-xfce.po) |
| Translation Project | 117 723 | [sv-tp.tmx](sv-tp.tmx) | [sv-tp.po](sv-tp.po) |
| Transifex | 227 083 | — | [sv-transifex.po](sv-transifex.po) |
| CrowdIn | 1 750 | [sv-crowdin.tmx](sv-crowdin.tmx) | [sv-crowdin.po](sv-crowdin.po) |
| Weblate | 22 854 | [sv-weblate.tmx](sv-weblate.tmx) | [sv-weblate.po](sv-weblate.po) |
| Blender | 70 264 | [sv-blender.tmx](sv-blender.tmx) | [sv-blender.po](sv-blender.po) |
| Inkscape | 15 892 | [sv-inkscape.tmx](sv-inkscape.tmx) | [sv-inkscape.po](sv-inkscape.po) |
| Stellarium | 44 409 | [sv-stellarium.tmx](sv-stellarium.tmx) | [sv-stellarium.po](sv-stellarium.po) |
| QGIS | 39 685 | [sv-qgis.tmx](sv-qgis.tmx) | [sv-qgis.po](sv-qgis.po) |
| ScummVM | 15 156 | [sv-scummvm.tmx](sv-scummvm.tmx) | [sv-scummvm.po](sv-scummvm.po) |

The former README described different collection-wide counts and a
`sv-complete.po` that is not present in this repository. Use the ecosystem
files above. [stats.json](stats.json) contains counts verified from the exports.

## Usage

Use a PO compendium with GNU gettext:

```bash
msgmerge --compendium sv-gnome.po --compendium sv-kde.po my-file.po my-file.pot -o filled.po
```

Look up a translation with Python:

```python
import polib

tm = {e.msgid: e.msgstr for e in polib.pofile('sv-gnome.po').translated_entries()}
print(tm.get('Save'))
```

TMX files can be imported into CAT tools. All 14 TMX exports contain the same
source/target pairs as their corresponding PO exports. Transifex is PO-only.

The exports preserve project references, but not the original message contexts
or plural identities. Treat matches as translation suggestions and review them
in their destination context. Agreement between export formats is not a
linguistic quality guarantee.

## Export repairs and control characters

Carriage returns are escaped as `\r` in PO and `&#13;` in TMX. This prevents
Python PO readers from splitting strings and XML readers from changing CR to LF.
Six Transifex translations were given the final newline required by their source
strings so the compendium passes `msgfmt --check`.

The TP and Ubuntu memories include five pairs containing control characters
(U+0007, U+000B or U+001B) forbidden in XML 1.0. Their TMX segments now use
[TMX native-code placeholders](https://www.ttt.org/oscarStandards/tmx/tmx14b.html):
`<ph x="1" type="x-control">U+001B</ph>` represents one ESC character.
The `x` values pair corresponding occurrences within each translation unit.
All original control characters remain in the PO files. Use PO for consumers
that need those bytes directly; CAT tools must preserve the placeholders.
The validator decodes this documented representation before comparing pairs.

## Validation

Requires Python 3.10+ and GNU gettext (`msgfmt`).

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
python3 scripts/validate.py
```

Validation runs gettext checks, parses every PO/TMX file, rejects duplicate
sources and invalid language pairs, compares the complete contents between
formats, and checks `stats.json`. After an intentional data update, regenerate
counts with `python3 scripts/validate.py --write-stats`.
GitHub Actions runs these checks on pushes and pull requests.

## Sources and reuse

The collection draws on GNOME, KDE, Mozilla, Ubuntu, Fedora, LibreOffice,
Translation Project, Transifex, Weblate, Blender, Inkscape, Stellarium, QGIS
and ScummVM translations. Project references are included in the exports.

License: CC BY 4.0.

Related: [Swedish FOSS Terminology](https://github.com/yeager/swedish-foss-terminology), [Computer Swedens IT-ord](https://it-ord.computersweden.se/)
and [svlang](https://github.com/yeager/svlang).
