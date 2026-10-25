# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3"]
# ///
"""Reaggregate saved synthetic/public outputs; no extraction or fitting replay.

Run with uv from any directory. Only the six source tables in INPUTS are read.
Outputs are written beside this script. No network or provider API calls occur
inside the script; uv may fetch its pinned Python dependency on first use.
"""
import csv
import hashlib
import io
import json
import statistics
import math
import collections
import platform
from pathlib import Path
import numpy as np
OUTPUT_DIR = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[4]
root = REPO / 'resources/software/bench/results'
INPUTS = {'t2/t2_extinction_A.tsv': 'synthetic estimator outputs; ideal-sampling arm', 't2/t2_extinction_B.tsv': 'synthetic estimator outputs; executed hiatus arm', 't2/t2_extinction_C.tsv': 'synthetic estimator outputs; corrected dating-error arm', 'e2/e2_pyrate_reps.tsv': 'synthetic per-replicate posterior interval and ESS summaries', 't3/t3_flag_ranges.tsv': 'synthetic occurrences and fossilbrush flags', 't3/v6_merged.tsv': 'reconstructions of sampled public collection coordinates'}
input_receipts = []

def rows(path):
    relative = path.relative_to(root).as_posix()
    if relative not in INPUTS:
        raise ValueError(f'Input is not in the bounded replay list: {relative}')
    data = path.read_bytes()
    parsed = list(csv.DictReader(io.StringIO(data.decode('utf-8')), delimiter='\t'))
    input_receipts.append({'path': path.relative_to(REPO).as_posix(), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'rows': len(parsed), 'material': INPUTS[relative]})
    return parsed

def f(r, k):
    return float(r[k])

def avg(x):
    return statistics.mean(x)
out = {}
a = rows(root / 't2/t2_extinction_A.tsv')
b = rows(root / 't2/t2_extinction_B.tsv')
c = rows(root / 't2/t2_extinction_C.tsv')
for arm, rr in [('A', a), ('B', b), ('C', c)]:
    x = [r for r in rr if r['dropped'] == '0']
    z = {'n': len(x), 'dropped': len(rr) - len(x)}
    for name, col in [('tbea_ss', 'tbea_ss_upper'), ('ede_ss', 'ede_ss_upper'), ('robson', 'ede_robson_upper')]:
        z[name] = avg((f(r, 'te_fwd') <= f(r, col) for r in x))
    for v in ['b', 'u']:
        z['griwm_' + v] = avg((min(f(r, 'griwm_' + v + '_q025_fwd'), f(r, 'griwm_' + v + '_q975_fwd')) <= f(r, 'te_fwd') <= max(f(r, 'griwm_' + v + '_q025_fwd'), f(r, 'griwm_' + v + '_q975_fwd')) for r in x))
    z['biased_median_bound'] = avg((f(r, 'te_fwd') <= f(r, 'griwm_b_med') for r in x))
    if arm == 'A':
        for name, est in [('griwm_u', lambda r: f(r, 'griwm_u_med')), ('ss_median', lambda r: f(r, 'last') + f(r, 'range') * (2 ** (1 / (f(r, 'n') - 1)) - 1))]:
            errs = [est(r) - f(r, 'te_fwd') for r in x]
            z[name + '_metrics'] = {'scaled_abs_median': statistics.median((abs(e) / f(r, 'range') for e, r in zip(errs, x))), 'rmse': math.sqrt(avg((e * e for e in errs))), 'before': avg((e < 0 for e in errs))}
        z['ss_agree_0.02'] = avg((abs(f(r, 'tbea_ss_upper') - f(r, 'ede_ss_upper')) <= 0.02 for r in x))
    if arm == 'B':
        ad = {r['case']: r for r in a}
        z['class'] = {}
        for cl in sorted({r['te_class'] for r in x}):
            y = [r for r in x if r['te_class'] == cl]
            z['class'][cl] = {'n': len(y), 'coverage_B': avg((f(r, 'te_fwd') <= f(r, 'tbea_ss_upper') for r in y)), 'paired_A': avg((f(ad[r['case']], 'te_fwd') <= f(ad[r['case']], 'tbea_ss_upper') for r in y))}
        z['mean_fossils_pair'] = [avg((f(ad[r['case']], 'n') for r in x)), avg((f(r, 'n') for r in x))]
    out[arm] = z
x = rows(root / 'e2/e2_pyrate_reps.tsv')
out['pyrate'] = {}
for arm in ['high', 'low']:
    y = [r for r in x if r['arm'] == arm and r['ess_ok'] == '1']
    z = {'n': len(y)}
    for p in ['lambda', 'mu', 'q']:
        z[p] = {'covered': sum((f(r, p + '_lo') <= f(r, p + '_true') <= f(r, p + '_hi') for r in y)), 'median_rel_bias': statistics.median((f(r, p + '_med') / f(r, p + '_true') - 1 for r in y)), 'below': sum((f(r, p + '_true') < f(r, p + '_lo') for r in y)), 'above': sum((f(r, p + '_true') > f(r, p + '_hi') for r in y)), 'min_ess': min((f(r, p + '_ess') for r in y))}
    out['pyrate'][arm] = z
x = rows(root / 't3/t3_flag_ranges.tsv')
z = {}
for label, y in [('injected', [r for r in x if r['injected'] == '1']), ('clean', [r for r in x if r['injected'] == '0'])]:
    flags = [r['fad_flag.5'] == '1' or r['lad_flag.5'] == '1' for r in y]
    pred = [any((r[k] not in ('NA', '', 'nan') and r[k] >= '5' for k in ['fad_diff', 'lad_diff'])) for r in y]
    numeric = [any((r[k] not in ('NA', '', 'nan') and float(r[k]) >= 5 for k in ['fad_diff', 'lad_diff'])) for r in y]
    z[label] = {'n': len(y), 'flagged': sum(flags), 'numeric_flagged': sum(numeric), 'text_prediction_mismatches': sum((a != b for a, b in zip(flags, pred)))}
out['fossilbrush'] = z
x = rows(root / 't3/v6_merged.tsv')
models = ['MERDITH2021', 'PALEOMAP', 'MATTHEWS2016_pmag_ref']
groups = collections.defaultdict(dict)
for r in x:
    if r['model'] in models and r['p_lat'] not in ('', 'NA', 'nan'):
        groups[r['collection_no'], r['age']][r['model']] = float(r['p_lat'])
sp = {k: max(d.values()) - min(d.values()) for k, d in groups.items() if len(d) == 3}
cnt = collections.Counter((k[0] for k in sp))
always = {k for k, v in cnt.items() if v == 6}
out['plate_spread'] = {'n_always': len(always)}
for age in ['10', '50', '100', '200', '300', '400']:
    z = {}
    for label, vals in [('all', [v for k, v in sp.items() if k[1] == age]), ('always', [v for k, v in sp.items() if k[1] == age and k[0] in always])]:
        z[label] = {'n': len(vals), 'median': float(np.median(vals)), 'q90': float(np.quantile(vals, 0.9))}
    out['plate_spread'][age] = z

def unit(lat, lng):
    la, lo = (np.radians(lat), np.radians(lng))
    return np.column_stack((np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)))
out['frame_fit'] = {}
for model in ['TorsvikCocks2017', 'MERDITH2021']:
    out['frame_fit'][model] = {}
    for age in ['10', '50', '100', '200', '300', '400']:
        y = [r for r in x if r['model'] == model and r['age'] == age and (r['p_lat'] not in ('', 'NA', 'nan')) and (r['a_lat'] not in ('', 'NA', 'nan'))]
        p = unit([f(r, 'p_lat') for r in y], [f(r, 'p_lng') for r in y])
        q = unit([f(r, 'a_lat') for r in y], [f(r, 'a_lng') for r in y])
        u, s, vt = np.linalg.svd(p.T @ q)
        rot = u @ np.diag((1, 1, np.linalg.det(u @ vt))) @ vt
        resid = np.degrees(2 * np.arcsin(np.clip(np.linalg.norm(p @ rot - q, axis=1) / 2, 0, 1)))
        out['frame_fit'][model][age] = {'n': len(y), 'rotation_deg': float(np.degrees(np.arccos(np.clip((np.trace(rot) - 1) / 2, -1, 1)))), 'max_residual_deg': float(max(resid))}
result_path = OUTPUT_DIR / 'reaggregate.json'
result_path.write_text(json.dumps(out, indent=2, allow_nan=False) + '\n')
manifest = {'scope': 'Derived-table reaggregation only; not gate-2 source/package clearance', 'inputs': input_receipts, 'runtime': {'python': platform.python_version(), 'python_implementation': platform.python_implementation(), 'numpy': np.__version__, 'platform': platform.platform(), 'machine': platform.machine()}, 'dependency_specification': {'python': '>=3.12,<3.13', 'numpy': '2.1.3'}, 'output': {'path': result_path.relative_to(REPO).as_posix(), 'sha256': hashlib.sha256(result_path.read_bytes()).hexdigest()}}
(OUTPUT_DIR / 'inputs.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Wrote {result_path.relative_to(REPO)} from {len(input_receipts)} synthetic/public tables')
