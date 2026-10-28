import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path

import numpy as np


old_path, new_path = map(Path, sys.argv[1:3])
constant = lambda *args: (0.0, np.zeros(2978), np.zeros(2978))
old_stub, new_stub = types.ModuleType("principal"), types.ModuleType("inditek_main_2")
old_stub.principal = constant
new_stub.inditek_main = constant
sys.modules.update({"principal": old_stub, "inditek_main_2": new_stub, "mat73": types.ModuleType("mat73")})


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load(old_path, "historical_sampler")
new = load(new_path, "deposited_sampler")
mu = np.array([161.0, 19.0, 0.035, 0.002, 2.0])
sigma = np.array([8.0, 1.9, 0.00035, 0.0003, 0.08])
bounds = [[50, 1000], [1, 150], [0.001, 0.1], [0.0001, 0.05], [1, 3.5]]
iterations = 25001


def batch_mcse(x):
    batches = np.asarray(x, dtype=float).reshape(20, 1000).mean(axis=1)
    return float(np.std(batches, ddof=1) / np.sqrt(len(batches)))


records = []
for version in ("historical", "deposited"):
    for seed in (34101, 34102, 34103, 34104):
        np.random.seed(seed)
        common = [mu.copy(), None, None, None, None, iterations, 5, None, None, None, None, None,
                  mu, sigma, bounds, sigma.copy(), iterations + 1, "proof", [0, 1, 2, 3, 4]]
        output = old.inditek_metropolis(*common) if version == "historical" else new.inditek_MCMC(*common, None, None)
        q = output["params_accepted_history"][5001:25001, 4]
        assert q.shape == (20000,) and np.isfinite(q).all() and np.all((q >= 1) & (q <= 3.5))
        lower, upper = q < 1.92, q > 2.08
        records.append({"version": version, "seed": seed, "draws": len(q), "mean": float(np.mean(q)),
                        "mean_mcse_batch1000": batch_mcse(q), "variance": float(np.var(q, ddof=1)),
                        "lower_tail": float(np.mean(lower)), "lower_mcse_batch1000": batch_mcse(lower),
                        "upper_tail": float(np.mean(upper)), "upper_mcse_batch1000": batch_mcse(upper),
                        "overall_acceptance": float(np.mean(output["acceptance_history"][5001:25001]))})

print(json.dumps({"old_source_sha256": hashlib.sha256(old_path.read_bytes()).hexdigest(),
                  "deposited_source_sha256": hashlib.sha256(new_path.read_bytes()).hexdigest(),
                  "target": {"mean": 2, "variance": 0.0064, "tail_at_one_sd": 0.1586552539},
                  "records": records}, indent=2, allow_nan=False))
