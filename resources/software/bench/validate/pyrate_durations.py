"""Post hoc diagnostic for E2: PyRate's inferred species times against the truth.

Usage: python pyrate_durations.py <e2_dir>
Needs <e2_dir>/species_truth/ from pyrate_attribution.R and the PyRate run logs.
"""

import glob
import json
import pathlib
import sys

import numpy as np

e2 = pathlib.Path(sys.argv[1])
rows = []
for truth in sorted((e2 / "species_truth").glob("*.tsv")):
    name = truth.stem
    log = glob.glob(str(e2 / "runs" / name / "pyrate_mcmc_logs" / "*_mcmc.log"))[0]
    d = np.genfromtxt(log, names=True, delimiter="\t", deletechars="")
    d = d[int(0.2 * len(d)):]
    t = np.genfromtxt(truth, names=True, delimiter="\t", dtype=None, encoding="utf-8")
    ts_hat = np.array([d[f"{s}_TS"].mean() for s in t["species"]])
    te_hat = np.array([d[f"{s}_TE"].mean() for s in t["species"]])
    dur_true, dur_hat = t["ts"] - t["te"], ts_hat - te_hat
    single = t["k"] == 1
    rows.append({
        "rep": name, "arm": name.split("_")[0], "n": len(t),
        "total_duration_ratio": float(dur_hat.sum() / dur_true.sum()),
        "singleton_duration_ratio": float(dur_hat[single].sum() / dur_true[single].sum()) if single.any() else None,
        "multi_duration_ratio": float(dur_hat[~single].sum() / dur_true[~single].sum()) if (~single).any() else None,
        "q_from_inferred_durations": float(t["k"].sum() / dur_hat.sum()),
        "q_from_true_durations": float(t["k"].sum() / dur_true.sum()),
        "q_posterior_median": float(np.median(d["q_rate"])),
    })

summary = {}
for arm in sorted({r["arm"] for r in rows}):
    a = [r for r in rows if r["arm"] == arm]
    summary[arm] = {k: float(np.median([r[k] for r in a if r[k] is not None]))
                    for k in ("total_duration_ratio", "singleton_duration_ratio", "multi_duration_ratio",
                              "q_from_inferred_durations", "q_from_true_durations", "q_posterior_median")}
(e2 / "e2_durations.json").write_text(json.dumps({"summary": summary, "reps": rows}, indent=2))
print(json.dumps(summary, indent=2))
