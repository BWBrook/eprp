# Tranche-5 M1-M3 (declared in ../VALIDATION_T5.md): doMI.R's habitat viability against a closed form, against its own
# saved traits, and its pO2 against TEOS-10.
# Usage: python t5_mi_checks.py <doMI output .nc> <deposited fields_biogem_3d.nc> <year> <out json>
import json
import math
import sys

import gsw
import netCDF4 as nc
import numpy as np
from scipy.stats import norm

mi_file, fields_file, year, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
kB, Tref = 8.61733326e-5, 15 + 273.15
uA, sA, uC, sC, uE, sE = 3.01, 0.49, 1.10, 0.42, 0.41, 0.29

m = nc.Dataset(mi_file)
f = nc.Dataset(fields_file)
dims = m["habitat_viability"].dimensions
hv = np.ma.masked_invalid(m["habitat_viability"][:]).astype(float)
temp = np.ma.masked_invalid(m["temperature"][:]).astype(float)
po2 = np.ma.masked_invalid(m["pO2"][:]).astype(float)
units = {v: getattr(m[v], "units", "") for v in ("temperature", "pO2", "habitat_viability")}
A0, E0, phic = (np.asarray(m[v][:], float) for v in ("A0", "E0", "phi_crit"))
n = A0.size

T_K = temp + 273.15 if temp.max() < 150 else temp
po2_atm = po2 / 1000 if po2.max() > 5 else po2
cells = ~np.ma.getmaskarray(hv) & ~np.ma.getmaskarray(T_K) & ~np.ma.getmaskarray(po2_atm)
Tc, Pc, Hc = T_K.data[cells], po2_atm.data[cells], hv.data[cells] / 100

# M1: closed form
x = (1 / Tc - 1 / Tref) / kB
pos = Pc > 0
p = np.zeros_like(Pc)
p[pos] = norm.cdf((uA + np.log(Pc[pos]) + uE * x[pos] - uC) / np.sqrt(sA**2 + sC**2 + (sE * x[pos]) ** 2))
se = np.sqrt(np.maximum(p * (1 - p), 1 / n) / n)
z = (Hc - p) / se
m1 = {"cells": int(cells.sum()), "cells_with_negative_pO2": int((~pos).sum()), "n_ecotypes": n, "max_abs_z": float(np.abs(z).max()), "mean_abs_z": float(np.abs(z).mean()),
      "max_abs_diff": float(np.abs(Hc - p).max()), "pass": bool(np.abs(z).max() <= 4)}

# M2: recompute from the saved traits
phi = A0[None, :] * Pc[:, None] * np.exp((E0[None, :] / kB) * (1 / Tc[:, None] - 1 / Tref))
hv2 = (phi >= phic[None, :]).mean(axis=1) * 100
ev = np.asarray(m["ecotype_viability"][:])
assert m["ecotype_viability"].dimensions[0] == "Ecotype"
ev_cells = ev[:, cells].T
ev2 = (phi >= phic[None, :]).astype(int)
m2 = {"max_abs_diff_percent": float(np.abs(hv2 - Hc * 100).max()), "pass": bool(np.abs(hv2 - Hc * 100).max() <= 1e-9),
      "post_hoc_ecotype_viability_mismatches": int((np.nan_to_num(ev_cells, nan=-1) != ev2).sum()),
      "post_hoc_ecotype_cells": int(ev2.size)}

# M3: independent pO2 from TEOS-10 on the same cells
it = int(np.argmin(np.abs(np.asarray(f["time"][:]) - year)))
mdep = np.asarray(m["Depth"][:], float)
zt = np.asarray(f["zt"][:], float)
lev = [int(np.argmin(np.abs(zt - d))) for d in mdep]
lat_f, lon_f = np.asarray(f["lat"][:], float), np.asarray(f["lon"][:], float)
SP = np.ma.masked_invalid(f["ocn_sal"][it][lev]).astype(float)
O2 = np.ma.masked_invalid(f["ocn_O2"][it][lev]).astype(float) * 1e6
t_in = np.ma.masked_invalid(f["ocn_temp"][it][lev]).astype(float)
assert dims[-3:] == ("Depth", "lat", "lon"), dims
D = np.broadcast_to(mdep[:, None, None], SP.shape)
LAT = np.broadcast_to(lat_f[None, :, None], SP.shape)
LON = np.broadcast_to(lon_f[None, None, :], SP.shape)
pdbar = gsw.p_from_z(-D, LAT)
SA = gsw.SA_from_SP(SP.data, pdbar, LON, LAT)
pt = gsw.pt0_from_t(SA, t_in.data, pdbar)
O2sat = gsw.O2sol_SP_pt(SP.data, pt)
Tpt = pt + 273.15
ph2o = np.exp(24.4543 - 6745.09 / Tpt - 4.8489 * np.log(Tpt / 100) - 0.000544 * SP.data)
surf = O2.data / O2sat * 0.20946 * (1 - ph2o)
def corr(nu_cm3):
    return surf * np.exp(nu_cm3 * 1e-6 * pdbar * 1e4 / (8.314472 * (t_in.data + 273.15)))
indep = corr(32.0)
ok = pos & (indep[cells] > 0)
dl = np.log(Pc[ok]) - np.log(indep[cells][ok])
dl319 = np.log(Pc[ok]) - np.log(corr(31.9)[cells][ok])
within = np.zeros(int(cells.sum()), bool)
within[ok] = np.abs(dl) <= 0.02
m3 = {"cells": int(cells.sum()), "cells_excluded_nonpositive": int((~ok).sum()), "median_abs_dlog": float(np.median(np.abs(dl))),
      "max_abs_dlog": float(np.abs(dl).max()), "fraction_within_0.02": float(within.mean()), "pass": bool(within.mean() >= 0.99),
      "nu_31.9_median_abs_dlog": float(np.median(np.abs(dl319))), "nu_31.9_max_abs_dlog": float(np.abs(dl319).max()),
      "depths_m": mdep.tolist()}

res = {"units_in_output": units, "temperature_interpreted_as": "degC" if temp.max() < 150 else "K",
       "pO2_interpreted_as": "matm" if po2.max() > 5 else "atm", "pO2_range": [float(po2.min()), float(po2.max())],
       "M1": m1, "M2": m2, "M3": m3}
json.dump(res, open(out, "w"), indent=2)
print(json.dumps(res, indent=2))
