"""Join paired support-build outputs by declared keys, preserve full diffs."""
import csv
import hashlib
import json
import pathlib
import statistics
import sys

root = pathlib.Path(sys.argv[1])


def read(path):
    return list(csv.DictReader(path.open(), delimiter='\t'))


def diff(file, keys):
    a_path, b_path = root / 'before' / file, root / 'after' / file
    a, b = read(a_path), read(b_path)
    index = lambda rows: {tuple(r[k] for k in keys): r for r in rows}
    ai, bi = index(a), index(b)
    assert len(ai) == len(a) and len(bi) == len(b)
    assert ai.keys() == bi.keys()
    count = {k: sum(ai[j][k] != bi[j][k] for j in ai) for k in a[0] if k not in keys}
    changed_rows = []
    for j in ai:
        if ai[j] == bi[j]:
            continue
        r = dict(zip(keys, j))
        for col in a[0]:
            if col not in keys:
                r[col + '_before'] = ai[j][col]
                r[col + '_after'] = bi[j][col]
        changed_rows.append(r)
    path = root / (file.replace('/', '_').replace('.tsv', '_diff.tsv'))
    if changed_rows:
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(changed_rows[0]), delimiter='\t', lineterminator='\n')
            writer.writeheader()
            writer.writerows(changed_rows)
    return {'rows': len(ai), 'changed_rows': len(changed_rows), 'changed_by_column': count,
            'before_sha256': hashlib.sha256(a_path.read_bytes()).hexdigest(), 'after_sha256': hashlib.sha256(b_path.read_bytes()).hexdigest()}


result = {}
for file, keys in [
    ('q012/lineage_bin_E.tsv', ['lineage', 'bin']),
    ('q012/lineage_coverage.tsv', ['lineage']),
    ('q012/pair_exposure.tsv', ['type', 'lineage_a', 'lineage_b']),
    ('q012/bin_sites.tsv', ['bin']),
    ('q007/event_sites.tsv', ['event', 'site']),
    ('q007/event_summary.tsv', ['event']),
]:
    result[file] = diff(file, keys)
a, b = read(root / 'before/q007/event_sites.tsv'), read(root / 'after/q007/event_sites.tsv')
events = sorted({r['event'] for r in a})
result['q007_sample_totals'] = {}
for e in events:
    n0, n1 = (sum(int(r['n_samples']) for r in rows if r['event'] == e) for rows in (a,b))
    result['q007_sample_totals'][e] = {'before': n0, 'after': n1, 'inflation_relative_to_dedup_pct': 100*(n0/n1-1)}
ea, eb = read(root / 'before/q012/lineage_bin_E.tsv'), read(root / 'after/q012/lineage_bin_E.tsv')
index = lambda rows: {(r['lineage'],r['bin']):r for r in rows}
ea, eb = index(ea), index(eb)
numeric = {}
for col in ['observed_mean_abs_pal_lat', 'used_value', 'E_standardised']:
    ds = [abs(float(ea[k][col])-float(eb[k][col])) for k in ea if ea[k][col] != 'NA' and eb[k][col] != 'NA']
    numeric[col] = {'before_nonmissing': sum(ea[k][col] != 'NA' for k in ea), 'after_nonmissing': sum(eb[k][col] != 'NA' for k in eb),
                    'paired_nonmissing': len(ds), 'paired_changed_gt_1e_9': sum(d>1e-9 for d in ds),
                    'paired_absolute_change_ge_1': sum(d>=1-1e-9 for d in ds), 'max_abs_paired_change': max(ds),
                    'missingness_changed': sum((ea[k][col]=='NA') != (eb[k][col]=='NA') for k in ea)}
result['q012_displayed_numeric_comparison'] = numeric
pair_checks = {}
for label, matrix in [('before',ea),('after',eb)]:
    lineages = {}
    for (lin,bin_), row in matrix.items():
        lineages.setdefault(lin, {})[bin_] = row
    mismatches = {}
    for p in read(root / label / 'q012/pair_exposure.tsv'):
        a, b = lineages[p['lineage_a']], lineages[p['lineage_b']]
        co = a.keys() & b.keys()
        for source_col, per_col, systematic_col, per_prefix, systematic_prefix in [
            ('observed_mean_abs_pal_lat','E_class','E_systematic_class','E','E_systematic'),
            ('used_value','used_perbin_class','used_systematic_class','used_perbin','used_systematic')]:
            bins = sorted(k for k in co if a[k][source_col]!='NA' and b[k][source_col]!='NA')
            diffs = [float(a[k][source_col])-float(b[k][source_col]) for k in bins]
            per = statistics.fmean(abs(d) for d in diffs) if diffs else None
            sy = abs(statistics.fmean(float(a[k][source_col]) for k in bins)-statistics.fmean(float(b[k][source_col]) for k in bins)) if diffs else None
            for col, val, prefix in [(per_col,per,per_prefix),(systematic_col,sy,systematic_prefix)]:
                cls = 'no_coexistence' if not co else 'insufficient' if len(bins)<3 else prefix+('_different' if val>=5 else '_similar')
                if cls != p[col]:
                    mismatches[col] = mismatches.get(col,0)+1
    pair_checks[label] = {'rows':len(read(root / label / 'q012/pair_exposure.tsv')), 'class_mismatches':mismatches,
                          'route':'Python means of joined three-decimal bin values, then original 5-degree and 3-bin rules; no original pair-comparison code called.'}
result['independent_pair_class_reaggregation'] = pair_checks
(root / 'paired_builds.json').write_text(json.dumps(result, indent=2) + '\n')
