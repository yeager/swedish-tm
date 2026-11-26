#!/usr/bin/env python3
"""Validate provenance metadata in a Home Assistant Core Lokalise TMX file.

The historical canonical file contains two documented ``tuid`` styles:
``lokalise:<translation-id>`` for entries that were read back through the
Lokalise API, and a source-key ``tuid`` for older entries whose ID has not yet
been recovered.  The default mode reports both styles without rewriting the
file.  Use ``--require-lokalise-ids`` as a migration gate once every legacy
entry has been reconciled through the API.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET


# Do not treat ordinary localized percentages such as ``50 % means`` or
# ``50 % innebär`` as printf placeholders. In Swedish text the required space
# after the percent sign would otherwise consume the first letter of the next
# word as a fake conversion specifier. Real placeholders are adjacent to ``%``
# and use a recognized conversion type.
RUNTIME_PLACEHOLDER = re.compile(
    r"\{[^{}]+\}|%%|%(?:\d+\$)?[-+#0]*(?:\d+|\*)?(?:\.(?:\d+|\*))?"
    r"(?:hh|h|ll|l|j|z|t|L)?[diouxXfFeEgGaAcspn]"
)
KEY_REFERENCE = re.compile(r"\[%key:[^%]+%\]")


def runtime_placeholders(value: str) -> list[str]:
    """Extract runtime formatting placeholders, excluding source key aliases."""
    return sorted(RUNTIME_PLACEHOLDER.findall(KEY_REFERENCE.sub("", value)))


def validate(path: Path, *, require_lokalise_ids: bool = False) -> Counter:
    """Return entry counts by provenance style or raise ``ValueError``."""
    root = ET.parse(path).getroot()
    if root.tag != "tmx" or root.get("version") != "1.4":
        raise ValueError("expected TMX 1.4 root")
    body = root.find("body")
    if body is None:
        raise ValueError("missing TMX body")

    units = body.findall("tu")
    tuids = [unit.get("tuid") for unit in units]
    if any(not tuid for tuid in tuids):
        raise ValueError("missing tuid")
    if len(set(tuids)) != len(tuids):
        raise ValueError("duplicate tuid")

    styles: Counter[str] = Counter()
    for unit in units:
        tuid = unit.get("tuid")
        source = unit.find("prop[@type='source']")
        status = unit.find("prop[@type='status']")
        variants = unit.findall("tuv")
        languages = {item.get("{http://www.w3.org/XML/1998/namespace}lang") for item in variants}
        if source is None or not source.text:
            raise ValueError(f"{tuid}: missing source provenance")
        # Keep unresolved source-path cases in the TMX as traceable review
        # follow-ups without presenting them as fully source-verified entries.
        valid_statuses = {
            "saved-and-read-back",
            "revalidated-prior-review",
            "verified-existing",
            "source-path-follow-up",
            "reference-target-updated-and-read-back",
        }
        if status is None or status.text not in valid_statuses:
            raise ValueError(
                f"{tuid}: expected one of {', '.join(sorted(valid_statuses))} statuses"
            )
        if len(variants) != 2 or languages != {"en", "sv"}:
            raise ValueError(f"{tuid}: expected one en and one sv segment")
        if any(item.find("seg") is None for item in variants):
            raise ValueError(f"{tuid}: missing segment")
        translations = {
            item.get("{http://www.w3.org/XML/1998/namespace}lang"): "".join(
                item.find("seg").itertext()
            )
            for item in variants
        }
        if not KEY_REFERENCE.search(translations["en"]) and runtime_placeholders(
            translations["en"]
        ) != runtime_placeholders(translations["sv"]):
            raise ValueError(f"{tuid}: runtime-placeholder mismatch")
        if tuid.startswith("lokalise:"):
            if not tuid.removeprefix("lokalise:").isdigit():
                raise ValueError(f"{tuid}: invalid Lokalise translation ID")
            styles["lokalise-id"] += 1
        else:
            styles["legacy-source-key"] += 1

    if require_lokalise_ids and styles["legacy-source-key"]:
        raise ValueError(f"{styles['legacy-source-key']} entries still use legacy source-key tuids")
    return styles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="canonical Home Assistant Core TMX")
    parser.add_argument("--require-lokalise-ids", action="store_true", help="fail if a legacy source-key tuid remains")
    args = parser.parse_args()
    try:
        styles = validate(args.path, require_lokalise_ids=args.require_lokalise_ids)
    except (OSError, ET.ParseError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"valid: {sum(styles.values())} entries; " + ", ".join(f"{style}={count}" for style, count in sorted(styles.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
