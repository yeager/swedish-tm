#!/usr/bin/env python3
"""Import the pinned, locally reviewed Hermes Agent Swedish catalog."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

ARCHIVE_COMMIT = "f60889b413494b02c1bc9765d92bca524a7ce1ea"
ARCHIVE_DIR = "Hermes-Agent/20261114"
SOURCE_REVISION = "abeeef4d491cba7ea6126a2f54d81c879da5059f"
SOURCE_SHA256 = "4ee783a2f73a784aecd293e09cd54a0ad91581de9e90fe0b2f6d85a67e174b21"
ASSEMBLED_PATH = f"{ARCHIVE_DIR}/sv.yaml"
ASSEMBLED_SHA256 = "e08332025c17cf5b2cd355ac9194c485a22e5847efadbfc40a9be5964cfd478c"
OUTPUT = Path(__file__).resolve().parents[1] / "reviewed/data/hermes-agent-20261114.jsonl"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


def flatten(node: Any, prefix: str = "") -> dict[str, str]:
    result: dict[str, str] = {}
    if not isinstance(node, dict):
        raise ValueError(f"expected YAML mapping at {prefix or '<root>'}")
    for key, value in node.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            result.update(flatten(value, path))
        elif isinstance(value, str):
            result[path] = value
        else:
            raise ValueError(f"non-string leaf at {path}")
    return result


def load_yaml(data: bytes) -> dict[str, str]:
    return flatten(yaml.safe_load(data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("translations_repo", type=Path, help="yeager/translations checkout")
    parser.add_argument("source_yaml", type=Path, help="locales/en.yaml at the pinned upstream revision")
    parser.add_argument("--write", action="store_true", help="write the generated JSONL")
    args = parser.parse_args()

    source_data = args.source_yaml.read_bytes()
    if sha256(source_data) != SOURCE_SHA256:
        raise ValueError("source YAML does not match the pinned upstream catalog checksum")
    source = load_yaml(source_data)
    assembled_data = git(args.translations_repo, "show", f"{ARCHIVE_COMMIT}:{ASSEMBLED_PATH}")
    if sha256(assembled_data) != ASSEMBLED_SHA256:
        raise ValueError("assembled Swedish catalog checksum mismatch")
    assembled = load_yaml(assembled_data)

    names = git(args.translations_repo, "ls-tree", "-r", "--name-only", ARCHIVE_COMMIT, "--", ARCHIVE_DIR).decode().splitlines()
    batch_paths = sorted(p for p in names if p.endswith(".json"))
    batches: dict[str, list[dict[str, str]]] = {}
    for path in batch_paths:
        raw = git(args.translations_repo, "show", f"{ARCHIVE_COMMIT}:{path}")
        batch = json.loads(raw)
        for key, target in batch["strings"].items():
            batches.setdefault(key, []).append({
                "path": path,
                "sha256": sha256(raw),
                "target": target,
                "component": batch.get("component", ""),
                "status": batch.get("status", ""),
            })

    if set(source) != set(assembled):
        raise ValueError("source and assembled Swedish catalog keys differ")
    missing_assembly = sorted(set(batches) - set(assembled))
    if missing_assembly:
        raise ValueError(f"reviewed delta keys are missing from assembled catalog: {missing_assembly[:5]}")
    rows = []
    for key in sorted(batches):
        if key not in source or key not in assembled:
            raise ValueError(f"reviewed key not found in pinned catalogs: {key}")
        selected = assembled[key]
        matching = [item for item in batches[key] if item["target"] == selected]
        if not matching:
            raise ValueError(f"assembled target is not present in a review batch: {key}")
        matching.sort(key=lambda item: (
            "correction" in item["path"].lower(),
            bool(item["status"]),
            bool(item["component"]),
            [int(n) for n in re.findall(r"\d+", item["path"])],
            item["path"],
        ))
        chosen = matching[-1]
        namespace = ".".join(key.split(".")[:2]) if "." in key else key
        component = chosen["component"] or namespace
        record_id = hashlib.sha256(f"Hermes Agent\0{key}".encode()).hexdigest()[:24]
        artifact_path = chosen["path"]
        rows.append({
            "id": record_id,
            "project": "Hermes Agent",
            "component": component,
            "context": f"Hermes Agent locale key {key}",
            "unit": key,
            "source": [source[key]],
            "target": [selected],
            "note": "Locally reviewed Swedish delta. The assembled catalog selects the latest reviewed value; no upstream submission or acceptance is evidenced.",
            "publication_status": "local-reviewed-delta",
            "evidence": {
                "artifact": f"https://github.com/yeager/translations/blob/{ARCHIVE_COMMIT}/{ASSEMBLED_PATH}",
                "sha256": ASSEMBLED_SHA256,
            },
            "source_evidence": {
                "format": "YAML",
                "source_catalog": f"https://github.com/NousResearch/hermes-agent/blob/{SOURCE_REVISION}/locales/en.yaml",
                "source_revision": SOURCE_REVISION,
                "source_catalog_sha256": SOURCE_SHA256,
                "source_reference": key,
                "reviewed_archive_commit": ARCHIVE_COMMIT,
                "matching_review_batch": artifact_path,
                "matching_review_batch_sha256": chosen["sha256"],
            },
        })

    if len(rows) != 3504:
        raise ValueError(f"expected 3504 unique reviewed delta keys, got {len(rows)}")
    encoded = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)
    if args.write:
        OUTPUT.write_text(encoded, encoding="utf-8", newline="\n")
    else:
        print(f"Validated {len(rows)} unique Hermes Agent delta records; use --write to save {OUTPUT}")


if __name__ == "__main__":
    main()
