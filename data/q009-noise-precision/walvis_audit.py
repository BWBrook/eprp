#!/usr/bin/env python3
"""Reproduce the sparse Walvis abundance timing census from the public supplement."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "q009-outcome-support"))
from audit import spreadsheet


def run(source, output):
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != "fefb143d84e84137250347fec393dae061214b4b1eb9004efbae02c83beb5a78":
        raise ValueError("Unexpected Gibbs source workbook")
    rows = spreadsheet(source)
    if rows[790].get('B') != 'age_ma_DT14_La11':
        raise ValueError("Unexpected Walvis source header")
    ages = sorted(float(rows[i]['B']) for i in range(791,817))
    gaps = [1000*(b-a) for a,b in zip(ages,ages[1:])]
    counts = [{"landmark_ma": age, "older_rows": sum(age < a <= age+.15 for a in ages),
               "younger_rows": sum(age-.15 <= a < age for a in ages)} for age in (64.,64.5,65.,65.5,66.)]
    result = {"source_sha256": digest, "sheet": "Figure 1 data", "source_rows_inclusive": [791,816],
              "rows": len(ages), "age_ma_min": min(ages), "age_ma_max": max(ages),
              "median_age_gap_kyr": statistics.median(gaps), "max_age_gap_kyr": max(gaps),
              "timing_census_before_gap_or_boundary_exclusions": counts,
              "landmarks_with_at_least_three_rows_each_window": sum(r['older_rows']>=3 and r['younger_rows']>=3 for r in counts),
              "qualification": "Converted cellular percentages; source age estimates; no exact raw lith denominators or independent observer assumed",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('walvis-summary.json'))
    args = parser.parse_args()
    run(args.source,args.output)
