import hashlib
import json
import sys
from pathlib import Path

import numpy as np


root = Path(sys.argv[1])
reports = {}
for model in ("proof", "open", "expo", "food", "temp"):
    path = root / f"inditekMCMCoutput_5002_{model}.npz"
    data = np.load(path, allow_pickle=False)
    old, new = data["params_accepted_history"], data["params_proposed_history"]
    rss_old, rss_new = data["rss_accepted_history"], data["rss_proposed_history"]
    flag = data["acceptance_history"]
    assert old.shape == (5003, 5, 6) and new.shape == (5002, 5, 6)
    counts = {"old_rule_impossible_rejections": 0, "deposited_rule_impossible_rejections": 0,
              "old_rule_accepted_below_minus_30": 0, "deposited_rule_accepted_below_minus_30": 0, "finite_steps": 0}
    examples = {"old_rule": [], "deposited_rule": []}
    for chain in range(6):
        priors = {"old_rule": 0.0 if model == "temp" else -1.0,
                  "deposited_rule": 0.0 if model == "temp" else -1.0}
        for i in range(1, 5002):
            if not (np.isfinite(rss_old[i, chain]) and np.isfinite(rss_new[i, chain])):
                continue
            likelihood_difference = -0.5 * (rss_new[i, chain] - rss_old[i, chain])
            q_old, q_new = old[i, 4, chain], new[i, 4, chain]
            if model == "temp":
                proposed_priors = {"old_rule": 0.0, "deposited_rule": 0.0}
            else:
                assert np.isfinite(q_old) and np.isfinite(q_new)
                proposed_priors = {"old_rule": -0.5 * ((q_old - 2.0) / 0.08) ** 2,
                                   "deposited_rule": -0.5 * ((q_new - 2.0) / 0.4) ** 2}
            counts["finite_steps"] += 1
            for rule in priors:
                log_ratio = likelihood_difference + proposed_priors[rule] - priors[rule]
                if flag[i, chain] == 0 and log_ratio > 1e-9:
                    counts[rule + "_impossible_rejections"] += 1
                    if len(examples[rule]) < 3:
                        examples[rule].append({"chain_index_zero_based": chain, "iteration": i, "log_ratio": float(log_ratio)})
                if flag[i, chain] == 1 and log_ratio < -30:
                    counts[rule + "_accepted_below_minus_30"] += 1
                if flag[i, chain] == 1:
                    priors[rule] = proposed_priors[rule]
    reports[model] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), **counts, "examples": examples}

print(json.dumps({"scope": "conditional replay: Q10 mean 2, sigma 0.08 in June 4 code and sigma 0.4 in deposited code; uniform draws unrecorded", "models": reports}, indent=2, allow_nan=False))
