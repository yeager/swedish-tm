import importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "validate_home_assistant_core_tmx", ROOT / "scripts" / "validate_home_assistant_core_tmx.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def write_tmx(path, tuid="lokalise:42", status="saved-and-read-back"):
    path.write_text(
        '<?xml version="1.0"?><tmx version="1.4"><body>'
        f'<tu tuid="{tuid}"><prop type="source">component::test</prop>'
        f'<prop type="status">{status}</prop>'
        '<tuv xml:lang="en"><seg>Test</seg></tuv>'
        '<tuv xml:lang="sv"><seg>Testa</seg></tuv></tu>'
        '</body></tmx>',
        encoding="utf-8",
    )


def test_accepts_lokalise_id_and_legacy_key(tmp_path):
    path = tmp_path / "sample.tmx"
    write_tmx(path)
    assert validator.validate(path)["lokalise-id"] == 1
    write_tmx(path, tuid="component::test")
    assert validator.validate(path)["legacy-source-key"] == 1


def test_accepts_revalidated_prior_review_status(tmp_path):
    path = tmp_path / "sample.tmx"
    write_tmx(path, status="revalidated-prior-review")
    assert validator.validate(path)["lokalise-id"] == 1


def test_accepts_reference_target_updated_alias_status(tmp_path):
    path = tmp_path / "sample.tmx"
    write_tmx(path, status="reference-target-updated-and-read-back")
    assert validator.validate(path)["lokalise-id"] == 1


def test_strict_mode_rejects_legacy_key(tmp_path):
    path = tmp_path / "sample.tmx"
    write_tmx(path, tuid="component::test")
    try:
        validator.validate(path, require_lokalise_ids=True)
    except ValueError as error:
        assert "legacy source-key" in str(error)
    else:
        raise AssertionError("strict mode accepted a legacy key")


def test_rejects_missing_provenance(tmp_path):
    path = tmp_path / "sample.tmx"
    write_tmx(path, status="draft")
    try:
        validator.validate(path)
    except ValueError as error:
        assert "saved-and-read-back" in str(error)
    else:
        raise AssertionError("invalid status was accepted")


def test_percent_spacing_is_not_mistaken_for_printf_placeholder():
    assert validator.runtime_placeholders("Probability 50% means on.") == []
    assert validator.runtime_placeholders("Sannolikhet 50 % innebär på.") == []


def test_recognizes_runtime_placeholders():
    assert validator.runtime_placeholders("{name} %1$s %02d %%") == [
        "%%",
        "%02d",
        "%1$s",
        "{name}",
    ]


def test_validation_rejects_mismatched_runtime_placeholder(tmp_path):
    path = tmp_path / "sample.tmx"
    write_tmx(path)
    contents = path.read_text(encoding="utf-8").replace("<seg>Testa</seg>", "<seg>{name}</seg>")
    path.write_text(contents, encoding="utf-8")
    try:
        validator.validate(path)
    except ValueError as error:
        assert "runtime-placeholder mismatch" in str(error)
    else:
        raise AssertionError("mismatched runtime placeholder was accepted")
