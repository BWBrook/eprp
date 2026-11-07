#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "scipy==1.15.3"]
# ///
"""Conditional original-sample counting and score-precision feasibility screen."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "q009-outcome-support"))
from audit import spreadsheet

SOURCE_SHA = "5fc615afdf94fa7842375e9c34b98d1f87f41e29700ef97da11b149eb59c7caa"
SCENARIOS = ((500, 1), (1000, 1), (250, 1), (2000, 1), (500, 2), (1000, 2))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metric(x, scale):
    mu = x.mean(axis=-2)
    var = x.var(axis=-2, ddof=1)
    cv = np.divide(np.sqrt(var), mu, out=np.full_like(mu, np.nan), where=mu > 0).sum(axis=-1)
    return cv, (var / scale**2).sum(axis=-1)


def finite_variance_factor(ages, rho):
    separation = np.abs(np.subtract.outer(ages, ages)) / .5
    covariance = np.power(rho, separation)
    return float(covariance.sum() / len(ages)**2)


def dependence(ages, values):
    good = np.isfinite(values)
    a, v = np.asarray(ages)[good], np.asarray(values)[good]
    pairs = np.isclose(np.abs(np.diff(a)), .5)
    rho = float(np.corrcoef(v[:-1][pairs], v[1:][pairs])[0, 1]) if pairs.sum() >= 3 else None
    if rho is not None and not np.isfinite(rho):
        rho = None
    return {"defined_windows": int(good.sum()), "adjacent_pairs": int(pairs.sum()), "lag1_response_correlation": rho,
            "heuristic_finite_ar1_effective_n": 1 / finite_variance_factor(a, max(0, rho)) if rho is not None else None,
            "sample_variance_across_windows": float(np.var(v, ddof=1)) if len(v) > 1 else None}


def simulate(p, m, n, design, repetitions, rng):
    if np.any(p < 0) or p.sum() > 1 + 1e-10:
        raise ValueError("Selected probabilities do not fit a multinomial simplex")
    probabilities = np.r_[p, max(0, 1 - p.sum())]
    probabilities /= probabilities.sum()
    if design == 1:
        counts = rng.multinomial(n, probabilities, size=(repetitions, m))
    else:
        active = probabilities > 0
        concentration = (n - design) / (design - 1)
        draws = rng.dirichlet(concentration * probabilities[active], size=(repetitions, m))
        active_counts = rng.multinomial(n, draws)
        counts = np.zeros((repetitions, m, len(probabilities)))
        counts[:, :, active] = active_counts
    return counts[:, :, :-1] / n


def save_tsv(path, records):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def run(source, output, private, repetitions):
    if digest(source) != SOURCE_SHA:
        raise ValueError("Unexpected source workbook")
    data = spreadsheet(source)
    headers = data[8]
    sample = [r for i, r in data.items() if i > 8 and r.get("AC") and r.get("Q") == "SA" and r.get("R", "").removeprefix("U") == "1209"]
    train = [r for r in sample if 60.15 <= float(r["AC"]) <= 65.9]
    fields = [c for c in headers if len(c) == 2 and "AD" <= c <= "CK" and headers[c].strip() not in ("total_remaining_nannos", "calcisphere_fragments")]
    selected = []
    scales = []
    for c in fields:
        if not all(r.get(c) for r in train):
            continue
        x = np.array([float(r[c]) / 100 for r in train])
        if np.mean(x > 0) > .65 and x.mean() >= .01:
            selected.append(c)
            scales.append(float(x.mean()))
    scale = np.array(scales)
    if len(scale) != 6:
        raise ValueError("Training-only taxon eligibility differs from inspected source")
    windows = []
    for age in np.arange(65.5, 56.4, -.5):
        before = [r for r in sample if age < float(r["AC"]) <= age + .15]
        after = [r for r in sample if age - .15 <= float(r["AC"]) < age]
        before_complete = [r for r in before if all(r.get(c) for c in selected)]
        after_complete = [r for r in after if all(r.get(c) for c in selected)]
        if len(before_complete) < 3 or len(after_complete) < 3:
            raise ValueError("Missing complete window; record an amended domain before proceeding")
        x = np.array([[float(r[c]) / 100 for c in selected] for r in before_complete])
        y = np.array([[float(r[c]) / 100 for c in selected] for r in after_complete])
        cv0, v0 = metric(x, scale)
        cv1, v1 = metric(y, scale)
        windows.append({"age": float(age), "m_past": len(x), "m_future": len(y), "excluded_past_rows": len(before)-len(x),
                        "excluded_future_rows": len(after)-len(y), "past_scv": float(cv0), "future_scv": float(cv1),
                        "past_v": float(v0), "future_v": float(v1), "p_past": x.mean(axis=0), "p_future": y.mean(axis=0)})
    ages = [w["age"] for w in windows]
    result = {"source_sha256": SOURCE_SHA, "script_sha256": digest(Path(__file__)), "parser_sha256": digest(HERE.parent/"q009-outcome-support/audit.py"),
              "protocol_sha256": digest(HERE/"PROTOCOL.md"), "seed": 20261108, "replicates_per_window_scenario": repetitions,
              "training_selection_rows": len(train), "candidate_windows": len(windows), "selected_taxa": [headers[c].strip() for c in selected],
              "excluded_past_rows": sum(w["excluded_past_rows"] for w in windows), "excluded_future_rows": sum(w["excluded_future_rows"] for w in windows),
              "dependence": {key: dependence(ages, [w[key] for w in windows]) for key in ("past_scv", "future_scv", "past_v", "future_v")}}
    result["definedness_by_domain"] = {name: {"windows": len(ww),
                                              "past_scv_defined": sum(np.isfinite(w["past_scv"]) for w in ww).item(),
                                              "future_scv_defined": sum(np.isfinite(w["future_scv"]) for w in ww).item(),
                                              "past_and_future_scv_defined": sum(np.isfinite(w["past_scv"]) and np.isfinite(w["future_scv"]) for w in ww).item()}
                                        for name, ww in (("older_training", [w for w in windows if w["age"]>=60.5]),
                                                         ("reserved_separation", [w for w in windows if w["age"]==60.0]),
                                                         ("possible_evaluation", [w for w in windows if w["age"]<=59.5]))}
    rng = np.random.default_rng(20261108)
    records = []
    private_rows = []
    for n, design in SCENARIOS:
        for kind in ("past", "future"):
            scv_means, scv_vars, obs_cv, v_ratios, scv_coverage, undefined, comparable_undefined = [], [], [], [], [], [], []
            for w in windows:
                p = w["p_"+kind]
                sims = simulate(p, w["m_future"], n, design, repetitions, rng)
                cv, v = metric(sims, scale)
                good = np.isfinite(cv)
                undefined.append(1 - good.mean())
                good_cv = cv[good]
                noise_v = float(design/n * np.sum(p*(1-p)/scale**2))
                v_ratios.append(noise_v/w["future_v"] if w["future_v"] > 0 else np.nan)
                if np.isfinite(w["future_scv"]) and good.sum() >= 2:
                    comparable_undefined.append(float(1-good.mean()))
                    scv_means.append(float(good_cv.mean()))
                    scv_vars.append(float(good_cv.var(ddof=1)))
                    obs_cv.append(w["future_scv"])
                    lo, hi = np.quantile(good_cv, [.025,.975])
                    scv_coverage.append(bool(lo <= w["future_scv"] <= hi))
                private_rows.append({"n": n, "design_effect": design, "composition_null": kind, "age_ma": w["age"],
                                     "counting_v_expected": noise_v, "counting_v_simulated_mean": float(v.mean()), "future_v": w["future_v"],
                                     "future_scv": w["future_scv"] if np.isfinite(w["future_scv"]) else None,
                                     "simulated_scv_undefined_rate": float(1-good.mean())})
            obs_var = float(np.var(obs_cv, ddof=1)) if len(obs_cv)>1 else np.nan
            records.append({"n": n, "design_effect": design, "composition_null": kind,
                            "scv_comparable_windows": len(obs_cv), "all_window_mean_simulated_scv_undefined_rate": float(np.mean(undefined)),
                            "comparable_window_mean_simulated_scv_undefined_rate": float(np.mean(comparable_undefined)) if comparable_undefined else "undefined",
                            "comparable_window_max_simulated_scv_undefined_rate": float(np.max(comparable_undefined)) if comparable_undefined else "undefined",
                            "observed_defined_scv_within_conditional_null_95_fraction": float(np.mean(scv_coverage)) if scv_coverage else "undefined",
                            "null_mean_between_window_variance_over_observed_scv_variance": float(np.var(scv_means, ddof=1)/obs_var) if obs_var>0 else "undefined",
                            "mean_null_within_window_scv_variance_over_observed_scv_variance": float(np.mean(scv_vars)/obs_var) if obs_var>0 else "undefined",
                            "median_expected_counting_v_over_observed_v": float(np.nanmedian(v_ratios)),
                            "max_expected_counting_v_over_observed_v": float(np.nanmax(v_ratios))})
    precision = []
    for name, aa in (("all_19_diagnostic_windows", ages), ("older_11_training_windows", [a for a in ages if a>=60.5]),
                     ("possible_7_evaluation_windows", [a for a in ages if a<=59.5])):
        for rho in (0.,.25,.5,.75,.9):
            factor = finite_variance_factor(aa, rho)
            standardized = float((norm.ppf(.975)+norm.ppf(.8))*np.sqrt(factor))
            for c in (.25,.5,1.,2.):
                precision.append({"domain": name, "n_windows": len(aa), "assumed_paired_loss_rho": rho,
                                  "conditional_effective_n": 1/factor, "assumed_sd_gain_over_baseline_mse": c,
                                  "normal_approx_detectable_relative_mse_gain": standardized*c,
                                  "max_sd_gain_over_baseline_mse_for_10pct_target": .1/standardized})
    output.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    serial_windows = [{k: v.tolist() if isinstance(v,np.ndarray) else (None if isinstance(v,float) and not np.isfinite(v) else v) for k,v in w.items()} for w in windows]
    (private/"window-diagnostics.json").write_text(json.dumps(serial_windows, indent=2, allow_nan=False)+"\n")
    (private/"counting-window-results.json").write_text(json.dumps(private_rows, indent=2, allow_nan=False)+"\n")
    result["private_result_sha256"] = {name: digest(private/name) for name in ("window-diagnostics.json","counting-window-results.json")}
    result["precision_model"] = "Conditional known paired-loss covariance; two-sided alpha.05 and power.8 normal approximation; not fitted forecasting power"
    result["runtime_versions"] = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__}
    (output/"summary.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    save_tsv(output/"counting-scenarios.tsv", records)
    save_tsv(output/"precision-sensitivity.tsv", precision)
    print(json.dumps(result, indent=2, allow_nan=False))
    print(json.dumps(records[:4], indent=2, allow_nan=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=HERE)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=4000)
    args = parser.parse_args()
    run(args.source, args.output, args.private_output, args.replicates)
