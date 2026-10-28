import hashlib
import json
import sys
import types
from pathlib import Path

import numpy as np


path = Path(sys.argv[1])
raw = path.read_bytes()
source_hash = hashlib.sha256(raw).hexdigest()
assert source_hash == "79256783eda56ae30fa653e8f1350a172cd6eb7201eefa2944347192ce4efedf"
source = raw.decode()
old_initial = "temp[gaus]=mu[gaus]"
new_initial = "temp[gaus]=((params_current[gaus] - mu[gaus]) / sigma[gaus])**2"
old_proposal = "temp[gaus]=((params_current[gaus] - mu[gaus]) / sigma[gaus])**2"
new_proposal = "temp[gaus]=((params_proposed[gaus] - mu[gaus]) / sigma[gaus])**2"
old_adaptation = "sigma_prop[index1]=max(sigma_prop[index1]*AR/(0.4),1e-12)"
new_adaptation = "sigma_prop[index1]=sigma_prop[index1]"
assert all(source.count(s) == 1 for s in (old_initial, old_proposal, old_adaptation))

stub = types.ModuleType("principal")
stub.principal = lambda *args: (0.0, np.zeros(2978), np.zeros(2978))
sys.modules.update({"principal": stub, "mat73": types.ModuleType("mat73")})
mu = np.array([161.0, 19.0, 0.035, 0.002, 2.0])
sigma = np.array([8.0, 1.9, 0.00035, 0.0003, 0.08])
bounds = [[50, 1000], [1, 150], [0.001, 0.1], [0.0001, 0.05], [1, 3.5]]
iterations = 50001


def batch_mcse(x):
    batches = np.asarray(x, dtype=float).reshape(45, 1000).mean(axis=1)
    return float(np.std(batches, ddof=1) / np.sqrt(len(batches)))


records = []
for version in ("historical_prior", "corrected_prior"):
    code = source
    if version == "corrected_prior":
        code = code.replace(old_proposal, new_proposal)
    code = code.replace(old_initial, new_initial).replace(old_adaptation, new_adaptation)
    module = types.ModuleType(version)
    exec(compile(code, str(path) + ":" + version, "exec"), module.__dict__)
    for seed in (34101, 34102, 34103, 34104):
        np.random.seed(seed)
        output = module.inditek_metropolis(mu.copy(), None, None, None, None, iterations, 5, None,
                                           None, None, None, None, mu, sigma, bounds, sigma.copy(),
                                           iterations + 1, "proof", [0, 1, 2, 3, 4])
        q = output["params_accepted_history"][5001:50001, 4]
        scales = output["sigma_prop"][5001:50001, :]
        assert q.shape == (45000,) and np.isfinite(q).all() and np.all((q >= 1) & (q <= 3.5))
        assert np.array_equal(scales, np.broadcast_to(sigma, scales.shape))
        lower, upper = q < 1.92, q > 2.08
        records.append({"variant": version, "seed": seed, "draws": int(q.size),
                        "mean": float(np.mean(q)), "mean_mcse_batch1000": batch_mcse(q),
                        "variance": float(np.var(q, ddof=1)),
                        "lower_tail": float(np.mean(lower)), "lower_mcse_batch1000": batch_mcse(lower),
                        "upper_tail": float(np.mean(upper)), "upper_mcse_batch1000": batch_mcse(upper),
                        "acceptance": float(np.mean(output["acceptance_history"][5001:50001])),
                        "proposal_scale_min": scales.min(axis=0).tolist(),
                        "proposal_scale_max": scales.max(axis=0).tolist()})

print(json.dumps({"source_sha256": source_hash, "iterations": iterations, "burn_discard": 5000,
                  "target": {"mean": 2, "variance": 0.0064, "tail_at_one_sd": 0.1586552539},
                  "modifications_shared": ["correct initial Gaussian prior", "hold proposal scales fixed"],
                  "corrected_variant_additional_modification": "evaluate proposed prior at proposed parameters",
                  "records": records}, indent=2, allow_nan=False))
