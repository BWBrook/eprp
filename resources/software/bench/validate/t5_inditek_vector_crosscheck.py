import json
import sys
from pathlib import Path

import numpy as np


result = {}
for model in ("proof", "open", "expo", "food", "temp"):
    data = np.load(Path(sys.argv[1]) / f"inditekMCMCoutput_5002_{model}.npz", allow_pickle=False)
    flags = data["acceptance_history"]
    accepted, proposed = data["params_accepted_history"], data["params_proposed_history"]
    current_rss, proposed_rss = data["rss_accepted_history"], data["rss_proposed_history"]
    totals, impossible, unlikely = 0, [0, 0], [0, 0]
    for chain in range(6):
        n = flags.shape[0]
        i = np.arange(1, n)
        previous = np.maximum.accumulate(np.where(flags[:, chain] == 1, np.arange(n), 0))
        last = previous[i - 1]
        valid = np.isfinite(current_rss[i, chain]) & np.isfinite(proposed_rss[i, chain])
        totals += int(valid.sum())
        for rule, sd in enumerate((0.08, 0.4)):
            if model == "temp":
                prior = np.zeros(len(i))
                candidate = prior
            else:
                previous_q = accepted[last, 4, chain] if rule == 0 else proposed[last, 4, chain]
                prior = np.where(last == 0, -1, -0.5 * ((previous_q - 2) / sd) ** 2)
                q = accepted[i, 4, chain] if rule == 0 else proposed[i, 4, chain]
                candidate = -0.5 * ((q - 2) / sd) ** 2
            ratio = -0.5 * (proposed_rss[i, chain] - current_rss[i, chain]) + candidate - prior
            impossible[rule] += int(np.sum(valid & (flags[i, chain] == 0) & (ratio > 1e-9)))
            unlikely[rule] += int(np.sum(valid & (flags[i, chain] == 1) & (ratio < -30)))
    result[model] = {"finite_steps": totals, "old_impossible": impossible[0], "deposited_impossible": impossible[1],
                     "old_accepted_below_minus_30": unlikely[0], "deposited_accepted_below_minus_30": unlikely[1]}
print(json.dumps(result, indent=2))
