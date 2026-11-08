"""Parent review: exact-decimal paired output comparison, no builder imports."""
import csv
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

root = Path(sys.argv[1])


def read(arm, table, keys):
    p = root / arm / 'q012' / table
    with p.open(newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    by_key = {tuple(row[k] for k in keys): row for row in rows}
    assert len(rows) == len(by_key)
    return by_key, hashlib.sha256(p.read_bytes()).hexdigest()


a, ah = read('before', 'lineage_bin_E.tsv', ['lineage', 'bin'])
b, bh = read('after', 'lineage_bin_E.tsv', ['lineage', 'bin'])
assert a.keys() == b.keys()
pairs = [(Decimal(a[k]['observed_mean_abs_pal_lat']), Decimal(b[k]['observed_mean_abs_pal_lat']))
         for k in a if a[k]['observed_mean_abs_pal_lat'] != 'NA' and b[k]['observed_mean_abs_pal_lat'] != 'NA']
lost = sum(a[k]['observed_mean_abs_pal_lat'] != 'NA' and b[k]['observed_mean_abs_pal_lat'] == 'NA' for k in a)
changed = sum(x != y for x, y in pairs)
large = sum(abs(x-y) >= 1 for x, y in pairs)
assert (len(a), len(pairs), changed, large, lost) == (3184, 2267, 1385, 411, 4)
c, ch = read('before', 'pair_exposure.tsv', ['type', 'lineage_a', 'lineage_b'])
d, dh = read('after', 'pair_exposure.tsv', ['type', 'lineage_a', 'lineage_b'])
assert c.keys() == d.keys()
flips = {col: sum(c[k][col] != d[k][col] for k in c) for col in
         ['E_class', 'E_systematic_class', 'used_systematic_class', 'used_perbin_class']}
assert list(flips.values()) == [8, 8, 2, 1]
print(json.dumps({'reviewer': 'main Codex', 'route': 'Independent CSV joins and exact Decimal comparisons of displayed values',
    'total_bin_rows': len(a), 'comparable_displayed_means': len(pairs), 'changed_displayed_means': changed,
    'absolute_change_at_least_one_degree': large, 'newly_missing_observed_means': lost,
    'pair_rows': len(c), 'pair_class_flips': flips,
    'input_sha256': {'before_bins': ah, 'after_bins': bh, 'before_pairs': ch, 'after_pairs': dh},
    'limit': 'Checks displayed outputs and classification counts, not new raw-mean calculations or biological inference.'}, indent=2))
