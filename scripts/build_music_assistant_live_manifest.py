#!/usr/bin/env python3
"""Build a Music Assistant TM manifest from Lokalise's live key read-back.

The manifest contains both source and target, stable Lokalise identifiers and
the project ID.  It is deliberately a small explicit-ID tool: a review batch
must name every key it adds to the translation memory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import keyring
import requests


def translation(key: dict, language: str) -> dict:
    for item in key["translations"]:
        if item["language_iso"] == language:
            return item
    raise ValueError(f"{key['key_id']}: missing {language} translation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("project_id")
    parser.add_argument("key_id", nargs="+", type=int)
    parser.add_argument("--target-language", default="sv_SE")
    parser.add_argument("--method", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    token = keyring.get_password("lokalise", "api_token")
    if not token:
        raise SystemExit("missing Lokalise API token in keyring")
    entries = []
    for key_id in args.key_id:
        response = requests.get(
            f"https://api.lokalise.com/api2/projects/{args.project_id}/keys/{key_id}",
            headers={"X-Api-Token": token}, params={"include_translations": 1}, timeout=30,
        )
        response.raise_for_status()
        key = response.json()["key"]
        source = translation(key, "en")
        target = translation(key, args.target_language)
        if not source["translation"] or not target["translation"]:
            raise ValueError(f"{key_id}: source or Swedish target is empty")
        entries.append({
            "key": key["key_name"]["web"], "key_id": str(key_id),
            "translation_id": str(target["translation_id"]),
            "project_id": args.project_id, "en": source["translation"],
            "sv": target["translation"], "verification_method": args.method,
            "verified_date": args.date,
        })
    args.output.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} entries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
