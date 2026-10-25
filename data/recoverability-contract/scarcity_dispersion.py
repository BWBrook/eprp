"""How the scarcity signature (founder-loss failures, timing dispersion) fades with founder number a."""
import json
import numpy as np

RNG = np.random.default_rng(20261025)
b, d = 2.0, 1.0
r = b - d
rows = []
for a in (1, 3, 10, 30, 100, 1000):
    n = 100_000 if a <= 100 else 20_000
    surv = RNG.random((n, a)) > d / b
    W = (RNG.exponential(b / r, size=(n, a)) * surv).sum(axis=1)
    pos = W > 0
    rows.append({"a": a, "P_fail": float(1 - pos.mean()), "P_fail_exact": (d / b) ** a,
                 "sd_T_given_success": float(np.std(np.log(W[pos])) / r)})
print(json.dumps(rows, indent=1))
