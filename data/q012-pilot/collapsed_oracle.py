# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 collapsed-likelihood oracle (collapsed_oracle.md, frozen at ad09251): one evaluator of
[integral p_theta(x) prod F_i(x_i) dx] / pi(theta) on three tiny forests, against an independent tensor-product
reference. No fit, optimiser over theta, bootstrap, HMC or cluster use.
    uv run --python 3.12 data/q012-pilot/collapsed_oracle.py      (writes collapsed_oracle_results.json)"""
import importlib.util
import json
import math
import multiprocessing as mp
import pathlib
import resource
import sys
import time

import numpy as np
from scipy import integrate, optimize

HERE = pathlib.Path(__file__).resolve().parent
sys.argv = sys.argv[:1]
_spec = importlib.util.spec_from_file_location("pilot", HERE / "pilot.py")
pilot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pilot)
P = pilot.P
D = json.loads((HERE / "payload_v6q80t" / "data" / "P11.json").read_text())
N = D["N"]
NAMES = pilot.param_names(N)[:35]
LOG2PI = math.log(2 * math.pi)
FORESTS = {"T1_root": [(1, None)], "T2_pair": [(2, None), (5, 0)], "T3_root_two_daughters": [(2, None), (5, 0), (7, 0)]}
COHORT = {"T1_root": {1}, "T2_pair": {2, 5}, "T3_root_two_daughters": {2, 5}}
SEL = {"T1_root": ("single", 1), "T2_pair": ("pair", 2, 5), "T3_root_two_daughters": ("pair", 2, 5)}


# ---------------------------------------------------------------- parameters
def p_to_u(p):
    return np.array([p["log_h0_1"]] + list(p["z_rw"]) + [math.log(p["tau"]), p["log_k"], p["log_lambda0"], p["kappa"],
                                                         p["log_b0"], p["kappa_b"], p["beta"], p["gamma"],
                                                         math.log(p["sigma"]), math.log(p["rho"]) - math.log1p(-p["rho"])])


def u_to_p(u):
    v = dict(zip(NAMES, (float(x) for x in u)))
    return dict(log_h0_1=v["log_h0_1"], z_rw=[v[f"z_rw.{j}"] for j in range(1, 25)], tau=math.exp(v["tau"]),
                **{k: v[k] for k in ("log_k", "log_lambda0", "kappa", "log_b0", "kappa_b", "beta", "gamma")},
                sigma=math.exp(v["sigma"]), rho=0.5 * (1 + math.tanh(0.5 * v["rho"])))


def coefs(p, lineages, coh, mode="full"):
    """Per-lineage (a1, ab, ak, lin, const): log F(x) = -a1 e^lz - ab e^(kb lz) - ak e^(kappa lz) + lin lz + const."""
    k, h = math.exp(p["log_k"]), P.log_h0_of(p)
    b0, lam0 = math.exp(p["log_b0"]), math.exp(p["log_lambda0"])
    cum = np.zeros(N)
    for s in range(D["S"]):
        cum[D["seg_lin"][s] - 1] += math.exp(h[D["seg_bin"][s] - 1] + p["beta"] * D["seg_E"][s] + p["gamma"] * D["seg_miss"][s]) \
            * (D["seg_a1"][s] ** k - D["seg_a0"][s] ** k)
    A = P.cohort_A(D, p)
    out = []
    for lin in lineages:
        i = lin - 1
        c = lin in coh
        if mode == "unit":
            out.append((0.0, 0.0, 0.0, 0.0, 0.0))
        elif mode == "selection":
            out.append((A[i] if c else 0.0, b0 * (D["c"] - D["o"][i]) if c else 0.0, 0.0, 0.0, 0.0))
        else:
            dpost = D["v"][i] - D["r"][i]
            ext, bif, mp_ = D["ext"][i], D["bif"][i], D["mplus"][i]
            const = (ext * (h[D["term_bin"][i] - 1] + p["log_k"] + (k - 1) * math.log(D["term_a"][i]) + p["beta"] * D["term_E"][i]
                            + p["gamma"] * D["term_miss"][i]) if ext else 0.0) + bif * p["log_b0"] + mp_ * p["log_lambda0"]
            out.append((cum[i] + (A[i] if c else 0.0), b0 * (dpost + ((D["c"] - D["o"][i]) if c else 0.0)), lam0 * dpost,
                        ext + p["kappa_b"] * bif + p["kappa"] * mp_, const))
    return out


def logF(cf, x, s2h, kb, kap):
    a1, ab, ak, lin, const = cf
    lz = x - s2h
    return -a1 * np.exp(lz) - ab * np.exp(kb * lz) - ak * np.exp(kap * lz) + lin * lz + const


def dlogF(cf, x, s2h, kb, kap):
    a1, ab, ak, lin, _ = cf
    lz = x - s2h
    return -a1 * np.exp(lz) - ab * kb * np.exp(kb * lz) - ak * kap * np.exp(kap * lz) + lin


def d2logF(cf, x, s2h, kb, kap):
    a1, ab, ak, _, _ = cf
    lz = x - s2h
    return -a1 * np.exp(lz) - ab * kb * kb * np.exp(kb * lz) - ak * kap * kap * np.exp(kap * lz)


def simpson_ab(n, a, b):
    """Simpson nodes on [a, b] (a and b may be arrays; nodes along a new last axis) and their log weights."""
    t = np.linspace(0.0, 1.0, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2], w[2:-1:2] = 4, 2
    a, b = np.asarray(a, float), np.asarray(b, float)
    X = a[..., None] + (b - a)[..., None] * t
    return X, np.log(w) + np.log((b - a) / (3 * n))[..., None]


def sinh_simpson(n, c, sc, lo, hi):
    """Repair 1b: Simpson in u with x = c + sc sinh(u) over [asinh((lo - c)/sc), asinh((hi - c)/sc)]; nodes dense near c,
    sparse in the tails. Arrays broadcast over leading axes; returns nodes and log weights including the Jacobian."""
    c, sc = np.asarray(c, float), np.asarray(sc, float)
    ua, ub = np.arcsinh((np.asarray(lo, float) - c) / sc), np.arcsinh((np.asarray(hi, float) - c) / sc)
    U, lw = simpson_ab(n, ua, ub)
    return c[..., None] + sc[..., None] * np.sinh(U), lw + np.log(sc[..., None] * np.cosh(U))


def level_bounds(h, m, s, delta):
    """Repair 1: [lo, hi] where the concave h falls delta nats below h(m) on each side, found by doubling steps out from
    m (initial step s) and 80 bisections; vectorised over m and s. Non-finite h counts as below the level."""
    m, s = np.asarray(m, float), np.asarray(s, float)
    level = h(m) - delta
    bounds = []
    for sgn in (-1.0, 1.0):
        step, inside = s.copy(), m.copy()
        for _ in range(200):
            below = ~(h(m + sgn * step) >= level)
            if np.all(below):
                break
            inside = np.where(below, inside, m + sgn * step)
            step = np.where(below, step, 2 * step)
        else:
            raise Unresolved("level set not bracketed in 200 doublings")
        a, b = inside, m + sgn * step
        for _ in range(80):
            mid = 0.5 * (a + b)
            below = ~(h(mid) >= level)
            b, a = np.where(below, mid, b), np.where(below, a, mid)
        bounds.append(b)
    return bounds[0], bounds[1]


def lse(a, axis=None):
    m = np.max(a, axis=axis, keepdims=True)
    return np.squeeze(m, axis=axis) + np.log(np.sum(np.exp(a - m), axis=axis))


class Unresolved(Exception):
    pass


# ---------------------------------------------------------------- evaluator (candidate)
def forest_precision(par, sig, rho):
    n = len(par)
    Lam = np.zeros((n, n))
    v = sig * sig * (1 - rho * rho)
    for i, pa in enumerate(par):
        if pa is None:
            Lam[i, i] += 1 / sig ** 2
        else:
            Lam[i, i] += 1 / v
            Lam[pa, pa] += rho * rho / v
            Lam[i, pa] -= rho / v
            Lam[pa, i] -= rho / v
    return Lam


def joint_mode(par, cfs, sig, rho, kb, kap):
    s2h = 0.5 * sig * sig
    Lam = forest_precision(par, sig, rho)
    x = np.zeros(len(par))
    obj = lambda z: -0.5 * float(z @ Lam @ z) + sum(float(logF(c, zi, s2h, kb, kap)) for c, zi in zip(cfs, z))
    for _ in range(200):
        g = -Lam @ x + np.array([dlogF(c, xi, s2h, kb, kap) for c, xi in zip(cfs, x)])
        H = Lam - np.diag([d2logF(c, xi, s2h, kb, kap) for c, xi in zip(cfs, x)])
        if not (np.all(np.isfinite(g)) and np.all(np.isfinite(H))):
            raise Unresolved("non-finite joint gradient or curvature")
        try:
            dl = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            raise Unresolved("singular joint curvature")
        dec2 = float(g @ dl)
        if not (math.isfinite(dec2) and np.all(np.isfinite(dl))) or dec2 < 0:
            raise Unresolved("invalid joint Newton step or decrement")
        if np.max(np.abs(dl)) < 1e-14 or dec2 <= 1e-20:
            x = x + dl
            break
        t, f0 = 1.0, obj(x)
        for _ in range(60):                     # Repair 2: Armijo backtracking, full steps once dec2 <= 1e-8
            f1 = obj(x + t * dl)
            if dec2 <= 1e-8 or (math.isfinite(f1) and f1 >= f0 + 1e-4 * t * dec2):
                break
            t *= 0.5
        else:
            raise Unresolved("joint line search failed")
        x = x + t * dl
    else:
        raise Unresolved("joint mode not converged in 200 iterations")
    H = Lam - np.diag([d2logF(c, xi, s2h, kb, kap) for c, xi in zip(cfs, x)])
    try:
        np.linalg.cholesky(H)
    except np.linalg.LinAlgError:
        raise Unresolved("joint curvature not positive definite")
    return x, np.sqrt(np.diag(np.linalg.inv(H)))


def leaf_message(cf, xp, sig, rho, kb, kap, n, delta):
    """log of integral K(x | xp) F(x) dx for each parent point, on conditional level-set grids (Repair 1)."""
    s2h, v = 0.5 * sig * sig, sig * sig * (1 - rho * rho)
    hobj = lambda z: -(z - rho * xp) ** 2 / (2 * v) + logF(cf, z, s2h, kb, kap)
    x = rho * xp
    for _ in range(200):
        g = -(x - rho * xp) / v + dlogF(cf, x, s2h, kb, kap)
        h2 = -1 / v + d2logF(cf, x, s2h, kb, kap)
        if not (np.all(np.isfinite(g)) and np.all(np.isfinite(h2))) or np.any(h2 >= 0):
            raise Unresolved("invalid conditional curvature")
        step = -g / h2
        dec2 = -g * g / h2
        done = (np.abs(step) < 1e-14) | (dec2 <= 1e-20)
        t, f0 = np.ones_like(x), hobj(x)
        for _ in range(60):                     # Repair 2: per-element Armijo backtracking
            f1 = hobj(x + t * step)
            ok = done | (dec2 <= 1e-8) | (np.isfinite(f1) & (f1 >= f0 + 1e-4 * t * dec2))
            if np.all(ok):
                break
            t = np.where(ok, t, 0.5 * t)
        else:
            raise Unresolved("conditional line search failed")
        x = x + np.where(done, 1.0, t) * step
        if np.all(done):
            break
    else:
        raise Unresolved("conditional mode not converged in 200 iterations")
    sc = 1 / np.sqrt(-(-1 / v + d2logF(cf, x, s2h, kb, kap)))

    def hc(X):
        c = xp if X.ndim == 1 else xp[:, None]
        return -(X - rho * c) ** 2 / (2 * v) - 0.5 * (LOG2PI + math.log(v)) + logF(cf, X, s2h, kb, kap)
    lo, hi = level_bounds(hc, x, sc, delta)
    X, lw = sinh_simpson(n, x, sc, lo, hi)
    return lse(lw + hc(X), axis=1)


def evaluator(p, forest, mode="full", n_node=200, n_cond=200, delta=50.0):
    nodes = FORESTS[forest]
    par = [pa for _, pa in nodes]
    if any(pa is not None and par[pa] is not None for pa in par):
        raise NotImplementedError("interior nodes (interpolated messages) are outside the frozen oracle")
    cfs = coefs(p, [lin for lin, _ in nodes], COHORT[forest], mode)
    sig, rho, kb, kap = p["sigma"], p["rho"], p["kappa_b"], p["kappa"]
    m, s = joint_mode(par, cfs, sig, rho, kb, kap)
    s2h = 0.5 * sig * sig

    def hroot(x):
        x = np.atleast_1d(np.asarray(x, float))
        tot = -x ** 2 / (2 * sig ** 2) - math.log(sig) - 0.5 * LOG2PI + logF(cfs[0], x, s2h, kb, kap)
        for j in range(1, len(nodes)):
            tot = tot + leaf_message(cfs[j], x, sig, rho, kb, kap, n_cond, delta)
        return tot
    lo, hi = level_bounds(hroot, np.array([m[0]]), np.array([s[0]]), delta)
    X, lw = sinh_simpson(n_node, m[0], s[0], lo[0], hi[0])
    return float(lse(lw + hroot(X)))


# ---------------------------------------------------------------- reference (independent)
def e_logint(E, p, forest, cfs):
    """log integrand in standardised innovations, vectorised over the leading axis of E (shape [..., d])."""
    sig, rho, kb, kap = p["sigma"], p["rho"], p["kappa_b"], p["kappa"]
    s2h, sc = 0.5 * sig * sig, sig * math.sqrt(1 - rho * rho)
    par = [pa for _, pa in FORESTS[forest]]
    X = []
    for i, pa in enumerate(par):
        X.append(sig * E[..., i] if pa is None else rho * X[pa] + sc * E[..., i])
    out = -0.5 * np.sum(E * E, axis=-1) - 0.5 * len(par) * LOG2PI
    for i, x in enumerate(X):
        out = out + logF(cfs[i], x, s2h, kb, kap)
    return out


def ref_box(p, forest, mode, delta):
    """Repair 1: per-axis Delta-level sets of the joint log integrand's axis profiles through its mode, in innovation
    coordinates; fixed at the base theta during differencing."""
    cfs = coefs(p, [lin for lin, _ in FORESTS[forest]], COHORT[forest], mode)
    d = len(FORESTS[forest])
    f = lambda e: -float(e_logint(np.asarray(e)[None, :], p, forest, cfs)[0])
    r = optimize.minimize(f, np.zeros(d), method="BFGS", options=dict(gtol=1e-10, maxiter=10000))
    mu, hstep = r.x, 1e-4
    Hm = np.zeros((d, d))
    for a in range(d):
        for b in range(d):
            ea, eb = np.eye(d)[a] * hstep, np.eye(d)[b] * hstep
            Hm[a, b] = (f(mu + ea + eb) - f(mu + ea - eb) - f(mu - ea + eb) + f(mu - ea - eb)) / (4 * hstep * hstep)
    try:
        sd = np.sqrt(np.diag(np.linalg.inv(Hm)))
    except np.linalg.LinAlgError:
        raise Unresolved("reference box: singular numerical Hessian")
    if not np.all(np.isfinite(sd)):
        raise Unresolved("reference box: non-finite scales")
    lo, hi = np.zeros(d), np.zeros(d)
    for a in range(d):
        prof = lambda T, a=a: e_logint(mu[None, :] + np.outer(np.atleast_1d(T), np.eye(d)[a]), p, forest, cfs)
        l, h = level_bounds(prof, np.array([0.0]), np.array([sd[a]]), delta)
        lo[a], hi[a] = mu[a] + l[0], mu[a] + h[0]
    return mu, sd, lo, hi


def reference(p, forest, box, mode="full", n=200):
    cfs = coefs(p, [lin for lin, _ in FORESTS[forest]], COHORT[forest], mode)
    mu, sd, lo, hi = box
    d = len(FORESTS[forest])
    ax = [sinh_simpson(n, mu[i], sd[i], lo[i], hi[i]) for i in range(d)]
    if d == 1:
        return float(lse(ax[0][1] + e_logint(ax[0][0][:, None], p, forest, cfs)))
    if d == 2:
        E = np.stack(np.meshgrid(ax[0][0], ax[1][0], indexing="ij"), axis=-1)
        return float(lse(ax[0][1][:, None] + ax[1][1][None, :] + e_logint(E, p, forest, cfs)))
    parts = []
    E12 = np.stack(np.meshgrid(ax[1][0], ax[2][0], indexing="ij"), axis=-1)
    W12 = ax[1][1][:, None] + ax[2][1][None, :]
    for a, la in zip(ax[0][0], ax[0][1]):
        E = np.concatenate([np.full(E12.shape[:2] + (1,), a), E12], axis=-1)
        parts.append(la + float(lse(W12 + e_logint(E, p, forest, cfs))))
    return float(lse(np.array(parts)))


def quad_reference(p, forest, mode="full"):
    """Second reference for T1 and T2: adaptive Gauss-Kronrod in x, values only."""
    nodes = FORESTS[forest]
    cfs = coefs(p, [lin for lin, _ in nodes], COHORT[forest], mode)
    sig, rho, kb, kap = p["sigma"], p["rho"], p["kappa_b"], p["kappa"]
    s2h, v = 0.5 * sig * sig, sig * sig * (1 - rho * rho)
    m, s = joint_mode([pa for _, pa in nodes], cfs, sig, rho, kb, kap)
    lr = lambda x: -x * x / (2 * sig * sig) - math.log(sig) - 0.5 * LOG2PI + logF(cfs[0], x, s2h, kb, kap)
    lo, hi = level_bounds(lambda x: np.asarray(lr(x)), np.array([m[0]]), np.array([s[0]]), 50.0)
    if len(nodes) == 1:
        g0 = lr(m[0])
        val, _ = integrate.quad(lambda x: math.exp(lr(x) - g0), lo[0], hi[0], points=[m[0]],
                                epsabs=0, epsrel=1e-12, limit=500)
        return g0 + math.log(val)
    g0 = lr(m[0]) - 0.5 * (LOG2PI + math.log(v)) + logF(cfs[1], m[1], s2h, kb, kap)

    def inner(xp):
        ld = lambda x: -(x - rho * xp) ** 2 / (2 * v) - 0.5 * (LOG2PI + math.log(v)) + logF(cfs[1], x, s2h, kb, kap)
        cm = rho * xp
        a, b = level_bounds(lambda x: np.asarray(ld(x)), np.array([cm]), np.array([math.sqrt(v)]), 60.0)
        val, _ = integrate.quad(lambda x: math.exp(lr(xp) + ld(x) - g0), min(a[0], m[1]), max(b[0], m[1]),
                                points=[m[1], cm], epsabs=0, epsrel=1e-12, limit=500)
        return val
    val, _ = integrate.quad(inner, lo[0], hi[0], points=[m[0]], epsabs=0, epsrel=1e-12, limit=500)
    return g0 + math.log(val)


# ---------------------------------------------------------------- selection normaliser as Stan computes it (Q80 AGH)
def log_pi_q80(p, forest):
    t, w = np.array(D["gh_t"]), np.array(D["gh_w"])
    A = P.cohort_A(D, p)
    b0 = math.exp(p["log_b0"])
    sel = SEL[forest]
    if sel[0] == "single":
        i = sel[1] - 1
        return float(P.QD.log_pi_1d(p["sigma"], A[i], b0 * (D["c"] - D["o"][i]), p["kappa_b"], t, w))
    a, b = sel[1] - 1, sel[2] - 1
    return float(P.QD.log_pi_2d(p["sigma"], p["rho"], A[a], b0 * (D["c"] - D["o"][a]), A[b], b0 * (D["c"] - D["o"][b]),
                                p["kappa_b"], t, w))


# ---------------------------------------------------------------- factor decomposition against python_target
def priors(p):
    lp = -0.5 * (p["log_h0_1"] - math.log(0.065)) ** 2 - 0.5 * float(np.sum(np.array(p["z_rw"]) ** 2))
    lp += -0.5 * (p["tau"] / 0.5) ** 2 - 0.5 * (p["log_k"] / 0.5) ** 2 - 0.5 * (p["log_lambda0"] - math.log(0.0708)) ** 2
    lp += -0.5 * p["kappa"] ** 2 - 0.5 * (p["log_b0"] - math.log(0.0082)) ** 2 - 0.5 * p["kappa_b"] ** 2
    lp += -0.5 * p["beta"] ** 2 - 0.5 * p["gamma"] ** 2 - 0.5 * p["sigma"] ** 2
    return lp


def decomposition_check(pe):
    _, x, A = P.pieces(D, pe)
    cfs = coefs(pe, list(range(1, N + 1)), set(D["coh"]), "full")
    s2h = 0.5 * pe["sigma"] ** 2
    mine = priors(pe) - 0.5 * float(np.sum(np.array(pe["eps"]) ** 2)) \
        + sum(float(logF(c, xi, s2h, pe["kappa_b"], pe["kappa"])) for c, xi in zip(cfs, x)) - P.log_norm_agh(D, pe, A)
    return abs(mine - P.python_target(D, pe))


# ---------------------------------------------------------------- point set (frozen in collapsed_oracle.md section 3)
def points():
    sp = P.stress_points(D)
    c0 = sp["central0"]
    pts = {"central0": c0, "central1": sp["central1"], "stress_s3_r09_kbm15": sp["stress_s3_r09_kbm15"],
           "low_rho": dict(c0, rho=0.05), "small_sigma": dict(c0, sigma=0.05)}
    import pandas as pd
    df = pd.read_csv(HERE.parents[1] / "scratch/q012-pilot/fetch-20261018-v6p2/runs/P11/attempt1/chain2.csv", comment="#")
    pts["high_rho_9707"] = P.draw_to_params(df.iloc[1707], N)
    att = HERE.parents[1] / "scratch/q012-pilot/fetch-20261021-v6q80t/runs/P11/attempt1"
    for ch, tr in ((1, 2779), (4, 2843)):
        for ln in (att / f"chain{ch}.trace.jsonl").read_text().splitlines():
            r = json.loads(ln)
            if r.get("type") == "divergence" and r["transition"] == tr:
                for k in ("previous", "failing"):
                    pts[f"c{ch}_{k}"] = pilot.constrain(r[k]["q"], N)
    # Repair 1 hold-outs, declared before run 2 and not used to design the repair.
    pts["holdout_c1f_sigma6"] = dict(pts["c1_failing"], sigma=6.0)
    pts["holdout_c1f_sigma20"] = dict(pts["c1_failing"], sigma=20.0)
    pts["holdout_9707_sigma8"] = dict(pts["high_rho_9707"], sigma=8.0)
    # Fresh hold-outs added with Repairs 1b and 2 (349dd3d); not looked at before run 2.
    pts["holdout_c4f_sigma15"] = dict(pts["c4_failing"], sigma=15.0)
    pts["holdout_9707_sigma5"] = dict(pts["high_rho_9707"], sigma=5.0)
    return pts


# ---------------------------------------------------------------- per-point task
H_FD = 1e-4
TOL = dict(value=1e-4, deriv=1e-3, self_value=1e-6, self_deriv=1e-5, unit=1e-8, selection=1e-6, decomposition=1e-9)


def grad(fun, u):
    g = np.zeros(len(u))
    base = fun(u)
    for j in range(len(u)):
        e = np.zeros(len(u)); e[j] = H_FD
        g[j] = (fun(u + e) - fun(u - e)) / (2 * H_FD)
    return base, g


def task(args):
    name, pe, forest = args
    out = dict(point=name, forest=forest, sigma=pe["sigma"], rho=pe["rho"], kappa_b=pe["kappa_b"])
    u0 = p_to_u(pe)
    try:
        # identities
        out["I1_unit_log_numerator"] = max(abs(evaluator(pe, forest, "unit", *s)) for s in ((200, 200, 50.0), (400, 400, 50.0)))
        box_sel = ref_box(pe, forest, "selection", 50.0)
        sel_ref = reference(pe, forest, box_sel, "selection", 400)
        out["I2_selection_minus_ref"] = evaluator(pe, forest, "selection") - sel_ref
        out["I2_selection_minus_q80"] = evaluator(pe, forest, "selection") - log_pi_q80(pe, forest)
        out["log_pi_q80"] = log_pi_q80(pe, forest)
        # evaluator: primary, resolution, domain; values and 35 derivatives; timing
        ev = {}
        for key, s in (("primary", (200, 200, 50.0)), ("resolution", (400, 400, 50.0)), ("domain", (200, 200, 70.0))):
            t0 = time.perf_counter()
            v = evaluator(pe, forest, "full", *s)
            ev[key + "_seconds"] = time.perf_counter() - t0
            ev[key] = grad(lambda u: evaluator(u_to_p(u), forest, "full", *s), u0)
        # reference: box at base theta, fixed during differencing
        boxes = {50: ref_box(pe, forest, "full", 50.0), 70: ref_box(pe, forest, "full", 70.0)}
        out["reference_box_delta50"] = [list(map(float, boxes[50][2])), list(map(float, boxes[50][3]))]
        rf = {}
        for key, (n, dl) in (("n200_L10", (200, 50)), ("n400_L10", (400, 50)), ("n400_L14", (400, 70))):
            t0 = time.perf_counter()
            reference(pe, forest, boxes[dl], "full", n)
            rf[key + "_seconds"] = time.perf_counter() - t0
            rf[key] = grad(lambda u: reference(u_to_p(u), forest, boxes[dl], "full", n), u0)
        pv, pg = ev["primary"]
        res = {}
        res["eval_self_resolution"] = (abs(ev["resolution"][0] - pv), float(np.max(np.abs(ev["resolution"][1] - pg))))
        res["eval_self_domain"] = (abs(ev["domain"][0] - pv), float(np.max(np.abs(ev["domain"][1] - pg))))
        rv, rg = rf["n400_L10"]
        res["ref_resolution"] = (abs(rf["n200_L10"][0] - rv), float(np.max(np.abs(rf["n200_L10"][1] - rg))))
        res["ref_domain"] = (abs(rf["n400_L14"][0] - rv), float(np.max(np.abs(rf["n400_L14"][1] - rg))))
        res["eval_vs_ref"] = (abs(pv - rv), float(np.max(np.abs(pg - rg))))
        jw = int(np.argmax(np.abs(pg - rg)))
        out.update(log_numerator_eval=pv, log_numerator_ref=rv, log_likelihood_collapsed=pv - out["log_pi_q80"],
                   worst_derivative_coordinate=NAMES[jw], derivative_eval_at_worst=float(pg[jw]), derivative_ref_at_worst=float(rg[jw]),
                   checks={k: dict(value=float(a), deriv=float(b)) for k, (a, b) in res.items()},
                   seconds=dict(evaluator={k: v for k, v in ev.items() if k.endswith("_seconds")},
                                reference={k: v for k, v in rf.items() if k.endswith("_seconds")}))
        if forest != "T3_root_two_daughters":
            out["quad_reference_minus_ref"] = quad_reference(pe, forest) - rv
        ref_ok = res["ref_resolution"][0] <= TOL["self_value"] and res["ref_resolution"][1] <= TOL["self_deriv"] \
            and res["ref_domain"][0] <= TOL["self_value"] and res["ref_domain"][1] <= TOL["self_deriv"]
        ev_ok = res["eval_self_resolution"][0] <= TOL["self_value"] and res["eval_self_resolution"][1] <= TOL["self_deriv"] \
            and res["eval_self_domain"][0] <= TOL["self_value"] and res["eval_self_domain"][1] <= TOL["self_deriv"]
        acc_ok = res["eval_vs_ref"][0] <= TOL["value"] and res["eval_vs_ref"][1] <= TOL["deriv"]
        ident_ok = out["I1_unit_log_numerator"] <= TOL["unit"] and abs(out["I2_selection_minus_ref"]) <= TOL["selection"]
        out.update(reference_qualified=bool(ref_ok), evaluator_converged=bool(ev_ok), accuracy_pass=bool(acc_ok),
                   identities_pass=bool(ident_ok),
                   status="pass" if (ref_ok and ev_ok and acc_ok and ident_ok) else
                   ("unresolved (reference not qualified)" if not ref_ok and ev_ok and ident_ok else "fail"))
    except Unresolved as e:
        out.update(status="unresolved", reason=str(e))
    out["maxrss_kb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return out


def main():
    t0 = time.time()
    pts = points()
    dec = {k: decomposition_check(v) for k, v in pts.items()}
    jobs = [(k, {kk: vv for kk, vv in v.items()}, f) for k, v in pts.items() for f in FORESTS]
    with mp.get_context("fork").Pool(pilot.workers(len(jobs))) as pool:
        rows = pool.map(task, jobs, chunksize=1)
    edges = sum(1 for pa in D["parent"] if pa)
    out = dict(spec="collapsed_oracle.md (ad09251) with Repairs 1, 1b and 2 (9ebc27c, 349dd3d); keys n200_L10/n400_L10/n400_L14 mean n=200/400 at Delta 50 and n=400 at Delta 70", tolerances=TOL, fd_step=H_FD, points={k: dict(sigma=v["sigma"], rho=v["rho"],
               kappa_b=v["kappa_b"]) for k, v in pts.items()},
               decomposition_abs_err=dec, decomposition_pass=bool(all(v <= TOL["decomposition"] for v in dec.values())),
               rows=rows, all_pass=bool(all(r["status"] == "pass" for r in rows)),
               status_counts={s: sum(r["status"] == s for r in rows) for s in sorted({r["status"] for r in rows})},
               p11_nominal=dict(nodes=N, edges=edges, roots=N - edges,
                                kernel_evaluations_per_call_primary=edges * 201 * 201 + (N - edges) * 201,
                                note="arithmetic count for leaf-type contractions; interior interpolation not included"),
               wall_seconds=time.time() - t0)
    (HERE / "collapsed_oracle_results_run2.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1, default=float))
    for r in rows:
        print(r["point"], r["forest"], r["status"], {k: r.get(k) for k in ("checks",)} if r["status"] != "pass" else "",
              r.get("reason", ""))


if __name__ == "__main__":
    main()
