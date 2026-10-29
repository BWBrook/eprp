"""Offline aggregate-only presence screen of the retained Benson Mollusca deposit."""
import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import zipfile


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def regions(path):
    with (path / 'country_codes.csv').open() as f:
        codes = list(csv.DictReader(f))
    names = {r[k].strip().lower(): r['ISO3166-1-Alpha-2'] for r in codes
             for k in ['official_name_en', 'CLDR display name'] if r[k]}
    names.update({'united kingdom': 'GB', 'moldova, republic of': 'MD',
                  'bosnia & herzegovina': 'BA', 'united states': 'US',
                  'hong kong sar china': 'HK', 'taiwan, province of china': 'TW',
                  'myanmar (burma)': 'MM', 'palestinian territories': 'PS',
                  "cote d'ivoire": 'CI', 'united states minor outlying islands (the)': 'UM'})
    result = {}
    with (path / 'marine_regions.csv').open() as f:
        for r in csv.DictReader(f):
            code = names[r['country_name'].strip().lower()]
            if code in result and result[code] != r['region_code']:
                raise ValueError('Conflicting static country mapping')
            result[code] = r['region_code']
    return result


def stages(path):
    with (path / 'pbdb_time_int.csv').open() as f:
        rows = [r for r in csv.DictReader(f) if r['scale_no'] == '1']
    by_id = {r['interval_no']: r for r in rows}
    selected = []
    for r in rows:
        if r['scale_level'] != '5':
            continue
        ancestors, seen, q = [], set(), r
        while q['interval_no'] not in seen:
            seen.add(q['interval_no']); ancestors.append(q['interval_name'])
            if q['parent_no'] not in by_id:
                break
            q = by_id[q['parent_no']]
        periods = set(ancestors) & {'Cretaceous', 'Paleogene'}
        if periods:
            selected.append((r['interval_name'], float(r['max_ma']), float(r['min_ma']), periods.pop()))
    return sorted(selected, key=lambda r: r[1])


def write_tsv(path, rows):
    with path.open('x', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
        w.writeheader(); w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive', type=Path); p.add_argument('public', type=Path)
    p.add_argument('static', type=Path); p.add_argument('output', type=Path)
    a = p.parse_args()
    inputs = [a.archive] + sorted(a.public.glob('occurrences__p*.csv')) + [a.static / n for n in ['country_codes.csv', 'marine_regions.csv', 'pbdb_time_int.csv']]
    if len(inputs) != 19:
        raise ValueError('Expected archive, 15 public chunks and three static files')
    signatures = {str(x): (x.stat().st_size, x.stat().st_mtime_ns) for x in inputs}
    hashes = {str(x): digest(x) for x in inputs}
    public = set()
    for path in inputs[1:16]:
        with path.open(newline='') as f:
            public.update(r['occurrence_no'] for r in csv.DictReader(f))
    if len(public) != 1782649:
        raise ValueError('Unexpected dated public membership cardinality')
    mapping, st = regions(a.static), stages(a.static)
    stats, member_hashes = Counter(), {}
    groups = defaultdict(lambda: {'occurrences': 0, 'collections': set(), 'cells': defaultdict(set)})
    stage_cells = defaultdict(lambda: defaultdict(set))
    with zipfile.ZipFile(a.archive) as z:
        taxon = next(n for n in z.namelist() if n.endswith('/Mollusca_data.csv'))
        source = next(n for n in z.namelist() if n.endswith('/Animalia^Chordata_data.csv'))
        mollusc = set()
        data = z.read(taxon); member_hashes[taxon] = hashlib.sha256(data).hexdigest()
        for r in csv.DictReader(io.StringIO(data.decode('utf-8-sig'))):
            stats['mollusca_member_rows'] += 1
            mollusc.add(r['occurrence_no'])
        stats['mollusca_member_distinct'] = len(mollusc)
        stats['mollusca_member_public'] = len(mollusc & public)
        data = z.read(source); member_hashes[source] = hashlib.sha256(data).hexdigest()
        seen = set()
        for r in csv.DictReader(io.StringIO(data.decode('utf-8-sig'))):
            oid = r['occurrence_no']
            if oid not in mollusc:
                continue
            if oid in seen:
                raise ValueError('Duplicate Mollusca occurrence in geographic member')
            seen.add(oid); stats['joined_mollusca'] += 1
            stats['joined_public'] += oid in public
            stats['joined_phylum_not_mollusca'] += r['phylum'] != 'Mollusca'
            if r['accepted_rank'] not in {'genus','subgenus','species'} or not r['genus'] or r['lithification1'] == 'unlithified':
                continue
            stats['rank_genus_lithification_pass'] += 1
            try:
                lat, lon, hi, lo = map(float, [r['paleolat'],r['paleolng'],r['max_ma'],r['min_ma']])
            except ValueError:
                continue
            if not all(map(math.isfinite,[lat,lon,hi,lo])) or not (-90<=lat<=90 and -180<=lon<=180 and hi>=lo):
                continue
            stats['coordinate_age_valid'] += 1
            matches = [s for s in st if lo >= s[2]-1e-9 and hi <= s[1]+1e-9]
            if len(matches) > 1:
                stats['ambiguous_stage_rows'] += 1
                continue
            if not matches:
                continue
            name = matches[0][0]; band = '0-20' if abs(lat)<20 else '20-40' if abs(lat)<40 else '>=40'
            cc = {'UK':'GB','AA':'AQ','FA':'FK'}.get(r['cc'],r['cc'])
            region = mapping.get(cc, 'UNKNOWN')
            stats['selected_unmapped_nonempty_country'] += bool(cc) and region == 'UNKNOWN'
            li = math.floor((lat+90)/5); mid = -90+(li+.5)*5
            # Match numpy's ties-to-even rounding in the original cheap screen.
            nl = max(1, round(72*math.cos(math.radians(mid))))
            cell = li*1000+math.floor((lon+180)/360*nl)
            for subset in ['original'] + (['dated_public_member'] if oid in public else []):
                stats[subset+'_selected_occurrences'] += 1
                g = groups[subset,name,band,region]
                g['occurrences'] += 1; g['collections'].add(r['collection_no']); g['cells'][cell].add(r['collection_no'])
                stage_cells[subset,name][cell].add(r['collection_no'])
        stats['mollusca_not_in_geographic_member'] = len(mollusc-seen)
    rows, overlap = [], []
    for subset in ['original','dated_public_member']:
        for name,hi,lo,period in st:
            for region in sorted(set(mapping.values())|{'UNKNOWN'}):
                eligible_bands=[]
                for band in ['0-20','20-40','>=40']:
                    g=groups[subset,name,band,region]
                    eligible = sum(len(v)>=2 for v in g['cells'].values())
                    if eligible: eligible_bands.append(band)
                    rows.append(dict(subset=subset,period=period,stage=name,stage_base_ma=hi,stage_top_ma=lo,band=band,region=region,occurrences=g['occurrences'],collections=len(g['collections']),cells=len(g['cells']),cells_ge2_within_region_band=eligible,cells_ge2_within_stage=sum(len(stage_cells[subset,name][c])>=2 for c in g['cells'])))
                overlap.append(dict(subset=subset,period=period,stage=name,region=region,bands_with_eligible_cells=','.join(eligible_bands),n_bands=len(eligible_bands),tropical_mid_overlap=int('0-20' in eligible_bands and '20-40' in eligible_bands),all_three_overlap=int(len(eligible_bands)==3)))
    for subset in ['original','dated_public_member']:
        stats[subset+'_selected_collections'] = len(set().union(*(g['collections'] for (sub,_,_,_),g in groups.items() if sub == subset)))
        cells = [v for (sub,_),cs in stage_cells.items() if sub == subset for v in cs.values()]
        stats[subset+'_stage_cells'] = len(cells)
        stats[subset+'_stage_cells_ge2'] = sum(len(v)>=2 for v in cells)
        stats[subset+'_region_band_cells_ge2'] = sum(r['cells_ge2_within_region_band'] for r in rows if r['subset']==subset)
    for x in inputs:
        if signatures[str(x)] != (x.stat().st_size,x.stat().st_mtime_ns):
            raise ValueError('An input changed')
    a.output.mkdir(exist_ok=False)
    write_tsv(a.output/'support.tsv', rows); write_tsv(a.output/'region-band-overlap.tsv',overlap)
    summary={'counts':dict(stats),'public_snapshot_unique_occurrences':len(public),'input_sha256':hashes,'archive_members_sha256':member_hashes,'stages':st,'region_codes':sorted(set(mapping.values())),'builder_sha256':digest(Path(__file__)),'output_sha256':{n:digest(a.output/n) for n in ['support.tsv','region-band-overlap.tsv']}}
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'counts':dict(stats),'stages':len(st)},sort_keys=True))

if __name__=='__main__':
    main()
