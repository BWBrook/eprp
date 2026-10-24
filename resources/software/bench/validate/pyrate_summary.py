"""Tranche-1 E2: coverage of PyRate's central 95% intervals (../VALIDATION.md).

Usage: python pyrate_summary.py <outdir>
Reads <outdir>/truth_<arm>.json and <outdir>/runs/<name>/pyrate_mcmc_logs/*_mcmc.log.
"""

import glob
import json
import pathlib
import sys

import numpy as np

out = pathlib.Path(sys.argv[1])
PARAMS = {"lambda": "lambda_0", "mu": "mu_0", "q": "q_rate"}


def ess(x):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    if n < 10 or np.var(x) == 0:
        return float("nan")
    f = np.fft.rfft(x, 2 * n)
    acf = np.fft.irfft(f * np.conj(f))[:n] / (np.var(x) * n)
    tau = -1.0
    for k in range(0, n - 1, 2):  # Geyer initial positive sequence: pairs (rho_0 + rho_1), (rho_2 + rho_3), ...
        pair = acf[k] + acf[k + 1]
        if pair < 0:
            break
        tau += 2 * pair
    return n / tau


rows, summary = [], {}
for truth_file in sorted(out.glob("truth_*.json")):
    t = json.loads(truth_file.read_text())
    arm = t["meta"]["arm"]
    covered = {p: 0 for p in PARAMS}
    usable, low_ess, missing = 0, 0, 0
    for name, tr in t["reps"].items():
        logs = glob.glob(str(out / "runs" / name / "pyrate_mcmc_logs" / "*_mcmc.log"))
        if not logs:
            missing += 1
            continue
        data = np.genfromtxt(logs[0], names=True, delimiter="\t")
        data = data[int(0.2 * len(data)):]
        row = {"arm": arm, "rep": name, "n_samples": len(data), "species_sampled": tr["species_sampled"]}
        ok = True
        for p, col in PARAMS.items():
            x = data[col]
            lo, med, hi = np.quantile(x, [0.025, 0.5, 0.975])
            e = ess(x)
            row.update({f"{p}_true": tr[p], f"{p}_lo": lo, f"{p}_med": med, f"{p}_hi": hi, f"{p}_ess": e,
                        f"{p}_cov": int(lo <= tr[p] <= hi)})
            ok = ok and e >= 100
        row["ess_ok"] = int(ok)
        rows.append(row)
        if not ok:
            low_ess += 1
            continue
        usable += 1
        for p in PARAMS:
            covered[p] += row[f"{p}_cov"]
    arm_rows = [r for r in rows if r["arm"] == arm and r["ess_ok"]]
    summary[arm] = {
        "reps": len(t["reps"]), "missing_logs": missing, "low_ess": low_ess, "usable": usable,
        "covered": covered,
        "median_rel_bias": {p: float(np.median([r[f"{p}_med"] / r[f"{p}_true"] - 1 for r in arm_rows])) if arm_rows else None
                            for p in PARAMS},
    }
    if arm == "high":
        summary[arm]["pass"] = bool(missing == 0 and low_ess <= 10 and all(covered[p] >= 90 for p in PARAMS))

cols = list(rows[0].keys()) if rows else []
with open(out / "e2_pyrate_reps.tsv", "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join(f"{r[c]:.6g}" if isinstance(r[c], float) else str(r[c]) for c in cols) + "\n")
(out / "e2_pyrate.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
