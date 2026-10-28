#!/usr/bin/env python3
"""Align deposited nannofossil tables without inventing ages or taxonomic equivalences."""
import argparse
import csv
import hashlib
import io
import json
import statistics
from decimal import Decimal
from pathlib import Path

IDS = ('893899', '893919', '997794', '997781', '997793')
TAXA = ('Neobiscutum', 'Praeprinsius', 'Cruciplacolithus', 'Coccolithus')


def read_source(path):
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    before, sep, data = text.partition('*/')
    if not sep:
        raise ValueError(f'PANGAEA metadata delimiter missing: {path}')
    rows = list(csv.DictReader(io.StringIO(data.lstrip('\r\n')), delimiter='\t'))
    if not rows:
        raise ValueError(f'No data rows in {path}')
    return rows, hashlib.sha256(raw).hexdigest()


def key(row):
    return row['H'], row['Core'], row['Depth sect [cm]']


def unique(rows, label):
    result = {key(r): r for r in rows}
    if len(result) != len(rows):
        raise ValueError(f'duplicate hole/core/depth key in {label}')
    return result


def save(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def build(input_dir, output_dir):
    data, hashes = {}, {}
    for ident in IDS:
        data[ident], hashes[ident] = read_source(input_dir / f'pangaea-{ident}.txt')
    raw, counts, percentages = (unique(data[i], i) for i in ('997794', '997781', '997793'))
    if counts.keys() != percentages.keys() or not counts.keys() <= raw.keys():
        raise ValueError('Source sample key mismatch')
    age_cols = [x for x in next(iter(counts.values())) if x.startswith('Age [Ma]')]
    if len(age_cols) != 2:
        raise ValueError('Expected both source age columns')
    rows = []
    max_pct_error = Decimal(0)
    for k, raw_row in raw.items():
        c, p = counts.get(k), percentages.get(k)
        row = {'hole': k[0], 'core': k[1], 'depth_section_cm': k[2],
               'source_depth_composite_rmcd': raw_row['Depth comp r [rmcd]'],
               'source_age_model_1_ma': '', 'source_age_model_2_ma': '', 'paired_dominant_table': str(bool(c)).lower()}
        row.update({taxon + '_pct': '' for taxon in TAXA})
        if c:
            for a in age_cols:
                if c[a] != p[a]:
                    raise ValueError(f'count/percentage age mismatch for {k}')
            row['source_age_model_1_ma'], row['source_age_model_2_ma'] = (c[a] for a in age_cols)
            fields = [x for x in c if x.endswith('[#]')]
            denom = sum(Decimal(c[x]) for x in fields if c[x])
            if denom:
                for name in fields:
                    value, pct = c[name], p[name.replace('[#]', '[%]')]
                    if value and pct:
                        max_pct_error = max(max_pct_error, abs(100 * Decimal(value) / denom - Decimal(pct)))
            row.update({taxon + '_pct': p[taxon + ' [%]'] for taxon in TAXA})
        rows.append(row)
    if max_pct_error > Decimal('0.000001'):
        raise ValueError(f'count/percentage mismatch: {max_pct_error}')
    pacific = []
    for r in data['893899']:
        small, large = r['Cruciplacolithus spp. [%] (small)'], r['Cruciplacolithus spp. [%] (large)']
        cruc = str(Decimal(small) + Decimal(large)) if small and large else ''
        pacific.append({'source_age_ka_bp': r['Age [ka BP]'],
                        'Neobiscutum_pct': r['Neobiscutum spp. [%]'],
                        'Praeprinsius_pct': r['Praeprinsius spp. [%]'],
                        'Cruciplacolithus_pct': cruc, 'Coccolithus_pct': r['Coccolithus spp. [%]']})
    output_dir.mkdir(parents=True, exist_ok=True)
    save(output_dir / 'el-kef-private.tsv', rows, list(rows[0]))
    save(output_dir / 'pacific-private.tsv', pacific, list(pacific[0]))
    differences = [abs(float(r[age_cols[0]]) - float(r[age_cols[1]])) * 1000 for r in counts.values()]
    events = {}
    for r in data['893919']:
        events[r['Event']] = events.get(r['Event'], 0) + 1
    result = {'input_sha256': hashes, 'source_rows': {k: len(v) for k, v in data.items()},
              'el_kef_unique_raw': len(raw), 'el_kef_dated': len(counts),
              'el_kef_raw_without_age': len(raw.keys() - counts.keys()),
              'age_model_difference_kyr_max': max(differences),
              'age_model_difference_kyr_median': statistics.median(differences),
              'age_model_difference_nonzero': sum(d > 1e-8 for d in differences),
              'max_count_percentage_error': str(max_pct_error),
              'alvarez_sample_events': events, 'aligned_taxa': list(TAXA),
              'qualifications': ['ODP ages remain ka BP; Jones ages remain source Ma values',
                 'ODP data interpolated, selected taxa only; percentages need not sum to 100',
                 'El Kef undated rows retained with blank percentages and ages',
                 'Cruciplacolithus ODP small and large size classes combined when both present',
                 'PANGAEA.893899 is CC BY-NC-ND 3.0; derived data kept private',
                 'no sample matching or ecological hypothesis test between sites']}
    (output_dir / 'summary.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    build(args.input, args.output)
