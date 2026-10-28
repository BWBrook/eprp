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
    assert rss_old.shape == rss_new.shape == flag.shape == (5002, 6)
    assert np.isin(flag, [0, 1]).all()
    expected_next = np.where(flag[1:5001, None, :] == 1, new[1:5001], old[1:5001])
    param_consistent = np.isclose(expected_next, old[2:5002], rtol=0, atol=0, equal_nan=True).all(axis=1)
    expected_rss = np.where(flag[1:5001] == 1, rss_new[1:5001], rss_old[1:5001])
    rss_consistent = np.isclose(expected_rss, rss_old[2:5002], rtol=0, atol=1e-9, equal_nan=True)
    checked = 0
    discrepancies = []
    for c in range(6):
        first = np.flatnonzero(flag[1:, c] == 1)
        if not first.size:
            continue
        first = int(first[0] + 1)
        for i in range(first + 1, 5002):
            if not np.isfinite(rss_new[i, c]) or not np.isfinite(rss_old[i, c]):
                continue
            same = np.isclose(old[i, :, c], new[i, :, c], rtol=0, atol=0, equal_nan=True)
            changed = np.flatnonzero(~same)
            if len(changed) != 1 or changed[0] == 4 or not same[4]:
                continue
            if rss_new[i, c] >= rss_old[i, c] - 1e-7:
                continue
            checked += 1
            if flag[i, c] == 0:
                discrepancies.append({"chain_index_zero_based": c, "iteration": i,
                                      "changed_parameter_index": int(changed[0]),
                                      "current_rss": float(rss_old[i, c]), "proposed_rss": float(rss_new[i, c]),
                                      "current_parameters": [None if not np.isfinite(x) else float(x) for x in old[i, :, c]],
                                      "proposed_parameters": [None if not np.isfinite(x) else float(x) for x in new[i, :, c]],
                                      "next_state_unchanged": bool(np.allclose(old[i, :, c], old[i + 1, :, c], rtol=0, atol=0, equal_nan=True))})
    reports[model] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "eligible_steps": checked, "rejected_improving_steps": len(discrepancies),
                      "next_state_parameter_mismatches": int(np.count_nonzero(~param_consistent)),
                      "next_state_rss_mismatches": int(np.count_nonzero(~rss_consistent)),
                      "examples": discrepancies[:5]}

print(json.dumps({"scope": "after first recorded acceptance; finite RSS, unchanged Q10, one non-Q10 parameter changed, RSS improves by more than 1e-7", "models": reports}, indent=2, allow_nan=False))
