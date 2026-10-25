import json
import math
from pathlib import Path


def size_test(a, n, b, m):
    pooled = (a + b) / (n + m)
    z = (a / n - b / m) / math.sqrt(pooled * (1 - pooled) * (1 / n + 1 / m))
    successes = a + b
    denominator = math.comb(n + m, n)

    def probability(k):
        return math.comb(successes, k) * math.comb(n + m - successes, n - k) / denominator

    observed = probability(a)
    fisher = sum(
        probability(k)
        for k in range(max(0, n - (n + m - successes)), min(n, successes) + 1)
        if probability(k) <= observed * (1 + 1e-12)
    )
    return {
        "counts": [a, n, b, m],
        "pooled_two_sided_z_p": math.erfc(abs(z) / math.sqrt(2)),
        "two_sided_fisher_p": fisher,
    }


directory = Path(__file__).resolve().parent
comparisons = json.loads((directory / "comparison.json").read_text())["comparisons"]
selected = [
    {key: row[key] for key in (
        "strategy", "duration", "p_persist_to_horizon", "excess_extinction_probability"
    )}
    for row in comparisons
    if row["initialisation"] == "stable_rounded"
    and row["dose_convention"] == "fixed_intensity"
    and row["route"] == "adult_survival"
    and row["post_disturbance_steps"] == 32
    and row["duration"] in (1, 4)
]
counts_large = [k for k in range(37) if 30.5 <= 100 * k / 36 < 31.5]
counts_small = [k for k in range(161) if 40.5 <= 100 * k / 160 < 41.5]
assert counts_large == [11] and counts_small == [65, 66]
tests = [size_test(a, 36, b, 160) for a in counts_large for b in counts_small]
assert all(test["pooled_two_sided_z_p"] > .2 and test["two_sided_fisher_p"] > .2 for test in tests)
by_case = {(row["duration"], row["strategy"]): row for row in selected}
assert len(by_case) == 4
assert by_case[1, "fast"]["p_persist_to_horizon"] < by_case[1, "slow"]["p_persist_to_horizon"]
assert by_case[4, "fast"]["p_persist_to_horizon"] > by_case[4, "slow"]["p_persist_to_horizon"]
output = {
    "source": "Valentine and Jablonski 1986, PNAS 83:6912-6914, page 6913",
    "assumptions": "n denotes group totals; percentages rounded to nearest whole percent; original unpublished data/test unavailable",
    "source_reported_p": "0.01<P<0.05",
    "size_tests": tests,
    "route_counterexample": {
        "conditions": "adult_survival, fixed_intensity, stable_rounded, 32 post-disturbance steps",
        "limit": "Changing duration also changes dose and total horizon; not an isolated duration effect",
        "rows": selected,
    },
}
(directory / "closure-checks.json").write_text(json.dumps(output, indent=2) + "\n")
print("Wrote closure-checks.json: two summary-count tests and four archived model rows")
