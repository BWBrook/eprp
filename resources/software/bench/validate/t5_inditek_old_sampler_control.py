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
sys.modules["principal"] = stub
sys.modules["mat73"] = types.ModuleType("mat73")
spec = importlib.util.spec_from_file_location("historical_sampler_under_test", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
indices = iter([0, 4])
draws = iter([np.array([[0.25], [0.0], [0.0], [0.0], [0.0]]),
              np.array([[0.0], [0.0], [0.0], [0.0], [2.5]])])
np.random.randint = lambda *args, **kwargs: next(indices)
np.random.randn = lambda *shape: next(draws)
np.random.rand = lambda *args: 0.5
initial = np.array([161.0, 19.0, 0.035, 0.002, 2.0])
mu = initial.copy()
sigma = np.array([8.0, 1.9, 0.00035, 0.0003, 0.08])
bounds = [[50, 1000], [1, 150], [0.001, 0.1], [0.0001, 0.05], [1, 3.5]]
result = module.inditek_metropolis(initial, None, None, None, None, 3, 5, None, None, None, None, None,
                                   mu, sigma, bounds, sigma.copy(), 1, "proof", [0, 1, 2, 3, 4])
proposal = result["params_proposed_history"][2]
correct_log_ratio = -0.5 * ((proposal[4] - 2.0) / 0.08) ** 2
actual = int(result["acceptance_history"][2][0])
correct = int(np.log(0.5) < correct_log_ratio)
assert int(result["acceptance_history"][1][0]) == 1
assert actual == 1 and correct == 0
print(json.dumps({"source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "first_step_accepted": 1, "initial_q10_second_step": 2.0,
                  "proposed_q10_second_step": float(proposal[4]), "uniform_draw": 0.5,
                  "correct_log_acceptance_ratio": float(correct_log_ratio),
                  "observed_second_acceptance": actual, "correct_second_acceptance": correct}, indent=2))
