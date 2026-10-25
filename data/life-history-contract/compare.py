"""Exact finite-horizon comparisons for an illustrative two-stage branching model."""

import json
import math
from pathlib import Path


def strategy(name, maturation, adult_survival, juvenile_survival=0.8):
    p = juvenile_survival * (1.0 - maturation)
    g = juvenile_survival * maturation
    f = (1.0 - adult_survival) * (1.0 - p) / g
    return {"name": name, "rates": [p, g, f, adult_survival],
            "generation_time": 1.0 / (1.0 - p) + 1.0 / (1.0 - adult_survival)}


def disturbed(s, route="none", multiplier=1.0):
    p, g, f, a = s["rates"]
    return p, g, f * (multiplier if route == "recruitment" else 1.0), a * (multiplier if route == "adult_survival" else 1.0)


def initial_counts(s, initialisation, total=40):
    p, g, f, a = s["rates"]
    fraction = (1.0 - a) / (g + 1.0 - a)
    j = round(total * fraction) if initialisation == "stable_rounded" else total // 2
    return j, total - j


def pgf(zj, za, vital_rates):
    p, g, f, s = vital_rates
    return 1.0 - p - g + p * zj + g * za, (1.0 - s + s * za) * math.exp(f * (zj - 1.0))


def evaluate(initial, schedule):
    j, a = initial
    minimum = float(j + a)
    for p, g, f, s in schedule:
        j, a = p * j + f * a, g * j + s * a
        minimum = min(minimum, j + a)
    qj = qa = 0.0
    for v in reversed(schedule):
        qj, qa = pgf(qj, qa, v)
    extinction = qj ** initial[0] * qa ** initial[1]
    return {"expected_final_abundance": j + a, "minimum_expected_abundance": minimum,
            "p_extinct_by_horizon": extinction, "p_persist_to_horizon": 1.0 - extinction}


STRATEGIES = [strategy("fast", 0.8, 0.5), strategy("slow", 0.2, 0.95)]


def checks():
    v = (0.3, 0.4, 0.7, 0.8)
    assert math.isclose(evaluate((1, 0), [v])["p_extinct_by_horizon"], 0.3)
    assert math.isclose(evaluate((0, 1), [v])["p_extinct_by_horizon"], 0.2 * math.exp(-0.7))
    assert evaluate((0, 0), [v])["p_persist_to_horizon"] == 0.0
    assert evaluate((2, 3), [(0.4, 0.6, 0.0, 1.0)] * 20)["p_persist_to_horizon"] == 1.0
    schedule = [(0.2, 0.5, 0.0, 0.8), (0.4, 0.3, 0.0, 0.6)] * 3
    sj = evaluate((1, 0), schedule)["expected_final_abundance"]
    sa = evaluate((0, 1), schedule)["expected_final_abundance"]
    assert math.isclose(evaluate((2, 3), schedule)["p_extinct_by_horizon"], (1.0 - sj) ** 2 * (1.0 - sa) ** 3)
    for s in STRATEGIES:
        p, g, f, a = s["rates"]
        assert math.isclose((1.0 - p) * (1.0 - a), f * g)
        vector = ((1.0 - a) / g, 1.0)
        j, adult = vector
        for _ in range(20):
            j, adult = p * j + f * adult, g * j + a * adult
        assert math.isclose(j + adult, sum(vector))
    return ["one-step extinction PGFs", "empty population", "zero mortality",
            "no-birth survival identity", "unit baseline eigenvalue and stable mean"]


def run():
    rows = []
    for initialisation in ("stable_rounded", "common_equal_stages"):
        for dose in ("fixed_intensity", "fixed_log_rate_budget"):
            for duration in (1, 4, 16):
                multiplier = 0.2 if dose == "fixed_intensity" else 0.2 ** (1.0 / duration)
                for recovery in (0, 8, 32):
                    for route in ("recruitment", "adult_survival"):
                        for s in STRATEGIES:
                            initial = initial_counts(s, initialisation)
                            schedule = [disturbed(s, route, multiplier)] * duration + [s["rates"]] * recovery
                            result = evaluate(initial, schedule)
                            control = evaluate(initial, [s["rates"]] * (duration + recovery))
                            rows.append({"strategy": s["name"], "initialisation": initialisation,
                                "initial_counts": initial, "dose_convention": dose,
                                "duration": duration, "duration_in_generations": duration / s["generation_time"],
                                "post_disturbance_steps": recovery, "route": route,
                                "rate_multiplier": multiplier, **result,
                                "control_p_persist": control["p_persist_to_horizon"],
                                "excess_extinction_probability": result["p_extinct_by_horizon"] - control["p_extinct_by_horizon"],
                                "mean_abundance_relative_to_control": result["expected_final_abundance"] / control["expected_final_abundance"]})
    order = []
    for s in STRATEGIES:
        for first, second in (("recruitment", "adult_survival"), ("adult_survival", "recruitment")):
            schedule = [disturbed(s, first, 0.2), disturbed(s, second, 0.2)] + [s["rates"]] * 8
            order.append({"strategy": s["name"], "first": first, "second": second,
                          **evaluate(initial_counts(s, "stable_rounded"), schedule)})
    return {"model": "two-stage independent branching; Poisson reproduction; finite horizon",
            "checks": checks(), "strategies": STRATEGIES, "comparisons": rows, "order_control": order}


if __name__ == "__main__":
    output = Path(__file__).with_name("comparison.json")
    output.write_text(json.dumps(run(), indent=2, allow_nan=False) + "\n")
    print(output)
