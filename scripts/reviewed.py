#!/usr/bin/env python3
"""Export and validate the review-derived memories without losing context or plurals."""
from __future__ import annotations
import argparse,collections,hashlib,json,subprocess,sys
from pathlib import Path
import xml.etree.ElementTree as ET
import polib
from import_reviewed import esc
ROOT=Path(__file__).resolve().parents[1]
LANG='{http://www.w3.org/XML/1998/namespace}lang'

def load(path):
    rows=[json.loads(line) for line in path.read_text(encoding='utf-8').split('\n') if line]
    seen=set()
    for r in rows:
        if not isinstance(r.get('id'),str) or r['id'] in seen: raise ValueError(f'{path}: duplicate or missing review ID')
        seen.add(r['id'])
        for key in ['project','component','unit','context','note','publication_status']:
            if not isinstance(r.get(key),str): raise ValueError(f'{path}: invalid {key}')
        for key in ['source','target']:
            if not isinstance(r.get(key),list) or not r[key] or not all(isinstance(x,str) and x for x in r[key]):raise ValueError(f'{path}: empty {key}')
        if len(r['source'])>2 or len(r['target'])>2:raise ValueError(f'{path}: unsupported Swedish plural structure')
        if len(r['target'])>1 and len(r['source']) not in [1,2]:raise ValueError('invalid plural')
        if not r.get('evidence',{}).get('artifact') or not r['evidence'].get('sha256'):raise ValueError('missing evidence')
    return rows

def context(r):
    # The ID disambiguates source units whose original catalogs had no context.
    return json.dumps([r['project'],r['component'],r['context'],r['unit'],r['id']],ensure_ascii=False,separators=(',',':'))

def po_entry(r):
    e=polib.POEntry(msgid=r['source'][0],msgctxt=context(r),comment='Review-note (JSON): '+json.dumps(r['note'],ensure_ascii=False),tcomment=f"Review: {r['id']}\nEvidence: {r['evidence']['artifact']}\nEvidence-SHA256: {r['evidence']['sha256']}\nSource-evidence: {json.dumps(r.get('source_evidence',{}),ensure_ascii=False)}\nPublication: {r['publication_status']}")
    if len(r['target'])==2:
        e.msgid_plural=r['source'][-1];e.msgstr_plural={i:t for i,t in enumerate(r['target'])}
    else:e.msgstr=r['target'][0]
    return e

def fields(r):
    return {k:r[k] for k in ['id','project','component','context','unit','publication_status']} | {'source_plural':r['source'][-1] if len(r['source'])==2 else '', 'evidence':r['evidence']['artifact'],'evidence_sha256':r['evidence']['sha256'],'source_evidence':json.dumps(r.get('source_evidence',{}),ensure_ascii=False,separators=(',',':')),'note_json':json.dumps(r['note'],ensure_ascii=False)}

def write(rows,po_path):
    po=polib.POFile(wrapwidth=0);po.metadata={'Project-Id-Version':'Swedish reviewed translation memory','Language':'sv','MIME-Version':'1.0','Content-Type':'text/plain; charset=UTF-8','Content-Transfer-Encoding':'8bit','Plural-Forms':'nplurals=2; plural=(n != 1);','Last-Translator':'Swedish FOSS review','Language-Team':'Swedish','PO-Revision-Date':'2026-09-20 00:00+0000'}
    for r in rows:po.append(po_entry(r))
    po.save(str(po_path))
    with po_path.with_suffix('.tmx').open('w',encoding='utf-8',newline='\n') as out:
        out.write('<?xml version="1.0" encoding="UTF-8"?>\n<tmx version="1.4">\n<header creationtool="swedish-tm reviewed.py" creationtoolversion="1" segtype="sentence" o-tmf="reviewed-jsonl" adminlang="en" srclang="en" datatype="PlainText"/>\n<body>\n')
        for r in rows:
            for i,t in enumerate(r['target']):
                out.write(f'<tu tuid="{r["id"]}-{i}">')
                for k,v in fields(r).items():out.write(f'<prop type="{k}">{esc(v)}</prop>')
                out.write(f'<prop type="plural_index">{i}</prop>')
                out.write(f'<tuv xml:lang="en"><seg>{esc(r["source"][min(i,len(r["source"])-1)])}</seg></tuv><tuv xml:lang="sv"><seg>{esc(t)}</seg></tuv></tu>\n')
        out.write('</body>\n</tmx>\n')

def validate(rows,po_path):
    from validate import segment_text
    po=polib.pofile(str(po_path),encoding='utf-8')
    expected=[po_entry(r) for r in rows]
    signature=lambda e:(e.msgctxt,e.msgid,e.msgid_plural,e.msgstr,dict(e.msgstr_plural),e.comment,e.tcomment)
    if [signature(e) for e in po]!=[signature(e) for e in expected]:raise ValueError(f'{po_path}: JSONL/PO mismatch')
    subprocess.run(['msgfmt','--check','-o','/dev/null',str(po_path)],check=True,capture_output=True)
    expected_tmx={f'{r["id"]}-{i}':(r['source'][min(i,len(r['source'])-1)],t,{**fields(r),'plural_index':str(i)}) for r in rows for i,t in enumerate(r['target'])}
    tree=ET.parse(po_path.with_suffix('.tmx'));actual={}
    for tu in tree.findall('./body/tu'):
        uid=tu.get('tuid')
        if uid in actual:raise ValueError('duplicate TMX unit')
        variants=tu.findall('tuv')
        if len(variants)!=2 or {v.get(LANG) for v in variants}!={'en','sv'}:raise ValueError('invalid languages')
        text={v.get(LANG):segment_text(v.find('seg')) for v in variants}
        props=tu.findall('prop');p={x.get('type'):''.join(x.itertext()) for x in props}
        if len(props)!=len(p):raise ValueError('duplicate TMX property')
        actual[uid]=(text['en'],text['sv'],p)
    if actual!=expected_tmx:raise ValueError(f'{po_path}: JSONL/TMX mismatch')
    return {'units':len(rows),'segments':len(expected_tmx),'distinct_pairs':len({(a,b) for a,b,_ in expected_tmx.values()})}

def run(root=ROOT,generate=False):
    source=root/'reviewed'/'data';out=root/'reviewed'/'catalogs';out.mkdir(parents=True,exist_ok=True)
    report={}
    for p in sorted(source.glob('*.jsonl')):
        rows=load(p);po_path=out/(p.stem+'.po')
        if generate:write(rows,po_path)
        report[p.stem]=validate(rows,po_path)
    if not report:raise ValueError('no reviewed data')
    stats={'catalogs':report,'units':sum(x['units'] for x in report.values()),'segments':sum(x['segments'] for x in report.values())}
    p=root/'reviewed'/'stats.json'
    if generate:p.write_text(json.dumps(stats,indent=2)+'\n')
    elif json.loads(p.read_text())!=stats:raise ValueError('stale reviewed stats')
    return stats
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    try:print(json.dumps(run(generate=args.write),indent=2))
    except (ValueError,subprocess.CalledProcessError) as e:
        print(e,file=sys.stderr)
        if getattr(e,'stderr',None):print(e.stderr.decode() if isinstance(e.stderr,bytes) else e.stderr,file=sys.stderr)
        sys.exit(1)
