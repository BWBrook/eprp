# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Cost probe (p11_fixedpoint.md, cost addendum), not an estimator: the gradient of each P11 tree's collapsed log
numerator by Fisher's identity, carried up the tree. A message's theta-gradient G_j(x_p) = E[dlogK + dlogF_j +
sum_c G_c | x_p] on the evaluator's own conditional nodes; interior tables hold G_c with exact x-derivatives
(E[d_x f] + (rho/v) Cov(f, x_c)) for local Hermite interpolation, tangent-extended outside the table like the value
messages. Validated against the frozen batch's finite-difference per-tree gradients (p11_fixedpoint_run.jsonl).
    uv run --python 3.12 data/q012-pilot/fisher_tree.py RESULTS.jsonl"""
import importlib.util
import json
import math
import pathlib
import sys
import time

import numpy as np
from scipy.interpolate import CubicHermiteSpline

HERE = pathlib.Path(__file__).resolve().parent
ARGS = sys.argv[1:]
sys.argv = sys.argv[:1]
_s = importlib.util.spec_from_file_location("fgp", HERE / "fisher_gradient_probe.py")
FG = importlib.util.module_from_spec(_s)
_s.loader.exec_module(FG)
F, O = FG.F, FG.O
IS, IR = FG.IS, FG.IR


class FisherTree(F.Tree):
    def __init__(self, p, nodes, coh, n_node=200, n_cond=200, n_tab=400, delta=50.0):
        self.p = p
        self.dcf = FG.coef_grad(O.p_to_u(p), [l for l, _ in nodes], coh)
        self.gtab = {}
        super().__init__(p, nodes, coh, "full", n_node, n_cond, n_tab, delta)

    def build_table(self, j):
        super().build_table(j)
        X = self.tables[j]["X"]
        self.gtab[j] = {}
        for c in self.kids[j]:
            G, dG = self.message_grad(c, X)
            self.gtab[j][c] = (CubicHermiteSpline(X, G, dG, axis=0), G[0], dG[0], G[-1], dG[-1])

    def ginterp(self, j, c, x):
        s, g0, d0, g1, d1 = self.gtab[j][c]
        lo, hi = self.tables[j]["lo"], self.tables[j]["hi"]
        out = s(np.clip(x, lo, hi))
        out = out + np.where((x < lo)[..., None], d0 * (x - lo)[..., None], 0.0)
        return out + np.where((x > hi)[..., None], d1 * (x - hi)[..., None], 0.0)

    def message_grad(self, j, xp):
        """(G_j, dG_j/dx_p) at parent points xp, each (len(xp), 35)."""
        rho, v, sig = self.rho, self.v, self.sig
        x0, sc, lo, hi = self.placement(j, xp)
        X, lw = O.sinh_simpson(self.n_cond, x0, sc, lo, hi)
        a = lw + self.hc(j, xp, X)
        w = np.exp(a - O.lse(a, axis=1)[:, None])
        d = X - rho * xp[:, None]
        f = FG.dlogF_du(self.cfs[j], self.dcf[j], X, self.p)
        f[..., IS] += d * d / v - 1
        f[..., IR] += (d * xp[:, None] / v - d * d * rho * sig * sig / v ** 2 + rho * sig * sig / v) * rho * (1 - rho)
        for c in self.kids[j]:
            f = f + self.ginterp(j, c, X)
        G = np.einsum("ab,abj->aj", w, f)
        fx = np.zeros_like(f)
        fx[..., IS] = -2 * rho * d / v
        fx[..., IR] = ((d - rho * xp[:, None]) / v + 2 * rho * rho * sig * sig * d / v ** 2) * rho * (1 - rho)
        EX = np.sum(w * X, axis=1)
        cov = np.einsum("ab,abj->aj", w, f * X[..., None]) - G * EX[:, None]
        return G, np.einsum("ab,abj->aj", w, fx) + (rho / v) * cov

    def gradient(self):
        sig = self.sig

        def hroot(x):
            x = np.atleast_1d(np.asarray(x, float))
            tot = -x ** 2 / (2 * sig ** 2) - math.log(sig) - 0.5 * O.LOG2PI + O.logF(self.cfs[0], x, self.s2h, self.kb, self.kap)
            for c in self.kids[0]:
                tot = tot + self.message(c, x)[0]
            return tot
        lo, hi = O.level_bounds(hroot, np.array([self.m[0]]), np.array([self.s[0]]), self.delta)
        self.check_coverage(lo[0], hi[0])
        X, lw = O.sinh_simpson(self.n_node, self.m[0], self.s[0], lo[0], hi[0])
        a = lw + hroot(X)
        w = np.exp(a - O.lse(a))
        f = FG.dlogF_du(self.cfs[0], self.dcf[0], X, self.p)
        f[:, IS] += X ** 2 / sig ** 2 - 1
        for c in self.kids[0]:
            f = f + self.message_grad(c, X)[0]
        return float(O.lse(a)), w @ f


def main():
    recs = {}
    for l in pathlib.Path(ARGS[0]).read_text().splitlines():
        r = json.loads(l)
        if r["kind"] == "cand" and r["arg"] == "primary" and "unresolved" not in r:
            recs[r["point"]] = r
    bank = F.load_bank()
    out = {}
    for name, r in recs.items():
        p = bank[name]
        row = {}
        for k, nodes in F.TREES.items():
            t0 = time.perf_counter()
            v, g = FisherTree(p, nodes, F.COH).gradient()
            sec = time.perf_counter() - t0
            gd = np.array(r["grad"][k])
            row[k] = dict(value_minus_batch=abs(v - r["per_tree"][k]), max_abs_grad_diff=float(np.max(np.abs(g - gd))),
                          worst=O.NAMES[int(np.argmax(np.abs(g - gd)))], max_abs_grad=float(np.max(np.abs(gd))), fisher_seconds=sec)
        tot = sum(x["fisher_seconds"] for x in row.values())
        out[name] = dict(trees=row, fisher_seconds_total=tot, fd_gradient_seconds_batch=r["gradient_seconds"],
                         max_abs_grad_diff=max(x["max_abs_grad_diff"] for x in row.values()))
        print(name, f"max |Fisher - FD| {out[name]['max_abs_grad_diff']:.2e}",
              {k: f"{x['max_abs_grad_diff']:.1e}" for k, x in row.items() if len(k) > 2},
              f"Fisher {tot:.1f} s vs FD {r['gradient_seconds']:.0f} s (mac-mini, loaded)", flush=True)
    (HERE / "fisher_tree_check.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
