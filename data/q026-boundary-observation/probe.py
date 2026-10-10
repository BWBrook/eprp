"""Small observation counterexample; no fossil data or fitted biological rates.

Twenty lineages persist throughout twelve unit bins. Names are replaced
one-for-one by a Poisson process; fossils have an independent Poisson rate.
Run: python3 data/q026-boundary-observation/probe.py
"""

import csv
import math
from pathlib import Path
import random
import statistics


N_LINEAGES = 20
N_BINS = 12
REPLICATES = 1000
SEED = 20261010


def one_side_detection(fossil_rate, replacement_rate, available_time):
    """Fossil before replacement or the observation-window end."""
    rate = fossil_rate + replacement_rate
    return fossil_rate / rate * -math.expm1(-rate * available_time)


def expected_boundary_count(fossil_rate, replacement_rate, boundary):
    return N_LINEAGES * one_side_detection(
        fossil_rate, replacement_rate, boundary
    ) * one_side_detection(fossil_rate, replacement_rate, N_BINS - boundary)


def boundary_count(occurrences, boundary):
    ranges = {}
    for name, time in occurrences:
        if name not in ranges:
            ranges[name] = [time, time]
        else:
            ranges[name][0] = min(ranges[name][0], time)
            ranges[name][1] = max(ranges[name][1], time)
    return sum(first < boundary < last for first, last in ranges.values())


def simulate(rng, fossil_rate, replacement_rate):
    bins = [set() for _ in range(N_BINS)]
    ranges = {}
    event_rate = fossil_rate + replacement_rate
    for lineage in range(N_LINEAGES):
        time, name_id = 0.0, 0
        while True:
            time += rng.expovariate(event_rate)
            if time >= N_BINS:
                break
            if rng.random() < fossil_rate / event_rate:
                name = (lineage, name_id)
                bins[int(time)].add(name)
                if name not in ranges:
                    ranges[name] = [time, time]
                else:
                    ranges[name][1] = time
            else:
                # The biological lineage persists; only its name changes.
                name_id += 1
    boundary_counts = [
        sum(first < t < last for first, last in ranges.values())
        for t in range(1, N_BINS)
    ]
    two_timers = [len(bins[t - 1] & bins[t]) for t in range(1, N_BINS)]
    assert all(0 <= two <= bc <= N_LINEAGES
               for two, bc in zip(two_timers, boundary_counts))
    return boundary_counts, two_timers, [len(names) for names in bins]


def main():
    # Same information through landmark t=1, different observed boundary counts
    # once a younger fossil is admitted. Missing right-hand support is not a
    # known biological zero and cannot be used as a prefix-only predictor.
    past = [("A", 0.2), ("A", 0.8)]
    record_a = past + [("A", 1.2)]
    record_b = past + [("B", 1.2)]
    assert [x for x in record_a if x[1] <= 1] == [
        x for x in record_b if x[1] <= 1
    ]
    assert boundary_count(record_a, 1) == 1
    assert boundary_count(record_b, 1) == 0

    # With complete instantaneous observation, one-for-one replacement never
    # changes the true boundary count. The detection formula has that limit.
    assert abs(expected_boundary_count(1e9, 2, 6) - N_LINEAGES) < 1e-6
    rows = []
    for fossil_rate in (0.5, 2.0):
        for replacement_rate in (0.0, 0.5, 2.0):
            rng = random.Random(SEED + len(rows))
            bc_means, two_means, bin_means, increment_ms = [], [], [], []
            for _ in range(REPLICATES):
                counts, twos, within = simulate(rng, fossil_rate, replacement_rate)
                bc_means.append(statistics.mean(counts))
                two_means.append(statistics.mean(twos))
                bin_means.append(statistics.mean(within))
                increment_ms.append(statistics.mean(
                    (after - before) ** 2
                    for before, after in zip(counts, counts[1:])
                ))
            analytic = statistics.mean(
                expected_boundary_count(fossil_rate, replacement_rate, t)
                for t in range(1, N_BINS)
            )
            empirical = statistics.mean(bc_means)
            # Independent replicate means, not correlated boundaries, define SE.
            mc_se = statistics.stdev(bc_means) / math.sqrt(REPLICATES)
            assert abs(empirical - analytic) < 6 * mc_se + 1e-10
            q = one_side_detection(fossil_rate, replacement_rate, 1)
            expected_twos = N_LINEAGES * q * q
            two_se = statistics.stdev(two_means) / math.sqrt(REPLICATES)
            assert abs(statistics.mean(two_means) - expected_twos) < 6 * two_se
            rows.append({
                "fossil_rate": fossil_rate,
                "replacement_rate": replacement_rate,
                "true_standing_count": N_LINEAGES,
                "boundary_mean_exact": analytic,
                "boundary_mean_simulated": empirical,
                "boundary_mean_mc_se": mc_se,
                "adjacent_two_timer_mean_exact": expected_twos,
                "adjacent_two_timer_mean_simulated": statistics.mean(two_means),
                "sampled_in_bin_mean": statistics.mean(bin_means),
                "boundary_increment_mean_square": statistics.mean(increment_ms),
                "true_count_increment_mean_square": 0,
                "replicates": REPLICATES,
                "seed": SEED + len(rows),
            })

    output = Path(__file__).with_name("summary.tsv")
    with output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], delimiter="\t",
                                lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: f"{v:.9f}" if isinstance(v, float) else v
                             for k, v in row.items()})
    print("Same-prefix fixture changes retrospective count from 1 to 0.")
    print("Analytical boundary/two-timer expectations checked against simulation.")
    print("All true standing counts are 20; true count increments are zero.")
    print(output)


if __name__ == "__main__":
    main()
