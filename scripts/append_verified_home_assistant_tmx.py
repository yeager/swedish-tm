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
    optional = {"verification_method", "verified_date"}
    if not required.issubset(entry) or not set(entry).issubset(required | optional) or any(not entry[name] for name in required):
        raise ValueError("each entry must have non-empty key_id, key, translation_id, en and sv")
    if not entry["translation_id"].isdigit() or not entry["key_id"].isdigit():
        raise ValueError(f"{entry['key']}: IDs must be decimal")
    properties = (
        ("source", entry["key"]),
        ("lokalise-key-id", entry["key_id"]),
        ("lokalise-project-id", "130246255a974bd3b5e8a1.51616605"),
        ("verification-method", entry.get("verification_method", "Lokalise UI readback")),
        ("status", "saved-and-read-back"),
        ("verified-date", entry.get("verified_date", "2026-11-20")),
    )
    props = "".join(f'<prop type="{name}">{escape(value)}</prop>' for name, value in properties)
    return (
        f'<tu tuid="lokalise:{entry["translation_id"]}">{props}'
        f'<tuv xml:lang="en"><seg>{escape(entry["en"])}</seg></tuv>'
        f'<tuv xml:lang="sv"><seg>{escape(entry["sv"])}</seg></tuv></tu>'
    )


def append(canonical: Path, manifest: Path, *, write: bool) -> int:
    root = ET.parse(canonical).getroot()
    body = root.find("body")
    if root.tag != "tmx" or body is None:
        raise ValueError("expected TMX with body")
    existing_ids = {item.get("tuid"): item for item in body.findall("tu")}
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
        if by_id is not None or by_key is not None:
            if by_id is None or by_key is None or by_id is not by_key:
                raise ValueError(f"conflicting canonical entry: {entry['key']}")
            replacements.append((tuid, rendered_unit))
        else:
            rendered.append(rendered_unit)
    if write:
        data = canonical.read_bytes()
        for tuid, rendered_unit in replacements:
            pattern = rb'<tu tuid="' + re.escape(tuid.encode()) + rb'">.*?</tu>'
            data, count = re.subn(pattern, rendered_unit.encode(), data, count=1, flags=re.DOTALL)
            if count != 1:
                raise ValueError(f"could not replace canonical entry: {tuid}")
        marker = b"</body>"
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
