# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4"]
# ///
"""Q-012 generator size calibration (Codex 76/1737, work item b). Generator only; no fits.

Declared before running (16 October 2026):
- Objective: the median recorded tree size nearest the observed 268.
- Candidates: lambda0 in {0.080, 0.088, 0.096}; every other reference setting fixed (config.json).
- Calibration seeds 40001-40100 for every candidate (common random numbers); validation seeds
  41001-41100 (disjoint) for the chosen candidate only. All outcomes retained, caps included.
- Process budget: 120 s for calibration plus validation; stop and report if it is exceeded.
- Also recorded (outside that budget): the original marginal-rate reference (lambda0 0.0708) on the
  earlier 300-seed panel 30000-30299, whose seeds and counts were not saved before.
Summaries beside N: terminal-event shares, total recorded lineage-Myr, parent-daughter links
(budding / boundary), lagged-exposure availability, caps.

Run from the repository root:  uv run --python 3.12 data/q012-prototype/calibrate.py
"""

import importlib.util
import json
import math
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.argv = [sys.argv[0], "calibrate"]
spec = importlib.util.spec_from_file_location("prototype", HERE / "prototype.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
OBSERVED = dict(N=268, ext=191, bif=24, single=1, present=52, lineage_Myr=2939.3, budding_links=208,
                boundary_links=49, lagged_E_availability=0.6671)


def summarise(seed, lam0):
    L, gi = P.generate(seed, {"lambda0": lam0})
    if gi["capped"]:
        return dict(seed=seed, capped=True)
    obsd, oi = P.observe(L, seed)
    ids, par, tO, tE, used = (obsd[k] for k in ("ids", "par", "tO", "tE", "used"))
    links = [i for i in ids if par[i] >= 0]
    boundary = sum(1 for i in links if abs(tO[i] - tE[par[i]]) < 1e-9)
    avail = [used[i][b] is not None for i in ids for b in used[i]]
    return dict(seed=seed, capped=False, N=oi["recorded"], **{k: oi["labels"][k] for k in ("ext", "bif", "single", "present")},
                lineage_Myr=round(sum(tO[i] - tE[i] for i in ids), 2), budding_links=len(links) - boundary,
                boundary_links=boundary, lagged_E_availability=round(float(np.mean(avail)), 4) if avail else None)


def panel(seeds, lam0):
    rows = [summarise(s, lam0) for s in seeds]
    ok = [r for r in rows if not r["capped"]]
    N = np.array([r["N"] for r in ok])
    tot = lambda k: sum(r[k] for r in ok)
    s = dict(lambda0=lam0, seeds=f"{seeds[0]}-{seeds[-1]}", n=len(rows), capped=len(rows) - len(ok),
             N_median=float(np.median(N)), N_q05=round(float(np.percentile(N, 5)), 2), N_q95=round(float(np.percentile(N, 95)), 2),
             share_N_ge_268=round(float(np.mean(N >= 268)), 3),
             end_shares={k: round(tot(k) / tot("N"), 3) for k in ("ext", "bif", "single", "present")},
             lineage_Myr_median=round(float(np.median([r["lineage_Myr"] for r in ok])), 1),
             budding_links_median=float(np.median([r["budding_links"] for r in ok])),
             boundary_links_median=float(np.median([r["boundary_links"] for r in ok])),
             lagged_E_availability_mean=round(float(np.mean([r["lagged_E_availability"] for r in ok if r["lagged_E_availability"] is not None])), 4))
    return s, rows


def main():
    out = dict(observed=OBSERVED, observed_end_shares={k: round(OBSERVED[k] / OBSERVED["N"], 3) for k in ("ext", "bif", "single", "present")})
    t0 = time.time()
    cal, rows_all = [], {}
    for lam0 in (0.080, 0.088, 0.096):
        s, rows = panel(list(range(40001, 40101)), lam0)
        cal.append(s); rows_all[f"cal_{lam0}"] = rows
        if time.time() - t0 > 120:
            out["stopped"] = "process budget exceeded during calibration"
            break
    out["calibration"] = cal
    if "stopped" not in out:
        best = min(cal, key=lambda s: abs(s["N_median"] - 268))
        out["chosen_lambda0"] = best["lambda0"]
        v, rows = panel(list(range(41001, 41101)), best["lambda0"])
        out["validation"] = v; rows_all["validation"] = rows
    out["seconds_calibration_and_validation"] = round(time.time() - t0, 1)
    out["budget_exceeded"] = out["seconds_calibration_and_validation"] > 120
    ref, rows = panel(list(range(30000, 30300)), 0.0708)
    out["original_reference_panel"] = ref; rows_all["original_reference_30000_30299"] = rows
    (HERE / "calibration.json").write_text(json.dumps(out, indent=1) + "\n")
    (HERE / "calibration_rows.json").write_text(json.dumps(rows_all) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
