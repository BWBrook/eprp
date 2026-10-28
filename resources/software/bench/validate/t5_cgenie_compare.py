# Tranche-5 C2/C3 (declared in ../VALIDATION_T5.md): a cGENIE run's BIOGEM 3-D fields against the deposited output.
# Usage: python3 t5_cgenie_compare.py <run fields_biogem_3d.nc> <deposited fields_biogem_3d.nc> <out json>
import json
import sys

import netCDF4 as nc
import numpy as np

run, dep, out = sys.argv[1:4]
a, b = nc.Dataset(run), nc.Dataset(dep)
dz = np.abs(np.diff(np.asarray(b["zt_edges"][:])))
vol = dz[:, None, None] * np.asarray(b["grid_area"][:])[None, :, :]
scale = {"ocn_temp": 1.0, "ocn_O2": 1e6}
units = {v: getattr(b[v], "units", "") for v in scale}

slices = []
for ib, t in enumerate(np.asarray(b["time"][:])):
    ia = np.flatnonzero(np.abs(np.asarray(a["time"][:]) - t) < 1e-6)
    if ia.size == 0:
        continue
    row = {"time": float(t)}
    for v, k in scale.items():
        fa = np.ma.masked_invalid(np.ma.asarray(a[v][ia[0]], dtype=float)) * k
        fb = np.ma.masked_invalid(np.ma.asarray(b[v][ib], dtype=float)) * k
        wet = ~np.ma.getmaskarray(fa) & ~np.ma.getmaskarray(fb)
        w = vol * wet
        ma, mb = float((fa.filled(0) * w).sum() / w.sum()), float((fb.filled(0) * w).sum() / w.sum())
        row[v] = {"run_mean": ma, "deposit_mean": mb, "diff": ma - mb,
                  "r": float(np.corrcoef(fa.data[wet], fb.data[wet])[0, 1]),
                  "max_abs_diff": float(np.abs(fa.data[wet] - fb.data[wet]).max()),
                  "identical": bool(np.array_equal(fa.filled(np.nan), fb.filled(np.nan), equal_nan=True)),
                  "wet_cells": int(wet.sum()),
                  "mask_mismatch": int((np.ma.getmaskarray(fa) != np.ma.getmaskarray(fb)).sum())}
    graded = bool(t > 100)
    row["graded"] = graded
    if graded:
        row["pass"] = bool(abs(row["ocn_temp"]["diff"]) <= 0.05 and abs(row["ocn_O2"]["diff"]) <= 1.0
                       and row["ocn_temp"]["r"] >= 0.99 and row["ocn_O2"]["r"] >= 0.99)
    slices.append(row)

graded = [s for s in slices if s["graded"]]
required_times = [float(t) for t in np.asarray(b["time"][:]) if t > 100]
ungraded_times = [float(t) for t in np.asarray(b["time"][:]) if t <= 100]
compared_times = {s["time"] for s in slices}
missing_required = [t for t in required_times if t not in compared_times]
missing_ungraded = [t for t in ungraded_times if t not in compared_times]
res = {"run": run, "units": units, "slices": slices, "slices_compared": len(slices),
       "slices_expected": int(b["time"].size), "pass_so_far": all(s["pass"] for s in graded) if graded else None,
       "graded_slices_expected": len(required_times), "graded_slices_compared": len(graded),
       "missing_graded_times": missing_required, "missing_ungraded_times": missing_ungraded,
       "complete": bool(required_times) and not missing_required, "ungraded_complete": not missing_ungraded}
json.dump(res, open(out, "w"), indent=2)
for s in slices:
    print("%8.1f  dT %+.4f  r_T %.5f  dO2 %+.3f  r_O2 %.5f  %s" % (s["time"], s["ocn_temp"]["diff"], s["ocn_temp"]["r"],
          s["ocn_O2"]["diff"], s["ocn_O2"]["r"], ("pass" if s.get("pass") else "FAIL") if s["graded"] else "(ungraded)"))
