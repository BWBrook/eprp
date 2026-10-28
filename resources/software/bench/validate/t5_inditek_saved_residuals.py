import hashlib
import json
import sys
from pathlib import Path

import numpy as np


root = Path(sys.argv[1])
result = {}
for model in ("proof", "open", "expo", "food", "temp"):
    path = root / f"inditekMCMCoutput_5002_{model}.npz"
    with np.load(path, allow_pickle=False) as saved:
        residuals = saved["residuals"]
        rss = saved["rss_proposed_history"]
        assert residuals.shape == (101, 2978, 6) and rss.shape == (5002, 6)
        finite = np.isfinite(residuals)
        sampled_rss = rss[np.arange(50, 5001, 50), :]
        result[model] = {"input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "residual_shape": list(residuals.shape), "finite_residual_values": int(finite.sum()),
                         "nonzero_finite_residual_values": int(np.count_nonzero(residuals[finite])),
                         "positive_finite_sampled_proposed_rss": int(np.sum(np.isfinite(sampled_rss) & (sampled_rss > 0))),
                         "sampled_proposed_rss_count": int(sampled_rss.size)}

print(json.dumps(result, indent=2, allow_nan=False))
