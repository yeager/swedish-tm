# Swedish Translation Memory

## Svenska

Detta översättningsminne innehåller engelska–svenska översättningspar från
FOSS-projekt. Använd det för förslag, aldrig som ensamt facit. Kontrollera varje
träff mot aktuell källtext och gränssnittskontext med l10n-lint, svlang,
hunspell-sv och swedish-foss-terminology.

### Användning

```bash
msgmerge --compendium sv-gnome.po --compendium sv-kde.po my-file.po my-file.pot -o filled.po
```

Bevara platshållare, taggar, snabbtangenter och radbrytningar exakt. Tillämpa
svensk skrivpolicy på förslaget: ingen komma omedelbart före `och`, svenska
citattecken, `…`, korrekt procentformat, siffergruppering och tankstreck i
intervall. Text före `|` i en Crowdin-sträng är kontextmetadata och får inte
visas i översättningen. Bedöm alltid betydelse, stilnivå och terminologi rad
för rad.

## English reference

**762 230 unique English–Swedish translation pairs** in 16 ecosystem exports
(881 171 entries before deduplicating across ecosystems). These counts describe
the files currently shipped in this repository, including the latest reviewed
GNOME and Translation Project updates.

## GNOME terminology update, 2026-11-28

The GNOME TM was refreshed from the reviewed archive after a full 72-string review of GNOME Music help on gnome-51. Thirty-one existing translations were corrected; no new translations were needed, and the catalog is complete and fuzzy-free. A 128-string review of the gnome-51 UI then corrected seven existing translations, reusing the recently reviewed 123-key `main` catalog and separately checking five branch-specific keys. The review archive includes the original PO, latest POT, reviewed PO, diff and validation report. The refresh also incorporates the GIMP Help terminology correction and complete latest-POT review of the glossary. `Bucket Fill` uses **Fyll** as the UI label and
**fyllnadsverktyg** in Swedish prose. The terminology correction covers 29
entries across five current master and gimp-help-3-0 catalogs (15 unique source
strings). The Loupe Help review added 66 GNOME TM entries; the 78-string catalog
also includes 11 unchanged image references and existing pairs. The exported
GNOME TM now contains 136 608 entries and passes the repository validator. The latest
GIMP Help glossary added 253 completed translations and corrected four existing
pairs; all 342 translatable entries are present, with 18 unused image metadata
markers intentionally left blank. The latest GIMP plug-in catalog completed 149
fuzzy or empty translations and corrected six existing pairs. GIMP Help
menus~colors~map added 138 completed source entries; 18 unused image markers
remain blank in its archive. The GIMP Help `menus~colors~components` review added
111 translations and updated 13 fuzzy entries against the latest POT; 26 unused
image metadata entries remain blank. The GIMP Help `menus~file` review filled
171 previously empty translations, cleared 29 fuzzy entries and synchronized
seven image references against the latest POT. The 58-string Disk Mounter Help review corrected 25 existing Swedish translations. The 82-string CPU Frequency Scaling Monitor Help review corrected 47 existing strings and updated the GNOME-specific frequency-governor terminology. The complete latest-POT reviews of GNOME Applets `accessx-status` and `charpick` corrected 20 and 32 existing translations respectively; the terminology list was extended for the Character Palette. The 73-string Netspeed help review corrected 25 existing strings and updated network and traffic terminology. The 32-string phodav catalog added nine translations, corrected sixteen existing strings, resolved five fuzzy entries, and translated the SIZE, CERT and KEY metavariables. The latest-POT libipuz review added eight translations and corrected six existing direction labels. The d-spy catalog added seven translations and corrected seven existing strings, including D-Bus property operations. Sushi completed the last untranslated GNOME-project string, and its preview terminology was standardized. Metronome’s rhythm instructions and tempo keywords were reviewed and the missing contributor credit was filled. The Decoder catalog translated its missing folder action and standardized the Swedish app name **Avkodare** and QR-code terminology. The oo7 catalog corrected the old/new keyring-password prompts and resolved both fuzzy translations. The libsoup catalog corrected the stale “Invalid chunk size” translation and completed two missing messages. WirePlumber’s latest POT was reviewed; audio-stream terminology was corrected and the read-only Damned Lies / merge-request requirement recorded. The one p11-kit fuzzy string was translated; Damned Lies is also read-only for that module. The GNOME Help site catalog added twelve translations and corrected sixteen existing strings, and its vocabulary was added to the GNOME TM. Deja Dup Help `main/help` was checked against the latest POT: 53 existing active translations were corrected; all 120 active messages are complete (113 obsolete entries remain in the PO file) and the upload was verified against the merged Damned Lies file. The gtk-vnc `master/po` catalog then had all three active strings reviewed and corrected; the complete upload was verified against Damned Lies. The two-string Tracker Miner chat-log catalog corrected `Chat logs miner` to **Chattloggsindexerare**; Damned Lies offers no workflow actions, so its complete review remains local and the blocker is recorded in the archive. Polkit’s fuzzy “Action ID” error was corrected and the read-only Damned Lies status documented. Showtime’s two fuzzy playback-speed entries were fixed, and Swedish wording for codecs, timestamps and volume controls was improved. The GNOME Maps `main` catalog was radgranskad against the latest POT on 2026-11-27: all 558 messages are translated and fuzzy-free; 16 new translations, 7 fuzzy entries resolved and 89 existing translations corrected. The module archive and current status report are in `translations/GNOME-granskning`. The Eartag `main` catalog was radgranskad against its latest POT: all 211 messages are complete and 48 existing translations were corrected. Audio-context entries keep `Publisher` → **Skivbolag** and `Compilation` → **Samlingsalbum** separate from the general TM meanings. The reviewed singular pairs updated the GNOME TM, including replacements for stale suggestions. GTK `main/po` was fully reviewed against its latest POT: 1 830/1 830 entries are complete, 22 translations were added and 188 existing translations corrected. The review was submitted to Damned Lies and archived with its original file, reviewed file, diff and validation report in `translations/GNOME-granskning/gtk/main/po`. The `at-spi2-core` `gnome-51/po` catalog was then checked against the same 176 source keys as its reviewed `main/po` counterpart; 46 existing translations were corrected, submitted to Damned Lies and archived with full verification. The GStreamer `main/po` catalog was reviewed against the latest 403-message POT; five translations were added, one fuzzy entry resolved and 200 existing translations corrected. The complete 403/0/0 catalog was submitted and verified against the merged Damned Lies file. Its terminology was added to the GNOME list and TM. The gedit-latex `master/po` catalog was then reviewed against its latest 211-message POT; 35 existing translations were corrected, and the complete 211/0/0 file was submitted and verified. LaTeX terminology was added to the GNOME list and the TM was refreshed from the review. Sound Juicer `master/po` was then reviewed against its latest 224-message POT; 70 existing entries were corrected, including the invariant singular/plural Swedish form `Katalognummer`. The complete 224/0/0 catalog was submitted and verified against the merged Damned Lies file. CD-ripping, GStreamer and music-metadata terminology was added to the GNOME list and TM. Evolution RSS `master/po` was then fully reviewed against the available POT: 96 existing translations were corrected and all 225 messages are complete. Damned Lies offered no workflow actions and rejected the reservation with HTTP 403, so this catalog remains locally complete and is listed as blocked from submission in the GNOME report. Evolution MAPI `master/po` was then checked against the current 226-message POT; 49 existing translations were corrected, with no untranslated or fuzzy entries. Its Swedish MAPI, GAL, Kerberos and calendar-permission terminology was added to the GNOME list and TM. The API offered no workflow actions for this catalog either, so it also remains ready locally but not submitted. Health `master/po` was then reviewed against its latest 228-message POT: 47 existing translations were corrected and the complete file was uploaded to Damned Lies with the comment “Granskad och klar”. The API reports 228/0/0, and the downloaded merged PO matches the reviewed file exactly. Pika Backup Help `main/help` was reviewed against its latest 107-message POT; 58 existing translations were corrected, the complete file was submitted with “Granskad och klar”, and the merged upload matches exactly. GNOME Commander Help `main/help` was checked against POT and latest merged action 1581909: 15 existing translations were corrected across 3,117 messages. The complete update was uploaded with “Granskad och klar” and action 1582138 verified the merged 3,117/0/0 catalog. The context-specific TM entry for `Powered` was replaced with **Med enheter**. Storage, deduplication, background portal and shell-command terminology was added to the GNOME glossary and TM. A further GIMP Help `dialogs` batch reviewed 20 Quick Mask and dialog-activation strings (14 new translations, 6 fuzzy corrections); 13 new singular pairs entered the GNOME TM, while 7 already had matching pairs. The component remains in progress with 2,030 user-facing strings and 62 unused image metadata markers left.

The refreshed TM also includes five post-upload Ptyxis corrections, including the reviewed Swedish wording **Profilen ”%s” togs bort** for `Removed profile “%s”`, the post-upload GNOME Text Editor metavariable correction, and the Rygel correction `ill-formed response string` → `felaktigt formaterad svarssträng`. The latest Rygel TM pair replaces the earlier, misleading `otydlig svarssträng` suggestion.

GNOME Firmware, Ptyxis and GNOME Text Editor were uploaded and verified on Damned Lies on 2026-11-27. Rygel's previous version was uploaded on 2026-11-23; two later quality corrections remain local and are queued for submission.

The refreshed GNOME TM validates with
136 608 entries (762 230 unique pairs across all exports).

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
|-----------|------------------:|-----|---------------|
| GNOME | 136 608 | [sv-gnome.tmx](sv-gnome.tmx) | [sv-gnome.po](sv-gnome.po) |
| KDE | 35 507 | [sv-kde.tmx](sv-kde.tmx) | [sv-kde.po](sv-kde.po) |
| Mozilla | 19 293 | [sv-mozilla.tmx](sv-mozilla.tmx) | [sv-mozilla.po](sv-mozilla.po) |
| Ubuntu | 50 525 | [sv-ubuntu.tmx](sv-ubuntu.tmx) | [sv-ubuntu.po](sv-ubuntu.po) |
| Fedora | 14 570 | [sv-fedora.tmx](sv-fedora.tmx) | [sv-fedora.po](sv-fedora.po) |
| LibreOffice | 44 495 | [sv-libreoffice.tmx](sv-libreoffice.tmx) | [sv-libreoffice.po](sv-libreoffice.po) |
| Xfce | 3 182 | [sv-xfce.tmx](sv-xfce.tmx) | [sv-xfce.po](sv-xfce.po) |
| Translation Project | 117 723 | [sv-tp.tmx](sv-tp.tmx) | [sv-tp.po](sv-tp.po) |
| Transifex | 227 083 | — | [sv-transifex.po](sv-transifex.po) |
| Crowdin | 1 918 | [sv-crowdin.tmx](sv-crowdin.tmx) | [sv-crowdin.po](sv-crowdin.po) |
| Weblate | 38 672 | [sv-weblate.tmx](sv-weblate.tmx) | [sv-weblate.po](sv-weblate.po) |
| Blender | 75 674 | [sv-blender.tmx](sv-blender.tmx) | [sv-blender.po](sv-blender.po) |
| Inkscape | 16 733 | [sv-inkscape.tmx](sv-inkscape.tmx) | [sv-inkscape.po](sv-inkscape.po) |
| Stellarium | 44 409 | [sv-stellarium.tmx](sv-stellarium.tmx) | [sv-stellarium.po](sv-stellarium.po) |
| QGIS | 39 685 | [sv-qgis.tmx](sv-qgis.tmx) | [sv-qgis.po](sv-qgis.po) |
| ScummVM | 15 156 | [sv-scummvm.tmx](sv-scummvm.tmx) | [sv-scummvm.po](sv-scummvm.po) |

The Fedora memory includes 333 unique strings added from the reviewed and submitted libvirt translation on 2026-11-26.

The former README described different collection-wide counts and a
`sv-complete.po` that is not present in this repository. Use the ecosystem
files above. [stats.json](stats.json) contains counts verified from the exports.

## Review with the companion tools

The translation memory provides suggestions, not authoritative translations.
Check every match against source text and the current interface context with
[l10n-lint](https://github.com/yeager/l10n-lint),
[svlang](https://github.com/yeager/svlang),
[hunspell-sv](https://github.com/yeager/hunspell-sv) and
[swedish-foss-terminology](https://github.com/yeager/swedish-foss-terminology).
Preserve placeholders, tags, shortcuts and line breaks exactly as in source.

Apply the Swedish style policy to suggestions: no comma directly before `och`,
Swedish quotation marks, the ellipsis character `…`, correct percent formatting,
digit grouping and an en dash in ranges. Rules are automated where safe;
meaning, register and domain terminology still require line-by-line review.
Text before `|` in a Crowdin string is context metadata and must not occur in
visible translation.

## Usage

Use a PO compendium with GNU gettext:

```bash
msgmerge --compendium sv-gnome.po --compendium sv-kde.po my-file.po my-file.pot -o filled.po
```

Look up a translation with Python. GNOME entries may have a message context, so
include it in the key when one is available:

```python
import polib

tm = {(e.msgctxt, e.msgid): e.msgstr
      for e in polib.pofile('sv-gnome.po').translated_entries()}
print(tm.get(('menu', 'Save')))
```

TMX files can be imported into CAT tools. All 15 TMX exports contain the same
source/target pairs as their corresponding PO exports. Transifex is PO-only.

The GNOME PO export preserves message contexts. The TMX exports preserve project
provenance but not message contexts or plural identities. Treat matches as
translation suggestions and review them in their destination context. Agreement
between export formats is not a linguistic quality guarantee.

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

### Home Assistant Core Lokalise provenance

The checked-in Home Assistant Core canonical TMX is intentionally validated
separately because it is a context-preserving Lokalise review ledger rather
than a PO compendium. Check its XML structure, language variants, source
provenance and review status with:

```bash
python3 scripts/validate_home_assistant_core_tmx.py \
  Home-Assistant/sv-home-assistant-core-lokalise-verified-20261120-canonical.tmx
```

Older entries can use their full source key as `tuid`; entries read back
through the Lokalise API use `lokalise:<translation-id>`. The default command
reports both styles. Once every older entry has been uniquely reconciled via
the API, use `--require-lokalise-ids` as the migration gate. Do not replace a
legacy key with an inferred ID.

## Sources and reuse

The collection draws on GNOME, KDE, Mozilla, Ubuntu, Fedora, LibreOffice,
Translation Project, Transifex, Weblate, Blender, Inkscape, Stellarium, QGIS
and ScummVM translations. Project references are included in the exports.

License: CC BY 4.0.

Related: [Swedish FOSS Terminology](https://github.com/yeager/swedish-foss-terminology), [Computer Swedens IT-ord](https://it-ord.computersweden.se/)
and [svlang](https://github.com/yeager/svlang).

## Review-derived project memories

Project-specific reviewed data and context-preserving PO/TMX exports are documented in [reviewed/README.md](reviewed/README.md). These supplement the ecosystem exports and retain original contexts, plural identities and review evidence.
