#!/usr/bin/env python3
"""Merge verified singular pairs from local GNOME review archives into the GNOME TM."""

from __future__ import annotations

import hashlib
import json
import subprocess
import argparse
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import polib


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
ARCHIVE = WORKSPACE / "translations" / "GNOME-granskning"
TRANSLATIONS_REPO = WORKSPACE / "translations"
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


def complete_po_header(text: str) -> str:
    """Keep the generated compendium's gettext header complete on every import."""
    lines = text.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.strip() == 'msgid ""')
    end = start + 1
    while end < len(lines) and lines[end].strip():
        end += 1
    fields = [
        '"Project-Id-Version: GNOME Swedish translation\\n"\n',
        '"PO-Revision-Date: ' + datetime.now().astimezone().strftime("%Y-%m-%d %H:%M%z") + '\\n"\n',
        '"Last-Translator: Daniel Nylander <gnome@danielnylander.se>\\n"\n',
        '"Language-Team: Swedish\\n"\n',
        '"Language: sv\\n"\n',
        '"MIME-Version: 1.0\\n"\n',
        '"Content-Type: text/plain; charset=UTF-8\\n"\n',
        '"Content-Transfer-Encoding: 8bit\\n"\n',
        '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n',
    ]
    lines[start:end] = [lines[start], lines[start + 1], *fields]
    return "".join(lines)


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
    baseline = complete_po_header(git_baseline())
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".po", prefix=".sv-gnome-baseline-",
        dir=ROOT, delete=False,
    ) as baseline_file:
        baseline_file.write(baseline)
        baseline_path = Path(baseline_file.name)
    try:
        tm = polib.pofile(str(baseline_path), encoding="utf-8")
    finally:
        baseline_path.unlink(missing_ok=True)
    existing = {(entry.msgctxt, entry.msgid): entry for entry in tm if not entry.msgid_plural}
    appended: list[polib.POEntry] = []
    added = overwritten = skipped_plural = conflicts = 0
    overwritten_entries: dict[tuple[str | None, str], polib.POEntry] = {}
    sources: list[dict[str, object]] = []
    for review in review_index:
        # Blocked inventory entries deliberately have no archived PO pair.
        # They belong in the review report but cannot contribute to the TM.
        if "path" not in review or "reviewed" not in review:
            continue
        path = ARCHIVE / review["path"] / review["reviewed"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing reviewed GNOME catalog: {path}")
        po = polib.pofile(str(path), encoding="utf-8")
        relative_archive_path = (Path("GNOME-granskning") / review["path"] / review["reviewed"]).as_posix()
        try:
            previous_text = subprocess.check_output(
                ["git", "show", f"HEAD:{relative_archive_path}"],
                cwd=TRANSLATIONS_REPO, text=True, stderr=subprocess.DEVNULL,
            )
            previous_po = polib.pofile(previous_text, encoding="utf-8")
            previous_pairs = {
                (entry.msgctxt, entry.msgid): entry
                for entry in previous_po if not entry.obsolete and not entry.msgid_plural
            }
        except subprocess.CalledProcessError:
            previous_pairs = {}
        singular = plural = 0
        for entry in po:
            if entry.obsolete or entry.fuzzy or not entry.msgid:
                continue
            # GNOME game catalogs may store non-prose payloads (keyboard maps,
            # letter sets and whole word lists) under source keys like
            # ``data-dictionary``. Keep these in the archived PO, but do not
            # add them to the reusable, context-free translation memory.
            if entry.msgid.startswith("data-"):
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
                previous = previous_pairs.get(key)
                if previous and previous.msgstr == target.msgstr and previous.msgstr != entry.msgstr:
                    # A reviewed correction supersedes the exact old pair stored
                    # in the context-free TM. Unrelated context conflicts remain
                    # untouched.
                    target.msgstr = entry.msgstr
                    provenance = f"from gnome:reviewed/{review['module']}/{review['branch']}"
                    comments = target.comment.splitlines() if target.comment else []
                    old_provenance = next((i for i, item in enumerate(comments) if item.startswith("from gnome:")), None)
                    if old_provenance is None:
                        comments.insert(0, provenance)
                    else:
                        comments[old_provenance] = provenance
                    target.comment = "\n".join(comments)
                    overwritten_entries[key] = target
                    overwritten += 1
                else:
                    conflicts += 1
        sources.append({"module": review["module"], "branch": review["branch"], "kind": review["kind"],
                        "path": str(path.relative_to(WORKSPACE)), "sha256": digest(path),
                        "singular_pairs": singular, "plural_pairs_not_in_compendium": plural})
    if added or overwritten:
        lines = baseline.splitlines(keepends=True)
        for entry in sorted(overwritten_entries.values(), key=lambda item: item.linenum, reverse=True):
            start, end = entry_bounds(lines, entry.linenum)
            lines[start:end] = str(entry).rstrip("\n").splitlines(keepends=True)
            if end == len(lines) or (end < len(lines) and lines[end].strip()):
                lines.insert(start + len(str(entry).splitlines()), "\n")
        merged = "".join(lines).replace(f"# Entries: {len(existing) - added}\n", f"# Entries: {len(existing)}\n", 1)
        if appended:
            merged += "\n" + "\n\n".join(str(entry).rstrip("\n") for entry in appended) + "\n"
        TM_PO.write_text(merged, encoding="utf-8")
        tm = polib.pofile(str(TM_PO), encoding="utf-8")
        write_tmx(tm)
    elif args.rebuild_tmx:
        write_tmx(polib.pofile(str(TM_PO), encoding="utf-8"))
    MANIFEST.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(), "sources": sources,
        "added_singular_pairs": added, "overwritten_reviewed_pairs": overwritten,
        "context_conflicts_not_overwritten": conflicts,
        "plural_pairs_not_in_context_free_compendium": skipped_plural,
        "note": "Plural pairs remain in their reviewed PO archives; sv-gnome.po is a context-free singular compendium.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added={added} overwritten={overwritten} conflicts={conflicts} plural_skipped={skipped_plural} sources={len(sources)}")


if __name__ == "__main__":
    main()
