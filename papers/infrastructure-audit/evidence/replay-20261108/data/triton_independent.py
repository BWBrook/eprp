"""Independent Python group keys, conservative deletion and Q012 bin means.

python3 triton_independent.py REMOTE_WORK_DIR
Projection and deletion indices remain on data host. The final receipt is counts only.
"""
import collections
import csv
import gzip
import hashlib
import json
import math
import pathlib
import statistics
import sys

work = pathlib.Path(sys.argv[1])
out = work / 'out'
priority = ['ForCenS', 'IODP', 'Neptune', 'Pangaea', 'Lloydetal2012', 'Fentonetal2016']
with gzip.open(work / 'projection.tsv.gz', 'rt') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
groups = collections.defaultdict(list)
for r in rows:
    key = (r['species'], float(r['abundance']), float(r['sample.depth']) if r['sample.depth'] else None,
           float(r['latitude_key']) if r['latitude_key'] else None, float(r['longitude_key']) if r['longitude_key'] else None)
    groups[key].append(r)
drop = set()
counts = collections.Counter()
for key, group in groups.items():
    if len(group) < 2:
        continue
    cross = len({r['db.source'] for r in group}) > 1
    counts['cross_source_groups' if cross else 'within_source_groups'] += 1
    counts['cross_source_excess_rows' if cross else 'within_source_excess_rows'] += len(group)-1
    if cross and key[2] is not None:
        best = min(priority.index(r['db.source']) for r in group)
        drop.update(int(r['row_index']) for r in group if priority.index(r['db.source']) > best)
(work / 'drop_rows.txt').write_text(''.join(str(i) + '\n' for i in sorted(drop)))
counts['rows_in'] = len(rows)
counts['rows_dropped'] = len(drop)
counts['rows_out'] = len(rows)-len(drop)
counts['duplicate_excess_total'] = sum(len(v)-1 for v in groups.values())
if '--prepare-only' in sys.argv:
    print(json.dumps(dict(counts)))
    sys.exit(0)


def table(p):
    return list(csv.DictReader(p.open(), delimiter='\t'))


sp = [r for r in table(work / 'inputs/species.tsv') if r['in_scope'] == 'True']
le = [r for r in table(work / 'inputs/lineage_edges.tsv') if r['in_scope'] == 'True']
xw = {r['triton_name']: r['s1_name'] for r in table(work / 'inputs/name_crosswalk.tsv') if r['s1_name']}
ranges = {r['morphospecies'].strip(): (float(r['end_Ma']), float(r['start_Ma'])) for r in sp}
members = collections.defaultdict(set)
for r in sp:
    for lin in r['lineages'].split(';'):
        if lin:
            members[lin].add(r['morphospecies'].strip())
kept = []
for r in rows:
    species = xw.get(r['species'].strip())
    if r['trim'] != 'inc' or not r['pal.lat'] or not r['age'] or species not in ranges:
        continue
    age = float(r['age'])
    if ranges[species][0] <= age <= ranges[species][1]:
        kept.append((species, age, abs(float(r['pal.lat'])), int(r['row_index'])))


def build(dedup):
    result = {}
    for lin in le:
        name = lin['lineage']
        young, old = float(lin['end_Ma']), float(lin['start_Ma'])
        bins = list(range(max(math.floor(young), math.ceil(old)-1), math.floor(young)-1, -1))
        bybin = collections.defaultdict(list)
        for species, age, lat, index in kept:
            if species in members[name] and young <= age <= old and (not dedup or index not in drop):
                bybin[math.floor(age)].append(lat)
        obs = {b: statistics.fmean(bybin[b]) if bybin[b] else None for b in bins}
        for b in bins:
            candidates = [q for q in [b+1, b+2] if q in obs and obs[q] is not None]
            result[(name, b)] = {'n_occ': len(bybin[b]), 'observed_mean_abs_pal_lat': obs[b],
                                  'used_value': obs[candidates[0]] if candidates else None}
    return result


before, after = build(False), build(True)
checks = {}
for label, expected in [('before', before), ('after', after)]:
    actual = table(out / label / 'q012/lineage_bin_E.tsv')
    disagreements = collections.Counter()
    rounding_differences = collections.Counter()
    for r in actual:
        py = expected[(r['lineage'], int(r['bin']))]
        for k in ['n_occ', 'observed_mean_abs_pal_lat', 'used_value']:
            a = None if r[k] == 'NA' else float(r[k])
            b = py[k]
            tolerance = 0 if k == 'n_occ' else .000500001
            if (a is None) != (b is None) or (a is not None and abs(a-b) > tolerance):
                disagreements[k] += 1
            if a is not None and round(b, 3) != a:
                rounding_differences[k] += 1
    checks[label] = {'rows': len(actual), 'independent_python_mismatches': dict(disagreements),
                     'three_decimal_tie_rounding_differences': dict(rounding_differences),
                     'verification_tolerance_degrees': .000500001,
                     'tolerance_reason': 'R outputs to 3 decimal places. Independent full-precision means/lagged means must lie within half that display unit; occurrence counts exact.'}
    assert len(actual) == len(expected)
    assert not disagreements, disagreements
diffs = {}
for col in ['observed_mean_abs_pal_lat', 'used_value']:
    ds = [abs(before[k][col]-after[k][col]) for k in before if before[k][col] is not None and after[k][col] is not None]
    diffs[col] = {'paired_nonmissing_bins': len(ds), 'changed_gt_1e-9': sum(d > 1e-9 for d in ds), 'changed_ge_1degree': sum(d >= 1-1e-9 for d in ds), 'max_absolute_change_degrees': max(ds)}
counts['by_source_dropped'] = dict(collections.Counter(r['db.source'] for r in rows if int(r['row_index']) in drop))
(out / 'triton_independent.json').write_text(json.dumps({'dedup': dict(counts), 'source_priority': priority, 'q012_independent_checks': checks, 'q012_bin_differences': diffs,
    'route': 'Python numeric-tuple grouping and species-lineage bin membership/full-precision means/older-bin lag independently implemented. R only loads raw RData; paired R builds use original builder body.',
    'limitations': ['Key collisions are not themselves proof of duplicate physical observations.', 'EPRP support quantities, no fitted biological outcome or external published analysis.']}, indent=2) + '\n')
