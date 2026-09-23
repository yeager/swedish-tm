# Swedish Translation Memory

**704 702 unique English–Swedish translation pairs** in 16 ecosystem exports
(811 676 entries before deduplicating across ecosystems). These counts describe
the files shipped in this repository  including the Translation Project update of 2026-09-23.

## Translation Project review update, 2026-09-23

The Translation Project export now contains 117 723 active, context-free singular
pairs. The review individually read 126 157 of 127 367 active source entries.
The remaining 1 210 entries are the explicitly excluded Wastesedge domain, which
has had no release for many years. It has not been represented as reviewed.

The update imports 33 484 verified source/previous-target/revised-target matches
into both `sv-tp.po` and `sv-tp.tmx`. It deliberately leaves out 184 plural
corrections, because this context-free singular compendium cannot preserve their
plural identity safely. [TP-REVIEW.md](TP-REVIEW.md) and the
[2026-09-23 audit](reviews/tp-2026-09-23.json) document the source baseline,
selection and exact output digests.

Every export remains a translation suggestion to be checked in its destination
context. All 16 PO files and 15 corresponding TMX files are checked in CI for
gettext validity, XML safety, format agreement and statistics consistency.

## Contents

| Ecosystem | Pairs in export | TMX | PO compendium |
|-----------|----------------:|-----|---------------|
\g<1>70 026\g<2> [sv-gnome.tmx](sv-gnome.tmx) | [sv-gnome.po](sv-gnome.po) |
\g<1>35 507\g<2> [sv-kde.tmx](sv-kde.tmx) | [sv-kde.po](sv-kde.po) |
\g<1>19 293\g<2> [sv-mozilla.tmx](sv-mozilla.tmx) | [sv-mozilla.po](sv-mozilla.po) |
\g<1>50 525\g<2> [sv-ubuntu.tmx](sv-ubuntu.tmx) | [sv-ubuntu.po](sv-ubuntu.po) |
\g<1>14 237\g<2> [sv-fedora.tmx](sv-fedora.tmx) | [sv-fedora.po](sv-fedora.po) |
\g<1>44 495\g<2> [sv-libreoffice.tmx](sv-libreoffice.tmx) | [sv-libreoffice.po](sv-libreoffice.po) |
\g<1>3 182\g<2> [sv-xfce.tmx](sv-xfce.tmx) | [sv-xfce.po](sv-xfce.po) |
\g<1>117 723\g<2> [sv-tp.tmx](sv-tp.tmx) | [sv-tp.po](sv-tp.po) |
\g<1>227 083\g<2> — | [sv-transifex.po](sv-transifex.po) |
\g<1>1 918\g<2> [sv-crowdin.tmx](sv-crowdin.tmx) | [sv-crowdin.po](sv-crowdin.po) |
\g<1>38 672\g<2> [sv-weblate.tmx](sv-weblate.tmx) | [sv-weblate.po](sv-weblate.po) |
\g<1>73 032\g<2> [sv-blender.tmx](sv-blender.tmx) | [sv-blender.po](sv-blender.po) |
\g<1>16 733\g<2> [sv-inkscape.tmx](sv-inkscape.tmx) | [sv-inkscape.po](sv-inkscape.po) |
\g<1>44 409\g<2> [sv-stellarium.tmx](sv-stellarium.tmx) | [sv-stellarium.po](sv-stellarium.po) |
\g<1>39 685\g<2> [sv-qgis.tmx](sv-qgis.tmx) | [sv-qgis.po](sv-qgis.po) |
\g<1>15 156\g<2> [sv-scummvm.tmx](sv-scummvm.tmx) | [sv-scummvm.po](sv-scummvm.po) |

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

## Review-derived project memories

Project-specific reviewed data and context-preserving PO/TMX exports are documented in [reviewed/README.md](reviewed/README.md). These supplement the ecosystem exports and retain original contexts, plural identities and review evidence.
