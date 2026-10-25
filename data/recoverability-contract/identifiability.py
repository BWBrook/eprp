"""Identifiability of four recovery mechanisms after provider loss.

Alternatives (autonomous variants) follow a linear birth-death process after
release, with per-capita birth b = b0*c_g, death d, optional import at rate m.
Service S = s*c_p*A; dependants are rescued when A reaches K = theta/(s*c_p).
For linear birth-death started from one individual, W = lim A(t)exp(-rt) is 0
with probability d/b and otherwise Exponential with mean b/r (r = b - d), so
the time to reach K is (ln K - ln W)/r.  Each world is tuned to the same median
recovery time; signatures are read from W, r and the import onset.  De novo
reversion: revertants arise at rate mu*N0*exp(-DELTA*t) from a declining
dependent population, each founding a birth-death lineage.
"""
import json
import math
import numpy as np

RNG = np.random.default_rng(20261025)
N = 200_000
K = 1e6
D = 1.0


def sample_W(a, b, n=N):
    r = b - D
    surv = RNG.random((n, a)) > D / b
    w = RNG.exponential(b / r, size=(n, a)) * surv
    return w.sum(axis=1)


def sample_W_import(m, b, horizon=60.0, n=N):
    r = b - D
    W = np.zeros(n)
    counts = RNG.poisson(m * horizon, size=n)
    for i, c in enumerate(counts):
        if c:
            t = RNG.uniform(0, horizon, size=c)
            alive = RNG.random(c) > D / b
            W[i] = (np.exp(-r * t[alive]) * RNG.exponential(b / r, size=alive.sum())).sum()
    return W


def times(W, r, k=K):
    T = np.full(W.shape, np.inf)
    pos = W > 0
    T[pos] = (math.log(k) - np.log(W[pos])) / r
    return T


def summary(name, W, r, k=K, extra=None):
    T = times(W, r, k)
    fin = T[np.isfinite(T)]
    out = {
        "world": name,
        "P_fail_never": float(np.mean(~np.isfinite(T))),
        "median_T": float(np.median(fin)),
        "sd_T_given_success": float(np.std(fin)),
        "slope_r": r,
        "median_lnW": float(np.median(np.log(W[W > 0]))),
        "threshold_K": k,
    }
    if extra:
        out.update(extra)
    return out


def solve(f, lo, hi, target, it=60):
    """Bisection for f decreasing in its argument."""
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if f(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


res = []
Ws = sample_W(3, 2.0)
s = summary("scarcity: a=3, full competence", Ws, 1.0)
res.append(s)
target = s["median_T"]

def med_growth(b):
    return float(np.median(times(sample_W(1000, b, 20_000), b - D)))
b_e = solve(med_growth, 1.05, 2.0, target)
res.append(summary("growth erosion: a=1000, c_g=%.3f" % (b_e / 2.0), sample_W(1000, b_e), b_e - D))

Wp = sample_W(1000, 2.0)
def med_prov(cp):
    return float(np.median(times(Wp[:20_000], 1.0, K / cp)))
cp = 1.0 / solve(lambda inv: -med_prov(1 / inv), 1.0, 1e6, -target)
res.append(summary("provision erosion: a=1000, c_p=%.4f" % cp, Wp, 1.0, K / cp))

def med_imp(m):
    return float(np.median(times(sample_W_import(m, 2.0, n=4000), 1.0)))
m = solve(med_imp, 1e-3, 50.0, target)
Wi = sample_W_import(m, 2.0, n=40_000)
res.append(summary("import: a=0, m=%.3f per unit time" % m, Wi, 1.0))

DELTA = 0.5


def sample_W_denovo(mu_n0, b, n=N):
    r = b - D
    lam = mu_n0 / DELTA
    counts = RNG.poisson(lam, size=n)
    W = np.zeros(n)
    for i, c in enumerate(counts):
        if c:
            t = RNG.exponential(1 / DELTA, size=c)
            alive = RNG.random(c) > D / b
            W[i] = (np.exp(-r * t[alive]) * RNG.exponential(b / r, size=alive.sum())).sum()
    return W


def med_dn(x):
    T = times(sample_W_denovo(x, 2.0, n=4000), 1.0)
    return float(np.median(T[np.isfinite(T)])) if np.isfinite(T).any() else np.inf
x = solve(med_dn, 1e-3, 50.0, target)
Wd = sample_W_denovo(x, 2.0, n=40_000)
res.append(summary("de novo reversion: a=0, mu*N0=%.3f, dependants decline at %.1f" % (x, DELTA), Wd, 1.0,
                   extra={"P_fail_exact": math.exp(-(x / DELTA) * (1 - D / 2.0))}))

t = np.array([0.25, 0.5, 1.0, 2.0])
onset = {
    "scarcity_lnA_minus_lnA0": (1.0 * t).round(3).tolist(),
    "import_lnA_early": np.log((m / 1.0) * (np.exp(t) - 1)).round(3).tolist(),
    "import_local_slope_dlnA_dt": (np.exp(t) / (np.exp(t) - 1)).round(3).tolist(),
}
out = {"seed": 20261025, "N": N, "K": K, "death": D, "worlds": res, "onset": onset}
print(json.dumps(out, indent=1))
