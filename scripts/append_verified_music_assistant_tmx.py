#!/usr/bin/env python3
"""Append or replace live-verified Music Assistant translations in a TMX."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET


REQUIRED = {"key", "key_id", "translation_id", "project_id", "en", "sv"}


def render(entry: dict[str, str]) -> str:
    if not REQUIRED.issubset(entry) or any(not str(entry[name]) for name in REQUIRED):
        raise ValueError("each entry requires non-empty project/key/translation IDs and en/sv")
    if not all(str(entry[name]).isdigit() for name in ("key_id", "translation_id")):
        raise ValueError(f"{entry['key']}: Lokalise IDs must be decimal")
    props = (("source", entry["key"]), ("lokalise-key-id", str(entry["key_id"])),
             ("lokalise-project-id", entry["project_id"]),
             ("verification-method", entry.get("verification_method", "Lokalise API live readback")),
             ("status", "saved-and-read-back"), ("verified-date", entry.get("verified_date", "")))
    meta = "".join(f'<prop type="{name}">{escape(value)}</prop>' for name, value in props)
    return (f'<tu tuid="lokalise:{entry["translation_id"]}">{meta}'
            f'<tuv xml:lang="en"><seg>{escape(entry["en"])}</seg></tuv>'
            f'<tuv xml:lang="sv"><seg>{escape(entry["sv"])}</seg></tuv></tu>')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("canonical", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = ET.parse(args.canonical).getroot(); body = root.find("body")
    if root.tag != "tmx" or body is None:
        raise ValueError("expected TMX with body")
    by_id = {unit.get("tuid"): unit for unit in body.findall("tu")}
    by_key = {unit.findtext("prop[@type='source']"): unit for unit in body.findall("tu")}
    entries = json.loads(args.manifest.read_text(encoding="utf-8"))
    added, replaced = [], []
    for entry in entries:
        unit = render(entry); tuid = f"lokalise:{entry['translation_id']}"; old = by_id.get(tuid) or by_key.get(entry["key"])
        if old is None:
            added.append(unit)
        else:
            replaced.append((old.get("tuid"), unit))
    if args.write:
        data = args.canonical.read_bytes()
        for old_id, unit in replaced:
            data, n = re.subn(rb'<tu tuid="' + re.escape(old_id.encode()) + rb'">.*?</tu>', unit.encode(), data, count=1, flags=re.DOTALL)
            if n != 1: raise ValueError(f"could not replace {old_id}")
        index = data.rfind(b"</body>")
        if index < 0: raise ValueError("missing closing TMX body")
        if added: data = data[:index] + ("\n" + "\n".join(added) + "\n").encode() + data[index:]
        args.canonical.write_bytes(data)
    print(f"{'written' if args.write else 'would write'}: added={len(added)}, replaced={len(replaced)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
