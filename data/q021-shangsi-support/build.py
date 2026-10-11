"""Extract six literal Shangsi Li rows; check a conditional design counterexample.

Standard library only. No model fitting, empirical power estimate or source repair.
Requires the checksum-matched publisher workbook; see README.md for retrieval.
"""
import argparse
import csv
import hashlib
import json
import math
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SHA256 = "6a53745faff1535d4504636fb4caa6ad18977dd1e86527e88d30b3f760e090c4"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
COLUMNS = {
    "sample_id": "B", "depth_m": "E", "formation": "G", "stage_as_stored": "H",
    "age_original_ma": "I", "age_study_ma": "J", "mc_icp_ms": "L",
    "mc_repeat": "M", "q_icp_ms": "N", "q_repeat": "O",
    "reported_delta7li_permil": "P", "reported_2sd_permil": "Q",
    "mn_sr_mol_mol": "Z",
}


def extract(source):
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != SHA256:
        raise ValueError(f"Workbook checksum mismatch: {digest}")
    with ZipFile(source) as z:
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        assert workbook.find("m:sheets/m:sheet", NS).get("name") == "Table S1"
        strings = ["".join(x.itertext()) for x in
                   ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    result = []
    for row in sheet.findall(".//m:row", NS):
        number, cells, formulas = row.get("r"), {}, {}
        for cell in row.findall("m:c", NS):
            v, f = cell.find("m:v", NS), cell.find("m:f", NS)
            value = "" if v is None else v.text
            if cell.get("t") == "s" and value:
                value = strings[int(value)]
            cells[cell.get("r")] = value
            if f is not None and f.text:
                formulas[cell.get("r")] = f.text
        if cells.get("C" + number) != "Shangsi" or not cells.get("P" + number):
            continue
        record = {"sheet": "Table S1", "xlsx_row": number,
                  "reported_2sd_formula": formulas.get("Q" + number, "")}
        record.update({key: cells.get(col + number, "") for key, col in COLUMNS.items()})
        result.append(record)
    assert [int(r["xlsx_row"]) for r in result] == [69, 70, 71, 76, 78, 80]
    return result


def response(t, amplitude, onset, tau):
    return 0.0 if t <= onset else amplitude * (-math.expm1(-(t - onset) / tau))


def design_check(rows):
    # Approximate 252 Ma origin is an illustrative coordinate, not a new date.
    ages = [float(r["age_study_ma"]) for r in rows]
    origin = 252.0
    times = [origin - a for a in ages]
    assert sum(t > 0 for t in times) == 1
    assert [r["stage_as_stored"] for r in rows].count("Induan") == 1
    t_last = max(times)
    tau, amplitude, delay = 1.0, 1.0, 0.25  # Hypothetical Myr, per mil, Myr.
    assert delay < t_last
    alternative_amplitude = response(t_last, amplitude, 0.0, tau) / response(t_last, 1.0, delay, tau)
    first = [response(t, amplitude, 0.0, tau) for t in times]
    second = [response(t, alternative_amplitude, delay, tau) for t in times]
    discrepancy = max(abs(x - y) for x, y in zip(first, second))
    assert discrepancy < 1e-12
    # Later predictions differ: equality is a limitation of this observation grid.
    later = [response(3.0, amplitude, 0.0, tau),
             response(3.0, alternative_amplitude, delay, tau)]
    assert abs(later[0] - later[1]) > 0.1

    anomaly = next(r for r in rows if r["xlsx_row"] == "76")
    visible = [float(anomaly[k]) for k in ("mc_icp_ms", "q_icp_ms", "q_repeat")]
    reported = float(anomaly["reported_delta7li_permil"])
    assert anomaly["reported_2sd_formula"] == "2*STDEV(L76:P76)"
    assert not math.isclose(statistics.mean(visible), reported)
    assert math.isclose(2 * statistics.stdev(visible + [reported]),
                        float(anomaly["reported_2sd_permil"]), rel_tol=1e-12)
    return {
        "kind": "Source-support check and conditional counterexample, not fitted Li histories",
        "source_sha256": SHA256,
        "sample_count": len(rows), "study_age_range_ma": [min(ages), max(ages)],
        "source_stage_counts": {k: sum(r["stage_as_stored"] == k for r in rows)
                                for k in sorted({r["stage_as_stored"] for r in rows})},
        "sample_age_covariance": "not supplied in the inspected table",
        "illustrative_step_response": {
            "coordinate_origin_ma": origin, "tau_myr": tau,
            "first_amplitude_permil": amplitude, "second_onset_delay_myr": delay,
            "second_amplitude_permil": alternative_amplitude,
            "sample_times_myr": times, "first_predictions": first, "second_predictions": second,
            "max_absolute_difference": discrepancy, "predictions_at_3_myr": later,
            "interpretation": "One post-onset sample cannot separate free amplitude and onset in this response family, even with fixed tau and exact ages.",
        },
        "row76_source_flag": {
            "reported_value": reported, "visible_replicate_mean_diagnostic_only": statistics.mean(visible),
            "formula": anomaly["reported_2sd_formula"],
            "action": "retain source literals; no correction or empirical uncertainty model inferred",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=ROOT / "data/raw/cao2022/41561_2022_1009_MOESM2_ESM.xlsx")
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    rows = extract(args.source)
    results = design_check(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "shangsi_samples.tsv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.output_dir / "design_check.json").write_text(json.dumps(results, indent=2) + "\n")
    print("Six source rows preserved; one Induan sample; conditional amplitude/onset counterexample passed.")


if __name__ == "__main__":
    main()
