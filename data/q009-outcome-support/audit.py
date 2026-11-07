#!/usr/bin/env python3
"""Count temporal support in pinned source tables without fitting recovery models."""

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import xml.etree.ElementTree as ET
import zipfile

EXPECTED = {
    "41586_2019_1590_MOESM2_ESM.xlsx": "5fc615afdf94fa7842375e9c34b98d1f87f41e29700ef97da11b149eb59c7caa",
    "pangaea-893899.txt": "8b6e57a894b91e430ef2e26a372cc9b25e56927b9d2f6fbfb068462e623b5906",
    "pangaea-893919.txt": "945a2aeadafd9efdb02c80ec31f41a3c5a851fb9c3e0b61abaff4232aefd0756",
    "pangaea-997781.txt": "60d0a282d2e9f3116778762254ee651a301344763a48806857f94b700122423e",
    "alvarez-fig2.xlsx": "a2b55b1bcdca2e59731ccfa25c9b3353bcdaacb7c1740253140bb9642cd2fd1c",
}
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def spreadsheet(path):
    with zipfile.ZipFile(path) as archive:
        strings = ["".join(s.itertext()) for s in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("s:si", NS)]
        root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    if root.findall(".//s:f", NS):
        raise ValueError("Unexpected source formula; inspect its cache before use")
    result = {}
    for row in root.findall(".//s:row", NS):
        cells = {}
        for c in row.findall("s:c", NS):
            key = c.attrib["r"].rstrip("0123456789")
            value = c.find("s:v", NS)
            if c.attrib.get("t") == "inlineStr":
                cells[key] = "".join(c.find("s:is", NS).itertext())
            elif value is not None:
                cells[key] = strings[int(value.text)] if c.attrib.get("t") == "s" else value.text
        result[int(row.attrib["r"])] = cells
    return result


def deposited(path):
    _, sep, body = path.read_text().partition("*/")
    if not sep:
        raise ValueError("Missing PANGAEA metadata terminator")
    return list(csv.DictReader(io.StringIO(body.lstrip()), delimiter="\t"))


def age_summary(ages):
    unique = sorted(set(ages))
    gaps = [1000 * (b - a) for a, b in zip(unique, unique[1:])]
    return {"rows": len(ages), "distinct_age_values": len(unique),
            "age_ma_min": min(unique), "age_ma_max": max(unique),
            "median_distinct_age_gap_kyr": statistics.median(gaps) if gaps else None,
            "largest_distinct_age_gap_kyr": max(gaps) if gaps else None}


def timing_landmarks(series, ages, investigators=None, youngest_allowed=None):
    ordered = sorted(set(ages))
    out = []
    for tick in range(math.ceil(2 * min(ages)), math.floor(2 * max(ages)) + 1):
        t = tick / 2
        past = [i for i, a in enumerate(ages) if t < a <= t + .15]
        future = [i for i, a in enumerate(ages) if t - .15 <= a < t]
        reasons = []
        if min(ages) > t - .15 or max(ages) < t + .15:
            reasons.append("window_outside_source_range")
        if len(past) < 3 or len(future) < 3:
            reasons.append("fewer_than_three_rows_in_a_window")
        if any(b - a > .1 + 1e-10 and a < t + .15 and b > t - .15 for a, b in zip(ordered, ordered[1:])):
            reasons.append("window_intersects_gap_over_100kyr")
        if youngest_allowed is not None and t - .15 < youngest_allowed:
            reasons.append("window_enters_poor_chronology_interval")
        labels = {investigators[i] for i in past + future} if investigators else set()
        if len(labels) > 1:
            reasons.append("window_crosses_investigator_codes")
        out.append({"series": series, "landmark_ma": t, "past_rows_older": len(past), "future_rows_younger": len(future),
                    "passes_timing_rules_only": not reasons, "failures": ";".join(reasons),
                    "investigator_codes": ";".join(sorted(labels))})
    return out


def run(inputs, output):
    hashes = {}
    for name, expected in EXPECTED.items():
        actual = hashlib.sha256((inputs / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Source hash mismatch: {name}")
        hashes[name] = actual
    workbook = spreadsheet(inputs / "41586_2019_1590_MOESM2_ESM.xlsx")
    headers = workbook[8]
    if headers.get("AC") != "Age_(Myr_ago)" or headers.get("O") != "Species richness":
        raise ValueError("Source schema changed")
    samples = [r for n, r in workbook.items() if n > 8 and r.get("AC")]
    raw_ages = [float(r["AC"]) for r in samples]
    richness = [float(r["N"]) for n, r in workbook.items() if n > 8 and r.get("N") and r.get("O")]
    variability = [float(r["A"]) for n, r in workbook.items() if n > 8 and r.get("A") and r.get("L")]
    pangaea = deposited(inputs / "pangaea-893919.txt")
    if len(samples) != len(pangaea):
        raise ValueError("Source row counts disagree")
    elkef = deposited(inputs / "pangaea-997781.txt")
    age_columns = [k for k in elkef[0] if k.startswith("Age [Ma]")]
    if len(age_columns) != 2:
        raise ValueError("Expected two El Kef age columns")
    result = {"source_sha256": hashes,
              "pacific_original": age_summary(raw_ages),
              "pacific_richness_separate_series": age_summary(richness),
              "pacific_published_variability_separate_series": age_summary(variability),
              "el_kef_age_columns": {k: age_summary([float(r[k]) for r in elkef if r[k]]) for k in age_columns},
              "qualifications": ["Age gaps are source-spacing diagnostics, not independent replicates or uncertainty bounds", "Workbook series use their own age columns; rows are not joined by spreadsheet row number", "Absolute one-Myr bins describe coverage only; no cross-site or cross-calibration age equivalence asserted", "Four-taxon nonblank support does not validate richness or a compositional closure", "No response model, effect estimate, outcome-defined event selection or power calculation"]}
    result["pacific_original"]["source_investigator_counts"] = dict(Counter(r["Q"] for r in samples))
    result["pacific_original"]["four_selected_taxa_nonblank_rows"] = sum(all(r.get(c) for c in ("AJ", "AP", "AQ", "AL", "AM")) for r in samples)
    comparison = spreadsheet(inputs / "alvarez-fig2.xlsx")
    if comparison[3].get("B") != "age_ma_W18":
        raise ValueError("Figure 2 schema changed")
    labelled = [{"source_excel_row": n, "literal_label": r["A"], "source_age_ma_W18": r["B"],
                 "interpretation": "published comparison row; date is not established as event onset"}
                for n, r in sorted(comparison.items()) if n > 3 and r.get("A") and r.get("B")]
    result["pacific_fig2_comparison_rows"] = sum(bool(r.get("B")) for n, r in comparison.items() if n > 3)
    result["pacific_fig2_labelled_rows"] = labelled
    timing = timing_landmarks("Pacific_original", raw_ages, [r["Q"] for r in samples])
    for k in age_columns:
        timing += timing_landmarks("El_Kef_" + k, [float(r[k]) for r in elkef], youngest_allowed=62.54)
    result["timing_rule_counts_only"] = {k: {"candidate_landmarks": sum(r["series"] == k for r in timing),
                                              "passes": sum(r["series"] == k and r["passes_timing_rules_only"] for r in timing)}
                                         for k in sorted({r["series"] for r in timing})}
    bins = []
    for site, ages, rows, investigator_key in (("Pacific_original", raw_ages, samples, "Q"), ("El_Kef_model_1", [float(r[age_columns[0]]) for r in elkef], elkef, None)):
        by_bin = defaultdict(list)
        for age, row in zip(ages, rows):
            by_bin[math.floor(age)].append((age, row))
        for lower, entries in sorted(by_bin.items()):
            counts = Counter(row[investigator_key] for age, row in entries) if investigator_key else {}
            bins.append({"series": site, "bin_ma_lower_inclusive": lower, "bin_ma_upper_exclusive": lower + 1,
                         "source_rows": len(entries), "distinct_age_values": len({a for a, r in entries}),
                         "source_investigator_counts": json.dumps(dict(counts), sort_keys=True)})
    result["source_field_names"] = {"pacific_sample_metadata": [headers[c] for c in ("Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC")],
                                    "el_kef_count_table": list(elkef[0]),
                                    "pacific_metadata_table": list(pangaea[0])}
    output.mkdir(parents=True, exist_ok=True)
    with (output / "timing-landmarks.tsv").open("w", newline="") as f:
        fields = [k for k in timing[0] if k != "series"] + ["series"]
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(timing)
    with (output / "published-comparison-rows.tsv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(labelled[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(labelled)
    with (output / "coverage-by-age.tsv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(bins[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(bins)
    result["audit_script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (output / "support-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("source_field_names", "source_sha256", "qualifications")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    run(args.input_dir, args.output)
