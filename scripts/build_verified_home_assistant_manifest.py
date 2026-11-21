#!/usr/bin/env python3
"""Build a reviewable verified-translation manifest from a Lokalise PO export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def records(po: Path, context_prefix: str, source: str, target: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    key_id = translation_id = context = msgid = None
    for line in po.read_text(encoding="utf-8").splitlines():
        if line.startswith("#. Lokalise key "):
            fields = line.split()
            key_id = fields[3].rstrip(";")
            translation_id = fields[9].rstrip(";")
            context = msgid = None
        elif line.startswith("msgctxt "):
            # The PO context is itself a JSON-encoded Lokalise context array.
            parts = json.loads(json.loads(line[8:]))
            context = parts[2]
        elif line.startswith("msgid "):
            msgid = json.loads(line[6:])
        elif line.startswith("msgstr ") and context and msgid == source:
            if context.startswith(context_prefix):
                assert key_id and translation_id
                result.append(
                    {
                        "key": context,
                        "key_id": key_id,
                        "translation_id": translation_id,
                        "en": source,
                        "sv": target,
                        "verification_method": "Lokalise API readback",
                        "verified_date": "2026-11-21",
                    }
                )
            msgid = None
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("po", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    entries = records(args.po, args.prefix, args.source, args.target)
    if not entries:
        raise SystemExit("no matching Lokalise records")
    args.output.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {len(entries)} entries")


if __name__ == "__main__":
    main()
