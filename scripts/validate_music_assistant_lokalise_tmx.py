#!/usr/bin/env python3
"""Validate provenance and language data in Music Assistant Lokalise TMX."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from xml.etree import ElementTree as ET


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        root = ET.parse(args.path).getroot()
        body = root.find("body")
        if root.tag != "tmx" or root.get("version") != "1.4" or body is None:
            raise ValueError("expected TMX 1.4 with body")
        units = body.findall("tu")
        ids = set()
        projects = set()
        for unit in units:
            tuid = unit.get("tuid", "")
            if not tuid.startswith("lokalise:") or not tuid.removeprefix("lokalise:").isdigit() or tuid in ids:
                raise ValueError(f"invalid or duplicate tuid: {tuid}")
            ids.add(tuid)
            properties = {item.get("type"): item.text for item in unit.findall("prop")}
            required = {"source", "lokalise-key-id", "lokalise-project-id", "verification-method", "status", "verified-date"}
            if not required.issubset(properties) or any(not properties[name] for name in required):
                raise ValueError(f"{tuid}: missing provenance property")
            if not properties["lokalise-key-id"].isdigit() or properties["status"] != "saved-and-read-back":
                raise ValueError(f"{tuid}: invalid identifier or status")
            projects.add(properties["lokalise-project-id"])
            languages = {item.get("{http://www.w3.org/XML/1998/namespace}lang") for item in unit.findall("tuv")}
            if languages != {"en", "sv"} or any(not (item.find("seg").text or "") for item in unit.findall("tuv")):
                raise ValueError(f"{tuid}: expected non-empty en and sv segments")
    except (OSError, ET.ParseError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"valid: {len(ids)} entries; projects={','.join(sorted(projects))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
