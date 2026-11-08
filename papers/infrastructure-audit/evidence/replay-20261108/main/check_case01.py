"""Counts-only, offline independent membership and regional-support check."""
import argparse
import csv
import hashlib
import io
import json
import platform
import zipfile
from collections import defaultdict
from pathlib import Path


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive', type=Path)
    p.add_argument('public_snapshot', type=Path)
    p.add_argument('replayed_support', type=Path)
    p.add_argument('expected_support', type=Path)
    a = p.parse_args()
    chunks = sorted(a.public_snapshot.glob('occurrences__p*.csv'))
    assert len(chunks) == 15
    public = set()
    for chunk in chunks:
        with chunk.open(newline='') as f:
            public.update(row['occurrence_no'] for row in csv.DictReader(f))
    with zipfile.ZipFile(a.archive) as z:
        name = next(n for n in z.namelist() if n.endswith('/Mollusca_data.csv'))
        raw = z.read(name)
        ids = [row['occurrence_no'] for row in csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))]
    members = set(ids)
    missing = len(members - public)
    by_subset = defaultdict(lambda: defaultdict(set))
    totals = defaultdict(int)
    with a.replayed_support.open(newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    for row in rows:
        subset = row['subset']
        totals[subset] += int(row['occurrences'])
        if row['band'] == '0-20' and row['region'] not in {'EU', 'NAm', 'UNKNOWN'} and int(row['cells_ge2_within_region_band']) > 0:
            by_subset[subset][row['stage']].add(row['region'])
    eligible = {s: sum(len(regions) >= 3 for regions in stages.values()) for s, stages in by_subset.items()}
    assert len(ids) == len(members) == 368760
    assert len(public) == 1782649 and missing == 71103
    assert totals == {'original': 69931, 'dated_public_member': 60103}
    assert eligible == {'original': 14, 'dated_public_member': 12}
    assert sha(a.replayed_support) == sha(a.expected_support)
    print(json.dumps({
        'case': 1, 'python': platform.python_version(),
        'source_archive_sha256': sha(a.archive),
        'taxon_member_sha256': hashlib.sha256(raw).hexdigest(),
        'public_snapshot_chunk_sha256': {x.name: sha(x) for x in chunks},
        'replayed_support_sha256': sha(a.replayed_support),
        'support_matches_committed_table': True, 'support_rows': len(rows),
        'public_snapshot_distinct_occurrences': len(public),
        'deposit_mollusca_distinct_occurrences': len(members),
        'deposit_mollusca_present_in_snapshot': len(members & public),
        'deposit_mollusca_absent_from_snapshot': missing,
        'mollusca_absent_fraction': missing / len(members),
        'selected_occurrences': totals,
        'stages_with_three_outside_tropical_regions': eligible,
        'stages_tested': len({r['stage'] for r in rows}),
        'limit': 'Membership is dated 2026-10-23; absence alone does not establish restriction status or a current access failure. Support is the cheap presence diagnostic, not estimator eligibility. No identifiers exported.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
