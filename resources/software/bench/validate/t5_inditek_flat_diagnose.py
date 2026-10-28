import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path

import numpy as np


path = Path(sys.argv[1])
stub = types.ModuleType("principal")
stub.principal = lambda *args: (0.0, np.zeros(2978), np.zeros(2978))
sys.modules.update({"principal": stub, "mat73": types.ModuleType("mat73")})
spec = importlib.util.spec_from_file_location("historical_sampler", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
mu = np.array([161.0, 19.0, 0.035, 0.002, 2.0])
sigma = np.array([8.0, 1.9, 0.00035, 0.0003, 0.08])
bounds = [[50, 1000], [1, 150], [0.001, 0.1], [0.0001, 0.05], [1, 3.5]]
np.random.seed(34101)
out = module.inditek_metropolis(mu.copy(), None, None, None, None, 25001, 5, None, None, None, None, None,
                                mu, sigma, bounds, sigma.copy(), 25002, "proof", [0, 1, 2, 3, 4])
blocks = []
for start in (1, 5001, 10001, 15001, 20001):
    end = start + 5000
    q = out["params_accepted_history"][start:end, 4]
    rss = out["rss_proposed_history"][start:end, 0]
    steps = out["sigma_prop"][start:end]
    blocks.append({"start": start, "end_exclusive": end, "q_min": float(np.min(q)), "q_max": float(np.max(q)),
                   "accepted": int(out["acceptance_history"][start:end].sum()),
                   "nonfinite_proposed_rss": int(np.count_nonzero(~np.isfinite(rss))),
                   "proposal_sd_last": steps[-1].tolist()})
assert abs(blocks[1]["q_min"] - 2.5250621710586048) < 1e-12 and blocks[1]["accepted"] == 0
print(json.dumps({"source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "seed": 34101,
                  "blocks": blocks}, indent=2, allow_nan=False))
