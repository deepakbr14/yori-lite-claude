"""Build one Claude plugin ZIP, excluding repository/developer tooling."""
import hashlib,json,zipfile
from pathlib import Path
from check_package import check,ROOT
check()
v=json.loads((ROOT/'.claude-plugin/plugin.json').read_text())['version']
out=ROOT.parent/f'yori-lite-{v}.zip'
allowed={'.claude-plugin','skills','schemas','templates','tests','references','scripts'}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and (p.relative_to(ROOT).parts[0] in allowed or p.parent==ROOT and p.suffix=='.md') and not p.name.startswith('private-') and p.name!='marketplace.json' and '__pycache__' not in p.parts and (p.suffix!='.py' or p.relative_to(ROOT).parts[0]=='scripts'))
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert '.claude-plugin/plugin.json' in z.namelist()
    assert '.claude-plugin/marketplace.json' not in z.namelist()
    assert len([x for x in z.namelist() if x.endswith('/SKILL.md')])==5
    assert not any(x.startswith(('.git/','tools/')) for x in z.namelist())
    for p in files:assert z.read(str(p.relative_to(ROOT)))==p.read_bytes()
print(f'PASS: ZIP CRC, root manifest, five skills, source-byte parity and excluded development files ({len(files)} files).')
print(out)
print('SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
