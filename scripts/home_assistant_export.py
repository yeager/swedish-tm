#!/usr/bin/env python3
"""Fetch and validate complete Swedish Home Assistant Lokalise translation memories.

The output intentionally distinguishes a live catalog snapshot from entries with
an individual Swedish linguistic-review record. It preserves every available
English/Swedish pair together with the Lokalise key context.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, time, urllib.request
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET
import polib
from import_reviewed import esc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Home-Assistant" / "source-archive" / "home-assistant"
PROJECTS = {
    "core": ("Home Assistant Core", "130246255a974bd3b5e8a1.51616605"),
    "frontend": ("Home Assistant Frontend", "3420425759f6d6d241f598.13594006"),
    "ios": ("Home Assistant Companion for iOS", "834452985a05254348aee2.46389241"),
    "android": ("Home Assistant Companion for Android", "145814835dd655bc5ab0d0.36753359"),
}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def api_get(url: str, token: str):
    request = urllib.request.Request(url, headers={"X-Api-Token": token, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response), {key.lower(): value for key, value in response.headers.items()}


def lokalise_token():
    """Read the API token from the environment or the desktop secret store."""
    token = os.environ.get("LOKALISE_TOKEN")
    if token:
        return token
    try:
        import keyring
        return keyring.get_password("lokalise", "api_token")
    except Exception:
        return None


def parse_variant(value: str):
    """Return ordered plural values, or a single nonempty string."""
    if not isinstance(value, str) or not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [value]
    if not isinstance(parsed, dict):
        return [value]
    ordered = [parsed[k] for k in ("one", "other") if isinstance(parsed.get(k), str) and parsed[k]]
    return ordered[:2]


def core_plural_source(key: dict):
    """Read plural source forms from current Core strings.json when available.

    Some entity states use literal state keys such as ``one`` and ``two``.
    Lokalise represents those as the language's ``one``/``other`` plural pair,
    and its source ``other`` can be empty even though Core has a real ``two``
    string. Prefer the checked out Core source in that case.
    """
    context = key.get("key_name", {}).get("other", "")
    parts = context.split("::")
    if len(parts) < 4 or parts[0] != "component":
        return []
    integration = parts[1]
    source_path = ROOT.parent.parent / "sources" / "home-assistant-core-current" / "homeassistant" / "components" / integration / "strings.json"
    if not source_path.is_file():
        return []
    try:
        node = json.loads(source_path.read_text(encoding="utf-8"))
        for part in parts[2:]:
            node = node[part]
    except (KeyError, TypeError, json.JSONDecodeError):
        return []
    if not isinstance(node, dict) or not isinstance(node.get("one"), str):
        return []
    other = node.get("other")
    if not isinstance(other, str) or not other:
        alternatives = [value for name, value in node.items() if name != "one" and isinstance(value, str) and value]
        other = alternatives[0] if len(alternatives) == 1 else ""
    return [node["one"], other] if other else []


def fetch_component(component: str, title: str, project_id: str, token: str, snapshot_date: str):
    rows = []
    excluded = []
    page = 1
    while True:
        # Lokalise's paginated key endpoint can otherwise serve a stale cached
        # translation list immediately after an individual-key update.  A
        # per-request cache buster keeps exports aligned with live readbacks.
        url = (f"https://api.lokalise.com/api2/projects/{project_id}/keys?"
               f"include_translations=1&limit=500&page={page}&cache_bust={time.time_ns()}")
        payload, headers = api_get(url, token)
        for key in payload.get("keys", []):
            if key.get("is_archived"):
                continue
            translations = {item.get("language_iso"): item for item in key.get("translations", [])}
            english = translations.get("en", {})
            swedish = translations.get("sv", {})
            source = parse_variant(english.get("translation", ""))
            target = parse_variant(swedish.get("translation", ""))
            if key.get("is_plural"):
                local_source = core_plural_source(key)
                if len(local_source) == 2:
                    source = local_source
            if not source or not target:
                reason = (
                    "empty-source-and-target" if not source and not target
                    else "empty-source" if not source
                    else "empty-target"
                )
                excluded.append({
                    "id": f"home-assistant:{component}:{key['key_id']}",
                    "project": title,
                    "component": component,
                    "unit": str(key["key_id"]),
                    "context": key.get("key_name", {}).get("other", ""),
                    "source": source,
                    "target": target,
                    "source_translation_raw": english.get("translation", ""),
                    "target_translation_raw": swedish.get("translation", ""),
                    "source_translation_id": english.get("translation_id"),
                    "target_translation_id": swedish.get("translation_id"),
                    "snapshot_date": snapshot_date,
                    "is_hidden": bool(key.get("is_hidden")),
                    "exclusion_reason": reason,
                    "note": "Lokalise key retained in exclusion inventory; no nonempty source/target pair is available for TMX.",
                })
                continue
            if len(source) != len(target):
                # A one-form source may legitimately have Swedish plural forms.
                if len(source) == 1 and len(target) == 2:
                    source = [source[0], source[0]]
                elif len(source) == 2 and len(target) == 1:
                    target = [target[0], target[0]]
                else:
                    excluded.append({
                        "id": f"home-assistant:{component}:{key['key_id']}",
                        "project": title,
                        "component": component,
                        "unit": str(key["key_id"]),
                        "context": key.get("key_name", {}).get("other", ""),
                        "source": source,
                        "target": target,
                        "source_translation_id": english.get("translation_id"),
                        "target_translation_id": swedish.get("translation_id"),
                        "snapshot_date": snapshot_date,
                        "is_hidden": bool(key.get("is_hidden")),
                        "exclusion_reason": "plural-form-count-mismatch",
                        "note": "Lokalise key retained in exclusion inventory because source and target plural forms cannot be paired safely.",
                    })
                    continue
            rows.append({
                "id": f"home-assistant:{component}:{key['key_id']}",
                "project": title,
                "component": component,
                "unit": str(key["key_id"]),
                "context": key.get("key_name", {}).get("other", ""),
                "source": source,
                "target": target,
                "source_translation_id": english.get("translation_id"),
                "target_translation_id": swedish.get("translation_id"),
                "source_key": key.get("key_name", {}).get("other", ""),
                "snapshot_date": snapshot_date,
                "review_status": "live-lokalise-export",
                "note": "Aktuell svensk Lokalise-export. Varje post måste fortfarande granskas i sitt gränssnittssammanhang.",
            })
        pages = int(headers["x-pagination-page-count"])
        if page >= pages:
            break
        page += 1
        # Sequential requests are already network-bound; keep a small yield
        # without adding enough delay to make a complete Core export stale.
        time.sleep(0.01)
    rows.sort(key=lambda row: int(row["unit"]))
    return rows, excluded


def snapshot_path(component: str) -> Path:
    return OUT / "snapshots" / f"{component}.jsonl"


def exclusion_path(component: str) -> Path:
    return OUT / "snapshots" / f"{component}-excluded.jsonl"


def write_snapshot(component: str, rows):
    path = snapshot_path(component)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
    return path


def write_exclusions(component: str, rows):
    path = exclusion_path(component)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    return path


def load_exclusions(component: str):
    path = exclusion_path(component)
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_snapshot(component: str):
    return [json.loads(line) for line in snapshot_path(component).read_text(encoding="utf-8").splitlines() if line]


def po_path(component: str) -> Path:
    return OUT / f"sv-home-assistant-{component}.po"


def write_component(component: str, rows):
    po = polib.POFile(wrapwidth=0)
    po.metadata = {
        "Project-Id-Version": f"Home Assistant {component} Swedish translation memory",
        "PO-Revision-Date": "2026-10-24 12:00+0200",
        "Last-Translator": "Daniel Nylander <po@danielnylander.se>",
        "Language-Team": "Swedish <tp-sv@listor.tp-sv.se>",
        "Language": "sv",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "8bit",
        "Plural-Forms": "nplurals=2; plural=(n != 1);",
    }
    for row in rows:
        context = json.dumps([row["project"], row["component"], row["context"], row["unit"]], ensure_ascii=False, separators=(",", ":"))
        comment = f"Lokalise key {row['unit']}; source translation {row['source_translation_id']}; Swedish translation {row['target_translation_id']}; snapshot {row['snapshot_date']}; {row['review_status']}"
        entry = polib.POEntry(msgctxt=context, msgid=row["source"][0], comment=comment)
        if len(row["source"]) == 2:
            entry.msgid_plural = row["source"][1]
            entry.msgstr_plural = {index: value for index, value in enumerate(row["target"])}
        else:
            entry.msgstr = row["target"][0]
        po.append(entry)
    path = po_path(component)
    po.save(str(path))
    digest = hashlib.sha256(snapshot_path(component).read_bytes()).hexdigest()
    tmx = path.with_suffix(".tmx")
    with tmx.open("w", encoding="utf-8", newline="\n") as out:
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n<tmx version="1.4">\n')
        out.write('<header creationtool="swedish-tm home_assistant_export.py" creationtoolversion="1" segtype="sentence" o-tmf="lokalise-live-export" adminlang="en" srclang="en" datatype="PlainText"/>\n<body>\n')
        for row in rows:
            for index, target in enumerate(row["target"]):
                source = row["source"][index]
                out.write(f'<tu tuid="{row["id"]}-{index}">')
                props = {
                    "project": row["project"], "component": component, "key_id": row["unit"],
                    "context": row["context"], "source_translation_id": str(row["source_translation_id"]),
                    "target_translation_id": str(row["target_translation_id"]), "snapshot_date": row["snapshot_date"],
                    "snapshot_sha256": digest, "review_status": row["review_status"], "note_json": json.dumps(row["note"], ensure_ascii=False),
                    "plural_index": str(index),
                }
                for key, value in props.items():
                    out.write(f'<prop type="{key}">{esc(value)}</prop>')
                out.write(f'<tuv xml:lang="en"><seg>{esc(source)}</seg></tuv><tuv xml:lang="sv"><seg>{esc(target)}</seg></tuv></tu>\n')
        out.write("</body>\n</tmx>\n")
    return {"units": len(rows), "segments": sum(len(row["target"]) for row in rows), "snapshot_sha256": digest}


def validate_component(component: str):
    rows = load_snapshot(component)
    excluded = load_exclusions(component)
    row_units = {str(row["unit"]) for row in rows}
    excluded_units = [str(row["unit"]) for row in excluded]
    if len(set(excluded_units)) != len(excluded_units):
        raise ValueError(f"{component}: duplicate key in exclusion inventory")
    if row_units.intersection(excluded_units):
        raise ValueError(f"{component}: key occurs in both export and exclusion inventory")
    valid_exclusion_reasons = {
        "empty-source-and-target",
        "empty-source",
        "empty-target",
        "plural-form-count-mismatch",
    }
    for row in excluded:
        if row.get("component") != component or not row.get("context") or not row.get("unit"):
            raise ValueError(f"{component}: malformed exclusion inventory row")
        if row.get("exclusion_reason") not in valid_exclusion_reasons:
            raise ValueError(f"{component}: unsupported exclusion reason for {row['unit']}")
        if not isinstance(row.get("is_hidden"), bool):
            raise ValueError(f"{component}: missing hidden-key state for excluded key {row['unit']}")
    expected = [(row["source"][index], target) for row in rows for index, target in enumerate(row["target"])]
    path = po_path(component)
    po = polib.pofile(str(path), encoding="utf-8")
    actual = []
    for entry in po:
        if entry.msgid_plural:
            actual.extend((entry.msgid if index == 0 else entry.msgid_plural, target) for index, target in sorted(entry.msgstr_plural.items()))
        else:
            actual.append((entry.msgid, entry.msgstr))
    if actual != expected:
        raise ValueError(f"{component}: PO does not match snapshot")
    tree = ET.parse(path.with_suffix(".tmx"))
    tmx = []
    for unit in tree.findall("./body/tu"):
        variants = {item.get(XML_LANG): "".join(item.find("seg").itertext()) for item in unit.findall("tuv")}
        tmx.append((variants["en"], variants["sv"]))
    if tmx != expected:
        raise ValueError(f"{component}: TMX does not match snapshot")
    return {
        "units": len(rows),
        "segments": len(expected),
        "pairs": len(set(expected)),
        "excluded_keys": len(excluded),
        "exclusion_reasons": dict(Counter(row["exclusion_reason"] for row in excluded)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Fetch all nonarchived Home Assistant keys from Lokalise.")
    parser.add_argument("--write", action="store_true", help="Generate PO and TMX files from snapshots.")
    parser.add_argument("--validate", action="store_true", help="Validate snapshots against PO and TMX outputs.")
    parser.add_argument(
        "--component",
        choices=tuple(PROJECTS),
        action="append",
        help="Limit the operation to a component; may be supplied more than once.",
    )
    args = parser.parse_args()
    if not (args.fetch or args.write or args.validate):
        parser.error("select at least one action")
    components = args.component or tuple(PROJECTS)
    today = dt.date.today().isoformat()
    if args.fetch:
        token = lokalise_token()
        if not token:
            parser.error("LOKALISE_TOKEN or the secure Lokalise keyring entry is required with --fetch")
        for component in components:
            title, project_id = PROJECTS[component]
            rows, excluded = fetch_component(component, title, project_id, token, today)
            previous_path = snapshot_path(component)
            previous = {}
            if previous_path.is_file():
                previous = {row["unit"]: row for row in load_snapshot(component)}
            for row in rows:
                old = previous.get(row["unit"])
                if not old or old.get("review_status") == "live-lokalise-export":
                    continue
                if old.get("source") == row["source"] and old.get("target") == row["target"]:
                    row["review_status"] = old["review_status"]
                    row["note"] = old.get("note", row["note"])
                else:
                    row["review_status"] = "needs-review-live-change"
                    row["note"] = (
                        f"Tidigare {old.get('review_status')} post ändrad i livekällan eller Lokalise sedan "
                        f"{old.get('snapshot_date')}; granskningsstatus måste förnyas."
                    )
            write_snapshot(component, rows)
            write_exclusions(component, excluded)
            print(component, "fetched", len(rows), "excluded with reason", len(excluded))
    result = {}
    if args.write:
        for component in components:
            result[component] = write_component(component, load_snapshot(component))
    if args.validate:
        for component in components:
            result[component] = validate_component(component)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
