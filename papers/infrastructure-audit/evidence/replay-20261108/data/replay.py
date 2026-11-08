"""Offline, counts-only independent checks. Execute on the authorised data host.

python3 replay.py DATA_ROOT OUTPUT_DIR [pbdb nsb fr2]
Only OUTPUT_DIR is written; no provider calls or occurrence identifiers emitted.
"""
import bisect
import collections
import csv
import hashlib
import io
import json
import os
import pathlib
import platform
import sqlite3
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
inputs = {}


def pin(p):
    p = pathlib.Path(p)
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    label = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else p.name
    inputs[label] = {'sha256': h.hexdigest(), 'bytes': p.stat().st_size}


def save(name, value):
    (OUT / (name + '.json')).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def xlsx(p):
    """Read first worksheet via ZIP/XML, independent of original openpyxl route."""
    pin(p)
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(p) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
        rows = []
        for r in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:sheetData/m:row', ns):
            cells = {}
            for c in r.findall('m:c', ns):
                ref = ''.join(t for t in c.attrib['r'] if t.isalpha())
                idx = 0
                for t in ref:
                    idx = idx * 26 + ord(t) - 64
                v = c.find('m:v', ns)
                text = '' if v is None else v.text or ''
                typ = c.get('t', 'n')
                if typ == 's':
                    text = strings[int(text)]
                elif typ == 'inlineStr':
                    text = ''.join(c.find('m:is', ns).itertext())
                cells[idx - 1] = (text.strip(), typ)
            if any(v[0] for v in cells.values()):
                rows.append(cells)
        return rows


def fr2():
    raw = ROOT / 'classic-compendia/fr2/bristol/raw/2026-10-23T0505Z_url'
    chapters = sorted(raw.glob('[0-9]*-*.xlsx'), key=lambda p: int(p.name.split('-')[0]))
    seq = []
    for p in chapters:
        for row in xlsx(p):
            seq.append((int(p.name.split('-')[0]), [row.get(i, ('', ''))[0] for i in range(92)]))
    life = [[row.get(i, ('', ''))[0] for i in range(92)] for row in xlsx(raw / 'All-Life.xlsx')][1:]
    assert len(life) == len(seq)
    kinds, by_chapter, extras = collections.Counter(), collections.Counter(), collections.Counter()
    for (ch, a), b in zip(seq, life):
        assert a[0].split() == b[0].split()
        if a == b:
            kinds['identical'] += 1
            continue
        if a[1:] == b[1:]:
            kinds['name_spacing'] += 1
            continue
        differences = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
        start = differences[0]
        shifted = all(b[i] == a[i + 1] for i in range(start, 91)) and not a[start]
        if shifted:
            cls = 'NFR_into_Holocene' if a[91] == 'NFR' and not any(a[5:91]) else 'habitat_and_range_shift' if start < 5 else 'range_shift'
            kinds[cls] += 1
            by_chapter[ch] += 1
            old_presence, new_presence = bool(a[90]) and a[90] != 'NFR', bool(b[90]) and b[90] != 'NFR'
            extras['literal_nonempty_Holocene_gain'] += int(bool(b[90]) and not bool(a[90]))
            extras['valid_code_Holocene_gain'] += int(new_presence and not old_presence)
        else:
            kinds['unexplained'] += 1
    save('fr2', {'rows': len(life), 'chapters': len(chapters), 'classes': kinds, 'shifted_by_chapter': by_chapter, 'diagnostics': extras,
                 'route': 'Direct OOXML cell vectors, aligned family names; exact shifted-tail equality. No original profiler imported.',
                 'limitation': 'Earliest Wayback copies not decoded in this replay. NFR is not a valid presence code: apparent Holocene inflation depends on parser.'})


def nsb():
    versions = ['2014-08-16_8238614', '2019-08-30_10059743', '2022-10-06_10063084', '2023-06-05_10063218']
    saved = {}
    for version in versions:
        p = ROOT / 'nsb/derived' / version / 'nsb.sqlite'
        pin(p)
        con = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
        models = collections.defaultdict(list)
        for hole, depth, age in con.execute("select m.site_hole,m.depth_mbsf,m.age_ma from neptune_age_model m join neptune_age_model_history h on h.site_hole=m.site_hole and h.revision_no=m.revision_no where h.current_flag='Y' and m.depth_mbsf is not null and m.age_ma is not null"):
            models[hole].append((float(depth), float(age)))
        models = {k: sorted(v) for k, v in models.items()}
        depths = {k: [v[0] for v in vs] for k, vs in models.items()}
        counts, holes = collections.Counter(), set()
        duplicate_depth = sum(len(v) - len(set(d for d, a in v)) for v in models.values())
        raw_ages, duplicate_depth_samples, ambiguous_ages = {}, 0, 0
        sensitivity = collections.Counter()
        for sid, hole, depth, stored in con.execute('select s.sample_id,h.site_hole,s.sample_depth_mbsf,s.sample_age_ma from neptune_sample s join neptune_hole_summary h using(hole_id)'):
            raw_ages[sid] = stored
            calc = None
            if hole in models and depth is not None and depths[hole][0] <= depth <= depths[hole][-1]:
                ds, points = depths[hole], models[hole]
                j = bisect.bisect_left(ds, depth)
                if ds[j] == depth:
                    calc = points[j][1]
                    last = bisect.bisect_right(ds, depth)
                    duplicate_depth_samples += last - j > 1
                    ambiguous_ages += len({a for d, a in points[j:last]}) > 1
                    if last-j > 1 and stored is not None:
                        lo, hi = points[j][1], points[last-1][1]
                        sensitivity['samples_differing_gt_001_first_tie'] += abs(stored-lo) > .01
                        sensitivity['samples_differing_gt_001_last_tie'] += abs(stored-hi) > .01
                        sensitivity['agreement_class_changes_first_vs_last'] += (abs(stored-lo) > .01) != (abs(stored-hi) > .01)
                else:
                    d0, a0 = points[j-1]
                    d1, a1 = points[j]
                    calc = (a0 * (d1-depth) + a1 * (depth-d0)) / (d1-d0)
            if stored is None:
                label = 'both undated' if calc is None else 'stored undated, model dates it'
            elif calc is None:
                label = 'stored dated, model cannot' if hole in models else 'stored dated, hole has no current model'
            else:
                diff = abs(stored-calc)
                label = 'agree (<=0.01 Myr)' if diff <= .01 else 'differ 0.01-0.5 Myr' if diff <= .5 else 'differ 0.5-1 Myr' if diff <= 1 else 'differ >1 Myr'
                if diff > .01:
                    holes.add(hole)
            counts[label] += 1
        saved[version] = raw_ages
        save('nsb_' + version[:10], {'classes': counts, 'samples': sum(counts.values()), 'holes_disagreeing': len(holes), 'duplicate_tie_depths': duplicate_depth,
                                   'samples_at_duplicate_depth': duplicate_depth_samples, 'samples_at_conflicting_tie_age': ambiguous_ages,
                                   'exact_duplicate_depth_sensitivity': sensitivity,
                                   'route': 'SQL current-revision join and independent weighted-endpoint interpolation, no extrapolation; first age at exact duplicate depth.'})
        con.close()
    a, b = saved[versions[0]], saved[versions[-1]]
    diffs = [abs(v-b[k]) for k, v in a.items() if v is not None and b.get(k) is not None]
    save('nsb_drift', {'matched_dated_samples': len(diffs), 'absolute_age_change_gt': {str(t): sum(d > t for d in diffs) for t in [.01, .5, 1, 5]},
                       'limitation': 'Magnitude replay, not attribution of changes to time-scale versus model updates.'})


def monarrez():
    from decimal import Decimal
    p = ROOT / 'register-deposits/monarrez2023-selectivity-zenodo/raw/8341743/ESM_Dataset_S1.xlsx'
    rows = xlsx(p)
    header_index = next(j for j, row in enumerate(rows) if any(val[0] == 'ch' for val in row.values()))
    headers = {val[0].lower(): i for i, val in rows[header_index].items()}
    hist = OUT.parent / 'monarrez_histories.tsv'
    pin(hist)
    pin(pathlib.Path(os.environ['EPRP_AUDIT_MONARREZ_RDATA']))
    hist_rows = list(csv.DictReader(hist.open(), delimiter='\t'))
    intact = {r['genus']: r['ch'] for r in hist_rows}
    assert all(intact[r['genus']] == r['ch'] for r in hist_rows)
    assert collections.Counter(r['genus'] for r in hist_rows) == collections.Counter(r[headers['genus']][0] for r in rows[header_index+1:])
    nchar = collections.Counter(map(len, intact.values()))
    counts = collections.Counter()
    assert len(nchar) == 1
    width = next(iter(nchar))
    for row in rows[header_index+1:]:
        genus = row[headers['genus']][0]
        value, typ = row[headers['ch']]
        original = intact[genus]
        assert set(original) <= {'0', '1'}
        decoded = format(Decimal(value), 'f').split('.')[0]
        padded = decoded.zfill(width)
        counts['rows'] += 1
        counts['numeric_xml'] += typ == 'n'
        counts['scientific_notation_xml'] += 'E' in value.upper()
        counts['intact_leading_zero'] += original.startswith('0')
        counts['leading_zero_lost_in_numeric'] += original.startswith('0') and not decoded.startswith('0')
        counts['same_integer_after_discarding_leading_zeros'] += int(original) == int(Decimal(value))
        counts['different_integer_value'] += int(original) != int(Decimal(value))
        counts['fully_recoverable_by_width_padding'] += original == padded
        counts['nonbinary_after_padding'] += bool(set(padded) - {'0', '1'})
        counts['binary_but_wrong_after_padding'] += set(padded) <= {'0', '1'} and padded != original
    save('monarrez', {'classes': counts, 'intact_history_length': width, 'intact_rows': len(hist_rows), 'unique_genus_keys': len(intact), 'duplicate_genus_extra_rows_identical_history': len(hist_rows)-len(intact),
                       'route': 'OOXML numeric cell strings decoded with arbitrary-precision Decimal and matched by genus to R-binary character histories.',
                       'limitations': ['R is used only to deserialize deposited binary; Python compares values. No raw histories or genus identifiers emitted.',
                                       'Fixed known width repairs leading-zero loss for exact integers; it cannot repair altered internal digits. No CMR fit rerun.']})


def pbdb():
    versions = ['20240107_10466717', '20240331_10931491', '20240401_10931518', '20250331_15111554', '20250410_15187705', '20260227_18803370', '20260802_21869245', '20260809_21869343']
    tables = {}
    for v in versions:
        p = ROOT / 'pbdb-chronosphere/tables/raw' / v / 'pbdb_csv.zip'
        pin(p)
        counts = collections.defaultdict(collections.Counter)
        with zipfile.ZipFile(p) as z:
            member = next(n for n in z.namelist() if n.endswith('.csv'))
            with z.open(member) as f:
                for r in csv.DictReader(io.TextIOWrapper(f, encoding='utf-8', newline='')):
                    if r['late_interval'] in ('', 'NA') and r['max_ma'] not in ('', 'NA'):
                        counts[r['early_interval']][round(float(r['max_ma']), 4)] += 1
        tables[v] = {k: (max(c, key=c.get), sum(c.values())) for k, c in counts.items()}
        print('PBDB aggregate completed', v, flush=True)
    comparisons = []
    for va, vb in zip(versions, versions[1:]):
        a, b = tables[va], tables[vb]
        changed = sorted(k for k in a.keys() & b.keys() if a[k][0] != b[k][0] and b[k][1] >= 50)
        both = [k for k in changed if a[k][1] >= 50]
        comparisons.append({'from': va, 'to': vb, 'changed_with_later_n_ge50': len(changed), 'changed_with_both_n_ge50': len(both),
                            'named_boundaries': {k: [a[k][0], b[k][0]] for k in ['Paibian', 'Olenekian', 'Anisian', 'Wuchiapingian'] if k in a and k in b}})
    save('pbdb', {'comparisons': comparisons, 'route': 'Full ZIP CSV streaming to interval/base-age frequency tables; occurrence IDs never selected, stored or output.',
                 'limitations': ['No live API request, so C021 historic-query example not replayed.', 'Coarse saved-snapshot brackets only; fine adjacent-download bracket scans not rerun.', 'C075 ICS chart comparison not replayed here.']})


if __name__ == '__main__':
    for name in sys.argv[3:] or ['pbdb', 'nsb', 'fr2']:
        globals()[name]()
    save('inputs_' + '_'.join(sys.argv[3:] or ['all']), {'python': platform.python_version(), 'inputs': inputs})
