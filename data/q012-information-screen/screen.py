# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "scipy==1.15.3"]
# ///
"""Exact generator complete-data LR ordering; no sampler or model fitting."""

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
from scipy.stats import beta, binom

HERE = Path(__file__).resolve().parent
PROTOTYPE = HERE.parent / "q012-prototype"
spec = importlib.util.spec_from_file_location("q012_primary_generator", PROTOTYPE / "prototype.py")
GEN = importlib.util.module_from_spec(spec)
spec.loader.exec_module(GEN)
PROTOCOL = json.loads((HERE / "protocol.json").read_text())


def score(lineages, sigma=0.5, eta_null=0.05, eta_alternative=0.2):
    rho0, rho1 = eta_null / sigma, eta_alternative / sigma
    if not (sigma > 0 and abs(rho0) < 1 and abs(rho1) < 1):
        raise ValueError("Invalid stationary inheritance kernel")
    v0, v1 = sigma**2 * (1-rho0**2), sigma**2 * (1-rho1**2)
    out, edges, cohort_edges = 0.0, 0, 0
    for child in lineages:
        parent = child["parent"]
        if parent < 0:
            continue
        xp, xd = lineages[parent]["x"], child["x"]
        out += -0.5 * math.log(v1/v0) - 0.5 * ((xd-rho1*xp)**2/v1 - (xd-rho0*xp)**2/v0)
        edges += 1
        cohort_edges += bool(child["cohort"])
    if cohort_edges != 1:
        raise ValueError(f"Expected the forced cohort inheritance edge, found {cohort_edges}")
    return out, edges


def replicate(seed, eta, ensemble):
    h = PROTOCOL["hypotheses"]
    lineages, info = GEN.generate(seed, {"rho": eta/h["sigma"], "sigma": h["sigma"],
                                         "lambda0": ensemble["lambda0"]})
    stat, edges = score(lineages, **h)
    observed, oi = GEN.observe(lineages, seed + 1000000000)
    ids, parents = observed["ids"], observed["par"]
    return dict(seed=seed, eta=eta, score=stat, true_lineages=len(lineages), true_edges=edges,
                capped=info["capped"], recorded=oi["recorded"],
                true_censors=sum(l["cause"] == "cens" for l in lineages),
                true_extinctions=sum(l["cause"] == "ext" for l in lineages),
                true_bifurcations=sum(l["cause"] == "bif" for l in lineages),
                recorded_labels=oi["labels"],
                recorded_edges=sum(parents[i] >= 0 for i in ids),
                recorded_lineage_Myr=sum(observed["tO"][i]-observed["tE"][i] for i in ids))


def cp_interval(successes, n, tail=0.025):
    lo = 0.0 if successes == 0 else float(beta.ppf(tail, successes, n-successes+1))
    hi = 1.0 if successes == n else float(beta.ppf(1-tail, successes+1, n-successes))
    return [lo, hi]


def threshold_bracket(calibration, alpha, failure):
    ordered = np.sort(calibration)
    n, p = len(ordered), 1-alpha
    lower_rank = int(binom.ppf(failure/2, n, p))
    upper_rank = int(binom.ppf(1-failure/2, n, p))+1
    at = lambda rank: -math.inf if rank <= 0 else math.inf if rank > n else float(ordered[rank-1])
    nominal_rank = math.ceil((1-alpha)*(n+1))
    return dict(lower=at(lower_rank), upper=at(upper_rank), nominal=at(nominal_rank),
                lower_rank=lower_rank, upper_rank=upper_rank, nominal_rank=nominal_rank,
                exact_bracket_coverage=float(binom.cdf(upper_rank-1,n,p)-binom.cdf(lower_rank-1,n,p)))


def describe(rows):
    quantiles = lambda key: dict(zip(("q05", "median", "q95"),
                                   np.quantile([r[key] for r in rows], [.05,.5,.95]).tolist()))
    labels = {k: sum(r["recorded_labels"].get(k,0) for r in rows)
              for k in ("ext", "bif", "single", "present")}
    nr = sum(r["recorded"] for r in rows)
    return dict(n=len(rows), capped=sum(r["capped"] for r in rows),
                true_lineages=quantiles("true_lineages"), true_edges=quantiles("true_edges"),
                recorded=quantiles("recorded"), recorded_lineage_Myr=quantiles("recorded_lineage_Myr"),
                recorded_label_totals=labels,
                pooled_recorded_label_shares={k: v/nr if nr else None for k,v in labels.items()},
                pooled_true_censor_share=sum(r["true_censors"] for r in rows)/sum(r["true_lineages"] for r in rows))


def analyse(panels):
    cal = [r["score"] for r in panels["calibration_null"]]
    alt = np.array([r["score"] for r in panels["evaluation_alternative"]])
    null = np.array([r["score"] for r in panels["evaluation_null"]])
    budget = PROTOCOL["simultaneous_error_budget"]
    th = threshold_bracket(cal, PROTOCOL["alpha"], budget["per_ensemble_quantile_bracket_failure"])
    k_lower, k_upper = int(np.sum(alt > th["upper"])), int(np.sum(alt > th["lower"]))
    lower = cp_interval(k_lower, len(alt), budget["per_ensemble_power_lower_failure"])[0]
    upper = cp_interval(k_upper, len(alt), budget["per_ensemble_power_upper_failure"])[1]
    k_alt, k_null = int(np.sum(alt > th["nominal"])), int(np.sum(null > th["nominal"]))
    conclusion = ("rules_out_target_for_this_generator_ensemble" if upper < PROTOCOL["target_power"] else
                  "permits_fresh_recorded_data_test" if lower > PROTOCOL["target_power"] else "inconclusive")
    return dict(thresholds=th, optimal_power_at_population_size_005=dict(
                    simultaneous_interval=[lower,upper], lower_threshold_successes=k_upper,
                    upper_threshold_successes=k_lower, n=len(alt)),
                nominal_threshold_alt=dict(successes=k_alt,n=len(alt),estimate=k_alt/len(alt),
                                           descriptive_cp95=cp_interval(k_alt,len(alt))),
                nominal_threshold_null=dict(successes=k_null,n=len(null),estimate=k_null/len(null),
                                            descriptive_cp95=cp_interval(k_null,len(null))),
                conclusion=conclusion, ensembles={k:describe(v) for k,v in panels.items()})


def hashes():
    paths = [HERE/"screen.py",HERE/"protocol.json",HERE/"PROTOCOL.md",
             PROTOTYPE/"prototype.py", PROTOTYPE/"config.json", PROTOTYPE/"quadrature.py"]
    return {str(p.relative_to(HERE.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def run(output, smoke=False):
    output.mkdir(parents=True, exist_ok=True)
    rowpath = output/"rows.jsonl"
    if rowpath.exists() or (output/"summary.json").exists():
        raise FileExistsError("Output exists: use a new output directory to preserve evidence")
    t0, result = time.monotonic(), {}
    with rowpath.open("x") as handle:
        for ei,ensemble in enumerate(PROTOCOL["ensembles"]):
            panels = {}
            for pi,(panel,settings) in enumerate(PROTOCOL["panels"].items()):
                if smoke and panel == "evaluation_null":
                    continue
                n = PROTOCOL["smoke"]["n_per_ensemble_per_hypothesis"] if smoke else settings["n"]
                start = (PROTOCOL["smoke"]["seed_start"]+ei*100+pi*10 if smoke else
                         ensemble["seed_base"]+settings["seed_offset"])
                eta = PROTOCOL["hypotheses"]["eta_"+settings["hypothesis"]]
                rows = []
                for seed in range(start,start+n):
                    row = dict(ensemble=ensemble["name"],panel=panel,**replicate(seed,eta,ensemble))
                    handle.write(json.dumps(row,allow_nan=False)+"\n")
                    rows.append(row)
                handle.flush()
                panels[panel] = rows
                print(json.dumps(dict(ensemble=ensemble["name"], panel=panel,n=n,
                                      elapsed_seconds=round(time.monotonic()-t0,3))),flush=True)
            result[ensemble["name"]] = {k:describe(v) for k,v in panels.items()} if smoke else analyse(panels)
    result = dict(mode="timing_only_no_power_inference" if smoke else "frozen_oracle_evaluation",
                  elapsed_seconds=time.monotonic()-t0, host=platform.node(), python=platform.python_version(),
                  numpy=np.__version__, source_sha256=hashes(), results=result)
    (output/"summary.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",choices=["smoke","run"])
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    run(args.output,args.mode=="smoke")
