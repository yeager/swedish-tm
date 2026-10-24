#!/usr/bin/env python3
"""Fetch and validate complete Swedish Home Assistant Lokalise translation memories.

The output intentionally distinguishes a live catalog snapshot from entries with
an individual Swedish linguistic-review record. It preserves every available
English/Swedish pair together with the Lokalise key context.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, time, urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET
import polib
from import_reviewed import esc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "home-assistant"
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


def fetch_component(component: str, title: str, project_id: str, token: str, snapshot_date: str):
    rows = []
    page = 1
    while True:
        url = f"https://api.lokalise.com/api2/projects/{project_id}/keys?include_translations=1&limit=500&page={page}"
        payload, headers = api_get(url, token)
        for key in payload.get("keys", []):
            if key.get("is_archived"):
                continue
            translations = {item.get("language_iso"): item for item in key.get("translations", [])}
            english = translations.get("en", {})
            swedish = translations.get("sv", {})
            source = parse_variant(english.get("translation", ""))
            target = parse_variant(swedish.get("translation", ""))
            if not source or not target:
                continue
            if len(source) != len(target):
                # A one-form source may legitimately have Swedish plural forms.
                if len(source) == 1 and len(target) == 2:
                    source = [source[0], source[0]]
                elif len(source) == 2 and len(target) == 1:
                    target = [target[0], target[0]]
                else:
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
        time.sleep(0.11)
    rows.sort(key=lambda row: int(row["unit"]))
    return rows


def snapshot_path(component: str) -> Path:
    return OUT / "snapshots" / f"{component}.jsonl"


def write_snapshot(component: str, rows):
    path = snapshot_path(component)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
    return path


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
    return {"units": len(rows), "segments": len(expected), "pairs": len(set(expected))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Fetch all nonarchived Home Assistant keys from Lokalise.")
    parser.add_argument("--write", action="store_true", help="Generate PO and TMX files from snapshots.")
    parser.add_argument("--validate", action="store_true", help="Validate snapshots against PO and TMX outputs.")
    args = parser.parse_args()
    if not (args.fetch or args.write or args.validate):
        parser.error("select at least one action")
    today = dt.date.today().isoformat()
    if args.fetch:
        token = os.environ.get("LOKALISE_TOKEN")
        if not token:
            parser.error("LOKALISE_TOKEN is required with --fetch")
        for component, (title, project_id) in PROJECTS.items():
            rows = fetch_component(component, title, project_id, token, today)
            write_snapshot(component, rows)
            print(component, "fetched", len(rows))
    result = {}
    if args.write:
        for component in PROJECTS:
            result[component] = write_component(component, load_snapshot(component))
    if args.validate:
        for component in PROJECTS:
            result[component] = validate_component(component)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
