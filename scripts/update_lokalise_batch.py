#!/usr/bin/env python3
"""Safely write an explicit, reviewed Lokalise translation batch.

The updates argument is a JSON object mapping key IDs to Swedish text.  Each
write is followed by a live read-back, so callers never add a translation to
the translation memory merely because a PUT request was accepted.
"""

from __future__ import annotations

import argparse
import json
import time

import keyring
import requests


def language_translation(key: dict, language: str) -> dict:
    for translation in key["translations"]:
        if translation["language_iso"] == language:
            return translation
    raise ValueError(f"{key['key_id']}: missing translation for {language}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_id")
    parser.add_argument("updates", help="JSON object: key ID -> reviewed string or plural-form object")
    parser.add_argument("--language", default="sv")
    parser.add_argument("--interval", type=float, default=0.13,
                        help="minimum seconds between API calls")
    args = parser.parse_args()
    updates = json.loads(args.updates)
    if not isinstance(updates, dict) or not updates:
        raise ValueError("updates must be a non-empty JSON object")
    token = keyring.get_password("lokalise", "api_token")
    if not token:
        raise RuntimeError("missing Lokalise API token in secure keyring")
    session = requests.Session()
    session.headers.update({"X-Api-Token": token})
    base = f"https://api.lokalise.com/api2/projects/{args.project_id}"
    verified = []
    for key_id, wanted in updates.items():
        key_id = str(key_id)
        response = session.get(f"{base}/keys/{key_id}", params={"include_translations": 1}, timeout=30)
        response.raise_for_status()
        key = response.json()["key"]
        if isinstance(wanted, str):
            if not wanted:
                raise ValueError(f"{key_id}: translation must be non-empty text")
        elif isinstance(wanted, dict):
            if not wanted or any(not isinstance(form, str) for form in wanted.values()):
                raise ValueError(f"{key_id}: plural translation must map forms to strings")
            if not key.get("is_plural"):
                raise ValueError(f"{key_id}: plural forms supplied for a non-plural key")
        else:
            raise ValueError(f"{key_id}: translation must be text or a plural-form object")
        target = language_translation(key, args.language)
        if wanted == "@source":
            wanted = language_translation(key, "en")["translation"]
            if not wanted:
                raise ValueError(f"{key_id}: source translation is empty")
        translation_id = target["translation_id"]
        time.sleep(args.interval)
        response = session.put(f"{base}/translations/{translation_id}", json={"translation": wanted}, timeout=30)
        response.raise_for_status()
        time.sleep(args.interval)
        response = session.get(f"{base}/translations/{translation_id}", timeout=30)
        response.raise_for_status()
        actual = response.json()["translation"]["translation"]
        if isinstance(wanted, dict) and isinstance(actual, str):
            actual = json.loads(actual)
        if actual != wanted:
            raise RuntimeError(f"{key_id}: read-back differed")
        verified.append({"key_id": key_id, "translation_id": str(translation_id)})
        time.sleep(args.interval)
    print(json.dumps(verified, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
