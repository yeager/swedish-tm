#!/usr/bin/env python3
"""List live Lokalise keys whose source and target translations are both empty.

The scan is deliberately sequential and retries rate limits.  It is intended
for reporting broken upstream localisation metadata, not for writing text.
"""

from __future__ import annotations

import argparse
import json
import time

import keyring
import requests


def get_page(session: requests.Session, url: str, page: int) -> requests.Response:
    for attempt in range(6):
        response = session.get(
            url,
            params={"include_translations": 1, "limit": 500, "page": page},
            timeout=90,
        )
        if response.status_code != 429:
            response.raise_for_status()
            return response
        time.sleep(min(60, 5 * (attempt + 1)))
    response.raise_for_status()
    raise AssertionError("unreachable")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_id")
    parser.add_argument("output")
    parser.add_argument("--source-language", default="en")
    parser.add_argument("--target-language", default="sv")
    parser.add_argument("--include-archived", action="store_true")
    parser.add_argument("--interval", type=float, default=1.1)
    args = parser.parse_args()

    token = keyring.get_password("lokalise", "api_token")
    if not token:
        raise RuntimeError("missing Lokalise API token in secure keyring")
    session = requests.Session()
    session.headers["X-Api-Token"] = token
    url = f"https://api.lokalise.com/api2/projects/{args.project_id}/keys"

    page = 1
    rows: list[dict[str, str | int]] = []
    while True:
        response = get_page(session, url, page)
        payload = response.json()
        for key in payload["keys"]:
            if key.get("is_archived") and not args.include_archived:
                continue
            translations = {item.get("language_iso"): item for item in key["translations"]}
            source = translations.get(args.source_language, {}).get("translation", "")
            target = translations.get(args.target_language, {}).get("translation", "")
            if not source and not target:
                rows.append({
                    "key_id": key["key_id"],
                    "key": key.get("key_name", {}).get("other", ""),
                    "source_translation_id": translations.get(args.source_language, {}).get("translation_id"),
                    "target_translation_id": translations.get(args.target_language, {}).get("translation_id"),
                    "is_archived": bool(key.get("is_archived")),
                })
        pages = int(response.headers["x-pagination-page-count"])
        if page >= pages:
            break
        page += 1
        time.sleep(args.interval)

    result = {"project_id": args.project_id, "pages": pages, "empty_keys": rows}
    with open(args.output, "w", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"wrote {len(rows)} empty keys to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
