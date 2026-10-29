import json
import math
from pathlib import Path


def profile(richness, weights):
    if len(richness) != len(weights) or not richness:
        raise ValueError("Matched non-empty vectors required")
    if any(not math.isfinite(x) or x < 0 for x in (*richness, *weights)):
        raise ValueError("Finite nonnegative values required")
    mass = [x * w for x, w in zip(richness, weights)]
    total = math.fsum(mass)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("No finite positive observed incidence mass")
    return [x / total for x in mass]


def affinity(p, q):
    return min(1.0, math.fsum(math.sqrt(x * y) for x, y in zip(p, q)))


def power_upper(p, q, n, alpha):
    a = affinity(p, q)
    if n == 0 or a == 1:
        tv_upper = 0.0
    elif a == 0:
        tv_upper = 1.0
    else:
        tv_upper = math.sqrt(-math.expm1(2 * n * math.log(a)))
    return min(1.0, alpha + tv_upper)


def counts(n, k):
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in counts(n - first, k - 1):
            yield (first, *rest)


def multinomial_probability(c, p):
    if any(ci > 0 and pi == 0 for ci, pi in zip(c, p)):
        return 0.0
    logp = math.lgamma(sum(c) + 1) - math.fsum(math.lgamma(ci + 1) for ci in c)
    logp += math.fsum(ci * math.log(pi) for ci, pi in zip(c, p) if ci)
    return math.exp(logp)


def exact_np(p, q, n, alpha):
    outcomes = []
    for c in counts(n, len(p)):
        p0, p1 = multinomial_probability(c, p), multinomial_probability(c, q)
        if p0 == p1 == 0:
            continue
        ratio = math.inf if p0 == 0 else p1 / p0
        outcomes.append((ratio, p0, p1))
    p0_total = math.fsum(x[1] for x in outcomes)
    p1_total = math.fsum(x[2] for x in outcomes)
    assert abs(p0_total - 1) < 1e-12 and abs(p1_total - 1) < 1e-12
    size, power = 0.0, 0.0
    for _, p0, p1 in sorted(outcomes, reverse=True):
        fraction = 1.0 if p0 == 0 else min(1.0, max(0.0, alpha - size) / p0)
        size += fraction * p0
        power += fraction * p1
    return dict(size=size, power=power, null_mass=p0_total, alternative_mass=p1_total,
                outcomes=len(outcomes))


def check():
    alpha = 0.05
    p = profile([1, 2, 3], [1, 1, 1])
    scaled = profile([11, 22, 33], [1, 1, 1])
    assert p == scaled
    assert abs(affinity(p, scaled) - 1) < 1e-15
    fixtures = {
        "pure_multiplicative_change": (p, scaled),
        "shared_dominant_cell": ([0.9, 0.05, 0.05], [0.9, 0.1, 0.0]),
        "masked_shared_cell": ([0.5, 0.5], [1.0, 0.0]),
        "disjoint_support": ([1.0, 0.0], [0.0, 1.0]),
    }
    rows = []
    for name, (p0, p1) in fixtures.items():
        for n in (0, 1, 4, 8):
            exact = exact_np(p0, p1, n, alpha)
            upper = power_upper(p0, p1, n, alpha)
            assert exact["power"] <= upper + 1e-12
            assert abs(exact["size"] - alpha) < 1e-12
            if name == "pure_multiplicative_change" or n == 0:
                assert abs(exact["power"] - alpha) < 1e-12
            if name == "disjoint_support" and n > 0:
                assert abs(exact["power"] - 1) < 1e-12
            rows.append(dict(fixture=name, n=n, affinity=affinity(p0, p1),
                             power_upper=upper, **exact))
    h_full = 1 - affinity(*fixtures["shared_dominant_cell"])
    h_masked = 1 - affinity(*fixtures["masked_shared_cell"])
    assert abs(h_masked / h_full - 10) < 1e-12
    invalid_rejected = 0
    for richness, weights in [([0, 0], [1, 1]), ([1, 2], [0, 0]),
                              ([1, -1], [1, 1]), ([1, math.nan], [1, 1])]:
        try:
            profile(richness, weights)
        except ValueError:
            invalid_rejected += 1
    assert invalid_rejected == 4
    return dict(scope="Synthetic design controls only; no INDITEK or empirical evaluation",
                alpha=alpha, rows=rows, invalid_profiles_rejected=invalid_rejected,
                squared_hellinger_full=h_full, squared_hellinger_masked=h_masked,
                conditional_mask_amplification=h_masked / h_full,
                all_pass=True)


if __name__ == "__main__":
    result = check()
    path = Path(__file__).with_name("observer-check.json")
    path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"all_pass": result["all_pass"], "exact_cases": len(result["rows"]),
                      "output": str(path)}))
