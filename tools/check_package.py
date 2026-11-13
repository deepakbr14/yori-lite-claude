"""Developer-only contract checks. Does not execute Claude or Google operations."""
import json,re,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def validate(value,schema):

    if 'const' in schema and (type(value)!=type(schema['const']) or value!=schema['const']): raise ValueError('const')
    if 'enum' in schema and value not in schema['enum']:raise ValueError('enum')
    t=schema.get('type')
    if t=='object' and not isinstance(value,dict):raise ValueError('object')
    if isinstance(value,dict):
        if not isinstance(value,dict): raise ValueError('object')
        if not set(schema.get('required',[]))<=value.keys(): raise ValueError('required')
        if schema.get('additionalProperties') is False and value.keys()-schema.get('properties',{}).keys(): raise ValueError('additional')
        for k,v in value.items():
            if k in schema.get('properties',{}):validate(v,schema['properties'][k])
    if t=='string':
        if not isinstance(value,str) or len(value)<schema.get('minLength',0):raise ValueError('string')
        if 'pattern' in schema and re.search(schema['pattern'],value) is None:raise ValueError('pattern')
    for branch in schema.get('allOf',[]):
        if 'if' in branch:
            try:validate(value,branch['if'])
            except ValueError:validate(value,branch.get('else',{}))
            else:validate(value,branch.get('then',{}))
        else:validate(value,branch)

def check():
    manifest=json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
    assert set(manifest)=={'name','displayName','version','description','author','repository','metadata'}
    assert manifest['name']=='yori-lite' and manifest['version']=='0.4.0'
    market=json.loads((ROOT/'.claude-plugin/marketplace.json').read_text())
    assert market['name']=='yori-lite-claude' and market['owner']['name']
    assert len(market['plugins'])==1
    entry=market['plugins'][0]
    assert entry['name']==manifest['name'] and entry['source']=='./' and entry['strict'] is True
    assert (ROOT/entry['source']/'.claude-plugin/plugin.json').is_file()
    pid=manifest['metadata']['pluginId'];assert str(uuid.UUID(pid[5:]))==pid[5:]
    schema=json.loads((ROOT/'schemas/config.schema.json').read_text())
    assert schema['properties']['plugin_id']['const']==pid
    good=json.loads((ROOT/'templates/config.example.json').read_text());validate(good,schema)
    legacy=dict(good);legacy.pop('storage_format');validate(legacy,schema)
    for fmt in ['metadata-v1','mixed-v1-v2','docs-v2']:validate(dict(good,storage_format=fmt),schema)
    invalid=[{},dict(good,schema_version=2),dict(good,storage_format='invented'),dict(good,plugin_id='yori_wrong'),dict(good,cortices={}),dict(good,schema_version=True),dict(good,active_cortex={'label':'x','google_drive_folder_id':'https://drive.google.com/folders/x'}),dict(good,active_cortex={'label':' ','google_drive_folder_id':'x'}),dict(good,active_cortex={'label':'x','google_drive_folder_id':'x','extra':True})]
    for bad in invalid:
        try:validate(bad,schema)
        except ValueError:pass
        else:raise AssertionError('accepted invalid config')
    skills=list((ROOT/'skills').glob('*/SKILL.md'));assert len(skills)==5
    for p in skills:
        s=p.read_text();assert s.startswith('---\n') and pid in s
        assert 'Conversation and scope — always apply' in s
        assert 'Never silently switch or merge Cortexes.' in s
        assert ('read-back' in s or 'read back' in s) and 'operation_id' in s
        assert len(s.encode())<1_000_000
        assert 'one question at a time' in s and 'Google Docs' in s and 'etag' in s
        assert 'generic engagement questions' in s and 'reasoned opinions' in s
        assert 'Do not offer three choices' in s and 'Do not announce every memory' in s
        assert 'What would you like me to know?' not in s
        assert 'Share one verified turn context' in s
        assert 'description' in s and 'operation_id' in s
        for link in re.findall(r'\]\(([^)]+)\)',s):
            if '://' not in link: assert (p.parent/link).resolve().is_file(), (p,link)
    for p in ROOT.rglob('*'):
        if not p.is_file() or '.git' in p.parts:continue
        assert p.name not in {'.mcp.json','mcp.json'}
        assert not any(x in p.parts for x in ['hooks','agents'])
        if p.suffix in {'.md','.json'}:
            s=p.read_text(); assert 'yori-prod-e70c6' not in s and '/mcp/claude' not in s
    contract=(ROOT/'references/operating-contract.md').read_text()
    assert 'Missing configuration is an ordinary setup state' in contract
    assert 'Account email identification is optional, never a prerequisite' in contract
    assert 'read-back' in contract or 'read back' in contract
    for p in (ROOT/'references').glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' not in link: assert (p.parent/link).resolve().is_file(), (p,link)
    assert not (ROOT/'templates/cortex_README.txt').exists()
    print('PASS: manifest and fixed UUID consistency; five isolated skills; valid config and 9 invalid config cases; scope/integrity contracts; no MCP/hooks/agents or personal service endpoints.')
if __name__=='__main__':check()
