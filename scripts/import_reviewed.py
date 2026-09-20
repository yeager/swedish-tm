#!/usr/bin/env python3
"""Merge context-free, reviewed workspace PO pairs into ecosystem TM catalogs."""
from __future__ import annotations
import datetime as dt
import re
from collections import defaultdict
from pathlib import Path
import polib

ROOT=Path(__file__).resolve().parents[1]
WS=ROOT.parent / 'translations'

def eligible(path):
    try: po=polib.pofile(str(path),encoding='utf-8')
    except Exception: return []
    return [(e.msgid,e.msgstr) for e in po if not e.obsolete and not e.fuzzy and e.msgid and e.msgstr and not e.msgid_plural and not e.msgctxt]

def candidates(paths):
    choices=defaultdict(set)
    for path in paths:
        for source,target in eligible(path): choices[source].add(target)
    return {s:next(iter(v)) for s,v in choices.items() if len(v)==1}

def esc(s):
    parts=[]
    for ch in s:
        n=ord(ch)
        if ch=='&':parts.append('&amp;')
        elif ch=='<':parts.append('&lt;')
        elif ch=='>':parts.append('&gt;')
        elif ch=='\r':parts.append('&#13;')
        elif n<32 and ch not in '\t\n':parts.append(f'<ph x="{len(parts)+1}" type="x-control">U+{n:04X}</ph>')
        else:parts.append(ch)
    return ''.join(parts)

def write_tmx(po_path,project):
    po=polib.pofile(str(po_path),encoding='utf-8')
    out=['<?xml version="1.0" encoding="UTF-8"?>','<tmx version="1.4">',f'  <header creationtool="TR Intelligence" creationtoolversion="1.0" datatype="PlainText" segtype="sentence" adminlang="en" srclang="en" o-tmf="TR-export" creationdate="{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}">',f'    <note>Swedish {project.upper()} Translation Memory</note>','  </header>','  <body>']
    for e in po:
        out += ['    <tu>',f'      <prop type="project">yeager:{project}</prop>',f'      <tuv xml:lang="en"><seg>{esc(e.msgid)}</seg></tuv>',f'      <tuv xml:lang="sv"><seg>{esc(e.msgstr)}</seg></tuv>','    </tu>']
    out += ['  </body>','</tmx>','']
    po_path.with_suffix('.tmx').write_text('\n'.join(out),encoding='utf-8')

def merge(name, paths, project):
    path=ROOT/f'sv-{name}.po'; po=polib.pofile(str(path),encoding='utf-8'); incoming=candidates(paths); existing={e.msgid:e for e in po}; changed=added=conflict=0
    for source,target in incoming.items():
        e=existing.get(source)
        if e:
            if e.msgstr != target: e.msgstr=target; changed+=1
        else:
            po.append(polib.POEntry(msgid=source,msgstr=target,comment=f'from yeager:{project}-review')); added+=1
    po.save(str(path)); write_tmx(path,project)
    print(name, 'incoming',len(incoming),'changed',changed,'added',added,'total',len(po))

if __name__ == '__main__':
    reviewed=sorted(WS.rglob('*reviewed*.po'))
    weblate=list((WS/'Weblate').rglob('*.po')) + [p for p in reviewed if p.parts[-2] not in {'SuperTux'}] + list(WS.glob('*/**/*published*.po'))
    merge('blender',[WS/'Blender/blender-ui-ui-sv.po'],'blender')
    merge('inkscape',[WS/'Inkscape/inkscape-master-sv.po'],'inkscape')
    merge('tp',list((WS/'tp-sv').glob('*.po')),'tp')
    merge('weblate',weblate,'weblate')
