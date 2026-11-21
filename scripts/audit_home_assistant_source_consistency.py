#!/usr/bin/env python3
"""List divergent Swedish targets for identical Home Assistant Core sources.

This is a candidate finder, not a translation authority.  It excludes long
sentences by default and prints the full Lokalise key identity needed for a
subsequent live API review.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Core JSONL snapshot")
    parser.add_argument("--max-words", type=int, default=4, help="maximum English source words (default: 4)")
    parser.add_argument("--min-occurrences", type=int, default=2, help="minimum occurrences of a source (default: 2)")
    args = parser.parse_args()
    groups: dict[str, list[dict]] = defaultdict(list)
    for line in args.snapshot.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if len(row.get("source", [])) != 1 or len(row.get("target", [])) != 1:
            continue
        source = row["source"][0]
        if not source or len(source.split()) > args.max_words:
            continue
        groups[source].append(row)
    for source, rows in sorted(groups.items()):
        targets = {row["target"][0] for row in rows}
        if len(rows) < args.min_occurrences or len(targets) < 2:
            continue
        print(f"SOURCE\t{source}\toccurrences={len(rows)}\ttargets={len(targets)}")
        for row in sorted(rows, key=lambda item: (item["target"][0], item["source_key"])):
            print(f"  {row['target'][0]}\t{row['source_key']}\t{row['unit']}\t{row['target_translation_id']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        # Normal when callers intentionally narrow the candidate list with
        # head, rg, or another downstream process that exits early.
        os._exit(0)
