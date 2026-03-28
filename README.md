# 🇸🇪 Swedish Translation Memory

The largest open collection of Swedish software translations — **777 206 unique en→sv translation pairs** from **3 299 open source projects**.

## 📊 Contents

### Per-ecosystem TM files

| Ecosystem | Unique pairs | TMX | PO (compendium) |
|-----------|-------------|-----|-----------------|
| **GNOME** | 86 737 | sv-gnome.tmx | sv-gnome.po |
| **KDE** | 57 839 | sv-kde.tmx | sv-kde.po |
| **Mozilla** | 19 832 | sv-mozilla.tmx | sv-mozilla.po |
| **Ubuntu** | 42 613 | sv-ubuntu.tmx | sv-ubuntu.po |
| **Fedora** | 11 856 | sv-fedora.tmx | sv-fedora.po |
| **LibreOffice** | 41 723 | sv-libreoffice.tmx | sv-libreoffice.po |
| **XFCE** | 3 125 | sv-xfce.tmx | sv-xfce.po |
| **Translation Project** | 99 340 | sv-tp.tmx | sv-tp.po |
| **Transifex** | 249 990 | — | sv-transifex.po |
| **Weblate** | 23 760 | sv-weblate.tmx | sv-weblate.po |
| **Blender** | 128 053 | sv-blender.tmx | sv-blender.po |
| **Inkscape** | 18 127 | sv-inkscape.tmx | sv-inkscape.po |
| **Stellarium** | 45 597 | sv-stellarium.tmx | sv-stellarium.po |
| **QGIS** | 35 903 | sv-qgis.tmx | sv-qgis.po |
| **ScummVM** | 15 156 | sv-scummvm.tmx | sv-scummvm.po |

### Complete TM

| File | Unique pairs | Size |
|------|-------------|------|
| **sv-complete.po** | 777 206 | 128 MB |

## 📖 Formats

**TMX** — Standard for all CAT tools (OmegaT, Trados, memoQ, Memsource, Lokalize, Virtaal, Poedit).

**PO** — Use as compendium with msgmerge:
```bash
msgmerge --compendium sv-gnome.po untranslated.po template.pot -o filled.po
```

## 🔧 Usage

```bash
# Fill translations from GNOME + KDE TM
msgmerge --compendium sv-gnome.po --compendium sv-kde.po my-file.po my-file.pot -o filled.po

# Python lookup
python3 -c "
import polib
tm = {e.msgid: e.msgstr for e in polib.pofile('sv-gnome.po').translated_entries()}
print(tm.get('Save'))  # → Spara
"
```

## 📋 Sources

- **GNOME** l10n (gitlab.gnome.org), **KDE** l10n (invent.kde.org), **Mozilla** (Pontoon)
- **Ubuntu** (Launchpad), **Fedora** (Weblate), **LibreOffice** l10n
- **Translation Project** (translationproject.org) — GNU/FSF projects
- **Transifex**, **Weblate** (hosted.weblate.org)
- **Blender**, **Inkscape**, **QGIS**, **Stellarium**, **ScummVM**, and 3 280+ more

## 🏷️ Quality

- **Gold**: GNOME, KDE, Mozilla official teams (human-reviewed)
- **Silver**: Ubuntu, Fedora, LibreOffice, Translation Project
- **Mixed**: Transifex, Weblate (varies by project)

See also [swedish-foss-terminology](https://github.com/yeager/swedish-foss-terminology) (326K curated terms).

## 📄 License

CC BY 4.0

## 🔗 Related

- [swedish-foss-terminology](https://github.com/yeager/swedish-foss-terminology) — Curated terminology bank
- [TR Quality Dashboard](https://danielnylander.se/sv-quality/) — Live quality metrics
