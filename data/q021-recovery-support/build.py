"""Preserve literal Li sample tables; summarise support without assigning new ages.

Standard library only. Inputs must match the published workbook checksums.
No isotope conversion, sample exclusion, age interpolation or model fitting.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
CAO_SHA = "6a53745faff1535d4504636fb4caa6ad18977dd1e86527e88d30b3f760e090c4"
RAUZI_SHA = "3f92702b0f60a9a7b1b9ecebca8508cdd1fb8dc8fc1e816addb04b33a88edd38"
CAO_URL = "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41561-022-01009-x/MediaObjects/41561_2022_1009_MOESM2_ESM.xlsx"
RAUZI_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11317597/supplementaryFiles"


def sheet(path, checksum):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != checksum:
        raise ValueError(f"Checksum mismatch for {path.name}: {digest}")
    with ZipFile(path) as z:
        strings = ["".join(s.itertext()) for s in
                   ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
        xml = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows = []
    for row in xml.findall(".//m:row", NS):
        cells, formulas = {}, {}
        for cell in row.findall("m:c", NS):
            col = cell.get("r").rstrip("0123456789")
            v, f = cell.find("m:v", NS), cell.find("m:f", NS)
            value = "" if v is None else v.text
            if cell.get("t") == "s" and value:
                value = strings[int(value)]
            elif cell.get("t") == "inlineStr":
                value = "".join(cell.find("m:is", NS).itertext())
            cells[col] = value
            if f is not None:
                formulas[col] = f.text
        rows.append((row.get("r"), cells, formulas))
    return rows


def extract_cao(path):
    columns = {"sample_id": "B", "depth_m": "E", "conodont_zone": "F",
               "formation": "G", "stage_as_stored": "H", "age_original_ma": "I",
               "age_study_ma": "J", "sr87_sr86": "K", "mc_icp_ms": "L",
               "mc_repeat": "M", "q_icp_ms": "N", "q_repeat": "O",
               "reported_delta7li_permil": "P", "reported_2sd_permil": "Q",
               "li_ppm": "R", "mg_ca_mmol_mol": "T", "rb_sr_mol_mol": "Y",
               "mn_sr_mol_mol": "Z"}
    result = []
    for n, cells, formulas in sheet(path, CAO_SHA):
        if cells.get("C") != "Shanggang" or not cells.get("P"):
            continue
        record = {"sheet": "Table S1", "xlsx_row": n,
                  "source_formulas": json.dumps(formulas, sort_keys=True)}
        record.update({name: cells.get(col, "") for name, col in columns.items()})
        record["source_url"] = CAO_URL
        result.append(record)
    return result


def extract_rauzi(path):
    columns = {"sample_id": "A", "depth_as_stored": "B", "rock_type_as_stored": "C",
               "delta7li_permil": "D", "std_error_permil": "E", "li_ppm": "F",
               "th_ppm": "G", "sc_ppm": "H", "tio2_wt_percent": "I",
               "al2o3_wt_percent": "J", "na2o_wt_percent": "K",
               "cao_wt_percent": "L", "k2o_wt_percent": "M"}
    result, section, depth_header = [], "", ""
    for n, cells, formulas in sheet(path, RAUZI_SHA):
        nonempty = {k: v for k, v in cells.items() if v}
        if set(nonempty) == {"A"}:
            section = cells["A"]  # Retain the original label, including spaces.
        elif cells.get("A") == "Sample":
            depth_header = cells["B"]
            assert "Age" not in " ".join(nonempty.values())
        elif cells.get("A") and cells.get("D"):
            assert section and depth_header
            record = {"sheet": "Sheet1", "xlsx_row": n,
                      "section_as_stored": section, "depth_header_as_stored": depth_header,
                      "source_formulas": json.dumps(formulas, sort_keys=True)}
            record.update({name: cells.get(col, "") for name, col in columns.items()})
            record["source_url"] = RAUZI_URL
            result.append(record)
    return result


def summarise(cao, rauzi):
    groups = {}
    for name in sorted({r["section_as_stored"] for r in rauzi}):
        rows = [r for r in rauzi if r["section_as_stored"] == name]
        groups[name] = {
            "rows": len(rows), "unique_sample_ids": len({r["sample_id"] for r in rows}),
            "depth_header": sorted({r["depth_header_as_stored"] for r in rows}),
            "depth_range_as_stored": [min(float(r["depth_as_stored"]) for r in rows),
                                      max(float(r["depth_as_stored"]) for r in rows)],
            "delta7li_range_permil": [min(float(r["delta7li_permil"]) for r in rows),
                                     max(float(r["delta7li_permil"]) for r in rows)],
            "rock_type_counts_as_stored": dict(sorted(Counter(r["rock_type_as_stored"] for r in rows).items())),
        }
    return {
        "source_sha256": {"cao": CAO_SHA, "rauzi_dataset_s3": RAUZI_SHA},
        "shanggang": {
            "li_rows": len(cao), "main_methods_reported_n": 15,
            "stage_counts_as_stored": dict(Counter(r["stage_as_stored"] for r in cao)),
            "study_age_range_ma": [min(float(r["age_study_ma"]) for r in cao),
                                   max(float(r["age_study_ma"]) for r in cao)],
            "mn_sr_at_least_3_rows": [r["xlsx_row"] for r in cao if float(r["mn_sr_mol_mol"]) >= 3],
            "mn_sr_at_least_4_rows": [r["xlsx_row"] for r in cao if float(r["mn_sr_mol_mol"]) >= 4],
            "q_vs_final_mismatch_rows": [r["xlsx_row"] for r in cao
                                         if r["q_icp_ms"] != r["reported_delta7li_permil"]],
        },
        "rauzi": {"li_rows": len(rauzi), "sections": groups,
                  "numerical_sample_ages_in_workbook": False,
                  "note": "Depths are not numerical ages. Split sections and faults require explicit crosswalks; authigenesis may postdate deposition."},
        "interpretation": "Support inventory only; counts are not independent temporal constraints. Source discrepancies retained, no exclusions or repairs.",
    }


def write_tsv(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cao", required=True, type=Path)
    parser.add_argument("--rauzi", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    cao, rauzi = extract_cao(args.cao), extract_rauzi(args.rauzi)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.output_dir / "shanggang_samples.tsv", cao)
    write_tsv(args.output_dir / "rauzi_samples.tsv", rauzi)
    (args.output_dir / "support_summary.json").write_text(json.dumps(summarise(cao, rauzi), indent=2) + "\n")
    print(f"Preserved {len(cao)} Shanggang and {len(rauzi)} Rauzi Li rows; no ages assigned.")


if __name__ == "__main__":
    main()
