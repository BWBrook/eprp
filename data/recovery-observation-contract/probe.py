"""Three deterministic counterexamples for the proposed recovery contract.

No fossil observations, empirical rates, climate data or fitted parameters.
Run from the repository root: python3 data/recovery-observation-contract/probe.py
"""

import csv
import itertools
import math
from pathlib import Path


def expected_rarefied_richness(counts, draws):
    total = sum(counts)
    denominator = math.comb(total, draws)
    return sum(1 - math.comb(total - count, draws) / denominator
               if total - count >= draws else 1 for count in counts)


def logistic_step(richness, capacity, exp_minus_r_dt=0.5):
    return capacity / (1 + (capacity / richness - 1) * exp_minus_r_dt)


def main():
    rows = []
    balanced = expected_rarefied_richness([10] * 10, 10)
    dominated = expected_rarefied_richness([91] + [1] * 9, 10)
    assert math.isclose(dominated, 1.9)
    assert balanced > dominated
    rows.extend([
        ("fixed_richness_and_effort", "balanced", "expected_rarefied_genera", balanced),
        ("fixed_richness_and_effort", "dominated", "expected_rarefied_genera", dominated),
    ])

    paths = {
        "aligned_levels": [(80, 80), (120, 120)],
        "opposed_levels": [(80, 120), (120, 80)],
        "independent_levels": list(itertools.product((80, 120), repeat=2)),
    }
    for name, values in paths.items():
        # Each time has exactly the same marginal distribution in all cases.
        for time in (0, 1):
            assert sum(v[time] == 80 for v in values) / len(values) == 0.5
        endpoints = [logistic_step(logistic_step(100, k1), k2) for k1, k2 in values]
        mean = sum(endpoints) / len(endpoints)
        variance = sum((value - mean) ** 2 for value in endpoints) / len(endpoints)
        rows.extend([
            ("same_capacity_marginals", name, "endpoint_mean", mean),
            ("same_capacity_marginals", name, "endpoint_variance", variance),
        ])

    for fraction in (0.1, 0.5, 0.9):
        # Constant K=1 and r=1; time to halve the initial deficit.
        half_time = math.log((2 - fraction) / (1 - fraction))
        endpoint = logistic_step(1 - fraction, 1, math.exp(-half_time))
        assert math.isclose(1 - endpoint, fraction / 2)
        rows.append(("logistic_loss_response", str(fraction), "deficit_half_time", half_time))

    output = Path(__file__).with_name("summary.tsv")
    with output.open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("probe", "case", "quantity", "value"))
        writer.writerows((*row[:3], f"{row[3]:.9f}") for row in rows)
    for row in rows:
        print(*row)


if __name__ == "__main__":
    main()
