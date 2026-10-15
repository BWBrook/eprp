# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Read-only Lamyman Zenodo v3 support audit; no outcome comparison or fitting."""
import argparse
import collections as C
import hashlib
import itertools
import json
from pathlib import Path
import re
import openpyxl

HASHES = {
    'S1. Morphospecies Key Information.xlsx': '88cd9b0a054aae64c9adfeadad5ec730dddfb11d169b8100ab61f803f0e05d84',
    'Supporting Data.xlsx': '2412991df3ff35d9f62275a500a474feff77e2c89b24ec86289574a8f7a7366b',
    'All_Species_Lineages.nex': 'e8bb5da6f67032f820b27ff2acc4e704b734102d4f4245bb3fddfd19b438ad95',
    'All_Species_Morphospecies.nex': '3a0867e048006975d60532c34bcaec548b051769a25b376bb62fafb94a009ce3',
}

def table(sheet):
    vals = list(sheet.values)
    return [dict(zip(vals[0], r)) for r in vals[1:] if any(v is not None for v in r)]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-dir', type=Path, default=Path('data/raw/lamyman2026'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.resolve() in [(args.source_dir / n).resolve() for n in HASHES]:
        raise ValueError('Output must not overwrite a source file')
    manifest = []
    for name, expected in HASHES.items():
        data = (args.source_dir / name).read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise ValueError(f'Hash mismatch before parsing: {name}: {actual}')
        manifest.append(dict(file=name, bytes=len(data), sha256=actual))
    s1 = openpyxl.load_workbook(args.source_dir / 'S1. Morphospecies Key Information.xlsx', read_only=True, data_only=True)
    s3 = openpyxl.load_workbook(args.source_dir / 'Supporting Data.xlsx', read_only=True, data_only=True)
    rows = table(s1['Key Information'])
    names = {r['Morphospecies']: r for r in rows}
    links = [(names[d['Ancestor']], d) for d in rows if d['Ancestor'] in names]
    offspring = C.defaultdict(list)
    for p, d in links:
        offspring[p['Morphospecies']].append(d)
    sisters = [q for ds in offspring.values() for q in itertools.combinations(ds, 2)]
    extinct = lambda q: all(r['End'] > 0 for r in q)
    known_distinct = lambda q: all(r['Dominant Ecogroup'] is not None for r in q) and q[0]['Dominant Ecogroup'] != q[1]['Dominant Ecogroup']
    counts = dict(rows=len(rows), unique_names=len(names), in_table_parent_edges=len(links), numeric_overlap=sum(p['End'] < d['Start'] for p, d in links), exact_boundary=sum(p['End'] == d['Start'] for p, d in links), End_zero=sum(r['End'] == 0 for r in rows), sister_pairs=len(sisters), sibships=sum(len(ds) > 1 for ds in offspring.values()))
    counts.update(ancestry_labels=dict(C.Counter(r['Ancestry evidence'] for r in rows)), sibship_size_frequencies=dict(sorted(C.Counter(map(len, offspring.values())).items())))
    counts.update(parent_pairs_both_End_positive=sum(map(extinct, links)), parent_pairs_both_End_positive_non_speculative_daughter_edge=sum(extinct(q) and q[1]['Ancestry evidence'] != 'speculative' for q in links), sister_pairs_both_End_positive=sum(map(extinct, sisters)), sister_pairs_both_End_positive_both_non_speculative_edges=sum(extinct(q) and all(r['Ancestry evidence'] != 'speculative' for r in q) for q in sisters))
    counts.update(parent_known_distinct_ecogroups=sum(map(known_distinct, links)), sister_known_distinct_ecogroups=sum(map(known_distinct, sisters)), parent_unequal_ecogroups_including_missing=sum(p['Dominant Ecogroup'] != d['Dominant Ecogroup'] for p, d in links), ecogroup_number_frequencies=dict(C.Counter(str(r['Number of Ecogroups']) for r in rows)))
    # Explicit derived normalization only: strip outer whitespace, including NBSP.
    # Raw workbook values and Nexus names remain unchanged; no fuzzy matching.
    gn = {r['GenusEpithet']: r['Gn'] for r in table(s3['Gn, Genera'])}
    short = C.defaultdict(list)
    for name in names:
        genus, epithet = name.split(' ', 1)
        short[(gn.get(genus, genus) + ' ' + epithet).strip()].append(name)
    lineages = table(s3['Lineages Tree2'])
    memberships = C.defaultdict(list)
    unresolved = []
    for r in lineages:
        for token in r['MorphospeciesGnInLineage'].split(','):
            hits = short.get(token.strip(), [])
            if len(hits) == 1:
                memberships[hits[0]].append(r['Biospecies code'])
            else:
                unresolved.append(dict(lineage=r['Biospecies code'], token=token))
    boundary = [dict(parent=p['Morphospecies'], daughter=d['Morphospecies'], boundary_Ma=d['Start'], daughter_edge_evidence=d['Ancestry evidence'], shared_listed_lineage=bool(set(memberships[p['Morphospecies']]) & set(memberships[d['Morphospecies']]))) for p, d in links if p['End'] == d['Start']]
    mapping = dict(normalization='Derived lookup strips outer whitespace including NBSP; raw sources unchanged; genus abbreviations expanded from S3 Gn, Genera A:B', lineage_table_rows=len(lineages), mapped_species=len(memberships), multiply_listed_species=sum(len(v) > 1 for v in memberships.values()), unresolved_tokens=unresolved, boundary_with_shared_listed_lineage=sum(r['shared_listed_lineage'] for r in boundary))
    nexus = {}
    for fn in ['All_Species_Morphospecies.nex', 'All_Species_Lineages.nex']:
        text = (args.source_dir / fn).read_text()
        block = re.search(r'taxlabels\s+(.*?);', text, re.S | re.I).group(1)
        labels = {v.strip().strip("'") for v in block.splitlines() if v.strip()}
        expected = set(names) if 'Morphospecies.nex' in fn else {r['Biospecies code'] for r in lineages}
        absent = sorted(expected - labels)
        nexus[fn] = dict(ntax=int(re.search(r'ntax=(\d+)', text, re.I).group(1)), taxlabels=len(labels), extra_tip_labels=sorted(labels - expected), source_names_absent_as_tips=absent)
        if 'Lineages.nex' in fn:
            nexus[fn]['absent_codes_present_as_internal_labels'] = sum(bool(re.search('label="' + re.escape(n) + r'(?: \[\d+\])?"', text)) for n in absent)
    excluded = ['Praepararotalia cretacea', 'Praepararotalia perclara']
    planktonic = [r for r in rows if r['Morphospecies'] not in excluded]
    reconciliation = dict(excluded_rows=excluded, planktonic_rows=len(planktonic), row_End_zero=sum(r['End'] == 0 for r in planktonic), row_End_positive=sum(r['End'] > 0 for r in planktonic), summary_living=s3['Overall Diversites']['D12'].value, summary_extinct=s3['Overall Diversites']['D13'].value, summary_discrepancy_preserved=True)
    locators = {
        'S1 count and schema': 'Key Information A1:M483; name A, ancestor B, evidence C, Start D, End F, dominant ecogroup K',
        '482 versus 480': 'S1 Key Information A387:A388; S3 Overall %Change Tree1v2 C2/F2; Overall Diversites D11/F11',
        'living contradiction': 'S3 Overall Diversites D12:D13; S1 F2:F483; matching S3 Morphospecies PrevailClass\'n O2:O483',
        'missing ecogroup': 'S1 Key Information K387; affected daughter rows37,388',
        'ecogroup definitions': 'S1 Ecogroups Key A2:D8',
        'lineage membership and ancestors': 'S3 Lineages Tree2 A1:I270; genus expansion Gn, Genera A:B; many-membership example B2/B61',
        '268 lineage summary': 'S3 Overall %Change Tree1v2 C3/F3; excludes L_Bolivina Clade',
        'Nexus mode warning': 'S3 S6. Phyl\'s (Ch\'gms) Contents E5; ntax line3 in each Nexus',
        'normalization examples': 'S1 Key Information A36 trailing NBSP; morphospecies Nexus Antarcticella cecionii label contains U+FFFD',
    }
    warnings = ['Numeric overlap does not independently verify budding; equality does not prove naming or pseudoextinction.', '333 filters the daughter ancestral EDGE, not the parent row\'s distinct earlier edge.', 'Missing ecological category does not establish a different habitat.', 'Lineage membership is many-to-many and cannot be used as an exclusive crosswalk without further definitions.', 'Nexus transforms buds into bifurcations; named ancestors may be tips; species/lineage row counts are not interchangeable with tip counts.', 'No rubric for evidence categories was established by this audit; labels are not statistical probabilities.', 'Source summary living count differs from row End coding; no values silently repaired.']
    out = dict(provider=dict(record='https://zenodo.org/records/21414007', api='https://zenodo.org/api/records/21414007', version_doi='10.5281/zenodo.21414007', concept_doi='10.5281/zenodo.18854730', version_index=2, published='2026-07-17', license='CC BY 4.0', archive_url='https://zenodo.org/api/records/21414007/files/Supplementary%20Data.zip/content', archive_bytes=1162702765, archive_provider_md5='45350e953472d0096d50a58b5c2b3c3c', archive_whole_md5_locally_verified=False), files=manifest, counts=counts, scope_reconciliation=reconciliation, lineage_membership=mapping, nexus_units=nexus, boundary_rows=boundary, source_locators=locators, semantic_warnings=warnings)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(f'Wrote {args.output}; all four source hashes match before parsing.')

if __name__ == '__main__':
    main()
