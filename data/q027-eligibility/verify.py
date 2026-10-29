"""Independently verify anonymous cell eligibility and aggregate Q-027 outputs."""
import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo


SUBSETS = ('original', 'dated_public_member')
STAGES = ('Albian', 'Campanian')
BANDS = ('tropical', 'midlatitude', 'higher')
REGIONS = ('AF', 'AOC', 'AS', 'ATA', 'AUS', 'CAm', 'EU', 'IOC', 'NAm', 'POC', 'RoW', 'SA', 'UNKNOWN')
EXCLUDED = {'EU', 'NAm', 'UNKNOWN'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def number(value):
    return float('nan') if value == 'NA' else float(value)


def logical(value):
    assert value in ('TRUE', 'FALSE', 'NA'), value
    return {'TRUE': True, 'FALSE': False, 'NA': None}[value]


def conjunction(*values):
    if False in values:
        return False
    return None if None in values else True


def verify_preparation_replay(directory, frozen):
    initial = directory / 'prepare-initial.py'
    final = directory / 'prepare.py'
    replay_path = directory / 'preparation-replay-receipt.json'
    summary_path = directory / 'preparation-summary.json'
    replay = json.loads(replay_path.read_text())
    summary = json.loads(summary_path.read_text())
    initial_hash, final_hash = digest(initial), digest(final)
    assert initial_hash == frozen['prepare.py'] == replay['initial_adapter_sha256']
    assert final_hash == replay['final_adapter_sha256'] == summary['preparation_sha256']
    assert replay['csv_bytes_unchanged'] is True
    assert replay['input_sha256'] == summary['input_sha256']
    csv_chain = {}
    for name in ('original.csv', 'dated_public_member.csv'):
        expected = frozen['preparation/' + name]
        assert expected == replay['csv_sha256'][name]['initial']
        assert expected == replay['csv_sha256'][name]['final'] == summary['output_sha256'][name]
        csv_chain[name] = dict(frozen_initial_and_final_sha256=expected, all_recorded_hashes_match=True)
    return dict(status='pass', initial_adapter_matches_run_freeze=True,
                initial_adapter_sha256=initial_hash, final_adapter_sha256=final_hash,
                final_replay_csv_hashes_match_run_freeze=csv_chain,
                replay_inputs_match_final_summary=True,
                amendment='Diagnostics, source-member hashing, stronger validation guards and RSS reporting; final replay yields identical incidence CSVs.',
                evidence_sha256={p.name: digest(p) for p in (initial, final, replay_path, summary_path)},
                verification_scope='Local source-file hashes and independent comparison of recorded CSV hash chains; raw CSVs remain remote and were not opened or rehashed by this verifier.')


def verify(directory):
    results = directory / 'results'
    paths = [results / name for name in ('cells.tsv', 'regional-support.tsv', 'region-overlap.tsv')]
    before = {path.name: digest(path) for path in paths}
    cells = read(paths[0])
    assert len(cells) == 459
    groups = defaultdict(Counter)
    states = Counter()
    cap_coverage_checks = []
    keys = set()
    checks = Counter()
    for cell in cells:
        key = cell['subset'], cell['stage'], cell['cell_id']
        assert key not in keys
        keys.add(key)
        subset, stage, _ = key
        assert subset in SUBSETS and stage in STAGES and cell['region'] in REGIONS
        frequency = [] if not cell['frequencies'] else [int(v) for v in cell['frequencies'].split(',')]
        T = int(cell['n_colls'])
        rows = sum(frequency)
        S = len(frequency)
        assert all(1 <= v <= T for v in frequency)
        assert frequency == sorted(frequency, reverse=True)
        assert rows == int(cell['n_mollusca_rows'])
        assert S == int(cell['n_genera'])
        assert sum(v == 1 for v in frequency) == int(cell['singletons'])
        assert sum(v == 2 for v in frequency) == int(cell['doubletons'])
        assert 0 <= T <= rows <= int(cell['n_pool_rows'])
        metadata = int(cell['clade_agnostic_n_total_colls'])
        assert int(cell['clade_agnostic_distinct_collection_ids']) <= metadata <= int(cell['n_pool_rows'])
        refs = number(cell['n_refs'])
        assert math.isnan(refs) or (refs.is_integer() and 1 <= refs <= rows)
        multiton = sum(v > 1 for v in frequency) / S if S else float('nan')
        saved_multiton = number(cell['multiton_ratio'])
        assert (math.isnan(multiton) and math.isnan(saved_multiton)) or math.isclose(multiton, saved_multiton, rel_tol=1e-12, abs_tol=1e-14)
        row_gate = rows > 10
        collection_quality = metadata >= 10
        reference_quality = None if math.isnan(refs) else refs >= 2
        multiton_quality = None if math.isnan(multiton) else multiton >= .3
        quality = conjunction(collection_quality, reference_quality, multiton_quality)
        lat = number(cell['cell_paleolat'])
        lon = number(cell['cell_paleolng'])
        assert math.isfinite(lat) and math.isfinite(lon) and abs(lat) <= 90
        band = 'tropical' if abs(lat) < 20 else 'midlatitude' if abs(lat) < 40 else 'higher'
        assert cell['band'] == band
        qD, t, ratio, coverage = (number(cell[k]) for k in ('qD', 't', 't_over_T', 'SC'))
        if not row_gate:
            state = 'not_run_le10_rows'
            assert all(math.isnan(v) for v in (qD, t, ratio, coverage))
            assert cell['method'] == 'NA' and not cell['error'] and not cell['warning']
        elif cell['error']:
            state = 'error'
            assert math.isnan(qD) and math.isnan(t)
        elif not (math.isfinite(qD) and math.isfinite(t)):
            state = 'nonfinite'
        else:
            assert qD >= 0 and t >= 0 and -1e-12 <= coverage <= 1 + 1e-12
            assert math.isclose(ratio, t / T, rel_tol=1e-12, abs_tol=1e-14)
            state = 't_zero' if t == 0 else 'above_2T' if t > 2 * T else 'finite_within_cap'
        assert cell['estimator_status'] == state
        if row_gate:
            q1 = sum(v == 1 for v in frequency)
            q2 = sum(v == 2 for v in frequency)
            q0 = ((T - 1) / T) * (q1 * q1 / (2 * q2) if q2 else q1 * (q1 - 1) / 2)
            A = T * q0 / (T * q0 + q1) if q1 else 1
            coverage_2T = 1 - (q1 / rows) * A ** (T + 1)
            assert math.isfinite(coverage_2T) and 0 <= coverage_2T <= 1
            within_cap_from_coverage = coverage_2T >= .9
            assert state in ('finite_within_cap', 'above_2T')
            assert within_cap_from_coverage == (state == 'finite_within_cap'), key
            cap_coverage_checks.append(dict(subset=subset, stage=stage, cell_id=cell['cell_id'],
                                            coverage_at_2T=coverage_2T,
                                            absolute_margin=abs(coverage_2T - .9),
                                            within_cap=within_cap_from_coverage))
        eligible = conjunction(row_gate, quality, state == 'finite_within_cap') is True
        expected_flags = dict(row_gate=row_gate, collection_quality=collection_quality,
                              reference_quality=reference_quality, multiton_quality=multiton_quality,
                              quality=quality, eligible=eligible)
        for name, expected in expected_flags.items():
            assert logical(cell[name]) is expected, (key, name, cell[name], expected)
            checks['cell_logical_flags'] += 1
        state_key = subset, stage, cell['region'], band
        count = groups[state_key]
        count['cells_with_pool'] += 1
        count['cells_with_mollusca'] += rows > 0
        count['cells_gt10_mollusca'] += row_gate
        count['cells_after_quality'] += conjunction(row_gate, quality) is True
        count['cells_eligible'] += eligible
        count['quality_passing_estimator_error'] += conjunction(row_gate, quality, state == 'error') is True
        count['quality_passing_above_2T'] += conjunction(row_gate, quality, state == 'above_2T') is True
        states[f'{subset}:{stage}:{state}'] += 1
    expected_support = {key: groups[key] for key in itertools.product(SUBSETS, STAGES, REGIONS, BANDS)}
    assert len(expected_support) == 156
    # First read aggregate values only after independent cell reconstruction is complete.
    support = read(paths[1])
    assert len(support) == len(expected_support)
    seen = set()
    metrics = ('cells_with_pool', 'cells_with_mollusca', 'cells_gt10_mollusca',
               'cells_after_quality', 'cells_eligible', 'quality_passing_estimator_error',
               'quality_passing_above_2T')
    for row in support:
        key = tuple(row[k] for k in ('subset', 'stage', 'region', 'band'))
        assert key in expected_support and key not in seen
        seen.add(key)
        assert set(row) == {'subset', 'stage', 'region', 'band', *metrics}
        for field in metrics:
            assert int(row[field]) == expected_support[key][field], (key, field)
            checks['regional_numeric_values'] += 1
    expected_overlap = {}
    for subset, region in itertools.product(SUBSETS, REGIONS):
        values = {f'{stage}_{band}': groups[subset, stage, region, band]['cells_eligible']
                  for stage, band in itertools.product(STAGES, ('tropical', 'midlatitude'))}
        expected_overlap[subset, region] = {**values,
            'both_bands_both_stages': all(v > 0 for v in values.values()),
            'outside_eu_nam_known': region not in EXCLUDED}
    overlap = read(paths[2])
    assert len(overlap) == len(expected_overlap) == 26
    seen = set()
    for row in overlap:
        key = row['subset'], row['region']
        assert key in expected_overlap and key not in seen
        seen.add(key)
        assert set(row) == {'subset', 'region', *expected_overlap[key]}
        for field, expected in expected_overlap[key].items():
            actual = logical(row[field]) if isinstance(expected, bool) else int(row[field])
            assert actual == expected, (key, field)
            checks['overlap_values'] += 1
    assert before == {path.name: digest(path) for path in paths}
    passing = {subset: sorted(region for (sub, region), values in expected_overlap.items()
                             if sub == subset and values['both_bands_both_stages'] and values['outside_eu_nam_known'])
               for subset in SUBSETS}
    endpoint_regions = {
        f'{subset}:{stage}': sorted(region for region in REGIONS
                                  if region not in EXCLUDED and
                                  all(groups[subset, stage, region, band]['cells_eligible'] > 0
                                      for band in ('tropical', 'midlatitude')))
        for subset, stage in itertools.product(SUBSETS, STAGES)}
    pair_path = directory.parent / 'q027-climate-pairing/results/pair-results.tsv'
    primary_pairs = [row for row in read(pair_path)
                     if row['scenario'] == 'literal_hot_cold' and
                     row['subset'] == 'dated_public_member' and row['passes'] == '1']
    endpoint_bounds = []
    for pair in primary_pairs:
        known = {stage: endpoint_regions[f'dated_public_member:{stage}']
                 for stage in (pair['hot_stage'], pair['cold_stage']) if stage in STAGES}
        upper_bound = len(set.intersection(*(set(v) for v in known.values()))) if known else None
        endpoint_bounds.append(dict(hot_stage=pair['hot_stage'], cold_stage=pair['cold_stage'],
                                    computed_endpoint_regions=known,
                                    shared_region_upper_bound=upper_bound,
                                    excludes_two_shared_regions=(upper_bound is not None and upper_bound < 2)))
    totals = {}
    for subset, stage in itertools.product(SUBSETS, STAGES):
        totals[f'{subset}:{stage}'] = {field: sum(count[field] for (sub, st, _, _), count in expected_support.items()
                                                  if sub == subset and st == stage) for field in metrics}
    source_paths = [directory / 'run.R', directory / 'prepare.py', directory / 'prepare-initial.py',
                    directory / 'preparation-replay-receipt.json', directory / 'preparation-summary.json',
                    directory / 'environment/controls.R', directory / 'environment/legacy_geometry.R',
                    directory.parents[1] / 'scratch/q027-independent-audit/source/functions/run_SQS_iNEXT_simple.R',
                    directory.parents[1] / 'scratch/q027-independent-audit/source/subscripts/rscript-run-grid-cell-subsampling-analysis-100km-dggridR-cells.R']
    assert len(cap_coverage_checks) == 235
    frozen = {}
    freeze_path = results / 'run-input-freeze.sha256'
    for line in freeze_path.read_text().splitlines():
        checksum, name = line.split(maxsplit=1)
        frozen[name] = checksum
    local_frozen_sources = {name: dict(frozen_sha256=checksum,
                                      current_sha256=digest(directory / name),
                                      matches=digest(directory / name) == checksum)
                            for name, checksum in frozen.items() if (directory / name).is_file()}
    receipt = dict(status='pass', verified_at=datetime.now(ZoneInfo('Australia/Hobart')).isoformat(),
                   method='Independent Python standard-library reconstruction from anonymous frequencies and saved diagnostics; no runner import and no raw records',
                   cells=len(cells), regional_support_rows=len(support), region_overlap_rows=len(overlap),
                   checks=dict(checks), passing_outside_regions=passing, totals=totals,
                   endpoint_both_band_outside_regions=endpoint_regions,
                   cheap_screen_primary_pair_endpoint_bounds=endpoint_bounds,
                   cheap_pair_results_sha256=digest(pair_path),
                   numerical_cap_check=dict(vectors=len(cap_coverage_checks),
                       accepted=sum(row['within_cap'] for row in cap_coverage_checks),
                       rejected=sum(not row['within_cap'] for row in cap_coverage_checks),
                       minimum_absolute_coverage_margin=min(row['absolute_margin'] for row in cap_coverage_checks),
                       nearest_boundary=min(cap_coverage_checks, key=lambda row: row['absolute_margin']),
                       formula='Q0=(T-1)/T*(Q1^2/(2Q2) if Q2>0 else Q1*(Q1-1)/2); A=T*Q0/(T*Q0+Q1) if Q1>0 else 1; C(2T)=1-(Q1/U)*A^(T+1)',
                       formula_provenance='Parent inspected installed iNEXT:::Chat.Sam; verifier independently implements the supplied analytic 2T coverage formula.'),
                   run_input_freeze_sha256=digest(freeze_path),
                   current_sources_vs_run_freeze=local_frozen_sources,
                   preparation_replay_provenance=verify_preparation_replay(directory, frozen),

                   endpoint_bound_assumptions=[
                       'Fixed dated-public subset, per-stage eligibility contract, fixed grid and modal-region definition.',
                       'Gate requires at least two identical named outside-EU/NAm/UNKNOWN regions, each supporting both bands in both stages.',
                       'Pairing does not pool cells or alter endpoint eligibility; intersection cardinality is bounded by either endpoint set.',
                       'No conclusion about other unscreened pairs or a different estimator/contract follows.'],
                   estimator_status_counts=dict(sorted(states.items())),
                   output_sha256=before,
                   source_sha256={str(p): digest(p) for p in source_paths},
                   verifier_sha256=digest(Path(__file__)),
                   limitations=[
                       'Does not independently recompute qD, t, or returned SC; the 2T acceptance boundary is independently checked from incidence frequencies.',
                       'Preparation replay provenance compares recorded CSV SHA256 chains; remote incidence CSV bytes were not locally rehashed.',
                       'Does not reconstruct frequency vectors, distinct metadata rows, reference counts or modal regions from raw records.',
                       'Does not independently validate the geometry, historical package equivalence, source cleaning or reconstruction joins.',
                       'Counts are eligibility support, not power, independent regional replication, empirical gradients or biological effects.'])
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--receipt', type=Path)
    arguments = parser.parse_args()
    receipt = verify(arguments.directory)
    destination = arguments.receipt or arguments.directory / 'verification.json'
    destination.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: receipt[key] for key in ('status', 'cells', 'regional_support_rows', 'region_overlap_rows', 'passing_outside_regions', 'totals')}, indent=2))
