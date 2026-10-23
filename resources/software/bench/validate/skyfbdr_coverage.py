"""Tranche-1 E3(a): coverage of the skyfbdr study's deposited runs (../VALIDATION.md).

Usage: python skyfbdr_coverage.py <study_dir> <outdir>
RevBayes indexes rates from the present (lambda[1] is the youngest stage);
paleobuddy and the study's true_vals.tsv index them from the origin, so
RevBayes lambda[i] is compared with true lambda(4 - i).
"""

import json
import pathlib
import sys

import numpy as np

study, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
truth = np.genfromtxt(study / "simulation/coverage/true_vals.tsv", names=True, delimiter="\t")
rates = [f"{r}{i}" for r in ("lambda", "mu", "psi") for i in (1, 2, 3)]
covered = {r: 0 for r in rates}
covered_unmapped = {r: 0 for r in rates}
rows, missing = [], 0
for rep in range(1, len(truth) + 1):
    log = study / f"output/coverage/skyfbdr_{rep}.log"
    if not log.exists():
        missing += 1
        continue
    d = np.genfromtxt(log, names=True, delimiter="\t", deletechars="")
    d = d[int(0.2 * len(d)):]
    row = {"rep": rep, "n_samples": len(d)}
    for r in rates:
        name, i = r[:-1], int(r[-1])
        t = truth[r][rep - 1]
        for label, col, counter in (("", f"{name}[{4 - i}]", covered), ("unmapped_", f"{name}[{i}]", covered_unmapped)):
            lo, hi = np.quantile(d[col], [0.025, 0.975])
            hit = int(lo <= t <= hi)
            counter[r] += hit
            row[f"{label}{r}_cov"] = hit
        row[f"{r}_true"] = t
    rows.append(row)

n = len(rows)
summary = {"reps": len(truth), "missing_logs": missing, "usable": n, "burn_in": 0.2,
           "coverage_mapped": {r: covered[r] / n for r in rates},
           "coverage_unmapped": {r: covered_unmapped[r] / n for r in rates},
           "binomial_2.5pct_count_for_1000": 936,
           "mapping": "RevBayes rate[k] (k = 1 youngest) compared with true value index 4 - k (index 1 oldest)"}
cols = list(rows[0].keys())
with open(out / "e3a_skyfbdr_reps.tsv", "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join(str(r[c]) for c in cols) + "\n")
(out / "e3a_skyfbdr.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
