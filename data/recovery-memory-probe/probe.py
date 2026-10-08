"""Small observation-error counterexample, not a fossil or recovery model.

Run: python3 data/recovery-memory-probe/probe.py
Only summary.tsv in this directory is written. Uses Python's standard library.
"""

import csv
import math
import random
from pathlib import Path


SEED = 20261008
REPLICATES = 100_000
MAX_LAG = 6


def run_case(width, shared_anchor, seed):
    rng = random.Random(seed)
    moments = [[0.0] * 5 for _ in range(MAX_LAG)]
    for _ in range(REPLICATES):
        # Independent replicate histories; the latent richness index is constant.
        errors = [rng.gauss(0, 1) for _ in range(width + MAX_LAG + 1)]
        observed = [sum(errors[t:t + width]) / width for t in range(MAX_LAG + 2)]
        loss = observed[0] - observed[1]
        anchor = observed[1] if shared_anchor else rng.gauss(0, 1)
        for h, totals in enumerate(moments, start=1):
            rebound = observed[h + 1] - anchor
            for j, value in enumerate((loss, rebound, loss * loss,
                                       rebound * rebound, loss * rebound)):
                totals[j] += value
    rows = []
    for h, (sx, sy, sxx, syy, sxy) in enumerate(moments, start=1):
        xx = sxx - sx * sx / REPLICATES
        yy = syy - sy * sy / REPLICATES
        xy = sxy - sx * sy / REPLICATES
        slope = xy / xx
        se = math.sqrt(max(0.0, yy - xy * xy / xx) / (REPLICATES - 2) / xx)
        # Covariance algebra for a width-w moving average of independent errors.
        def covariance(lag):
            return max(width - lag, 0) / width**2
        if shared_anchor:
            expected = (covariance(h + 1) - covariance(1) - covariance(h)
                        + covariance(0)) / (2 * (covariance(0) - covariance(1)))
        else:
            assert width == 1  # This control uses a separate unsmoothed measurement.
            expected = 0.0
        # Broad Monte Carlo check against an independently derived exact result.
        assert abs(slope - expected) < 6 * se + 1e-10, (width, h, slope, expected)
        rows.append({"case": f"ma{width}_" + ("shared" if shared_anchor else "independent")
                     + "_anchor", "width": width, "lag_bins": h,
                     "replicates": REPLICATES, "seed": seed,
                     "exact_slope": f"{expected:.6f}", "simulated_slope": f"{slope:.6f}",
                     "monte_carlo_se": f"{se:.6f}"})
    return rows


def main():
    rows = []
    for i, (width, shared) in enumerate(((1, True), (3, True), (1, False))):
        rows.extend(run_case(width, shared, SEED + i))
    path = Path(__file__).with_name("summary.tsv")
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row["case"], row["lag_bins"], row["exact_slope"], row["simulated_slope"])


if __name__ == "__main__":
    main()
