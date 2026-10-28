import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np


root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
from inditek_rhonet_2 import inditek_rhonet


def qlinear(values, p):
    a = sorted(values)
    index = (len(a) - 1) * p
    lo = math.floor(index)
    hi = math.ceil(index)
    return a[lo] + (index - lo) * (a[hi] - a[lo])


base_food = [0.5, 1.0, 2.0, 4.0, 8.0]
base_temp = [-5.0, 0.0, 5.0, 10.0, 15.0]
food = np.tile(np.asarray(base_food)[:, None], (1, 3))
temp = np.asarray([[x, x + 3, x - 4] for x in base_temp])
times = np.asarray([541, 270, 0])
rho = np.full(542, 0.01)
points = np.zeros((5, 3, 2))
kfood, kmin, kmax, smin, smax, q10 = 0.5, 10.0, 100.0, 0.002, 0.035, 2.0


def evaluate(t, model):
    return inditek_rhonet(kfood, kmin, food, t, rho, np.asarray([]), kmax, smin, smax,
                          q10, 0, 0, points, times, model)


f1 = {}
for model in ("proof", "food", "temp", "expo"):
    values, carrying, ext = evaluate(temp, model)
    assert ext.size == 0 and np.isfinite(values[:, [0, 271, 541]]).all()
    expected = np.empty((5, 3))
    for col in range(3):
        tmax = qlinear(temp[:, col], 0.99)
        for row in range(5):
            food_factor = 1 if model == "food" else max(0, min(1, food[row, col] / (kfood + food[row, col])))
            temp_factor = 1 if model == "temp" else max(0, min(1, q10 ** ((temp[row, col] - tmax) / 10)))
            expected[row, col] = smin + (smax - smin) * food_factor * temp_factor
    rate_error = float(np.max(np.abs(values[:, [0, 271, 541]] - expected)))
    if model == "expo":
        assert carrying is None
        k_error = None
    else:
        lo, hi = qlinear(food.ravel(), 0.01), qlinear(food.ravel(), 0.99)
        expected_k = np.asarray([[max(kmin, min(kmax, kmin + (kmax-kmin) * (food[i, j]-lo)/(hi-lo)))
                                  for j in range(3)] for i in range(5)])
        k_error = float(np.max(np.abs(carrying - expected_k)))
    shifted, _, _ = evaluate(temp + 10, model)
    shift_error = float(np.max(np.abs(shifted[:, [0, 271, 541]] - values[:, [0, 271, 541]])))
    f1[model] = {"rate_max_abs_error": rate_error, "capacity_max_abs_error": k_error,
                 "uniform_shift_max_abs_error": shift_error,
                 "pass": rate_error <= 1e-12 and (k_error is None or k_error <= 1e-12) and shift_error <= 1e-12}

print(json.dumps({"source_sha256": hashlib.sha256((root / "inditek_rhonet_2.py").read_bytes()).hexdigest(),
                  "time_slices": times.tolist(), "results": f1, "all_pass": all(x["pass"] for x in f1.values())},
                 indent=2, allow_nan=False))
