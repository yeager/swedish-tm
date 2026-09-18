import importlib.util
from pathlib import Path
import xml.etree.ElementTree as ET

import polib
import pytest

spec = importlib.util.spec_from_file_location('validate', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def test_controls_and_carriage_returns_are_preserved():
    segment = ET.fromstring('<seg>A&#13;B<ph x="1" type="x-control">U+001B</ph>C</seg>')
    assert validator.segment_text(segment) == 'A\rB\x1bC'


@pytest.mark.parametrize('xml', ['<seg><ph type="x-control">U+0020</ph></seg>',
                                  '<seg><ph type="x-control">U+000A</ph></seg>',
                                  '<seg><ph>bad</ph></seg>'])
def test_invalid_inline_codes_are_rejected(xml):
    with pytest.raises(ValueError):
        validator.segment_text(ET.fromstring(xml))


def sample(root, target='Spara'):
    po = polib.POFile()
    po.metadata = {'Language': 'sv', 'Content-Type': 'text/plain; charset=UTF-8'}
    po.append(polib.POEntry(msgid='Save', msgstr='Spara'))
    po.save(str(root / 'sv-test.po'))
    (root / 'sv-test.tmx').write_text(
        '<tmx version="1.4"><body><tu><tuv xml:lang="en"><seg>Save</seg></tuv>'
        f'<tuv xml:lang="sv"><seg>{target}</seg></tuv></tu></body></tmx>', encoding='utf-8')


def test_matching_catalogs(tmp_path):
    sample(tmp_path)
    report = validator.validate(tmp_path)
    assert report['unique_pairs'] == 1
    assert report['files']['sv-test'] == {'po_entries': 1, 'tmx_entries': 1}


def test_cross_format_mismatch_fails(tmp_path):
    sample(tmp_path, target='Fel')
    with pytest.raises(ValueError, match='PO/TMX mismatch'):
        validator.validate(tmp_path)


def test_wrong_language_fails(tmp_path):
    sample(tmp_path)
    p = tmp_path / 'sv-test.tmx'
    p.write_text(p.read_text().replace('xml:lang="sv"', 'xml:lang="de"'))
    with pytest.raises(ValueError, match='en and one sv'):
        validator.validate(tmp_path)


def test_newline_mismatch_fails_gettext(tmp_path):
    sample(tmp_path)
    p = tmp_path / 'sv-test.po'
    p.write_text(p.read_text().replace('msgid "Save"', 'msgid "Save\\n"'))
    with pytest.raises(ValueError, match='msgid'):
        validator.validate(tmp_path)


def test_invalid_xml_is_rejected(tmp_path):
    sample(tmp_path, target='Spara\x0b')
    with pytest.raises(ET.ParseError):
        validator.validate(tmp_path)
