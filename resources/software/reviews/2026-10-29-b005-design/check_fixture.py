import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
from inditek_alphadiv_2 import inditek_alphadiv
from alphadiv_expo import alphadiv_expo
from inditek_gridding_alphadiv_2 import inditek_gridding_alphadiv

pt = np.array([[541, 531, 521]])
points = np.zeros((3, 3, 3))
points[:, :, 0] = np.array([0.25, 10.25, 20.25])[:, None]
points[:, :, 1] = np.array([0.25, 20.25, 40.25])[:, None]
points[:, :, 2] = np.array([10, 20, 30])[None, :]
lon = np.array([[0, 1]])
capacity = np.repeat(np.array([2., 5., 10.])[:, None], 3, axis=1)
rates = np.full((3, 542), 0.1)


def evaluate(k, r, ext):
    arrays = [pt, points, k, r, lon, ext]
    before = [a.copy() for a in arrays]
    bounded = inditek_alphadiv(pt, points, r, k, 2.5, 2.5, lon, ext)[1]
    unbounded = alphadiv_expo(pt, points, r, 2.5, 2.5, lon, ext)
    assert all(np.array_equal(a, b, equal_nan=True) for a, b in zip(arrays, before))
    return bounded, unbounded


def reference(k, extinction=False):
    vals = [1.]
    d = 1.
    for interval in range(2):
        if extinction and interval == 1:
            for index in range(11, 21):
                r = -.5 if index == 15 else .1
                feedback = 1 if k is None or index == 15 else 1-d/k
                d = max(1., d + r*d*feedback)
                if k is not None:
                    d = min(k, d)
        else:
            d = d + .1*d*(1 if k is None else 1-d/k)
            d = d*math.exp(.9) if k is None else k/(1+(k/d-1)*math.exp(-.9))
        vals.append(d)
    return vals


results = {}
for label, extinction in [('constant', False), ('forced_extinction', True)]:
    r = rates.copy()
    ext = np.array([15], dtype=int) if extinction else np.array([], dtype=int)
    if extinction:
        r[:, 15] = -.5
    bounded, unbounded = evaluate(capacity, r, ext)
    expected_b = np.array([reference(k, extinction) for k in [2, 5, 10]])
    expected_u = np.array([reference(None, extinction)]*3)
    err_b = float(np.max(np.abs(bounded-expected_b)))
    err_u = float(np.max(np.abs(unbounded-expected_u)))
    results[label] = {'bounded': bounded.tolist(), 'unbounded': unbounded.tolist(),
                      'bounded_max_error': err_b, 'unbounded_max_error': err_u,
                      'pass': err_b <= 1e-10 and err_u <= 1e-10}
    if not extinction:
        repeated = evaluate(capacity, r, ext)
        results['deterministic'] = all(np.array_equal(a,b) for a,b in zip((bounded,unbounded),repeated))
        grids = []
        for d in [bounded, unbounded]:
            x, y, grid = inditek_gridding_alphadiv(d, points, np.arange(-89.75,90,.5),
                                                   np.arange(-179.75,180,.5), np.ones((720,360,3)))
            keep = np.isfinite(grid)
            slope = np.polyfit(np.abs(y[keep]), np.log1p(grid[keep]), 1)[0]
            grids.append({'finite_cells': int(keep.sum()), 'diversities': grid[keep].tolist(),
                          'slope_log1p_per_latitude_degree': float(slope)})
        results['gridding'] = {'bounded': grids[0], 'unbounded': grids[1]}
        results['common_finite_mask'] = grids[0]['finite_cells'] == grids[1]['finite_cells'] == 3

b, u = evaluate(np.full_like(capacity,1e30), rates, np.array([], dtype=int))
results['large_finite_capacity_max_difference'] = float(np.max(np.abs(b-u)))
b, u = evaluate(capacity, np.zeros_like(rates), np.array([], dtype=int))
results['zero_rate_common_control'] = bool(np.array_equal(b, np.ones((3,3))) and np.array_equal(b,u))
with np.errstate(invalid='ignore'):
    b, u = evaluate(np.full_like(capacity,np.inf), rates, np.array([], dtype=int))
results['infinite_capacity_bounded_nonfinite_count'] = int(np.sum(~np.isfinite(b)))
results['all_declared_controls_pass'] = bool(results['constant']['pass'] and results['forced_extinction']['pass']
    and results['deterministic'] and results['zero_rate_common_control'] and results['common_finite_mask']
    and results['large_finite_capacity_max_difference'] <= 1e-10)
names = ['inditek_main_2.py','inditek_rhonet_2.py','inditek_alphadiv_2.py','alphadiv_expo.py','inditek_gridding_alphadiv_2.py']
print(json.dumps({'source_sha256': {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names},
                  'numpy_version': np.__version__, 'python_version': sys.version.split()[0],
                  'results': results}, indent=2, allow_nan=False))
