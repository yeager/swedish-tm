#!/usr/bin/env python3
"""Verify a checked-in Home Assistant TMX manifest against Lokalise.

This is deliberately a read-only gate.  Local exports can become stale or
reuse an ID after upstream key changes, so a translation-ID readback alone is
not enough provenance: the live key's name, Swedish translation ID/text and
English text are all checked before an entry is admitted to the TMX.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT = "130246255a974bd3b5e8a1.51616605"


def token() -> str:
    try:
        import keyring
    except ImportError as error:
        raise RuntimeError("Python keyring is required for the Lokalise credential") from error
    value = keyring.get_password("lokalise", "api_token")
    if not value:
        raise RuntimeError("no Lokalise token in keyring service 'lokalise', account 'api_token'")
    return value


def key_resource(key_id: str, api_token: str) -> dict:
    request = Request(
        f"https://api.lokalise.com/api2/projects/{PROJECT}/keys/{key_id}",
        headers={"X-Api-Token": api_token},
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)["key"]


def verify(entry: dict, resource: dict) -> str | None:
    names = resource.get("key_name", {})
    if entry["key"] not in set(names.values()):
        return f"live key name is {names!r}, not {entry['key']!r}"
    translations = resource.get("translations", [])
    swedish = [item for item in translations if item.get("language_iso") == "sv"]
    english = [item for item in translations if item.get("language_iso") == "en"]
    if len(swedish) != 1 or str(swedish[0].get("translation_id")) != str(entry["translation_id"]):
        return "live Swedish translation ID does not match manifest"
    if swedish[0].get("translation") != entry["sv"]:
        return f"live Swedish text is {swedish[0].get('translation')!r}, not {entry['sv']!r}"
    if len(english) != 1 or english[0].get("translation") != entry["en"]:
        return "live English text does not match manifest"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="+", help="JSON manifest(s) to verify")
    parser.add_argument("--delay", type=float, default=1.2, help="seconds between requests (default: 1.2)")
    args = parser.parse_args()
    try:
        api_token = token()
        entries = [entry for path in args.manifest for entry in json.loads(path.read_text(encoding="utf-8"))]
        failures = []
        for number, entry in enumerate(entries, 1):
            problem = verify(entry, key_resource(str(entry["key_id"]), api_token))
            if problem:
                failures.append(f"{entry['key']}: {problem}")
            if number < len(entries):
                time.sleep(args.delay)
    except (OSError, ValueError, KeyError, RuntimeError, HTTPError, URLError) as error:
        print(error, file=sys.stderr)
        return 1
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"verified live Lokalise identity and text for {len(entries)} manifest entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
