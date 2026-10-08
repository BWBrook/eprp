# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.5.3", "pandas==3.0.6", "mat-io==1.0.0"]
# ///
"""Read-only replay and bounded correction audit of Claude's coupling probe."""

import hashlib
import json
import subprocess
import types
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "data/phanda-stage-differences/build.py"
AUDITED_COMMIT = "e5b1c317e426c2c276005300a8581fa9e09422dc"
AUDITED_SHA256 = "ac1531bcb5e779de0a54b6ca458c95ec77afa9cc406f52f6c78ec8ace5bcaf4f"
ORIGINAL_OUTPUT_SHA256 = "3f09f976c1a41d10aaa39db131ed6b9641796a31e616e76de8cd076298f796cb"
OUT = ROOT / "data/derived/phanda-coupling-audit"
N = 120_000
SEED = 20261009


def moments(x):
    mean = x.mean()
    centered = x - mean
    return mean, np.mean(centered**2), np.mean(centered**4)


def sign_probability_lower_bounds(y, o):
    """CDF-separation bounds valid under every coupling of the given marginals.

    P(Y>O) >= P(O<=t,Y>t) >= F_O(t)-F_Y(t), for every t.
    Swapping Y and O gives the negative-sign bound. No posterior is inferred.
    """
    ys, os = np.sort(y), np.sort(o)
    thresholds = np.unique(np.concatenate([ys, os]))
    fy = np.searchsorted(ys, thresholds, side="right") / ys.size
    fo = np.searchsorted(os, thresholds, side="right") / os.size
    return float(np.max(fo - fy)), float(np.max(fy - fo))


def load_audited_source():
    source = subprocess.check_output([
        "git", "-C", str(ROOT), "show",
        f"{AUDITED_COMMIT}:data/phanda-stage-differences/build.py",
    ])
    if hashlib.sha256(source).hexdigest() != AUDITED_SHA256:
        raise SystemExit("Audited build checksum mismatch")
    upstream = types.ModuleType("upstream_probe")
    upstream.__file__ = str(UPSTREAM)
    exec(compile(source, str(UPSTREAM), "exec"), upstream.__dict__)
    return upstream


def compare_original_output(results, path):
    if not path.exists():
        return "skipped: original output absent", None
    if hashlib.sha256(path.read_bytes()).hexdigest() != ORIGINAL_OUTPUT_SHA256:
        return "skipped: output differs from audited original", None
    deposited = pd.read_csv(path, sep="\t")
    replay = results[results.coupling != "fully_independent_corrected"].copy()
    replay.coupling = replay.coupling.str.replace("fully_independent_original", "fully_independent")
    joined = replay.merge(deposited, on=["younger", "older", "coupling"], suffixes=("_audit", "_source"))
    max_replay_error = max((joined[f"{c}_audit"] - joined[f"{c}_source"]).abs().max()
                           for c in ["mean", "sd", "q05", "q50", "q95"])
    assert len(joined) == 336 and max_replay_error <= 0.00005001
    assert (joined.sign_resolved_audit == joined.sign_resolved_source).all()
    return "passed: 336 original rows within rounding", float(max_replay_error)


def main():
    upstream = load_audited_source()
    # Upstream load verifies pinned source checksum; raw source must exist.
    if not upstream.RAW.exists():
        raise SystemExit("Raw source missing; this audit does not download data")
    meta, samples = upstream.load()
    original_rng = np.random.default_rng(upstream.SEED)
    p = (np.arange(upstream.GRID) + 0.5) / upstream.GRID
    rows, diagnostics = [], []
    for i in range(len(meta) - 1):
        young, old = samples[i], samples[i + 1]
        shared = np.concatenate([
            original_rng.choice(young[s], upstream.N_PER_SCENARIO)
            - original_rng.choice(old[s], upstream.N_PER_SCENARIO)
            for s in range(12)
        ])
        # Deliberately preserve the faulty source order solely for diagnostic replay.
        faulty, labels = [], []
        for s in range(12):
            y = original_rng.choice(young[s], upstream.N_PER_SCENARIO)
            label = original_rng.integers(12)
            labels.append(int(label))
            faulty.append(y - original_rng.choice(old[label], upstream.N_PER_SCENARIO))
        faulty = np.concatenate(faulty)
        aligned = upstream.pooled_quantiles(young, p) - upstream.pooled_quantiles(old, p)
        reversed_d = upstream.pooled_quantiles(young, p) - upstream.pooled_quantiles(old, p[::-1])
        y_pool, o_pool = np.concatenate(young), np.concatenate(old)
        # Each row has equal-size scenario blocks, including merged rows.
        assert len({x.size for x in young}) == len({x.size for x in old}) == 1
        rng = np.random.default_rng(np.random.SeedSequence([SEED, i]))
        corrected = rng.choice(y_pool, N) - rng.choice(o_pool, N)
        ym, yv, ym4 = moments(y_pool)
        om, ov, om4 = moments(o_pool)
        positive_bound, negative_bound = sign_probability_lower_bounds(y_pool, o_pool)
        expected_mean, expected_var = ym - om, yv + ov
        mean_se = np.sqrt(expected_var / N)
        var_se = np.sqrt((ym4 + om4 + 6 * yv * ov - expected_var**2) / N)
        diagnostics.append(dict(
            younger=meta.Stage[i], older=meta.Stage[i + 1],
            original_older_labels=json.dumps(labels), older_distinct_labels=len(set(labels)),
            exact_independence_mean=expected_mean, exact_independence_sd=np.sqrt(expected_var),
            corrected_mean_z=(corrected.mean() - expected_mean) / mean_se,
            corrected_variance_z=(corrected.var() - expected_var) / var_se,
            faulty_mean_error=faulty.mean() - expected_mean,
            corrected_mean_error=corrected.mean() - expected_mean,
            all_coupling_positive_probability_lower_bound=positive_bound,
            all_coupling_negative_probability_lower_bound=negative_bound,
        ))
        for name, values in [
            ("shared_label_independent", shared), ("fully_independent_original", faulty),
            ("fully_independent_corrected", corrected), ("quantile_aligned", aligned),
            ("reverse_quantile", reversed_d),
        ]:
            rows.append(dict(younger=meta.Stage[i], older=meta.Stage[i + 1], coupling=name,
                             **upstream.summarise(values)))
    results, diagnostics = pd.DataFrame(rows), pd.DataFrame(diagnostics)
    OUT.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUT / "stage_differences.tsv", sep="\t", index=False, float_format="%.8f")
    diagnostics.to_csv(OUT / "independence_diagnostics.tsv", sep="\t", index=False, float_format="%.8f")
    replay_check, max_replay_error = compare_original_output(results, upstream.OUT / "stage_differences.tsv")
    signs = results.pivot(index=["younger", "older"], columns="coupling", values="sign_resolved")
    changed = signs.fully_independent_original != signs.fully_independent_corrected
    near = results[results.coupling == "fully_independent_corrected"].copy()
    near["margin"] = np.minimum(near.q05.abs(), near.q95.abs())
    repeat_pairs = set(signs.index[changed]) | set(zip(near[near.margin < 0.10].younger, near[near.margin < 0.10].older))
    repeat_rows = []
    for i in range(len(meta) - 1):
        key = (meta.Stage[i], meta.Stage[i + 1])
        if key not in repeat_pairs:
            continue
        yp, op = np.concatenate(samples[i]), np.concatenate(samples[i + 1])
        for repeat in range(1, 6):
            rng = np.random.default_rng(np.random.SeedSequence([SEED, i, repeat]))
            d = rng.choice(yp, N) - rng.choice(op, N)
            repeat_rows.append(dict(younger=key[0], older=key[1], repeat=repeat, **upstream.summarise(d)))
    pd.DataFrame(repeat_rows).to_csv(OUT / "targeted_mc_repeats.tsv", sep="\t", index=False, float_format="%.8f")
    report = {
        "source_build_commit": AUDITED_COMMIT,
        "source_build_sha256": AUDITED_SHA256,
        "original_output_comparison": replay_check,
        "pairs": len(meta) - 1, "draws_per_independence_pair": N,
        "max_original_replay_error_vs_rounded_table": max_replay_error,
        "median_sd": results.groupby("coupling").sd.median().to_dict(),
        "sign_resolved_counts": results.groupby("coupling").sign_resolved.sum().astype(int).to_dict(),
        "all_four_tested_signs_count": int(signs[["shared_label_independent", "fully_independent_corrected", "quantile_aligned", "reverse_quantile"]].all(axis=1).sum()),
        "changed_independence_signs": [list(x) for x in signs.index[changed]],
        "max_abs_corrected_mean_z": float(diagnostics.corrected_mean_z.abs().max()),
        "max_abs_corrected_variance_z": float(diagnostics.corrected_variance_z.abs().max()),
        "median_abs_original_mean_error": float(diagnostics.faulty_mean_error.abs().median()),
        "median_abs_corrected_mean_error": float(diagnostics.corrected_mean_error.abs().median()),
        "max_abs_original_mean_error": float(diagnostics.faulty_mean_error.abs().max()),
        "max_abs_corrected_mean_error": float(diagnostics.corrected_mean_error.abs().max()),
        "older_distinct_labels_range": [int(diagnostics.older_distinct_labels.min()), int(diagnostics.older_distinct_labels.max())],
        "median_abs_median_difference_original_vs_corrected": float((results[results.coupling == "fully_independent_original"].q50.reset_index(drop=True) - results[results.coupling == "fully_independent_corrected"].q50.reset_index(drop=True)).abs().median()),
        "targeted_repeat_pairs": len(repeat_pairs),
        "pairs_with_all_coupling_sign_probability_lower_bound_above_95pct": int(
            (diagnostics[["all_coupling_positive_probability_lower_bound", "all_coupling_negative_probability_lower_bound"]].max(axis=1) > .95).sum()),
    }
    (OUT / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("Changed sign rows:")
    print(results.merge(pd.DataFrame(list(signs.index[changed]), columns=["younger", "older"]), on=["younger", "older"]).to_string(index=False))
    print("Targeted independent-draw repeats:")
    print(pd.DataFrame(repeat_rows).to_string(index=False))
    print("Five tested-coupling robust pairs: valid all-coupling probability lower bounds:")
    robust = signs[["shared_label_independent", "fully_independent_corrected", "quantile_aligned", "reverse_quantile"]].all(axis=1)
    print(diagnostics.merge(pd.DataFrame(list(signs.index[robust]), columns=["younger", "older"]),
                            on=["younger", "older"])[["younger", "older", "all_coupling_positive_probability_lower_bound", "all_coupling_negative_probability_lower_bound"]].to_string(index=False))


if __name__ == "__main__":
    main()
