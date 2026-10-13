#!/usr/bin/env python3
"""Preserve Taylor 2026 Table S1 and report support, without fitting a model."""

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean
from xml.etree import ElementTree as ET
from zipfile import ZipFile

SHA256 = "5a34ca9c21319466353d0904c0155a1d178838f9bbf2b4e150702cc746629fc6"
DOI = "https://doi.org/10.2475/001c.156171"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FIELDS = ["section", "sample_id", "height_m", "stage", "age_ma",
          "delta7li_permil", "err_as_reported", "li_ppm", "li_ca_umol_mol",
          "mg_ca_mmol_mol", "al_ca_mmol_mol", "sr_ca_mmol_mol",
          "mn_sr_mol_mol", "carbonate_wt_percent", "reference"]
HEADER = ["Section", "Sample ID", "Height (m)", "Stage", "Age (Ma)",
          "d7Licarb (‰)", "err.", "Li (ppm)", "Li/Ca (umol/mol)",
          "Mg/Ca (mmol/mol)", "Al/Ca (mmol/mol)", "Sr/Ca (mmol/mol)",
          "Mn/Sr (mol/mol)", "wt.% carbonate", "Reference", ""]
EARLY = {"Induan", "Olenekian"}
LATER = {"Anisian", "Ladinian", "Carnian"}


def extract(path):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SHA256:
        raise ValueError(f"Unexpected source SHA-256: {digest}")
    with ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
    tables = doc.findall(".//w:tbl", NS)
    assert len(tables) == 1
    rows = [["".join(t.text or "" for t in cell.findall(".//w:t", NS))
             for cell in row.findall("w:tc", NS)]
            for row in tables[0].findall("w:tr", NS)]
    assert len(rows) == 86 and rows[2] == HEADER
    records = []
    for n, cells in enumerate(rows[3:], 4):
        assert len(cells) == 16 and cells[-1] == ""
        r = {"docx_table": "1", "docx_row": str(n)}
        r.update(zip(FIELDS, cells[:15]))
        r["labelled_duplicate"] = str(r["sample_id"].endswith("-dup")).lower()
        r["base_id_from_suffix"] = r["sample_id"].removesuffix("-dup")
        r["source_doi"] = DOI
        records.append(r)
    assert Counter(r["section"] for r in records) == {
        "Taskent": 35, "Takachiho": 29, "Shanggang": 16, "Shangsi": 3}
    assert len({(r["section"], r["sample_id"]) for r in records}) == 83
    return records, rows[0][0]


def span(rows, field):
    values = [float(r[field]) for r in rows if r[field] not in ("", "NA")]
    return [min(values), max(values)] if values else None


def contrast(rows, late_stages, collapse_duplicates):
    # This alternative weights labelled base samples equally; it is a
    # descriptive sensitivity, not an adjudication of the authors' pipeline.
    grouped = defaultdict(list)
    for r in rows:
        key = r["base_id_from_suffix"] if collapse_duplicates else r["sample_id"]
        grouped[key].append(r)
    points = []
    for members in grouped.values():
        assert len({(r["stage"], r["age_ma"], r["height_m"]) for r in members}) == 1
        points.append({"stage": members[0]["stage"],
                       "value": mean(float(r["delta7li_permil"]) for r in members)})
    early = [r["value"] for r in points if r["stage"] in EARLY]
    late = [r["value"] for r in points if r["stage"] in late_stages]
    return {"early_n": len(early), "later_n": len(late),
            "early_mean_permil": round(mean(early), 6),
            "later_mean_permil": round(mean(late), 6),
            "later_minus_early_permil": round(mean(late) - mean(early), 6)}


def summarise(records, caption):
    sections = {}
    for section in ("Taskent", "Takachiho", "Shanggang", "Shangsi"):
        rows = [r for r in records if r["section"] == section]
        stages = {}
        for stage in dict.fromkeys(r["stage"] for r in rows):
            group = [r for r in rows if r["stage"] == stage]
            stages[stage] = {"rows": len(group),
                "base_ids": len({r["base_id_from_suffix"] for r in group}),
                "source_age_range_ma": span(group, "age_ma"),
                "row_mean_delta7li_permil": round(mean(float(r["delta7li_permil"]) for r in group), 6)}
        result = {"rows": len(rows),
                  "base_ids": len({r["base_id_from_suffix"] for r in rows}),
                  "source_age_range_ma": span(rows, "age_ma"), "stages": stages,
                  "missing_counts": {k: sum(r[k] in ("", "NA") for r in rows)
                                     for k in FIELDS},
                  "al_ca_range_mmol_mol": span(rows, "al_ca_mmol_mol"),
                  "err_range_as_reported": span(rows, "err_as_reported")}
        if section in ("Taskent", "Takachiho"):
            by_id = {r["sample_id"]: r for r in rows}
            pairs = []
            for r in rows:
                if r["labelled_duplicate"] == "true":
                    original = by_id[r["base_id_from_suffix"]]
                    pairs.append({"base_id": original["sample_id"],
                                  "docx_rows": [original["docx_row"], r["docx_row"]],
                                  "absolute_delta7li_difference_permil": round(abs(float(original["delta7li_permil"]) - float(r["delta7li_permil"])), 6)})
            result["labelled_duplicate_pairs"] = pairs
            result["descriptive_contrasts"] = {
                late_name: {weight: contrast(rows, late, collapse)
                            for weight, collapse in (("all_rows", False), ("equal_base_samples", True))}
                for late_name, late in (("Anisian_minus_Induan_Olenekian", {"Anisian"}),
                                       ("Anisian_Ladinian_Carnian_minus_Induan_Olenekian", LATER))}
            last_early = min((r for r in rows if r["stage"] in EARLY), key=lambda r: float(r["age_ma"]))
            first_later = max((r for r in rows if r["stage"] in LATER), key=lambda r: float(r["age_ma"]))
            result["sample_gap_across_source_stage_groups"] = {
                "last_early_sample": last_early["sample_id"], "last_early_age_ma": last_early["age_ma"],
                "first_later_sample": first_later["sample_id"], "first_later_age_ma": first_later["age_ma"],
                "nominal_gap_myr": round(float(last_early["age_ma"]) - float(first_later["age_ma"]), 6)}
            floor = .36 if section == "Taskent" else .58
            result["rows_below_stated_bracketing_2sd"] = [r["docx_row"] for r in rows if float(r["err_as_reported"]) < floor]
            result["rows_with_all_s5_element_ratios"] = sum(all(r[k] not in ("", "NA") and float(r[k]) > 0 for k in ("sr_ca_mmol_mol", "li_ca_umol_mol", "mg_ca_mmol_mol", "mn_sr_mol_mol")) for r in rows)
        sections[section] = result
    return {"source_sha256": SHA256, "source_caption": caption,
            "source_columns": HEADER, "sections": sections,
            "interpretation": "Support inventory and descriptive arithmetic only. Source ages/stages/NA/rounding retained. No age errors, mineral phases or alteration corrections imputed. No fit, test, confidence interval, power claim or independent-row assumption.",
            "contrast_policy": "Early=source Induan+Olenekian; later=specified source stages. Equal-base alternative averages only explicitly labelled -dup pairs, then weights base IDs equally. Neither policy corrects the raw table."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    records, caption = extract(args.table)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "table_s1.tsv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    (args.output_dir / "support_summary.json").write_text(
        json.dumps(summarise(records, caption), indent=2, ensure_ascii=False) + "\n")
    print("Preserved 83 rows: 64 Taylor rows (60 base IDs) and 19 reused Cao rows.")


if __name__ == "__main__":
    main()
