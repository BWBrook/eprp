import hashlib
import json
import sys
from pathlib import Path

import numpy as np


path = Path(sys.argv[1])
data = np.load(path, allow_pickle=False)
accepted = data["params_accepted_history"]
proposed = data["params_proposed_history"]
accepted_rss = data["rss_accepted_history"]
proposed_rss = data["rss_proposed_history"]
flags = data["acceptance_history"]
assert accepted.shape == (5003, 5, 6) and proposed.shape == (5002, 5, 6)
assert flags.shape == (5002, 6) and np.isin(flags, [0, 1]).all()


def prob(log_ratio):
    return float(np.exp(min(0.0, log_ratio)))


chains = []
for chain in range(6):
    first = np.flatnonzero(flags[1:, chain] == 1)
    assert first.size
    first = int(first[0] + 1)
    initial = accepted[0, :, chain]
    assert np.isfinite(initial).all()
    assert np.allclose(accepted[1:first + 1, :, chain], initial, rtol=0, atol=1e-12)
    assert 1.6 <= initial[4] <= 2.4
    initial_prior = -0.5 * ((initial[4] - 2) / 0.4) ** 2
    attempts = []
    for i in range(1, first + 1):
        if not np.isfinite(proposed_rss[i, chain]):
            attempts.append({"iteration": i, "out_of_bounds_or_missing_rss": True})
            continue
        q = proposed[i, 4, chain]
        proposed_prior = -0.5 * ((q - 2) / 0.4) ** 2
        likelihood_difference = -0.5 * (proposed_rss[i, chain] - accepted_rss[i, chain])
        correct = likelihood_difference + proposed_prior - initial_prior
        implemented = likelihood_difference + proposed_prior + 1.0
        attempts.append({"iteration": i, "observed_acceptance": int(flags[i, chain]),
                         "current_rss": float(accepted_rss[i, chain]), "proposed_rss": float(proposed_rss[i, chain]),
                         "current_parameters": initial.tolist(), "proposed_parameters": proposed[i, :, chain].tolist(),
                         "current_q10": float(initial[4]), "proposed_q10": float(q),
                         "correct_log_ratio": float(correct), "implemented_log_ratio": float(implemented),
                         "correct_acceptance_probability": prob(correct),
                         "implemented_acceptance_probability": prob(implemented),
                         "rejection_incompatible_with_deposited_rule": bool(flags[i, chain] == 0 and implemented >= 0)})
    chains.append({"chain_index_zero_based": chain, "initial_q10": float(initial[4]),
                   "correct_initial_log_prior": float(initial_prior), "implemented_initial_log_prior": -1.0,
                   "first_accepted_iteration": first, "attempts": attempts})

print(json.dumps({"input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "interpretation": "conditional on the deposited source and proof prior; proposal uniform draws are not recorded",
                  "chains": chains}, indent=2, allow_nan=False))
