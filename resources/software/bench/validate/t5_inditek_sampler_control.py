import importlib.util
import hashlib
import json
import sys
import types
from pathlib import Path

import numpy as np


path = Path(sys.argv[1])
stub = types.ModuleType("inditek_main_2")
stub.inditek_main = lambda *args: (0.0, np.zeros(2978), np.zeros(2978))
sys.modules["inditek_main_2"] = stub
sys.modules["mat73"] = types.ModuleType("mat73")
spec = importlib.util.spec_from_file_location("inditek_sampler_under_test", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
def run(q10, index, draw, uniform):
    initial = np.array([161.0, 19.0, 0.035, 0.002, q10])
    mu = np.array([161.0, 19.0, 0.035, 0.002, 2.0])
    sigma = np.array([40.0, 9.5, 0.00175, 0.0015, 0.4])
    bounds = [[50, 1000], [1, 150], [0.001, 0.1], [0.0001, 0.05], [1, 3.5]]
    proposal_sd = 0.2 * sigma
    np.random.randint = lambda *args, **kwargs: index
    def normal(*shape):
        values = np.zeros(shape)
        values[index, 0] = draw
        return values
    np.random.randn = normal
    np.random.rand = lambda *args: uniform
    result = module.inditek_MCMC(initial, None, None, None, None, 2, 5, None, None, None, None, None,
                                mu, sigma, bounds, proposal_sd, 1, "proof", [0, 1, 2, 3, 4], None, None)
    proposed = result["params_proposed_history"][1]
    prior_before = -0.5 * ((q10 - 2.0) / 0.4) ** 2
    prior_after = -0.5 * ((proposed[4] - 2.0) / 0.4) ** 2
    correct_log_ratio = prior_after - prior_before
    return {"initial_q10": q10, "proposed": proposed.tolist(), "uniform_draw": uniform,
            "accepted": int(result["acceptance_history"][1][0]),
            "correct_log_acceptance_ratio": correct_log_ratio,
            "correct_acceptance": int(np.log(uniform) < correct_log_ratio)}


result = {"at_prior_mean": run(2.0, 0, 0.25, 0.5),
          "away_from_prior_mean": run(3.0, 0, 0.25, 0.5),
          "within_proof_initial_range": run(2.3, 4, 2.5, 0.8)}
assert result["at_prior_mean"]["accepted"] == result["at_prior_mean"]["correct_acceptance"] == 1
assert result["away_from_prior_mean"]["accepted"] == 0 and result["away_from_prior_mean"]["correct_acceptance"] == 1
assert result["within_proof_initial_range"]["accepted"] == 1 and result["within_proof_initial_range"]["correct_acceptance"] == 0
print(json.dumps({"source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "results": result}, indent=2))
