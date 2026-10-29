"""Remote-only, offline source adapter for the Q027 Albian–Campanian gate.

Private incidence CSVs stay on the authorised compute host. stdout contains
aggregate diagnostics only. Source files are never modified.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re
import time
import zipfile


PRIMARY = ['Animalia^Chordata', 'Chordata^Tetrapoda', 'Tetrapoda']
MARINE = ['Pinnipedimorpha', 'Cetacea', 'Sirenia', 'Sauropterygia',
          'Ichthyosauromorpha', 'Mosasauria', 'Thalattosuchia']
SELECTED = {'Albian', 'Campanian'}
SCHEMA = ['stage', 'plate_model_age', 'source_row', 'occurrence_no',
          'collection_no', 'reference_no', 'genus', 'is_mollusca',
          'is_excluding_unlithified_pass', 'lat', 'lng', 'paleolng',
          'paleolat', 'cc', 'Region', 'lithology1', 'lithification1',
          'environment']
METADATA = ['collection_no', 'reference_no', 'lithology1', 'lithification1',
            'environment', 'cc', 'Region']


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def number(x):
    try:
        out = float(x)
        return out if math.isfinite(out) else None
    except (ValueError, TypeError):
        return None


def integer(x):
    n = number(x)
    return '' if n is None or not (-2147483647 <= n <= 2147483647) else str(int(n))


def missing(x):
    return '' if x in ('', 'NA', None) else x


def majority(hi, lo, stages):
    if hi is None or lo is None or hi <= lo:
        return None
    hits = [name for name, top, base in stages
            if (min(hi, base) - max(lo, top)) / (hi - lo) > .5]
    return hits[0] if len(hits) == 1 else None


def controls():
    st = [('older', 5., 10.), ('younger', 0., 5.)]
    assert majority(10, 5, st) == 'older'
    assert majority(8, 3, st) == 'older'
    assert majority(8, 2, st) is None
    assert majority(5, 5, st) is None
    assert majority(None, 5, st) is None
    assert 'Genus (Subgenus) species'.split(' ')[0] == 'Genus'
    rows = [('coll', 'genus', False), ('coll', 'genus', True)]
    def dedup(rs):
        seen, out = set(), []
        for row in rs:
            if row[:2] not in seen:
                seen.add(row[:2]); out.append(row)
        return out
    assert dedup(rows)[0][2] is False
    assert dedup([r for r in rows if r[2]])[0][2] is True


class Archive:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.hashes = {}

    def member(self, suffix):
        hits = [n for n in self.z.namelist() if n.endswith('/' + suffix)]
        if len(hits) != 1:
            raise ValueError('Ambiguous or absent source member: ' + suffix)
        return hits[0]

    def data(self, suffix):
        name = self.member(suffix)
        data = self.z.read(name)
        self.hashes[name] = hashlib.sha256(data).hexdigest()
        return data

    def text(self, suffix):
        return self.data(suffix).decode('utf-8-sig')

    def rows(self, suffix):
        return csv.DictReader(io.StringIO(self.text(suffix)))


def region_map(code):
    rows = list(code.rows('input/country-codes_csv.csv'))
    names = {r[k].strip().lower(): r['ISO3166-1-Alpha-2'] for r in rows
             for k in ['official_name_en', 'CLDR display name'] if r[k]}
    names.update({'united kingdom': 'GB', 'moldova, republic of': 'MD',
                  'bosnia & herzegovina': 'BA', 'united states': 'US',
                  'hong kong sar china': 'HK', 'taiwan, province of china': 'TW',
                  'myanmar (burma)': 'MM', 'palestinian territories': 'PS',
                  "cote d'ivoire": 'CI', 'united states minor outlying islands (the)': 'UM'})
    out = {}
    for r in code.rows('input/marine_regions.csv'):
        cc = names[r['country_name'].strip().lower()]
        cc = {'GB': 'UK', 'AQ': 'AA', 'FK': 'FA'}.get(cc, cc)
        if cc in out and out[cc] != r['region_code']:
            raise ValueError('Conflicting region map')
        out[cc] = r['region_code']
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--code', type=Path, required=True)
    parser.add_argument('--public', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    a = parser.parse_args()
    controls()
    started = time.monotonic()
    a.output.mkdir(parents=True, exist_ok=False)
    public_files = sorted(a.public.glob('occurrences__p*.csv'))
    if len(public_files) != 15:
        raise ValueError('Expected 15 dated public membership files')
    files = [a.source, a.code] + public_files
    signatures = {str(p): (p.stat().st_size, p.stat().st_mtime_ns) for p in files}
    input_hashes = {str(p): sha(p) for p in files}
    public = set()
    for path in public_files:
        with path.open(newline='') as f:
            public.update(integer(r['occurrence_no']) for r in csv.DictReader(f))
    if len(public) != 1782649 or '' in public:
        raise ValueError('Unexpected public membership set')
    source, code = Archive(a.source), Archive(a.code)
    mollusca = {integer(r['occurrence_no']) for r in source.rows('Mollusca_data.csv')}
    tetrapoda = {integer(r['occurrence_no']) for r in source.rows('Tetrapoda_data.csv')}
    marine = set()
    for name in MARINE:
        marine.update(integer(r['occurrence_no']) for r in source.rows(name + '_data.csv'))
    terms = set(code.text('input/exclude-terms/marine-tetrapod-terms.txt').split())
    terrestrial = set(re.findall(r'"([^"]*)"', code.text('input/exclude-terms/terrestrial_and_freshwater_taxa.R')))
    mapping = region_map(code)
    stages = [(r['interval_name'], float(r['min_ma']), float(r['max_ma']))
              for r in code.rows('input/pbdb_time_int.csv')
              if r['scale_no'] == '1' and r['scale_level'] == '5']
    stage_names = [s[0] for s in stages]
    if len(stage_names) != len(set(stage_names)):
        raise ValueError('Stage names are not unique')
    atlas = defaultdict(list)
    for r in code.rows('input/PaleoDEMS netcdf/PaleoAtlasTimeIntervalsv22b copy.csv'):
        atlas[r['Stratigraphic Age Description']].append(r)
    ages = {}
    for r in code.rows('input/PaleoDEMS netcdf/stages_scotese_lookup_table.csv'):
        if r['bin'] in SELECTED:
            matches = atlas[r['scotese_map_name']]
            if len(matches) != 1:
                raise ValueError('Stage-map join is not one-to-one')
            ages[r['bin']] = float(matches[0]['Plate Model Age'])
    if set(ages) != SELECTED:
        raise ValueError('Missing selected map ages')
    recon = defaultdict(list)
    recon_stats = Counter()
    for r in code.rows('offline_gplates_reconstructions.csv'):
        recon_stats['rows'] += 1
        key = tuple(number(r[k]) for k in ['plate_model_age', 'lat', 'lng'])
        recon[key].append((number(r['paleolng']), number(r['paleolat'])))
    recon_stats['distinct_join_keys'] = len(recon)
    recon_stats['duplicate_join_keys'] = sum(len(v) > 1 for v in recon.values())
    counts = {s: Counter() for s in ['original', 'dated_public_member']}
    seen = {s: set() for s in counts}
    occurrence_ids = {s: set() for s in counts}
    selected_ids = {s: set() for s in counts}
    metadata_coords = {s: defaultdict(set) for s in counts}
    collection_coords = {s: defaultdict(set) for s in counts}
    outfiles = {s: (a.output / (s + '.csv')).open('x', newline='') for s in counts}
    writers = {s: csv.DictWriter(f, fieldnames=SCHEMA) for s, f in outfiles.items()}
    for w in writers.values():
        w.writeheader()
    age_cache = {}
    source_row = 0
    primary_sizes = {}
    for name in PRIMARY:
        rows = source.rows(name + '_data.csv')
        nrows = 0
        for r in rows:
            source_row += 1; nrows += 1
            oid = integer(r['occurrence_no'])
            subsets = ['original'] + (['dated_public_member'] if oid in public else [])
            def passed(gate):
                for subset in subsets:
                    counts[subset][gate] += 1
            passed('membership_rows')
            if not integer(r['geoplate']):
                continue
            passed('geoplate_pass')
            if r['order'] == 'Rodentia' or (oid in tetrapoda and
                    not (oid in marine or any(r[k] in terms for k in ['class', 'order', 'family', 'genus', 'accepted_name']))):
                continue
            passed('marine_tetrapod_pass')
            if any(r[k] in terrestrial for k in ['order', 'family', 'phylum', 'accepted_name', 'class']):
                continue
            passed('terrestrial_names_pass')
            if r['geogscale'] == 'basin':
                continue
            passed('basin_scale_pass')
            if r['stratscale'] == 'group':
                continue
            passed('group_scale_pass')
            if 'soft parts' in r['pres_mode']:
                continue
            passed('soft_parts_pass')
            lat, lng = number(r['lat']), number(r['lng'])
            if lat is None or lng is None or not (-90 <= lat <= 90 and -180 <= lng <= 180):
                continue
            passed('modern_coordinate_pass')
            genus = missing(r['accepted_name']).split(' ')[0]
            coll = integer(r['collection_no'])
            key = (coll, genus)
            hi, lo = number(r['max_ma']), number(r['min_ma'])
            agekey = (hi, lo)
            if agekey not in age_cache:
                age_cache[agekey] = majority(hi, lo, stages)
            stage = age_cache[agekey]
            sift = int(not (r['lithification1'] == 'unlithified' or
                           (r['lithification1'] == 'poorly lithified' and 'sieve' in r['collection_methods'])))
            for subset in subsets:
                c = counts[subset]
                if key in seen[subset]:
                    c['duplicate_genus_collection_removed'] += 1
                    continue
                seen[subset].add(key); c['genus_collection_dedup_pass'] += 1
                if oid in occurrence_ids[subset]:
                    c['duplicate_occurrence_after_dedup'] += 1
                occurrence_ids[subset].add(oid)
                if hi is None or lo is None:
                    c['missing_or_nonfinite_age'] += 1
                elif hi == lo:
                    c['zero_duration_age'] += 1
                elif hi < lo:
                    c['reversed_age'] += 1
                if stage is None:
                    c['no_unique_majority_stage'] += 1
                    continue
                c['majority_stage_pass_all_stages'] += 1
                if stage not in SELECTED:
                    continue
                c['selected_stage_rows'] += 1
                c[stage + '_selected_stage_rows'] += 1
                coords = recon.get((ages[stage], lat, lng), [])
                if not coords:
                    c['missing_reconstruction_rows'] += 1
                    coords = [(None, None)]
                elif len(coords) > 1:
                    c['multiple_reconstruction_match_input_rows'] += 1
                    c['reconstruction_join_expansion_rows'] += len(coords) - 1
                for plng, plat in coords:
                    cc = r['cc']
                    if cc == 'NA':
                        c['literal_NA_country_rows'] += 1
                    region = mapping.get(cc, '')
                    if not region:
                        c['unmapped_nonempty_country_rows' if cc else 'empty_country_rows'] += 1
                    out = dict(stage=stage, plate_model_age=ages[stage], source_row=source_row,
                               occurrence_no=oid, collection_no=coll, reference_no=integer(r['reference_no']),
                               genus=genus, is_mollusca=int(oid in mollusca),
                               is_excluding_unlithified_pass=sift, lat=lat, lng=lng,
                               paleolng=plng, paleolat=plat, cc=cc, Region=region,
                               lithology1=missing(r['lithology1']), lithification1=missing(r['lithification1']),
                               environment=missing(r['environment']))
                    if out['lithology1'] == 'not reported':
                        out['lithology1'] = ''
                    writers[subset].writerow(out)
                    c['prepared_rows'] += 1
                    c[stage + '_prepared_rows'] += 1
                    c['mollusca_rows'] += out['is_mollusca']
                    c['mollusca_sifting_pass_rows'] += out['is_mollusca'] * sift
                    c[stage + '_mollusca_sifting_pass_rows'] += out['is_mollusca'] * sift
                    c['missing_genus_rows'] += not bool(genus)
                    c['missing_collection_rows'] += not bool(coll)
                    c['missing_reference_rows'] += not bool(out['reference_no'])
                    c['invalid_reconstructed_coordinate_rows'] += (plng is None or plat is None or not (-180 <= plng <= 180 and -90 <= plat <= 90))
                    selected_ids[subset].add(oid)
                    metadata_coords[subset][(stage, tuple(out[k] for k in METADATA))].add((lat, lng, plng, plat))
                    collection_coords[subset][(stage, coll)].add((lat, lng, plng, plat))
        primary_sizes[name] = nrows
    for f in outfiles.values():
        f.close()
    for subset, c in counts.items():
        c['distinct_prepared_occurrences'] = len(selected_ids[subset])
        c['distinct_selected_metadata_rows_before_grid'] = len(metadata_coords[subset])
        c['metadata_keys_with_multiple_coordinates'] = sum(len(v) > 1 for v in metadata_coords[subset].values())
        c['collection_stage_keys_with_multiple_coordinates'] = sum(len(v) > 1 for v in collection_coords[subset].values())
        if c['duplicate_occurrence_after_dedup'] or c['reconstruction_join_expansion_rows'] or c['metadata_keys_with_multiple_coordinates']:
            raise ValueError('Unexpected source cardinality: see private partial output')
    for p in files:
        if signatures[str(p)] != (p.stat().st_size, p.stat().st_mtime_ns):
            raise ValueError('Input changed while preparing')
    summary = dict(schema=SCHEMA, metadata_distinct_keys=METADATA,
                   counts={k: dict(v) for k, v in counts.items()},
                   primary_member_rows=primary_sizes, public_distinct_members=len(public),
                   mollusca_distinct_members=len(mollusca), mollusca_dated_public_members=len(mollusca & public),
                   stage_bounds=[s for s in stages if s[0] in SELECTED],
                   stage_map_ages=ages, region_codes=sorted(set(mapping.values())),
                   reconstruction=dict(recon_stats), input_sha256=input_hashes,
                   source_member_sha256=source.hashes, code_member_sha256=code.hashes,
                   preparation_sha256=sha(__file__), controls_passed=True,
                   runtime_seconds=time.monotonic() - started,
                   output_sha256={s + '.csv': sha(a.output / (s + '.csv')) for s in counts},
                   source_order=PRIMARY, membership_before_dedup=True,
                   clade_agnostic_includes_unlithified=True,
                   missing_readr_tokens=['', 'NA'], literal_NA_cc_preserved=True)
    (a.output / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: summary[k] for k in ['counts', 'stage_map_ages', 'reconstruction', 'runtime_seconds']}, sort_keys=True))


if __name__ == '__main__':
    main()
