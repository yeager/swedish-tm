import importlib.util,json,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import reviewed

def row(n='one',target=None):
    return {'id':n,'project':'Example','component':'editor','context':'geometry','unit':n,'source':['%n face','%n faces'],'target':target or ['%n yta','%n ytor'],'note':'Reviewed','publication_status':'reviewed-local','evidence':{'artifact':'https://example.org/source','sha256':'a'*64}}

def test_context_plural_and_unicode_roundtrip(tmp_path):
    first=row();second=row('two',['%n ansikte','%n ansikten']);second['context']='portrait'
    third=row('three');third['source']=['Text\u2028line\r\x1b'];third['target']=['Text\u2028rad\r\x1b']
    third['note']='Historical note with \x00 control and "quoted" text.'
    path=tmp_path/'sv.po';rows=[first,second,third]
    source=tmp_path/'source.jsonl';source.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    assert reviewed.load(source)==rows
    reviewed.write(rows,path)
    assert reviewed.validate(rows,path)['segments']==5

def test_detects_context_tampering(tmp_path):
    path=tmp_path/'sv.po';rows=[row()];reviewed.write(rows,path)
    tmx=path.with_suffix('.tmx');tmx.write_text(tmx.read_text().replace('geometry','portrait'))
    with pytest.raises(ValueError,match='mismatch'):reviewed.validate(rows,path)

def test_rejects_duplicate_review_ids(tmp_path):
    path=tmp_path/'source.jsonl';path.write_text(json.dumps(row())+'\n'+json.dumps(row())+'\n')
    with pytest.raises(ValueError,match='duplicate'):reviewed.load(path)
