# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Cost probe for the P11 fixed-point deliverable (p11_fixedpoint.md section 4), not an estimator: does Fisher's
identity, grad log Z = E_post[grad log g(x)], computed on the evaluator's own quadrature nodes, reproduce the
finite-difference gradient of the collapsed log numerator on the oracle's T1 and T2 forests, and at what cost?
Coefficient derivatives are central differences of the cheap coefs() (h = 1e-6); everything else is analytic.
    uv run --python 3.12 data/q012-pilot/fisher_gradient_probe.py"""
import importlib.util
import json
import math
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.argv = sys.argv[:1]
_s = importlib.util.spec_from_file_location("p11", HERE / "p11_fixedpoint.py")
F = importlib.util.module_from_spec(_s)
_s.loader.exec_module(F)
O = F.O
IS = O.NAMES.index("sigma")
IR = O.NAMES.index("rho")
IKB = O.NAMES.index("kappa_b")
IK = O.NAMES.index("kappa")


def coef_grad(u, lins, coh, h=1e-6):
    """d(a1, ab, ak, lin, const)/du for each lineage: (n, 5, 35)."""
    out = np.zeros((len(lins), 5, len(u)))
    for j in range(len(u)):
        e = np.zeros(len(u)); e[j] = h
        cp = np.array(O.coefs(O.u_to_p(u + e), lins, coh)); cm = np.array(O.coefs(O.u_to_p(u - e), lins, coh))
        out[:, :, j] = (cp - cm) / (2 * h)
    return out


def dlogF_du(cf, dcf, x, p):
    """d log F(x)/du for all 35 coordinates at nodes x (shape x.shape + (35,))."""
    a1, ab, ak, lin, const = cf
    sig, kb, kap = p["sigma"], p["kappa_b"], p["kappa"]
    lz = x - 0.5 * sig * sig
    ea, eb, ek = np.exp(lz), np.exp(kb * lz), np.exp(kap * lz)
    g = (-ea[..., None] * dcf[0] - eb[..., None] * dcf[1] - ek[..., None] * dcf[2] + lz[..., None] * dcf[3] + dcf[4])
    g[..., IKB] += -ab * eb * lz
    g[..., IK] += -ak * ek * lz
    g[..., IS] += O.dlogF(cf, x, 0.5 * sig * sig, kb, kap) * (-sig * sig)
    return g


def fisher_T(p, forest, n_node=200, n_cond=200, delta=50.0):
    """Gradient of the log numerator of a one- or two-node forest by Fisher's identity on the evaluator's nodes."""
    nodes, coh = O.FORESTS[forest], O.COHORT[forest]
    lins = [l for l, _ in nodes]
    u = O.p_to_u(p)
    t = F.Tree(p, nodes, coh, "full", n_node, n_cond, 400, delta)
    cfs, dcf = t.cfs, coef_grad(u, lins, coh)
    sig, rho = p["sigma"], p["rho"]
    v = sig * sig * (1 - rho * rho)

    def hroot(x):
        tot = -x ** 2 / (2 * sig ** 2) - math.log(sig) - 0.5 * O.LOG2PI + O.logF(cfs[0], x, t.s2h, t.kb, t.kap)
        return tot + (t.message(1, x)[0] if len(nodes) > 1 else 0.0)
    lo, hi = O.level_bounds(hroot, np.array([t.m[0]]), np.array([t.s[0]]), delta)
    X, lw = O.sinh_simpson(n_node, t.m[0], t.s[0], lo[0], hi[0])
    a = lw + hroot(X)
    wr = np.exp(a - O.lse(a))
    groot = dlogF_du(cfs[0], dcf[0], X, p)
    groot[:, IS] += X ** 2 / sig ** 2 - 1
    grad = wr @ groot
    if len(nodes) > 1:
        xc0, sc, clo, chi = t.placement(1, X)
        Y, lwc = O.sinh_simpson(n_cond, xc0, sc, clo, chi)
        b = lwc + t.hc(1, X, Y)
        wc = np.exp(b - O.lse(b, axis=1)[:, None])
        gc = dlogF_du(cfs[1], dcf[1], Y, p)
        d = Y - rho * X[:, None]
        gc[..., IS] += d * d / v - 1
        gc[..., IR] += (d * X[:, None] / v - d * d * rho * sig * sig / v ** 2 + rho * sig * sig / v) * rho * (1 - rho)
        grad = grad + wr @ np.einsum("ab,abj->aj", wc, gc)
    return grad


def main():
    bank = F.load_bank()
    out = {}
    for name in ("central0", "stress_s3_r09_kbm15", "high_rho_9707", "c1_failing", "holdout_9707_sigma8"):
        p = bank[name]
        u = O.p_to_u(p)
        for fo in ("T1_root", "T2_pair"):
            t0 = time.perf_counter()
            gF = fisher_T(p, fo)
            tf = time.perf_counter() - t0
            t0 = time.perf_counter()
            f = lambda uu: F.Tree(O.u_to_p(uu), O.FORESTS[fo], O.COHORT[fo], "full", 200, 200, 400, 50.0).log_integral()
            _, gD = O.grad(f, u)
            td = time.perf_counter() - t0
            dif = np.abs(gF - gD)
            out[f"{name}/{fo}"] = dict(max_abs_diff=float(dif.max()), worst=O.NAMES[int(dif.argmax())],
                                       max_abs_grad=float(np.abs(gD).max()), fisher_seconds=tf, fd_seconds=td)
            print(name, fo, out[f"{name}/{fo}"], flush=True)
    (HERE / "fisher_gradient_probe.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
