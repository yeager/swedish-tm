#!/usr/bin/env python3
"""Refresh only matching Evolution-owned TM entries without rewriting the PO."""
from pathlib import Path
import os
import sys
import polib

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[2]
MODULE = os.environ.get("GNOME_TM_MODULE", "evolution")
BRANCH = os.environ.get("GNOME_TM_BRANCH", "master")
STEM = os.environ.get("GNOME_TM_STEM", f"{MODULE}.{BRANCH}.sv")
ARCHIVE = WORKSPACE / "translations/GNOME-granskning" / MODULE / BRANCH / "po"
sys.path.insert(0, str(ROOT / "scripts"))
from import_gnome_reviewed import write_tmx  # noqa: E402

before = polib.pofile(str(ARCHIVE / f"{STEM}.original.po"), encoding="utf-8")
after = polib.pofile(str(ARCHIVE / f"{STEM}.reviewed.po"), encoding="utf-8")
old = {(e.msgctxt, e.msgid): e for e in before if not e.obsolete}
new = {(e.msgctxt, e.msgid): e for e in after if not e.obsolete}
tm_path = ROOT / "sv-gnome.po"
tm = polib.pofile(str(tm_path), encoding="utf-8")
replacements = []
for entry in tm:
    source = old.get((entry.msgctxt, entry.msgid))
    reviewed = new.get((entry.msgctxt, entry.msgid))
    if not source or not reviewed or source.msgstr == reviewed.msgstr:
        continue
    if entry.comment == f"from gnome:{MODULE}" and entry.msgstr == source.msgstr:
        replacement = polib.POEntry(**entry.__dict__)
        replacement.msgstr = reviewed.msgstr
        replacements.append((entry.linenum, str(replacement).rstrip("\n")))
lines = tm_path.read_text(encoding="utf-8").splitlines()
for line_number, replacement in sorted(replacements, reverse=True):
    start = line_number - 1
    while start and lines[start - 1].strip():
        start -= 1
    end = line_number - 1
    while end < len(lines) and lines[end].strip():
        end += 1
    lines[start:end] = replacement.splitlines()
tm_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
write_tmx(polib.pofile(str(tm_path), encoding="utf-8"))
print(f"updated={len(replacements)}")
