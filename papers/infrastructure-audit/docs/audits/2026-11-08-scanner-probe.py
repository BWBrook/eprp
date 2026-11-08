"""Check current/proposed allowlists using non-live, deterministic controls."""
import json
import os
import random
import string
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
PROPOSAL = Path(__file__).with_name('2026-11-08-gitleaks-proposed.toml')
rng = random.Random(90418)
alphabet = string.ascii_letters + string.digits
provider = 'ghp_' + ''.join(rng.choices(alphabet, k=36))
generic = 'brook2026A' + ''.join(rng.choices(alphabet, k=45))
summary = {}
generic_pairs = {('generic-control.yaml', 'generic-api-key'), ('bare-key-control.yaml', 'generic-api-key')}
with tempfile.TemporaryDirectory(prefix='infra-scanner-check-') as folder:
    root = Path(folder)
    fixture = root / 'fixture'
    (fixture / 'references').mkdir(parents=True)
    bibliography = REPO / 'papers/infrastructure-audit/references/refs.yaml'
    (fixture / 'references/refs.yaml').write_text(bibliography.read_text() + '\ntoken: ' + provider + '\n')
    (fixture / 'provider-control.yaml').write_text('token: ' + provider + '\n')
    (fixture / 'generic-control.yaml').write_text('api_key: ' + generic + '\n')
    (fixture / 'bare-key-control.yaml').write_text('key: ' + generic + '\n')
    for name, config in [('reviewed', REPO / '.gitleaks.toml'), ('proposed', PROPOSAL)]:
        report = root / (name + '.json')
        result = subprocess.run([
            'gitleaks', 'detect', '--no-git', '--no-banner', '--redact',
            '--config', str(config), '--source', str(fixture),
            '--report-format', 'json', '--report-path', str(report)
        ], capture_output=True, text=True, env=dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null'))
        assert result.returncode == 1, (name, result.stderr)
        findings = json.loads(report.read_text())
        pairs = {(Path(row['File']).name, row['RuleID']) for row in findings}
        expected = {('provider-control.yaml', 'github-pat'), ('refs.yaml', 'github-pat')}
        assert expected <= pairs <= expected | generic_pairs, (name, pairs)
        if name == 'proposed':
            assert generic_pairs <= pairs, (name, pairs)
        summary[name] = sorted(pairs)
print(json.dumps({'findings': summary, 'active_configuration_changed': False,
    'reviewed_generic_controls_detected': generic_pairs <= set(map(tuple, summary['reviewed'])),
    'proposed_generic_controls_detected': generic_pairs <= set(map(tuple, summary['proposed'])),
    'meaning': 'Provider controls must remain detected in both configurations. Generic-control booleans expose whether non-citation matches are suppressed. No live credential or external request.'}, indent=2))
