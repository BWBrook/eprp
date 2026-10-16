"""Q-012 cohort normaliser: adaptive Gauss-Hermite (AGH) and a dense Simpson reference.

The log integrand for one cohort lineage, with log S(x) = -A exp(x - s2h) - B exp(kb (x - s2h)),
s2h = sigma^2 / 2 and B = b0 (c - o), is jointly concave in the cohort frailties, so Newton
iterations from zero find a unique mode. AGH centres and scales the Gauss-Hermite nodes at that
mode (1-D), or at the joint mode with the Cholesky factor of the inverse negative Hessian (2-D).
This module mirrors the Stan functions exactly; `reference_*` are independent dense Simpson
integrals over standard-normal innovations, used only for the precision gate.
"""

import math

import numpy as np

NEWTON_ITERS = 50


def _logS(x, sig, A, B, kb):
    s2h = 0.5 * sig * sig
    return -A * np.exp(x - s2h) - B * np.exp(kb * (x - s2h))


def log_pi_1d(sig, A, B, kb, t, w):
    s2h = 0.5 * sig * sig
    m = 0.0
    for _ in range(NEWTON_ITERS):
        e1, e2 = A * math.exp(m - s2h), B * math.exp(kb * (m - s2h))
        g1 = -m / sig ** 2 - e1 - kb * e2
        g2 = -1 / sig ** 2 - e1 - kb * kb * e2
        m -= g1 / g2
    e1, e2 = A * math.exp(m - s2h), B * math.exp(kb * (m - s2h))
    s = 1 / math.sqrt(1 / sig ** 2 + e1 + kb * kb * e2)
    x = m + math.sqrt(2) * s * t
    h = -x * x / (2 * sig ** 2) - math.log(sig) - 0.5 * math.log(2 * math.pi) + _logS(x, sig, A, B, kb)
    terms = np.log(w) + t * t + h
    mx = terms.max()
    return math.log(math.sqrt(2) * s) + mx + math.log(np.exp(terms - mx).sum())


def log_pi_2d(sig, rho, Ap, Bp, Ad, Bd, kb, t, w):
    s2h = 0.5 * sig * sig
    sc2 = sig * sig * (1 - rho * rho)
    y = np.zeros(2)
    for _ in range(NEWTON_ITERS):
        ep1, ep2 = Ap * math.exp(y[0] - s2h), Bp * math.exp(kb * (y[0] - s2h))
        ed1, ed2 = Ad * math.exp(y[1] - s2h), Bd * math.exp(kb * (y[1] - s2h))
        g = np.array([-y[0] / sig ** 2 + rho * (y[1] - rho * y[0]) / sc2 - ep1 - kb * ep2,
                      -(y[1] - rho * y[0]) / sc2 - ed1 - kb * ed2])
        H = np.array([[-1 / sig ** 2 - rho * rho / sc2 - ep1 - kb * kb * ep2, rho / sc2],
                      [rho / sc2, -1 / sc2 - ed1 - kb * kb * ed2]])
        y = y - np.linalg.solve(H, g)
    ep1, ep2 = Ap * math.exp(y[0] - s2h), Bp * math.exp(kb * (y[0] - s2h))
    ed1, ed2 = Ad * math.exp(y[1] - s2h), Bd * math.exp(kb * (y[1] - s2h))
    P = -np.array([[-1 / sig ** 2 - rho * rho / sc2 - ep1 - kb * kb * ep2, rho / sc2],
                   [rho / sc2, -1 / sc2 - ed1 - kb * kb * ed2]])
    Lc = np.linalg.cholesky(np.linalg.inv(P))
    T1, T2 = np.meshgrid(t, t, indexing="ij")
    W = np.log(w)[:, None] + np.log(w)[None, :] + T1 ** 2 + T2 ** 2
    X1 = y[0] + math.sqrt(2) * (Lc[0, 0] * T1)
    X2 = y[1] + math.sqrt(2) * (Lc[1, 0] * T1 + Lc[1, 1] * T2)
    h = (-X1 ** 2 / (2 * sig ** 2) - math.log(sig) - (X2 - rho * X1) ** 2 / (2 * sc2) - 0.5 * math.log(sc2)
         - math.log(2 * math.pi) + _logS(X1, sig, Ap, Bp, kb) + _logS(X2, sig, Ad, Bd, kb))
    terms = W + h
    mx = terms.max()
    return math.log(2.0) + math.log(Lc[0, 0] * Lc[1, 1]) + mx + math.log(np.exp(terms - mx).sum())


def _simpson(n, lo=-12.0, hi=12.0):
    e = np.linspace(lo, hi, n + 1)
    wt = np.ones(n + 1)
    wt[1:-1:2], wt[2:-1:2] = 4, 2
    return e, wt * (hi - lo) / (3 * n)


def reference_1d(sig, A, B, kb, n=1600):
    e, wt = _simpson(n)
    v = _logS(sig * e, sig, A, B, kb) - 0.5 * e * e - 0.5 * math.log(2 * math.pi)
    mx = v.max()
    return mx + math.log(np.sum(wt * np.exp(v - mx)))


def reference_2d(sig, rho, Ap, Bp, Ad, Bd, kb, n=1600):
    e, wt = _simpson(n)
    E1, E2 = np.meshgrid(e, e, indexing="ij")
    xp = sig * E1
    xd = rho * xp + sig * math.sqrt(1 - rho * rho) * E2
    v = _logS(xp, sig, Ap, Bp, kb) + _logS(xd, sig, Ad, Bd, kb) - 0.5 * (E1 ** 2 + E2 ** 2) - math.log(2 * math.pi)
    mx = v.max()
    return mx + math.log(np.sum(wt[:, None] * wt[None, :] * np.exp(v - mx)))
