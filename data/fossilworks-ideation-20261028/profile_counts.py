#!/usr/bin/env python3
"""Read-only, question-oriented summaries of the pinned public Fossilworks input."""

import argparse
import collections
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import statistics


ASSEMBLY_SHA256 = "ae1fdeb113ade4a72d9fd23a08d9082720c308d0b0c593f6bf9fb4ed36861610"
ANNOTATIONS_SHA256 = "ebac4771b4b0f400c7cb91b9c4e8499ba781731374148f3f77aac672737f66b6"
SAMPLES = """s AS (SELECT * FROM samples_rows WHERE _fw_row_id IN
 (SELECT MIN(_fw_row_id) FROM samples_rows GROUP BY "sample no"))"""
COUNTS = """g AS (SELECT "sample no" sn,sum(CAST(count AS INTEGER)) n,count(*) r
 FROM register_rows GROUP BY "sample no")"""

QUERIES = {
    "interval_support": f'''WITH {SAMPLES},{COUNTS}
 SELECT s."time interval",count(*) samples,
 sum(g.n>=200 AND CAST(s.richness AS INT)>=10) n200_richness10,
 sum(g.n>=500 AND CAST(s.richness AS INT)>=20) n500_richness20,
 sum(s."max Ma"<>'' AND s."min Ma"<>'' AND
 CAST(s."max Ma" AS REAL)-CAST(s."min Ma" AS REAL) BETWEEN 0 AND 0.1) valid_width_le_100kyr
 FROM s JOIN g ON g.sn=s."sample no" GROUP BY s."time interval" ORDER BY samples DESC''',
    "countries": '''SELECT country,count(DISTINCT "sample no") samples
 FROM samples_rows GROUP BY country ORDER BY samples DESC,country''',
    "life_forms": '''SELECT "life form",count(*) register_rows,
 count(DISTINCT "sample no") samples FROM register_rows GROUP BY "life form"
 ORDER BY register_rows DESC,"life form"''',
    "taphonomic_tokens": '''SELECT
 count(DISTINCT CASE WHEN "taphonomic context"='' THEN "sample no" END) blank,
 count(DISTINCT CASE WHEN "taphonomic context" LIKE '%human accumulation%' THEN "sample no" END) human,
 count(DISTINCT CASE WHEN "taphonomic context" LIKE '%bird accumulation%' THEN "sample no" END) bird,
 count(DISTINCT CASE WHEN "taphonomic context" LIKE '%carnivore accumulation%' THEN "sample no" END) carnivore,
 count(DISTINCT CASE WHEN "taphonomic context" LIKE '%pitfall trap%' THEN "sample no" END) pitfall,
 count(DISTINCT CASE WHEN "taphonomic context" LIKE '%cave%' THEN "sample no" END) cave FROM samples_rows''',
    "sampling_methods": '''SELECT "sampling methods",count(DISTINCT "sample no") samples
 FROM samples_rows GROUP BY "sampling methods" ORDER BY samples DESC,"sampling methods"''',
    "age_basis": '''SELECT "age basis",count(DISTINCT "sample no") samples
 FROM samples_rows GROUP BY "age basis" ORDER BY samples DESC,"age basis"''',
    "sample_qc": '''SELECT status,count(*) summary_rows,count(DISTINCT s."sample no") samples
 FROM sample_qc q JOIN samples_rows s ON s._fw_row_id=q.sample_row_id GROUP BY status ORDER BY status''',
    "count_units": '''SELECT count_unit,review_level,count(*) register_rows,
 count(DISTINCT sample_no) samples FROM annotations.register_count_evidence
 GROUP BY count_unit,review_level ORDER BY register_rows DESC,count_unit,review_level''',
    "duplicate_taxon_keys": '''SELECT count(*) keys,sum(n-1) excess_rows FROM
 (SELECT "sample no",genus,qualifier,species,count(*) n FROM register_rows
 GROUP BY "sample no",genus,qualifier,species HAVING n>1)''',
    "source_reuse": '''WITH g AS (SELECT "ref no",count(DISTINCT "sample no") n
 FROM samples_rows GROUP BY "ref no") SELECT count(*) refs,sum(n>1) multisample_refs,
 sum(CASE WHEN n>1 THEN n ELSE 0 END) samples_in_multisample_refs,max(n) largest FROM g''',
    "coordinate_reuse": '''WITH s AS (SELECT DISTINCT "sample no",latitude,longitude FROM samples_rows),
 g AS (SELECT latitude,longitude,count(*) n FROM s GROUP BY latitude,longitude HAVING n>1)
 SELECT count(*) coordinate_groups,sum(n) samples,max(n) largest FROM g''',
    "country_rodent_support": '''SELECT country,"time interval",count(DISTINCT "sample no") samples,
 count(DISTINCT "ref no") refs,count(*) register_rows,sum(CAST(count AS INT)) counted_units
 FROM register_rows WHERE country IN ('United States','France','Spain')
 AND "time interval" IN ('Early Miocene','Middle Miocene','Late Miocene','Early Oligocene',
 'Late Eocene','Middle Eocene','Early Eocene') AND "life form"='rodents'
 GROUP BY country,"time interval" ORDER BY country,"time interval"''',
    "candidate_series": f'''WITH {SAMPLES},{COUNTS}
 SELECT s."ref no",count(*) samples,count(DISTINCT s.Ma) distinct_ma,
 count(DISTINCT s."max Ma"||'|'||s."min Ma") bound_pairs_including_blank,
 min(g.n) min_units,max(g.n) max_units,min(CAST(s.richness AS INT)) min_richness,
 max(CAST(s.richness AS INT)) max_richness,
 sum(s."max Ma"='' OR s."min Ma"='') missing_bounds,
 group_concat(DISTINCT s."time interval") intervals,
 group_concat(DISTINCT s."sampling methods") methods,
 group_concat(DISTINCT s."taphonomic context") contexts
 FROM s JOIN g ON g.sn=s."sample no"
 WHERE s."ref no" IN ('2390','3135','3692','3701','3742','3779','3798','4050','4300','4473')
 GROUP BY s."ref no" ORDER BY s."ref no"''',
    "candidate_citations": '''SELECT DISTINCT ref_no,authors,year,title,doi FROM references_rows
 WHERE ref_no IN ('2390','3135','3692','3701','3742','3779','3798','4050','4300','4473')
 ORDER BY ref_no''',
    "hell_creek": '''SELECT "time interval",count(DISTINCT "sample no") samples,
 count(*) register_rows,sum(CAST(count AS INT)) counted_units FROM register_rows
 WHERE formation='Hell Creek' GROUP BY "time interval" ORDER BY "time interval"''',
    "bluegrass_sampling_contrast": '''SELECT "sample no","life form",count(*) register_rows,
 sum(CAST(count AS INT)) counted_units FROM register_rows WHERE "sample no" IN ('3423','3424')
 GROUP BY "sample no","life form" ORDER BY "sample no","life form"''',
    "within_reference_age_overlap": f'''WITH {SAMPLES},v AS (SELECT *,
 CAST("max Ma" AS REAL) hi,CAST("min Ma" AS REAL) lo FROM s WHERE "max Ma"<>''
 AND "min Ma"<>'' AND CAST("max Ma" AS REAL)>=CAST("min Ma" AS REAL))
 SELECT count(*) pairs_with_both_valid_bounds,
 sum(a.lo<b.hi AND b.lo<a.hi) strict_overlap_pairs,
 sum(a.lo=b.lo AND a.hi=b.hi) identical_bounds_pairs
 FROM v a JOIN v b ON a."ref no"=b."ref no" AND a."sample no"<b."sample no"''',
}


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def distribution(values):
    values = sorted(values)
    q25, _, q75 = statistics.quantiles(values, n=4, method="exclusive")
    return dict(n=len(values), minimum=values[0], q25=q25,
                median=statistics.median(values), q75=q75, maximum=values[-1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assembly", type=Path)
    parser.add_argument("annotations", type=Path)
    args = parser.parse_args()
    for path, expected in [(args.assembly, ASSEMBLY_SHA256), (args.annotations, ANNOTATIONS_SHA256)]:
        if sha256(path) != expected:
            raise ValueError(f"Input hash mismatch: {path}")
    with closing(sqlite3.connect(args.assembly.resolve().as_uri()+"?mode=ro", uri=True)) as c:
        c.row_factory = sqlite3.Row
        c.execute("ATTACH DATABASE ? AS annotations", (args.annotations.resolve().as_uri()+"?mode=ro",))
        c.execute("PRAGMA query_only=ON")
        sample_groups = collections.defaultdict(list)
        for row in c.execute("SELECT * FROM samples_rows ORDER BY _fw_row_id"):
            sample_groups[row["sample no"]].append(dict(row))
        for rows in sample_groups.values():
            for row in rows[1:]:
                if any(row[k] != rows[0][k] for k in row if k != "_fw_row_id"):
                    raise ValueError("Repeated summaries differ beyond source row ID")
        samples = [rows[0] for rows in sample_groups.values()]
        sizes = [dict(r) for r in c.execute('SELECT "sample no",sum(CAST(count AS INT)) n,count(*) r FROM register_rows GROUP BY "sample no"')]
        valid_widths = [float(s["max Ma"])-float(s["min Ma"]) for s in samples
                        if s["max Ma"] and s["min Ma"] and float(s["max Ma"])>=float(s["min Ma"])]
        result = {
            "inputs": {"assembly_sha256": ASSEMBLY_SHA256, "annotations_sha256": ANNOTATIONS_SHA256},
            "definitions": {
                "scope": "20 retained public interval exports, not provider census or PBDB-held records",
                "sample": "Exact provider sample no; 22 duplicate summaries checked identical except _fw_row_id, then represented once for summaries only",
                "count_sum": "Sum of all retained register counts for a sample; mixed or unknown units; duplicate register rows retained",
                "richness": "Provider richness, not independent species-level taxonomic adjudication",
                "quantiles": "Python statistics.quantiles(n=4, method=exclusive)",
                "ages": "Literal numeric provider Ma and bounds; no calibration, midpoint assignment, or repair; widths are uncertainty envelopes, not measured durations",
                "overlap": "Strict interval overlap within same reference, conditional on both valid bounds; identical bounds include zero-width pairs; no probabilistic age interpretation",
                "coordinates": "Exact modern coordinate strings, not paleocoordinates or proof of independence",
                "context": "Literal substring retrieval; categories overlap and do not identify formation mechanisms",
            },
            "summary": {
                "sample_ids": len(samples), "sample_summary_rows": sum(map(len, sample_groups.values())),
                "samples_repeated_across_selected_intervals": sum(len({r['_fw_interval_id'] for r in rows})>1 for rows in sample_groups.values()),
                "register_count_sum": distribution([s['n'] for s in sizes]),
                "register_rows_per_sample": distribution([s['r'] for s in sizes]),
                "provider_richness": distribution([int(s['richness']) for s in samples]),
                "valid_age_width_Ma": distribution(valid_widths),
                "missing_age_bounds": sum(not s['max Ma'] or not s['min Ma'] for s in samples),
                "valid_age_width_le_Ma": {str(w):sum(0<=x<=w for x in valid_widths) for w in [0,0.001,0.01,0.1,1,5]},
                "reversed_age_bounds": [{k:s[k] for k in ['sample no','Ma','max Ma','min Ma']} for s in samples
                                        if s['max Ma'] and s['min Ma'] and float(s['max Ma'])<float(s['min Ma'])],
                "sample_count_sum_ge": {str(n):sum(s['n']>=n for s in sizes) for n in [50,100,200,500,1000]},
                "missing_coordinates": sum(not s['latitude'] or not s['longitude'] for s in samples),
            },
            "queries": {name:{"sql":sql,"result":[dict(r) for r in c.execute(sql)]} for name,sql in QUERIES.items()},
        }
    for path, expected in [(args.assembly, ASSEMBLY_SHA256), (args.annotations, ANNOTATIONS_SHA256)]:
        if sha256(path) != expected:
            raise ValueError(f"Input hash changed during read-only profiling: {path}")
    result['input_hashes_verified_before_and_after'] = True
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
