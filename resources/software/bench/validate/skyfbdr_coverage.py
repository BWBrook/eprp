"""Tranche-1 E3(a): coverage of the skyfbdr study's deposited runs (../VALIDATION.md).

Usage: python skyfbdr_coverage.py <study_dir> <outdir>
RevBayes indexes rates from the present (lambda[1] is the youngest stage);
paleobuddy and the study's true_vals.tsv index them from the origin, so
RevBayes lambda[i] is compared with true lambda(4 - i). Also reported (A2
follow-up): pooled coverage, coverage by quintile of the true value,
burn-in sensitivity and effective sample sizes.
"""

import json
import pathlib
import sys

import numpy as np

study, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
truth = np.genfromtxt(study / "simulation/coverage/true_vals.tsv", names=True, delimiter="\t")
rates = [f"{r}{i}" for r in ("lambda", "mu", "psi") for i in (1, 2, 3)]
burnins = (0.0, 0.2, 0.5)


def ess(x):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    if np.var(x) == 0:
        return float("nan")
    f = np.fft.rfft(x, 2 * n)
    acf = np.fft.irfft(f * np.conj(f))[:n] / (np.var(x) * n)
    tau = -1.0
    for k in range(0, n - 1, 2):
        pair = acf[k] + acf[k + 1]
        if pair < 0:
            break
        tau += 2 * pair
    return n / tau


hits = {b: {r: [] for r in rates} for b in burnins}
hits_unmapped = {r: [] for r in rates}
ess_vals = {r: [] for r in rates}
true_vals = {r: [] for r in rates}
rows, missing = [], 0
for rep in range(1, len(truth) + 1):
    log = study / f"output/coverage/skyfbdr_{rep}.log"
    if not log.exists():
        missing += 1
        continue
    full = np.genfromtxt(log, names=True, delimiter="\t", deletechars="")
    row = {"rep": rep, "n_samples": len(full)}
    for r in rates:
        name, i = r[:-1], int(r[-1])
        t = truth[r][rep - 1]
        true_vals[r].append(t)
        for b in burnins:
            d = full[int(b * len(full)):]
            lo, hi = np.quantile(d[f"{name}[{4 - i}]"], [0.025, 0.975])
            hits[b][r].append(int(lo <= t <= hi))
        d = full[int(0.2 * len(full)):]
        lo, hi = np.quantile(d[f"{name}[{i}]"], [0.025, 0.975])
        hits_unmapped[r].append(int(lo <= t <= hi))
        ess_vals[r].append(ess(d[f"{name}[{4 - i}]"]))
        row[f"{r}_true"] = t
        row[f"{r}_cov"] = hits[0.2][r][-1]
        row[f"unmapped_{r}_cov"] = hits_unmapped[r][-1]
    rows.append(row)

n = len(rows)


def by_quintile(r):
    t = np.array(true_vals[r]); h = np.array(hits[0.2][r])
    edges = np.quantile(t, [0, 0.2, 0.4, 0.6, 0.8, 1.0])
    q = np.clip(np.searchsorted(edges, t, side="right") - 1, 0, 4)
    return [float(h[q == k].mean()) for k in range(5)]


summary = {"reps": len(truth), "missing_logs": missing, "usable": n, "burn_in": 0.2,
           "coverage_mapped": {r: float(np.mean(hits[0.2][r])) for r in rates},
           "coverage_unmapped": {r: float(np.mean(hits_unmapped[r])) for r in rates},
           "coverage_pooled_mapped": float(np.mean([np.mean(hits[0.2][r]) for r in rates])),
           "coverage_by_burn_in": {str(b): {r: float(np.mean(hits[b][r])) for r in rates} for b in burnins},
           "coverage_by_true_value_quintile": {r: by_quintile(r) for r in rates},
           "ess_median": {r: float(np.median(ess_vals[r])) for r in rates},
           "ess_min": {r: float(np.min(ess_vals[r])) for r in rates},
           "binomial_2.5pct_count_for_1000": 936,
           "mapping": "RevBayes rate[k] (k = 1 youngest) compared with true value index 4 - k (index 1 oldest)"}
cols = list(rows[0].keys())
with open(out / "e3a_skyfbdr_reps.tsv", "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join(str(r[c]) for c in cols) + "\n")
(out / "e3a_skyfbdr.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
