"""Hash fixed Triton inputs and copied builder code without loading their data."""
import hashlib
import json
import pathlib
import platform
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

mirror, work = map(pathlib.Path, sys.argv[1:3])
files = {
    'Triton_v1_RData': mirror / 'triton/raw/Triton_v1_13517414/triton.RData',
    'Triton_v3_RData': mirror / 'triton/raw/Triton_v3_13517414/triton_update_2023.RData',
    'Triton_v4_RData': mirror / 'triton/derived/Triton_v4_13517414/triton_update_2023.RData',
    'PhanSST_32cc98ed53_CSV': mirror / 'climate-forcing/phansst/raw/2023-03-09_32cc98ed53/PhanSST_v001.csv',
}
code_checks = {}
for version in (1,3):
    path = mirror / f'triton/raw/Triton-code_v{version}_13517429/Triton_code.zip'
    files[f'Triton_code_v{version}_ZIP'] = path
    with zipfile.ZipFile(path) as z:
        name = next(n for n in z.namelist() if n.endswith('Triton_6CombinedData.R') and not n.startswith('__MACOSX'))
        data = z.read(name)
        code_checks[f'v{version}'] = {'member':name, 'member_sha256':hashlib.sha256(data).hexdigest(),
            'active_duplicated_calls':sum(bool(re.search(r'\bduplicated\s*\(',line)) for line in data.decode('utf-8').splitlines() if not line.lstrip().startswith('#'))}
files.update({str(p.relative_to(work)): p for p in [*(work/'inputs').glob('*.tsv'), *(work/'scripts').glob('*.R'), *(work/'scripts').glob('*.py')]})
entries = {}
for name, p in files.items():
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(8<<20), b''):
            h.update(chunk)
    entries[name] = {'sha256': h.hexdigest(), 'bytes': p.stat().st_size}
result = {'completed_at_UTC':datetime.now(timezone.utc).isoformat(), 'execution_surface':'Authorised Linux data host; fixed-source files opened read-only; no live provider calls.',
          'python': platform.python_version(), 'R': subprocess.check_output(['Rscript','--vanilla','-e','cat(R.version.string)'], text=True), 'inputs': entries,
          'source_deduplication_operations':code_checks,
          'source_revision': 'bc7e1d81b2f36954ca517639cf4f789ad362d658',
          'source_revision_scope': 'EPRP checkout at task start; original q012/q007 builders and frozen support tables copied read-only. Script hashes identify replay code.'}
(work / 'out/inputs_triton.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
