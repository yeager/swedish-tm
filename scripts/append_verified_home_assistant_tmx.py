#!/usr/bin/env python3
"""Append read-back Home Assistant Core translations to the canonical TMX.

The input is a checked-in JSON list so that each memory addition is reviewable
without reproducing a Lokalise session. It appends new entries and replaces an
existing entry only when both its key and Lokalise translation ID match. It
does not contact Lokalise.
"""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET


def unit(entry: dict[str, str]) -> str:
    required = {"key", "key_id", "translation_id", "en", "sv"}
    optional = {
        "verification_method",
        "verified_date",
        "status",
        "source_revision",
        "previous_review",
    }
    if not required.issubset(entry) or not set(entry).issubset(required | optional) or any(not entry[name] for name in required):
        raise ValueError("each entry must have non-empty key_id, key, translation_id, en and sv")
    # JSON producers may emit these numeric Lokalise identifiers as JSON
    # numbers; normalize before validating instead of rejecting valid input.
    translation_id = str(entry["translation_id"])
    key_id = str(entry["key_id"])
    if not translation_id.isdigit() or not key_id.isdigit():
        raise ValueError(f"{entry['key']}: IDs must be decimal")
    properties = [
        ("source", entry["key"]),
        ("lokalise-key-id", key_id),
        ("lokalise-project-id", "130246255a974bd3b5e8a1.51616605"),
        ("verification-method", entry.get("verification_method", "Lokalise UI readback")),
        ("status", entry.get("status", "saved-and-read-back")),
        ("verified-date", entry.get("verified_date", "2026-11-20")),
        ("source-revision", entry.get("source_revision", "")),
    ]
    if entry.get("previous_review"):
        properties.append(("review-history", entry["previous_review"]))
    props = "".join(f'<prop type="{name}">{escape(value)}</prop>' for name, value in properties)
    return (
        f'<tu tuid="lokalise:{translation_id}">{props}'
        f'<tuv xml:lang="en"><seg>{escape(entry["en"])}</seg></tuv>'
        f'<tuv xml:lang="sv"><seg>{escape(entry["sv"])}</seg></tuv></tu>'
    )


def replacement_with_existing_layout(rendered_unit: bytes, original_unit: bytes) -> bytes:
    """Keep an existing TMX unit's multiline layout when replacing its data."""
    match = re.search(rb"\n([ \t]+)<prop\b", original_unit)
    if match is None:
        return rendered_unit
    child_indent = match.group(1)
    close_match = re.search(rb"\n([ \t]+)</tu>$", original_unit)
    close_indent = close_match.group(1) if close_match else b""
    segment_match = re.search(rb"\n([ \t]+)<seg\b", original_unit)
    segment_indent = segment_match.group(1) if segment_match else child_indent + b"  "

    value = rendered_unit
    value = value.replace(b"><prop", b">\n" + child_indent + b"<prop", 1)
    value = value.replace(b"</prop><prop", b"</prop>\n" + child_indent + b"<prop")
    value = value.replace(b"</prop><tuv", b"</prop>\n" + child_indent + b"<tuv")
    value = re.sub(
        rb'(<tuv xml:lang="[^"]+">)<seg>',
        lambda m: m.group(1) + b"\n" + segment_indent + b"<seg>",
        value,
    )
    value = value.replace(b"</seg></tuv>", b"</seg>\n" + child_indent + b"</tuv>")
    value = value.replace(b"</tuv><tuv", b"</tuv>\n" + child_indent + b"<tuv")
    value = value.replace(b"</tuv></tu>", b"</tuv>\n" + close_indent + b"</tu>")
    return value


def append(canonical: Path, manifest: Path, *, write: bool) -> int:
    root = ET.parse(canonical).getroot()
    body = root.find("body")
    if root.tag != "tmx" or body is None:
        raise ValueError("expected TMX with body")
    existing_ids = {}
    for item in body.findall("tu"):
        tuid = item.get("tuid")
        if tuid in existing_ids:
            # Preserve the first record position while replacing its content
            # with the most recently reviewed unit.
            index = list(body).index(existing_ids[tuid])
            body.remove(existing_ids[tuid])
            body.insert(index, item)
        existing_ids[tuid] = item
    existing_keys = {item.findtext("prop[@type='source']"): item for item in body.findall("tu")}
    entries = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("manifest must contain a JSON list")
    rendered = []
    replacements = []
    for entry in entries:
        rendered_unit = unit(entry)
        tuid = f"lokalise:{entry['translation_id']}"
        by_id = existing_ids.get(tuid)
        by_key = existing_keys.get(entry["key"])
        legacy_tuid = f"lokalise:{entry['key_id']}"
        by_legacy_id = existing_ids.get(legacy_tuid)
        if by_id is not None or by_key is not None or by_legacy_id is not None:
            # Lokalise can retain a translation ID while moving it to a new
            # key/source during upstream catalogue migrations.  The manifest
            # has just been verified against the live key, so replace this
            # single translation-ID entry rather than retaining stale source
            # metadata.  A matching key with a *different* translation ID is
            # still a conflict and must never be overwritten implicitly.
            if by_id is not None and (by_key is None or by_key is by_id):
                replacements.append((tuid, rendered_unit))
            elif by_key is not None and by_key is by_legacy_id:
                # Older UI-review records used the Lokalise key ID as tuid.
                # A live manifest supplies the actual translation ID.
                replacements.append((legacy_tuid, rendered_unit))
            else:
                raise ValueError(f"conflicting canonical entry: {entry['key']}")
        else:
            rendered.append(rendered_unit)
    if write:
        data = canonical.read_bytes()
        for tuid, rendered_unit in replacements:
            pattern = rb'<tu tuid="' + re.escape(tuid.encode()) + rb'">.*?</tu>'
            match = re.search(pattern, data, flags=re.DOTALL)
            if match is None:
                count = 0
            else:
                original_unit = match.group(0)
                formatted_unit = replacement_with_existing_layout(rendered_unit.encode(), original_unit)
                data, count = re.subn(pattern, formatted_unit, data, count=1, flags=re.DOTALL)
            if count != 1:
                raise ValueError(f"could not replace canonical entry: {tuid}")
        marker = b"</body>"
        index = data.rfind(marker)
        if index < 0:
            raise ValueError("missing closing TMX body")
        # Normalize duplicate translation IDs discovered in historical data.
        dedup = {}
        for item in body.findall("tu"):
            dedup[item.get("tuid")] = item
        if len(dedup) != len(body.findall("tu")):
            seen = set()
            for item in list(body.findall("tu")):
                tuid = item.get("tuid")
                if tuid in seen:
                    body.remove(item)
                else:
                    seen.add(tuid)
            data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            index = data.rfind(marker)
            if index < 0:
                raise ValueError("missing closing TMX body")
        if rendered:
            data = data[:index] + ("\n" + "\n".join(rendered) + "\n").encode() + data[index:]
        canonical.write_bytes(data)
    return len(rendered) + len(replacements)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("canonical", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    print(f"{'appended' if args.write else 'would append'}: {append(args.canonical, args.manifest, write=args.write)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
