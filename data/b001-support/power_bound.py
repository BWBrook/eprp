"""Best-case discrimination bound for B-001's repeatability rho.

Balanced guilds x events, complete uncensored log delays, event fixed
effects, no clade term and no detection error. Exact F-based 90% interval
for rho (two one-sided 5% decisions). Real designs are less informative.

  uv run -q --no-project --with scipy==1.14.1 python -I data/b001-support/power_bound.py
"""

import csv
import pathlib

from scipy.stats import f

RHO0, RHO1, ALPHA = 0.1, 0.5, 0.05
OUT = pathlib.Path(__file__).resolve().parent / "power_bound.tsv"


def lam(rho, m):
    return 1 + m * rho / (1 - rho)


rows = [["events", "guilds_in_all_events", "P_lo_gt_rho0_given_rho1", "P_hi_lt_rho1_given_0",
         "P_lo_gt_rho0_given_rho0"]]
for m in (3, 5):
    for a in (4, 5, 6, 7, 8, 10, 12, 15, 16, 17, 20, 25, 30):
        d1, d2 = a - 1, (a - 1) * (m - 1)
        f_hi, f_lo = f.ppf(1 - ALPHA, d1, d2), f.ppf(ALPHA, d1, d2)
        rows.append([m, a,
                     f"{f.sf(lam(RHO0, m) * f_hi / lam(RHO1, m), d1, d2):.3f}",
                     f"{f.cdf(lam(RHO1, m) * f_lo, d1, d2):.3f}",
                     f"{f.sf(f_hi, d1, d2):.3f}"])
with OUT.open("w", newline="") as fh:
    csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(rows)
for r in rows:
    print("\t".join(map(str, r)))
