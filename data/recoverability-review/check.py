"""Reproduce bounded counterexamples for the Codex recoverability review."""

import hashlib
import json
import math
from pathlib import Path

import numpy as np


source = Path(__file__).resolve().parents[1] / "recoverability-contract"
original = json.loads((source / "identifiability.json").read_text())
rng = np.random.default_rng(123)
deadline = []
for idx, a in ((0, 3), (1, 1000), (2, 1000)):
    w = original["worlds"][idx]
    r = w["slope_r"]
    b = 1.0 + r
    weights = rng.gamma(rng.binomial(a, r / b, size=1_000_000), b / r)
    deadline.append({"world": w["world"], "probability_W_proxy_time_le_13":
                     float(np.mean(weights >= w["threshold_K"] * math.exp(-13 * r)))})
m = 3.303
weights = rng.gamma(m / 2.0, 2.0, size=1_000_000)
deadline.append({"world": "import, rounded m=3.303, arrivals continue indefinitely",
                 "probability_W_proxy_time_le_13": float(np.mean(weights >= 1e6 * math.exp(-13)))})
r = original["worlds"][1]["slope_r"]
out = {
    "source_sha256": {n: hashlib.sha256((source / n).read_bytes()).hexdigest()
                      for n in ("identifiability.py", "identifiability.json", "scarcity_dispersion.py", "scarcity_dispersion.json")},
    "numpy_version": np.__version__, "seed": 123, "draws_per_deadline_comparison": 1_000_000,
    "finite_K2": {"b": 2, "d": 1, "a": 1,
        "true_never_hit": 1/3, "eventual_extinction": 1/2,
        "true_hit_by_1": 2/3 * (1-math.exp(-3)),
        "W_proxy_hit_by_1": 0.5*math.exp(-math.exp(-1)),
        "W_proxy_negative_time": 0.5*math.exp(-1)},
    "deadline_13_under_W_proxy": deadline,
    "import_P_zero": [{"t": t, "probability": (1/(2*math.exp(t)-1))**(m/2)} for t in (0.25, 0.5, 1.0, 2.0)],
    "growth_erosion_nearcritical_extinction_a1000_b1p0001_d1": (1/1.0001)**1000,
    "large_K_timing_error_scale": {"baseline": math.sqrt(3/1e6), "growth": math.sqrt((r+2)/(1e6*r))/r},
}
Path(__file__).with_name("checks.json").write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
print(json.dumps(out, indent=2))
