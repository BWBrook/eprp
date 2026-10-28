#!/usr/bin/env python3
"""Join Alvarez's original sample percentages to PANGAEA sample metadata privately."""
import argparse
import collections
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from decimal import Decimal
from pathlib import Path

from align import read_source, save

NS = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
SELECTED = {'AJ': 'Coccolithus', 'AP': 'Neobiscutum', 'AQ': 'Praeprinsius'}


def column_name(n):
    s = ''
    while n:
        n, i = divmod(n - 1, 26)
        s = chr(65 + i) + s
    return s


def read_workbook(path):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with zipfile.ZipFile(path) as archive:
        shared = ET.fromstring(archive.read('xl/sharedStrings.xml'))
        strings = [''.join(si.itertext()) for si in shared.findall('x:si', NS)]
        sheet = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
    if sheet.findall('.//x:f', NS):
        raise ValueError('Unexpected formula in source workbook')
    rows = {}
    for row in sheet.findall('.//x:row', NS):
        cells = {}
        for cell in row.findall('x:c', NS):
            col = re.match(r'([A-Z]+)', cell.attrib['r']).group(1)
            value = cell.find('x:v', NS)
            if cell.attrib.get('t') == 'inlineStr':
                cells[col] = ''.join(cell.find('x:is', NS).itertext())
            elif value is not None:
                cells[col] = strings[int(value.text)] if cell.attrib.get('t') == 's' else value.text
        rows[int(row.attrib['r'])] = cells
    headers = rows[8]
    columns = [column_name(i) for i in range(30, 90)]
    if any(not headers.get(c) for c in columns) or headers.get('CL'):
        raise ValueError('Unexpected original abundance columns')
    expected = {'AJ': 'coccolithus', 'AL': 'cruciplacolithus_small', 'AM': 'cruciplacolithus_large',
                'AP': 'neobiscutum', 'AQ': 'praeprinsius', 'AC': 'Age_(Myr_ago)'}
    if any(headers.get(c, '').strip() != v for c, v in expected.items()):
        raise ValueError('Unexpected workbook taxonomy or age header')
    if any(n > 8 and any(row.get(c) for c in ('Q', 'R', 'S', 'T', 'U', 'V', 'W')) and not row.get('AC')
           for n, row in rows.items()):
        raise ValueError('Workbook sample metadata without an age')
    samples = [(n, row) for n, row in sorted(rows.items()) if n > 8 and row.get('AC')]
    if not samples:
        raise ValueError('No source sample rows')
    return samples, headers, columns, digest


def cm_label(value):
    number = Decimal(value)
    nearest = number.to_integral_value()
    return str(nearest) if abs(number - nearest) < Decimal('1e-8') else format(number.normalize(), 'f')


def sample_label(row):
    site = row['R'].removeprefix('U')
    result = f"198-{site}{row['S']}-{row['T']}{row['U']}-{row['V']},{cm_label(row['W'])}"
    return result + ('-' + cm_label(row['X']) if row.get('X') else '')


def build(workbook, table_e, output):
    samples, headers, columns, workbook_hash = read_workbook(workbook)
    deposited, table_hash = read_source(table_e)
    by_label = {r['Sample label']: r for r in deposited}
    if len(by_label) != len(deposited):
        raise ValueError('Duplicate PANGAEA sample label')
    originals = {sample_label(r): (n, r) for n, r in samples}
    if len(originals) != len(samples):
        raise ValueError('Duplicate workbook sample label')
    if originals.keys() != by_label.keys():
        raise ValueError('Workbook and PANGAEA sample labels do not agree')
    differences = {name: [] for name in ('mbsf', 'rmcd', 'armcd', 'age_ka')}
    comparisons = [('Z', 'Depth sed [m]', 'mbsf', Decimal(1), Decimal('.005')),
                   ('AA', 'Depth comp r [rmcd]', 'rmcd', Decimal(1), Decimal('.005')),
                   ('AB', 'Depth adj rmcd [armcd]', 'armcd', Decimal(1), Decimal('.005')),
                   ('AC', 'Age [ka BP]', 'age_ka', Decimal(1000), Decimal('.5'))]
    metadata = [column_name(i) for i in range(17, 30)]
    rows = []
    for label, (number, r) in originals.items():
        p = by_label[label]
        for col, pname, name, scale, tolerance in comparisons:
            a, b = r.get(col, ''), p.get(pname, '')
            if bool(a) != bool(b):
                raise ValueError(f'Asymmetric {name} missingness: {label}')
            if a:
                delta = abs(Decimal(a) * scale - Decimal(b))
                if delta > tolerance + Decimal('1e-8'):
                    raise ValueError(f'{name} outside published precision: {label}')
                differences[name].append(delta)
        entry = {'sample_label': label, 'event': p['Event'], 'provider_investigator': p['Investigator'],
                 'source_excel_row': number}
        entry.update({f'source_{col}_{headers[col].strip()}': r.get(col, '') for col in metadata})
        entry.update({f'source_{col}_{headers[col].strip()}_pct': r.get(col, '') for col in columns})
        for col, name in SELECTED.items():
            entry[name + '_pct'] = r.get(col, '')
        small, large = r.get('AL', ''), r.get('AM', '')
        entry['Cruciplacolithus_pct'] = str(Decimal(small) + Decimal(large)) if small and large else ''
        rows.append(entry)
    output.mkdir(parents=True, exist_ok=True)
    save(output / 'pacific-original-percentages-private.tsv', rows, list(rows[0]))
    result = {'workbook_sha256': workbook_hash, 'pangaea_893919_sha256': table_hash,
              'original_samples': len(rows), 'workbook_abundance_columns': len(columns),
              'sample_events': dict(collections.Counter(r['event'] for r in rows)),
              'source_investigators': dict(collections.Counter(r['Q'] for _, r in samples)),
              'source_abundance_blanks': sum(not r.get(c, '') for _, r in samples for c in columns),
              'source_abundance_explicit_zeroes': sum(r.get(c, '') != '' and Decimal(r[c]) == 0
                                                      for _, r in samples for c in columns),
              'matching_checks': {k: {'compared': len(v), 'max_absolute_difference': str(max(v)) if v else None}
                                  for k, v in differences.items()},
              'qualifications': ['Original observations are percentages, not integer counts',
                  'Excel floating artifacts normalized only while constructing sample-label join keys',
                  'Blanks are preserved, not replaced by zero; original workbook fields are retained',
                  'Comparable names are a provisional crosswalk, not validated taxonomic equivalence',
                  'Private derived table includes source material with unconfirmed redistribution rights',
                  'No cross-site age harmonization or ecological hypothesis test']}
    (output / 'pacific-original-summary.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('workbook', type=Path)
    p.add_argument('pangaea_table_e', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    build(a.workbook, a.pangaea_table_e, a.output)
