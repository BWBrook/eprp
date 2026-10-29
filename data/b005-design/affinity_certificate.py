import hashlib
import json
import math
from pathlib import Path


def certificate():
    source = Path(__file__).with_name("map-check.json")
    saved = json.loads(source.read_text())
    a, alpha, target = saved["affinity"], saved["alpha"], saved["target_power"]
    assert 0 < a < 1 and 0 < alpha < target < 1
    sufficient_n = math.ceil(math.log(min(alpha, 1 - target)) / math.log(a))
    necessary_n = math.ceil(math.log1p(-(target - alpha) ** 2) / (2 * math.log(a)))
    rows = []
    for n in (sufficient_n - 1, sufficient_n, saved["n"]):
        error_sum_upper = a ** n
        rows.append(dict(n=n, error_sum_upper=error_sum_upper,
                         size_upper=error_sum_upper, power_lower=1 - error_sum_upper,
                         certifies_declared_targets=error_sum_upper <= min(alpha, 1 - target)))
    assert not rows[0]["certifies_declared_targets"]
    assert all(r["certifies_declared_targets"] for r in rows[1:])
    return dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                observer="Frozen multinomial independent cell-incidence law",
                rule="Reject P0 when P1/P0 > 1, equivalently log ratio > 0; ties accepted",
                theorem="size + false-negative probability = sum min(P0,P1) <= affinity**n",
                affinity=a, alpha=alpha, target_power=target,
                necessary_n=necessary_n, sufficient_n=sufficient_n, rows=rows,
                exact_optimal_n_computed=False,
                meaning="Analytic operating-characteristic bounds, not zero realised error or an empirical fossil result")


if __name__ == "__main__":
    result = certificate()
    Path(__file__).with_name("affinity-certificate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
