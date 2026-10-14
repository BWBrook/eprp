#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Audit the original Walton–Korn workbook without saving or modifying it.

Run: uv run data/ammonoid-growth-support/audit_workbook.py
Outputs are audit aggregates, locators and exception records, not cleaned data.
"""

import argparse
from collections import Counter, defaultdict
import csv
from hashlib import md5, sha256
import json
import math
from pathlib import Path
import re
import sys
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import openpyxl
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw/ammonoid-growth-walton-korn-2018/Ontogenetic_Conch_Parameter_Data.xlsx"
EXPECTED_SHA = "fbe2012f1d420ef7b292141ae0ed0ea8d046c4c15303663565dc72e0727ebe40"
DATA_URL = "https://doi.org/10.5061/dryad.c17p8"
PAPER_URL = "https://doi.org/10.1111/pala.12308"
MEASURES = ("dm", "CWI", "UWI", "WER")
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def hashes(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest(), "md5": md5(raw).hexdigest()}


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def cell_type(cell):
    if cell.value is None:
        return "blank"
    if cell.data_type == "f":
        return "formula"
    if cell.data_type == "e":
        return "excel_error"
    if isinstance(cell.value, bool):
        return "boolean"
    if numeric(cell.value):
        return "numeric" if math.isfinite(cell.value) else "nonfinite_numeric"
    if isinstance(cell.value, str):
        return "literal_NA" if cell.value == "NA" else "text"
    return type(cell.value).__name__


def grouped_rows(sheet, columns):
    groups = defaultdict(list)
    for row in range(2, sheet.max_row + 1):
        groups[tuple(sheet.cell(row, col).value for col in columns)].append(row)
    return [{"key": list(key), "rows": rows} for key, rows in groups.items() if len(rows) > 1]


def write_tsv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit(source, outdir):
    before = hashes(source)
    if before["sha256"] != EXPECTED_SHA:
        raise ValueError(f"Source SHA256 does not match the agreed original: {before['sha256']}")
    book = openpyxl.load_workbook(source, data_only=False)
    cached = openpyxl.load_workbook(source, data_only=True)
    if book.sheetnames != ["Species", *MEASURES]:
        raise ValueError(f"Unexpected sheet layout: {book.sheetnames}")
    species = book["Species"]
    if [c.value for c in species[1]] != ["Species", "Family", "Superfamily", "Stage", "Period", "CWI Ontog", "UWI Ontog", "Source"]:
        raise ValueError("Species schema changed; inspect before adapting the audit")
    expected_whorls = [f"Whorl {12-i/2:g}" for i in range(25)]
    for name in MEASURES:
        sheet = book[name]
        if sheet.max_row != species.max_row or sheet.max_column != 31:
            raise ValueError(f"Unexpected dimensions for {name}")
        if [sheet.cell(1, c).value for c in range(7, 32)] != expected_whorls:
            raise ValueError(f"Unexpected whorl headers for {name}")

    summary = {
        "source": {"path": str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source),
                   "dataset_url": DATA_URL, "paper_url": PAPER_URL, "hashes_before": before},
        "software": {"python": sys.version.split()[0], "openpyxl": openpyxl.__version__},
        "interpretation_limits": [
            "Rows are workbook series records, not established independent specimens.",
            "Repeated labels remain separate rows; no deduplication or silent value correction.",
            "Whorl indices are copied labels, not verified absolute age, maturity, embryonic stages or completeness.",
            "Stage/Period columns describe geological assignments, not individual developmental stages.",
            "Source strings are unresolved citations/material descriptions, not inferred DOI links.",
            "No ancestry, sister relationship or evolutionary transition is inferred from chronology or taxonomy.",
            "Numeric ratios above one are not automatically invalid: CWI has no imposed upper bound.",
            "openpyxl does not evaluate formulas; formula and cached-value inventories are separate.",
        ],
        "sheets": {},
    }
    issues = []
    formula_records, error_records, hyperlinks, comments = [], [], [], []
    for sheet in book:
        types = Counter(cell_type(c) for row in sheet for c in row)
        for row in sheet:
            for cell in row:
                loc = f"{sheet.title}!{cell.coordinate}"
                if cell.data_type == "f":
                    cc = cached[sheet.title][cell.coordinate]
                    formula_records.append({"locator": loc, "formula": cell.value,
                                            "cached_value": cc.value, "cached_type": cell_type(cc)})
                if cell.data_type == "e":
                    error_records.append({"locator": loc, "error": cell.value})
                if cell.hyperlink:
                    hyperlinks.append({"locator": loc, "target": cell.hyperlink.target,
                                       "location": cell.hyperlink.location})
                if cell.comment:
                    comments.append({"locator": loc, "text": cell.comment.text})
        summary["sheets"][sheet.title] = {
            "rows_including_header": sheet.max_row, "data_rows": sheet.max_row-1,
            "columns": sheet.max_column, "headers": {c.coordinate: c.value for c in sheet[1]},
            "cell_inventory_in_declared_rectangle": dict(sorted(types.items())),
            "hidden": sheet.sheet_state, "merged_ranges": [str(r) for r in sheet.merged_cells.ranges],
            "exact_duplicate_full_rows": grouped_rows(sheet, range(1, sheet.max_column+1)),
        }
    summary["formulas"] = {"count": len(formula_records), "records": formula_records}
    summary["excel_errors"] = {"count": len(error_records), "records": error_records}
    summary["hyperlinks"] = hyperlinks
    summary["comments"] = comments
    summary["defined_names"] = list(book.defined_names)
    summary["external_link_count"] = len(book._external_links)
    with ZipFile(source) as archive:
        xml_inventory = []
        for name in sorted(n for n in archive.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)):
            tree = ET.fromstring(archive.read(name))
            cells = tree.findall(".//s:c", NS)
            xml_inventory.append({"xml_part": name, "stored_cell_elements": len(cells),
                                  "formula_elements": len(tree.findall(".//s:f", NS)),
                                  "value_elements": len(tree.findall(".//s:v", NS))})
    summary["raw_xml_inventory"] = xml_inventory

    labels = [species.cell(r, 1).value for r in range(2, species.max_row+1)]
    source_groups = defaultdict(list)
    for row in range(2, species.max_row+1):
        source_groups[species.cell(row, 8).value].append(row)
    summary["taxon_records"] = {
        "row_count": len(labels), "distinct_exact_species_labels": len(set(labels)),
        "duplicate_species_labels": grouped_rows(species, [1]),
        "distinct_families": len({species.cell(r, 2).value for r in range(2, species.max_row+1)}),
        "distinct_superfamilies": len({species.cell(r, 3).value for r in range(2, species.max_row+1)}),
        "period_row_counts": dict(Counter(species.cell(r, 5).value for r in range(2, species.max_row+1))),
        "stage_row_counts": dict(Counter(species.cell(r, 4).value for r in range(2, species.max_row+1))),
        "source_string_groups": [{"source_text": key, "count": len(rows), "Species_rows": rows,
                                   "source_column": "H", "dataset_url": DATA_URL}
                                  for key, rows in source_groups.items()],
        "CWI_Ontog_codes": dict(Counter(species.cell(r, 6).value for r in range(2, species.max_row+1))),
        "UWI_Ontog_codes": dict(Counter(species.cell(r, 7).value for r in range(2, species.max_row+1))),
        "code_interpretation": "Exact source codes preserved; no legend or molecular meaning inferred.",
    }
    stage_periods = defaultdict(lambda: defaultdict(list))
    for row in range(2, species.max_row+1):
        stage_periods[species.cell(row, 4).value][species.cell(row, 5).value].append(row)
    summary["taxon_records"]["stage_labels_assigned_multiple_periods"] = [
        {"stage_label": stage, "periods_and_Species_rows": dict(periods),
         "locators": [f"Species!D{row}:E{row}" for rows in periods.values() for row in rows],
         "interpretation": "Observed inconsistent period assignment for a repeated stage label; no source value corrected."}
        for stage, periods in stage_periods.items() if len(periods) > 1]
    alignment = {}
    for name in MEASURES:
        sheet = book[name]
        mismatch = []
        for row in range(2, sheet.max_row+1):
            for col in range(1, 6):
                if sheet.cell(row, col).value != species.cell(row, col).value:
                    mismatch.append({"locator": f"{name}!{get_column_letter(col)}{row}",
                                     "Species_locator": f"Species!{get_column_letter(col)}{row}",
                                     "value": sheet.cell(row, col).value, "Species_value": species.cell(row, col).value})
        alignment[name] = {"metadata_columns_compared": "A:E", "exact_label_sequence_matches":
                           [sheet.cell(r, 1).value for r in range(2, sheet.max_row+1)] == labels,
                           "metadata_cell_mismatches": mismatch,
                           "parameter_codes_F": dict(Counter(sheet.cell(r, 6).value for r in range(2, sheet.max_row+1)))}
        values = [c for row in sheet.iter_rows(min_row=2, min_col=7) for c in row if numeric(c.value)]
        minimum, maximum = min(c.value for c in values), max(c.value for c in values)
        zero = [c.coordinate for c in values if c.value == 0]
        negative = [c.coordinate for c in values if c.value < 0]
        for cell in values:
            flag = None
            if not math.isfinite(cell.value):
                flag = "nonfinite"
            elif name in ("dm", "CWI", "WER") and cell.value <= 0:
                flag = "nonpositive"
            elif name == "UWI" and not 0 <= cell.value <= 1:
                flag = "outside_screening_interval_0_1"
            elif name == "WER" and cell.value <= 1:
                flag = "WER_at_or_below_one_review_only"
            if flag or cell.value == 0:
                issues.append({"kind": flag or "zero_recorded_not_automatically_invalid", "sheet": name,
                               "cell": cell.coordinate, "value": cell.value,
                               "taxon_label": sheet.cell(cell.row, 1).value})
        summary["sheets"][name]["measurement_inventory_G2_AE180"] = {
            "counts": dict(Counter(cell_type(c) for row in sheet.iter_rows(min_row=2, min_col=7) for c in row)),
            "numeric_min": minimum, "numeric_max": maximum,
            "numeric_min_locators": [c.coordinate for c in values if c.value == minimum],
            "numeric_max_locators": [c.coordinate for c in values if c.value == maximum],
            "zero_cells": zero, "negative_cells": negative,
            "screening_rule": {"dm": ">0; units not labelled in headers", "CWI": ">0; no upper bound imposed",
                               "UWI": "0<=uw/dm<=1 as a screening interval, not source validation",
                               "WER": ">0; <=1 marked review-only"}[name],
        }
    summary["alignment_to_Species"] = alignment

    series_rows = []
    mask_diffs = defaultdict(list)
    complete_counts = []
    for row in range(2, species.max_row+1):
        record = {"Species_row": row, "taxon_label": species.cell(row, 1).value,
                  "source_locator": f"Species!H{row}", "source_text": species.cell(row, 8).value,
                  "dataset_url": DATA_URL}
        all_numeric_columns = []
        for col in range(7, 32):
            if all(numeric(book[name].cell(row, col).value) for name in MEASURES):
                all_numeric_columns.append(col)
            for name in ("CWI", "UWI", "WER"):
                dm_present = numeric(book["dm"].cell(row, col).value)
                val_present = numeric(book[name].cell(row, col).value)
                if dm_present != val_present:
                    mask_diffs[name].append({"metric_locator": f"{name}!{get_column_letter(col)}{row}",
                                             "diameter_locator": f"dm!{get_column_letter(col)}{row}",
                                             "diameter_numeric": dm_present, "metric_numeric": val_present})
        for name in MEASURES:
            cols = [c for c in range(7, 32) if numeric(book[name].cell(row, c).value)]
            record[f"{name}_numeric_n"] = len(cols)
            record[f"{name}_first_last_numeric_cells"] = f"{get_column_letter(cols[0])}{row}:{get_column_letter(cols[-1])}{row}" if cols else ""
            gaps = [c for c in range(min(cols), max(cols)+1) if c not in cols] if cols else []
            record[f"{name}_internal_nonnumeric_n"] = len(gaps)
            for col in gaps:
                issues.append({"kind": "internal_nonnumeric_gap", "sheet": name,
                               "cell": f"{get_column_letter(col)}{row}", "value": book[name].cell(row, col).value,
                               "taxon_label": species.cell(row, 1).value})
        record["all_four_numeric_same_whorl_n"] = len(all_numeric_columns)
        complete_counts.append(len(all_numeric_columns))
        series_rows.append(record)
    summary["measurement_pairing"] = {
        "same_whorl_all_four_numeric_cell_positions": sum(complete_counts),
        "rows_with_any_all_four_numeric_position": sum(n > 0 for n in complete_counts),
        "per_row_all_four_numeric_n_distribution": dict(sorted(Counter(complete_counts).items())),
        "diameter_vs_metric_numeric_mask_disagreements": {
            name: {"count": len(mask_diffs[name]), "metric_present_diameter_absent": sum(not x["diameter_numeric"] for x in mask_diffs[name]),
                   "first_10_exact_locators": mask_diffs[name][:10]} for name in ("CWI", "UWI", "WER")},
    }
    profiles = defaultdict(list)
    for row in range(2, species.max_row+1):
        profile = tuple(book[name].cell(row, col).value for name in MEASURES for col in range(7,32))
        profiles[profile].append(row)
    summary["repeated_combined_numeric_and_NA_profiles"] = [rows for rows in profiles.values() if len(rows)>1]
    summary["series_structure"] = {
        "measurement_rows_per_sheet": len(labels), "measurement_columns": "G:AE",
        "whorl_headers": expected_whorls, "specimen_id_field": None,
        "series_identifier": "sheet row number only; individual specimen identity is not explicit",
        "measurement_unit_field": None, "collection_or_source_field": "Species!H2:H180",
        "duplicate_label_interpretation": "Repeated taxon labels do not establish repeated specimens or erroneous duplicates; preserve both records.",
    }
    scans = {
        "maturity_or_early_life": r"\b(adult|juvenile|mature|maturity|embryo|embryonic|hatchling|hatching|larval|larva|nepionic|ammonitella|protoconch)\b",
        "specimen_or_individual": r"\b(specimen|individual|voucher|catalogue|catalog)\b",
        "phylogeny_or_relationship": r"\b(phylogeny|phylogenetic|ancestor|ancestral|descendant|sister|transition|branch|node|newick|nexus)\b",
    }
    summary["explicit_label_scans"] = {}
    for label, pattern in scans.items():
        hits = [{"locator": f"{sheet.title}!{c.coordinate}", "text": c.value}
                for sheet in book for row in sheet for c in row
                if isinstance(c.value, str) and re.search(pattern, c.value, re.IGNORECASE)]
        summary["explicit_label_scans"][label] = {"pattern": pattern, "hits": hits,
            "scope": "all worksheet cell text; comments separately inventoried; not a search of the cited literature"}
    summary["explicit_maturity_coverage"] = "Not computable without life-stage labels; no inference from diameter or Whorl 0."
    summary["explicit_evolutionary_transition_count"] = 0 if not summary["explicit_label_scans"]["phylogeny_or_relationship"]["hits"] else None
    summary["evolutionary_transition_limit"] = "No relationship table or tree is among the five observed sheets; zero explicit transitions is not zero historical transitions."
    summary["issues"] = {"counts": dict(Counter(x["kind"] for x in issues)), "records": issues}
    after = hashes(source)
    summary["source"]["hashes_after"] = after
    summary["source"]["unchanged"] = before == after
    if before != after:
        raise RuntimeError("Source changed during audit; refuse to write results")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "workbook-audit-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
    write_tsv(outdir / "workbook-series-audit.tsv", series_rows, list(series_rows[0]))
    print(json.dumps({"taxon_rows": len(labels), "distinct_taxon_labels": len(set(labels)),
                      "numeric_measurements": {n: summary["sheets"][n]["measurement_inventory_G2_AE180"]["counts"] for n in MEASURES},
                      "issues": summary["issues"]["counts"], "source_unchanged": before == after,
                      "output_directory": str(outdir)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    audit(args.source.resolve(), args.output_dir.resolve())
