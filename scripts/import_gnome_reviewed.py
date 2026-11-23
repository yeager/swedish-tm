#!/usr/bin/env python3
"""Merge verified singular pairs from local GNOME review archives into the GNOME TM."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import polib


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE = ROOT.parents[1]
ARCHIVE = Path(os.environ.get(
    "GNOME_REVIEW_ARCHIVE", DEFAULT_WORKSPACE / "translations" / "GNOME-granskning"
)).resolve()
WORKSPACE = ARCHIVE.parent.parent
INDEX = ARCHIVE / "index.json"
TM_PO = ROOT / "sv-gnome.po"
TM_TMX = ROOT / "sv-gnome.tmx"
MANIFEST = ROOT / "gnome-reviewed-manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_name(entry: polib.POEntry) -> str:
    for comment in entry.comment.splitlines():
        if comment.startswith("from gnome:"):
            return comment.removeprefix("from ")
    return "gnome:reviewed"


def write_tmx(po: polib.POFile) -> None:
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>', '<tmx version="1.4">',
        f'  <header creationtool="GNOME local review" creationtoolversion="1.0" datatype="PlainText" segtype="sentence" adminlang="en" srclang="en" o-tmf="TMX" creationdate="{now}">',
        '    <note>Swedish GNOME Translation Memory</note>', '  </header>', '  <body>',
    ]
    for entry in po:
        if not entry.msgid or not entry.msgstr or entry.obsolete or entry.fuzzy or entry.msgid_plural:
            continue
        lines.extend((
            '    <tu>', f'      <prop type="project">{escape(project_name(entry))}</prop>',
            f'      <tuv xml:lang="en"><seg>{escape(entry.msgid)}</seg></tuv>',
            f'      <tuv xml:lang="sv"><seg>{escape(entry.msgstr)}</seg></tuv>', '    </tu>',
        ))
    lines.extend(('  </body>', '</tmx>', ''))
    TM_TMX.write_text("\n".join(lines), encoding="utf-8")


def git_baseline() -> str:
    return subprocess.check_output(["git", "show", "HEAD:sv-gnome.po"], cwd=ROOT, text=True)


def entry_bounds(lines: list[str], line_number: int) -> tuple[int, int]:
    """Find the complete blank-line separated PO entry around a polib line."""
    start = line_number - 1
    while start and lines[start - 1].strip():
        start -= 1
    end = line_number - 1
    while end < len(lines) and lines[end].strip():
        end += 1
    return start, end


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild-tmx", action="store_true",
                        help="Regenerate the TMX from the checked-in PO even if no pairs are added.")
    parser.add_argument("--rebuild-tmx-only", action="store_true",
                        help="Regenerate only the TMX; do not alter the review manifest.")
    args = parser.parse_args()
    if args.rebuild_tmx_only:
        write_tmx(polib.pofile(str(TM_PO), encoding="utf-8"))
        return
    review_index = json.loads(INDEX.read_text(encoding="utf-8"))["reviews"]
    baseline = git_baseline()
    tm = polib.pofile(baseline, encoding="utf-8")
    existing = {(entry.msgctxt, entry.msgid): entry for entry in tm if not entry.msgid_plural}
    appended: list[polib.POEntry] = []
    updated_entries: list[polib.POEntry] = []
    added = updated = skipped_plural = 0
    sources: list[dict[str, object]] = []
    for review in review_index:
        path = ARCHIVE / review["path"] / review["reviewed"]
        po = polib.pofile(str(path), encoding="utf-8")
        singular = plural = 0
        for entry in po:
            if entry.obsolete or entry.fuzzy or not entry.msgid:
                continue
            if entry.msgid_plural:
                plural += 1
                skipped_plural += 1
                continue
            if not entry.msgstr:
                continue
            singular += 1
            key = (entry.msgctxt, entry.msgid)
            target = existing.get(key)
            if target is None:
                target = polib.POEntry(msgid=entry.msgid, msgstr=entry.msgstr, msgctxt=entry.msgctxt,
                                       comment=f"from gnome:reviewed/{review['module']}/{review['branch']}")
                tm.append(target)
                existing[key] = target
                appended.append(target)
                added += 1
            elif target.msgstr != entry.msgstr:
                # A completed line review is authoritative. Keep an audit
                # trail when replacing an older context-free TM suggestion.
                target.msgstr = entry.msgstr
                source = f"from gnome:reviewed/{review['module']}/{review['branch']}"
                if source not in target.comment.splitlines():
                    target.comment = f"{target.comment}\n{source}".strip()
                updated_entries.append(target)
                updated += 1
        sources.append({"module": review["module"], "branch": review["branch"], "kind": review["kind"],
                        "path": str(path.relative_to(WORKSPACE)), "sha256": digest(path),
                        "singular_pairs": singular, "plural_pairs_not_in_compendium": plural})
    if added or updated:
        lines = baseline.splitlines(keepends=True)
        # Replace changed baseline entries in reverse order so original line
        # locations remain valid, while preserving the rest of the file.
        for entry in sorted(updated_entries, key=lambda item: item.linenum, reverse=True):
            start, end = entry_bounds(lines, entry.linenum)
            lines[start:end] = [str(entry).rstrip("\n") + "\n"]
        merged = "".join(lines)
        if added:
            merged = merged.replace(f"# Entries: {len(existing) - added}\n", f"# Entries: {len(existing)}\n", 1)
        if appended:
            merged += "\n" + "\n\n".join(str(entry).rstrip("\n") for entry in appended) + "\n"
        TM_PO.write_text(merged, encoding="utf-8")
        tm = polib.pofile(str(TM_PO), encoding="utf-8")
        write_tmx(tm)
    elif args.rebuild_tmx:
        write_tmx(polib.pofile(str(TM_PO), encoding="utf-8"))
    MANIFEST.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(), "sources": sources,
        "added_singular_pairs": added, "updated_reviewed_pairs": updated,
        "plural_pairs_not_in_context_free_compendium": skipped_plural,
        "note": "Plural pairs remain in their reviewed PO archives; sv-gnome.po is a context-free singular compendium.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added={added} updated={updated} plural_skipped={skipped_plural} sources={len(sources)}")


if __name__ == "__main__":
    main()
