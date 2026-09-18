#!/usr/bin/env python3
"""Validate the shipped PO/TMX data and report reproducible entry counts."""
import argparse
import collections
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import polib

XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'


def segment_text(segment):
    """Decode our documented TMX representation of XML-forbidden controls."""
    if segment is None:
        raise ValueError('missing TMX segment')
    parts = [segment.text or '']
    for child in segment:
        if (child.tag != 'ph' or child.get('type') != 'x-control'
                or not re.fullmatch(r'U\+[0-9A-F]{4}', child.text or '') or len(child)):
            raise ValueError('unsupported TMX inline code')
        code = int(child.text[2:], 16)
        if code >= 32 or code in (9, 10, 13):
            raise ValueError('invalid control placeholder')
        parts.extend((chr(code), child.tail or ''))
    return ''.join(parts)


def tmx_pairs(path):
    stack = []
    for event, element in ET.iterparse(path, events=('start', 'end')):
        if event == 'start':
            stack.append(element)
            if len(stack) == 1 and (element.tag != 'tmx' or element.get('version') != '1.4'):
                raise ValueError('expected TMX 1.4 root')
            continue
        if element.tag == 'tu':
            if len(stack) != 3 or stack[-2].tag != 'body':
                raise ValueError('translation unit outside TMX body')
            variants = element.findall('tuv')
            if len(variants) != 2 or {v.get(XML_LANG) for v in variants} != {'en', 'sv'}:
                raise ValueError('expected exactly one en and one sv variant')
            pair = {v.get(XML_LANG): segment_text(v.find('seg')) for v in variants}
            yield pair['en'], pair['sv']
            stack[-2].remove(element)
        stack.pop()


def validate(root):
    files = {}
    all_pairs = set()
    catalogs = sorted(root.glob('sv-*.po'))
    if not catalogs:
        raise ValueError('no PO catalogs found')
    for path in catalogs:
        # GNU gettext catches constraints polib deliberately does not enforce.
        check = subprocess.run(['msgfmt', '--check', '-o', '/dev/null', str(path)],
                               text=True, capture_output=True)
        if check.returncode:
            raise ValueError(check.stderr.strip())
        po = polib.pofile(str(path), encoding='utf-8')
        if po.metadata.get('Language') != 'sv':
            raise ValueError(f'{path.name}: expected Language: sv')
        if any(e.obsolete or e.fuzzy or not e.msgid or not e.msgstr or e.msgid_plural or e.msgctxt for e in po):
            raise ValueError(f'{path.name}: expected active, translated singular pairs without context')
        if len({e.msgid for e in po}) != len(po):
            raise ValueError(f'{path.name}: duplicate source')
        pairs = collections.Counter((e.msgid, e.msgstr) for e in po)
        if any(n != 1 for n in pairs.values()):
            raise ValueError(f'{path.name}: duplicate pair')
        all_pairs.update(pairs)
        info = {'po_entries': len(po)}
        tmx = path.with_suffix('.tmx')
        if tmx.exists():
            exported = collections.Counter(tmx_pairs(tmx))
            if exported != pairs:
                missing = sum((pairs - exported).values())
                extra = sum((exported - pairs).values())
                raise ValueError(f'{tmx.name}: PO/TMX mismatch ({missing} missing, {extra} extra pairs)')
            info['tmx_entries'] = sum(exported.values())
        files[path.stem] = info
    for path in root.glob('sv-*.tmx'):
        if path.stem not in files:
            raise ValueError(f'{path.name}: missing corresponding PO')
    return {'files': files, 'total_po_entries': sum(v['po_entries'] for v in files.values()),
            'unique_pairs': len(all_pairs)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write-stats', action='store_true', help='update stats.json after validation')
    args = parser.parse_args()
    try:
        report = validate(args.root)
        stats = args.root / 'stats.json'
        if args.write_stats:
            stats.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        elif json.loads(stats.read_text(encoding='utf-8')) != report:
            raise ValueError('stats.json is stale; validate with --write-stats')
    except (OSError, ValueError, ET.ParseError) as error:
        print(error, file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
