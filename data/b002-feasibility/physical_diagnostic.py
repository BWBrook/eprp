"""Replay published component volumes; no thickness or through-growth inference."""

from pathlib import Path
import csv
import hashlib
import json
from decimal import Decimal as D

ROOT = Path(__file__).resolve().parent

def read(name):
    with (ROOT / name).open(newline='') as handle:
        return list(csv.DictReader(handle))

def write(name, rows):
    with (ROOT / name).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

def printed_bounds(text):
    value = D(text)
    half = D(5).scaleb(value.as_tuple().exponent - 1)
    return value - half, value + half

proportions = []
for row in read('naglik2015-fidelites-selected.csv'):
    diameter = D(row['diameter_mm'])
    chamber = D(row['chamber_volume_mm3'])
    septum = D(row['septum_volume_mm3'])
    cl, ch = printed_bounds(row['chamber_volume_mm3'])
    sl, sh = printed_bounds(row['septum_volume_mm3'])
    proportions.append({
        'species': row['species'],
        'chamber_number': row['chamber_number'],
        'diameter_mm': str(diameter),
        'septum_to_chamber_volume_ratio': str(septum/chamber),
        'rounding_only_ratio_lower': str(sl/ch),
        'rounding_only_ratio_upper': str(sh/cl),
        'chamber_volume_over_diameter_cubed': str(chamber/diameter**3),
        'septum_volume_over_diameter_cubed': str(septum/diameter**3),
    })
write('volume-proportions.csv', proportions)

endpoints = []
sensitivity = []
for row in read('naglik2016-endpoints.csv'):
    shell = D(row['shell_plus_septa_volume_cm3'])
    living = D(row['living_chamber_volume_cm3'])
    siphuncle = D(row['siphuncle_volume_cm3'])
    gas = D(row['phragmocone_volume_cm3'])
    volume = D(row['reported_total_volume_cm3'])
    assert shell + living + siphuncle + gas == volume
    body_mass = living*D(row['assumed_tissue_density_g_cm3'])
    siphuncle_mass = siphuncle*D(row['assumed_siphuncle_density_g_cm3'])
    dry_mass = shell*D(row['assumed_shell_plus_septa_density_g_cm3']) + body_mass + siphuncle_mass
    displaced_mass = D('1.026') * volume
    capacity = D('1.013') * gas
    q = (displaced_mass - dry_mass)/capacity
    endpoints.append({
        'species': row['species'],
        'displaced_mass_g': str(displaced_mass),
        'recomputed_gas_only_mass_g': str(dry_mass),
        'source_reported_total_mass_g': row['reported_total_mass_g'],
        'mass_difference_source_minus_recomputed_g': str(D(row['reported_total_mass_g']) - dry_mass),
        'full_chamber_liquid_capacity_g': str(capacity),
        'q_all_chambers_loadable_envelope': str(q),
        'min_q_one_minus_q': str(min(q, 1-q)),
        'source_total_mass_q': str((displaced_mass - D(row['reported_total_mass_g']))/capacity),
    })
    for shell_density in ('2.62', '2.66'):
        for fluid_density in ('1.013', '1.026'):
            mass = shell*D(shell_density) + body_mass + siphuncle_mass
            sensitivity.append({
                'species': row['species'],
                'shell_plus_septa_density_g_cm3': shell_density,
                'cameral_fluid_density_g_cm3': fluid_density,
                'q': str((displaced_mass-mass)/(D(fluid_density)*gas)),
            })
write('endpoint-loading.csv', endpoints)
write('endpoint-density-sensitivity.csv', sensitivity)
summary = {
    'scope': 'One specimen, six selected post-10-mm chambers, descriptive volume proportions; three reconstructed endpoints, hypothetical full-capacity loading envelope.',
    'fidelites_late_to_earlier_ratio': str(D(proportions[-1]['septum_to_chamber_volume_ratio'])/D(proportions[0]['septum_to_chamber_volume_ratio'])),
    'fidelites_ratio_percent_decline': str(100*(1-D(proportions[-1]['septum_to_chamber_volume_ratio'])/D(proportions[0]['septum_to_chamber_volume_ratio']))),
    'all_six_ratio_rounding_intervals_have_common_intersection': max(D(r['rounding_only_ratio_lower']) for r in proportions) <= min(D(r['rounding_only_ratio_upper']) for r in proportions),
    'stage_q_estimable': False,
    'thickness_allometry_estimable': False,
    'source_table_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('naglik2015-fidelites-selected.csv', 'naglik2016-endpoints.csv')},
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT/'diagnostic-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
for row in endpoints:
    print(row['species'], row['q_all_chambers_loadable_envelope'])
