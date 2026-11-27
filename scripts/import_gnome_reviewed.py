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
DEFAULT_WORKSPACE = ROOT.parents[0]
ARCHIVE = Path(os.environ.get(
    "GNOME_REVIEW_ARCHIVE", DEFAULT_WORKSPACE / "translations" / "GNOME-granskning"
)).resolve()
WORKSPACE = ARCHIVE.parent.parent
INDEX = ARCHIVE / "index.json"
TM_PO = ROOT / "sv-gnome.po"
TM_TMX = ROOT / "sv-gnome.tmx"
MANIFEST = ROOT / "gnome-reviewed-manifest.json"
CONTEXT_OVERRIDES = ROOT / "gnome-context-overrides.json"


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
        ))
        if entry.msgctxt:
            lines.append(f'      <prop type="context">{escape(entry.msgctxt)}</prop>')
        lines.extend((
            f'      <tuv xml:lang="en"><seg>{escape(entry.msgid)}</seg></tuv>',
            f'      <tuv xml:lang="sv"><seg>{escape(entry.msgstr)}</seg></tuv>', '    </tu>',
        ))
    lines.extend(('  </body>', '</tmx>', ''))
    TM_TMX.write_text("\n".join(lines), encoding="utf-8")


def progress_sources() -> list[dict[str, object]]:
    sources = []
    directory = ROOT / "reviews" / "gnome-progress"
    for audit_path in sorted(directory.glob("*.json")):
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        source = {
            "module": audit["module"],
            "branch": audit["branch"],
            "component": audit["component"],
            "path": str(audit_path.relative_to(ROOT)),
            "sha256": digest(audit_path),
            "reviewed_pairs": audit["reviewed_entries_included_in_tm"],
            "new_translations": audit["new_translations_in_batch"],
            "remaining_untranslated": audit["remaining_untranslated_in_work_catalog"],
            "pot_sha256": audit["latest_pot_sha256"],
        }
        batch_path = audit.get("reviewed_batch_file")
        if batch_path:
            batch_file = ROOT / batch_path
            source["reviewed_batch_file"] = str(batch_file.relative_to(ROOT))
            source["reviewed_batch_sha256"] = digest(batch_file)
        sources.append(source)
    return sources


def progress_reviews() -> list[tuple[dict[str, object], Path, polib.POFile]]:
    """Read individually reviewed in-progress batches for inclusion in the TM."""
    reviews = []
    directory = ROOT / "reviews" / "gnome-progress"
    for audit_path in sorted(directory.glob("*.json")):
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        batch_name = audit.get("reviewed_batch_file")
        if not batch_name:
            continue
        batch_path = ROOT / batch_name
        batch = polib.pofile(str(batch_path), encoding="utf-8")
        reviews.append((audit, batch_path, batch))
    return reviews


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
    all_reviews = json.loads(INDEX.read_text(encoding="utf-8"))["reviews"]
    # A complete local review remains valid TM material even if the upstream
    # workflow is externally blocked (for example, by a reservation or team
    # membership). Submission status and review eligibility are independent.
    eligible_statuses = {"Klar lokalt", "Klar och inskickad", "Klar utan ändringar",
                         "Externt blockerad"}
    eligible_branches = {"main", "master", "gnome-51"}
    review_index = [review for review in all_reviews
                    if review.get("status") in eligible_statuses
                    and review.get("branch") in eligible_branches]
    context_overrides = {}
    if CONTEXT_OVERRIDES.exists():
        overrides = json.loads(CONTEXT_OVERRIDES.read_text(encoding="utf-8"))
        context_overrides = {
            (item["module"], item["branch"], item["msgid"]): item["msgctxt"]
            for item in overrides
        }
    for review in review_index:
        if not review.get("reviewed"):
            raise ValueError(f"completed review has no reviewed catalog: {review.get('module')}/{review.get('branch')}")
    baseline = git_baseline()
    tm = polib.pofile(baseline, encoding="utf-8")
    existing = {(entry.msgctxt, entry.msgid): entry for entry in tm if not entry.msgid_plural}
    appended: list[polib.POEntry] = []
    updated_entries: dict[int, polib.POEntry] = {}
    added = updated = skipped_plural = 0
    progress_added = progress_updated = 0
    progress_results = []
    sources: list[dict[str, object]] = []
    for review in review_index:
        path = ARCHIVE / review["path"] / review["reviewed"]
        po = polib.pofile(str(path), encoding="utf-8")
        singular = plural = 0
        for entry in po:
            if entry.obsolete or entry.fuzzy or not entry.msgid or entry.msgid.startswith("@@image:"):
                continue
            if entry.msgid_plural:
                plural += 1
                skipped_plural += 1
                continue
            if not entry.msgstr:
                continue
            singular += 1
            msgctxt = context_overrides.get(
                (review["module"], review["branch"], entry.msgid), entry.msgctxt
            )
            key = (msgctxt, entry.msgid)
            target = existing.get(key)
            if target is None:
                target = polib.POEntry(msgid=entry.msgid, msgstr=entry.msgstr, msgctxt=msgctxt,
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
                if target.linenum is not None:
                    updated_entries[target.linenum] = target
                updated += 1
        sources.append({"module": review["module"], "branch": review["branch"], "kind": review["kind"],
                        "path": str(path.relative_to(WORKSPACE)), "sha256": digest(path),
                        "singular_pairs": singular, "plural_pairs_not_in_compendium": plural})
    for audit, batch_path, batch in progress_reviews():
        origin = f"from gnome:reviewed/{audit['module']}/{audit['branch']}/{audit['component']}"
        batch_added = batch_updated = batch_matched = 0
        for entry in batch:
            if entry.obsolete or entry.fuzzy or not entry.msgid or entry.msgid_plural or not entry.msgstr or entry.msgid.startswith("@@image:"):
                continue
            key = (entry.msgctxt, entry.msgid)
            target = existing.get(key)
            if target is None:
                target = polib.POEntry(msgid=entry.msgid, msgstr=entry.msgstr, msgctxt=entry.msgctxt,
                                       comment=origin)
                tm.append(target)
                existing[key] = target
                appended.append(target)
                added += 1
                progress_added += 1
                batch_added += 1
            elif target.msgstr != entry.msgstr:
                target.msgstr = entry.msgstr
                if origin not in target.comment.splitlines():
                    target.comment = f"{target.comment}\n{origin}".strip()
                if target.linenum is not None:
                    updated_entries[target.linenum] = target
                updated += 1
                progress_updated += 1
                batch_updated += 1
            else:
                batch_matched += 1
        progress_results.append({
            "module": audit["module"], "branch": audit["branch"],
            "component": audit["component"], "batch": str(batch_path.relative_to(ROOT)),
            "sha256": digest(batch_path), "entries_added": batch_added,
            "entries_updated": batch_updated, "entries_already_matching": batch_matched,
        })
    if added or updated:
        lines = baseline.splitlines(keepends=True)
        # Replace changed baseline entries in reverse order so original line
        # locations remain valid, while preserving the rest of the file.
        for entry in sorted(updated_entries.values(), key=lambda item: item.linenum, reverse=True):
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
        "selection": {
            "completed_current_branches": len(review_index),
            "all_index_records": len(all_reviews),
            "excluded_status_or_branch": len(all_reviews) - len(review_index),
        },
        "incremental_sources": progress_sources(),
        "progress_import_results": progress_results,
        "added_singular_pairs": added, "updated_reviewed_pairs": updated,
        "plural_pairs_not_in_context_free_compendium": skipped_plural,
        "note": "Plural pairs remain in their reviewed PO archives. Context overrides keep ambiguous project-specific terms separate in sv-gnome.po; TMX stores project provenance and gettext context metadata.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added={added} updated={updated} plural_skipped={skipped_plural} sources={len(sources)} "
          f"progress_added={progress_added} progress_updated={progress_updated}")


if __name__ == "__main__":
    main()
