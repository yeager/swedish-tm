import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "append_verified_home_assistant_tmx",
    ROOT / "scripts" / "append_verified_home_assistant_tmx.py",
)
append_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(append_tool)


def entry(**overrides):
    value = {
        "key": "component::test::name",
        "key_id": "77",
        "translation_id": "42",
        "en": "Hue/Sat color",
        "sv": "Nyans-/mättnadsfärg",
        "verification_method": "Lokalise API read-back",
        "verified_date": "2026-11-28",
        "status": "saved-and-read-back",
        "source_revision": "abc123",
        "previous_review": "reviews/previous-candidates.json",
    }
    return value | overrides


def write_canonical(path, *, legacy=False):
    key_id = "" if legacy else '<prop type="lokalise-key-id">77</prop>'
    path.write_text(
        '<?xml version="1.0"?><tmx version="1.4"><body>'
        '<tu tuid="lokalise:42"><prop type="source">component::test::name</prop>'
        f"{key_id}<prop type=\"status\">verified-existing</prop>"
        '<tuv xml:lang="en"><seg>Hue/Sat color</seg></tuv>'
        '<tuv xml:lang="sv"><seg>Hue/Sat-färg</seg></tuv></tu>'
        '</body></tmx>',
        encoding="utf-8",
    )


def test_append_keeps_previous_review_metadata(tmp_path):
    canonical = tmp_path / "canonical.tmx"
    write_canonical(canonical)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps([entry()]), encoding="utf-8")

    assert append_tool.append(canonical, manifest, write=True) == 1
    unit = ET.parse(canonical).find(".//tu")
    assert unit is not None
    assert unit.findtext("prop[@type='review-history']") == "reviews/previous-candidates.json"
    assert unit.findtext("prop[@type='source-revision']") == "abc123"
    assert unit.findtext("prop[@type='status']") == "saved-and-read-back"


def test_replaces_legacy_lokalise_tuid_without_key_id(tmp_path):
    canonical = tmp_path / "canonical.tmx"
    write_canonical(canonical, legacy=True)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps([entry()]), encoding="utf-8")

    assert append_tool.append(canonical, manifest, write=True) == 1
    root = ET.parse(canonical)
    units = root.findall(".//tu")
    assert len(units) == 1
    assert units[0].get("tuid") == "lokalise:42"
    assert units[0].findtext("prop[@type='lokalise-key-id']") == "77"
    assert units[0].findtext("prop[@type='review-history']") == "reviews/previous-candidates.json"
