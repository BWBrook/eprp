# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "scipy==1.14.1", "cmdstanpy==1.2.4", "pandas==2.2.3"]
# ///
"""Q-038 posterior-predictive scoring (contract v2 section 4 and v3 section A), vectorised over posterior draws.
Parameters use a draws-last layout (core.eta broadcasts over it). For each draw the stage-k reference count is summed
exactly (the only positive count that can still yield 'no record in k+1..k+M'); the binomial tail beyond the largest
count kept has mass below TAIL in every draw. The set and count law conditions after integration over draws.
    uv run --python 3.12 data/q038-probe/score.py checks       # S1-S4, writes score_checks.json"""
import copy
import itertools
import json
import math
import pathlib
import sys
import time

import numpy as np
from scipy import special, stats

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402

TAIL = 1e-18
W, M_WINDOW = 3, 3


# ---------------------------------------------------------------- parameters in draws-last layout
def stack(plist):
    """A list of core parameter dicts (one per draw) in draws-last layout."""
    P = {"delta": np.array([p["delta"] for p in plist]).T}
    for key in ("alpha", "omega", "f_fam", "g_ord", "b_fam", "nu"):
        P[key] = {c: np.array([np.asarray(p[key][c], float) for p in plist]).T for c in core.CLASSES}
    for key in ("beta_b", "beta_e", "gd0", "gd"):
        P[key] = {c: np.array([float(p[key][c]) for p in plist]) for c in core.CLASSES}
    P["gamma"] = {c: [np.array([p["gamma"][c][j] for p in plist]) for j in range(3)] for c in core.CLASSES}
    return P


def from_stan(v):
    """cmdstanpy stan_variables() dict -> draws-last layout; stage-indexed arrays get an unused index 0."""
    pad = lambda a: np.concatenate([np.zeros((1, a.shape[1])), a], axis=0)
    P = {"delta": v["delta"].T}
    for i, c in enumerate(core.CLASSES):
        for key, src, padded in (("alpha", "alpha", True), ("nu", "nu", True), ("omega", "omega", False),
                                 ("f_fam", "f_fam", False), ("g_ord", "g_ord", False), ("b_fam", "b_fam", False)):
            a = v[src][:, i, :].T
            P.setdefault(key, {})[c] = pad(a) if padded else a
        for key in ("beta_b", "beta_e", "gd0", "gd"):
            P.setdefault(key, {})[c] = v[key][:, i]
        P.setdefault("gamma", {})[c] = [v["gam"][:, i, j] for j in range(3)]
    return P


def theta_v(P, cls, fam, t, w):
    return np.exp(P["gd0"][cls] + P["gd"][cls] * w + P["b_fam"][cls][fam] + P["nu"][cls][t])


def log_phi(e):
    """(log phi, log(1 - phi)) for eta = logit(1 - phi), stably."""
    return -np.logaddexp(0.0, e), -np.logaddexp(0.0, -e)


def log1m_exp(x):
    return np.where(x > -0.6931471805599453, np.log(-np.expm1(x)), np.log1p(-np.exp(x)))


# ---------------------------------------------------------------- one genus: log q and log(1 - q) over draws
def membership_v(h, k, cls, fam, ordr, P, D):
    """log P(alive at k-1 | records up to k-1): the CJS filter censored at k-1 (core.membership, vectorised)."""
    l = max(h.counts)
    if l == k - 1:
        return 0.0
    lph, l1m, lp0 = {}, {}, {}
    for s in range(l, k - 1):
        lph[s], l1m[s] = log_phi(core.eta(P, cls, fam, ordr, s, h.hazard_features(s, D)))
        lp0[s + 1] = -theta_v(P, cls, fam, s + 1, h.w(s + 1)) * D["E"][s + 1]
    num = sum(lph[s] for s in range(l, k - 1)) + sum(lp0[t] for t in range(l + 1, k))
    logchi = 0.0
    for s in range(k - 2, l - 1, -1):
        logchi = np.logaddexp(l1m[s], lph[s] + lp0[s + 1] + logchi)
    return num - logchi


def log_q(h, k, cls, fam, ordr, P, D, M=M_WINDOW):
    """(log q, log(1 - q)) with q = P(no record in k+1..k+M | records up to k-1), each genus's own future marks
    integrated: the stage-k count r is summed exactly, then the zero-record survival recursion."""
    lpi = membership_v(h, k, cls, fam, ordr, P, D)
    lph_a, l1m_a = log_phi(core.eta(P, cls, fam, ordr, k - 1, h.hazard_features(k - 1, D)))       # k-1 -> k
    lph_k, l1m_k = log_phi(core.eta(P, cls, fam, ordr, k, h.hazard_features(k, D)))               # event k -> k+1
    pk = np.atleast_1d(-np.expm1(-theta_v(P, cls, fam, k, h.w(k))))
    Ek = int(D["E"][k])
    rmax = min(max(int(np.max(stats.binom.isf(TAIL, Ek, pk))), 0), Ek) if Ek else 0
    r = np.arange(rmax + 1)
    lpmf = stats.binom.logpmf(r[:, None], Ek, pk[None, :])
    l1mF = []
    for rr in r:
        hh = copy.deepcopy(h)
        hh.add(k, int(rr))
        G = 0.0
        for t in range(k + M, k + 1, -1):
            lph, l1m = log_phi(core.eta(P, cls, fam, ordr, t - 1, hh.hazard_features(t - 1, D)))
            G = np.logaddexp(l1m, lph + (-theta_v(P, cls, fam, t, hh.w(t)) * D["E"][t]) + G)
        l1mF.append(lph_k + log1m_exp(-theta_v(P, cls, fam, k + 1, hh.w(k + 1)) * D["E"][k + 1] + G))
    l1mq = lpi + lph_a + special.logsumexp(lpmf + np.array(l1mF), axis=0)
    return log1m_exp(l1mq), l1mq


# ---------------------------------------------------------------- set and count laws, conditioned after integration
def log_count_pmf(lq, l1mq, D_):
    """log P(D | theta) per draw: Poisson-binomial dynamic programme in log space, so rare counts cannot underflow
    (Codex 76/2247: the probability-space version returned +inf for N = 1000, q = 0.99, D = 1)."""
    n = lq.shape[0]
    f = np.full((n + 1,) + lq.shape[1:], -np.inf)
    f[0] = 0.0
    for i in range(n):
        new = np.full_like(f, -np.inf)
        new[0] = f[0] + l1mq[i]
        new[1:i + 2] = np.logaddexp(f[1:i + 2] + l1mq[i], f[0:i + 1] + lq[i])
        f = new
    return f[D_]


def batch_se(x, nb=20):
    """Batch-means SE of a mean over draws ordered chain by chain."""
    nb = min(nb, x.size)
    b = np.array([c.mean() for c in np.array_split(x, nb)])
    return float(b.std(ddof=1) / math.sqrt(nb))


def set_scores(lq, l1mq, S):
    """Conditional set score log[sum_m P(S|m) / sum_m P(D|m)], its gain per genus against log 1/C(N,D), and the
    unconditional score log mean_m P(S|m); delta-method batch-means SEs."""
    S = np.asarray(S, bool)
    n, D_ = len(S), int(S.sum())
    lPS = np.sum(np.where(S[:, None], lq, l1mq), axis=0)
    lPD = log_count_pmf(lq, l1mq, D_)
    m = lPS.size
    a, b = np.exp(lPS - lPS.max()), np.exp(lPD - lPD.max())
    am, bm = a.mean(), b.mean()
    nb = min(20, m)
    ab = np.array([[x.mean(), y.mean()] for x, y in zip(np.array_split(a, nb), np.array_split(b, nb))])
    cv = np.cov(ab.T) / nb
    se_cond = math.sqrt(max(cv[0, 0] / am ** 2 + cv[1, 1] / bm ** 2 - 2 * cv[0, 1] / (am * bm), 0.0))
    cond = 0.0 if D_ in (0, n) else float(special.logsumexp(lPS) - special.logsumexp(lPD))   # endpoints: exactly 0
    if not math.isfinite(cond) or cond > 1e-9:
        raise ValueError(f"conditional log probability {cond} is not a valid log probability")
    base = -(special.gammaln(n + 1) - special.gammaln(D_ + 1) - special.gammaln(n - D_ + 1))
    return dict(N=n, D=D_, informative=bool(0 < D_ < n), conditional=float(cond), conditional_se=se_cond,
                gain_per_genus=float((cond - base) / n), uncond=float(special.logsumexp(lPS) - math.log(m)),
                uncond_se=batch_se(a) / am)


def risk_set(genera, k):
    """Genera first recorded by k-1 whose last prefix record is >= k - W (contract section 2)."""
    out = []
    for gi, g in enumerate(genera):
        pre = [t for t in range(g["f"], k) if g["counts"][t] > 0]
        if g["f"] <= k - 1 and pre and pre[-1] >= k - W:
            out.append(gi)
    return out


def score_event(genera, k, P, D, M=M_WINDOW):
    """Per-class O (records) and B (true members' deaths at k) set scores for forward event k, given draws P that are
    shared across classes (contract section 8 gates are per class; pooling rewards class severity differences,
    Codex 76/2247)."""
    return {c: _score_class(genera, k, P, D, M, c) for c in core.CLASSES}


def _score_class(genera, k, P, D, M, cls):
    R = [i for i in risk_set(genera, k) if genera[i]["cls"] == cls]
    lq, l1mq = zip(*[log_q(core.history_from_counts(genera[i]["counts"], genera[i]["f"], k - 1), k, genera[i]["cls"],
                           genera[i]["fam"], genera[i]["ord"], P, D, M) for i in R])
    S_O = [not any(genera[i]["counts"][k + 1:k + M + 1] > 0) for i in R]
    out = dict(O=set_scores(np.array(lq), np.array(l1mq), S_O))
    mem = [i for i in R if genera[i]["death"] >= k]
    lb = [log_phi(core.eta(P, genera[i]["cls"], genera[i]["fam"], genera[i]["ord"], k,
                           core.history_from_counts(genera[i]["counts"], genera[i]["f"], k - 1).hazard_features(k, D)))
          for i in mem]
    out["B"] = set_scores(np.array([x[1] for x in lb]), np.array([x[0] for x in lb]), [genera[i]["death"] == k for i in mem])
    return out


# ---------------------------------------------------------------- checks
def checks():
    D = core.load_design()
    man = json.loads((HERE / "manifest.json").read_text())
    out = {}
    rng = np.random.default_rng(5)
    plist = [core.truth_params(rng, D, man["omega_calibrated"]) for _ in range(6)]
    P = stack(plist)
    # S1: vectorised q equals core.predict_q(exact=True) draw by draw (actual design, simulated genera, three events)
    gen = core.simulate(np.random.default_rng(38001), D, plist[0])
    worst, n = 0.0, 0
    for k in (21, 38, 68):
        for i in risk_set(gen, k)[:12]:
            g = gen[i]
            h = core.history_from_counts(g["counts"], g["f"], k - 1)
            lq, _ = log_q(h, k, g["cls"], g["fam"], g["ord"], P, D, M=2)
            for m, p in enumerate(plist):
                worst = max(worst, abs(math.exp(lq[m]) - core.predict_q(h, k, 2, g["cls"], g["fam"], g["ord"], p, D, exact=True)))
                n += 1
    out["S1_vectorised_q_vs_predict_q"] = dict(max_abs=worst, comparisons=n)
    # S2: q + (1 - q) = 1 from the complementary formulas
    out["S2_complement_max_abs"] = max(float(np.max(np.abs(np.exp(a) + np.exp(b) - 1)))
                                       for a, b in [log_q(core.history_from_counts(gen[i]["counts"], gen[i]["f"], 37), 38,
                                                          gen[i]["cls"], gen[i]["fam"], gen[i]["ord"], P, D)
                                                    for i in risk_set(gen, 38)[:20]])
    # S3: the conditional set law, by brute force over all sets of a small risk set, is normalised for every D and
    # equals sum_m P(S|m) / sum_m P(D|m); the count DP equals brute-force enumeration
    sub = risk_set(gen, 38)[:9]
    lq, l1mq = map(np.array, zip(*[log_q(core.history_from_counts(gen[i]["counts"], gen[i]["f"], 37), 38, gen[i]["cls"],
                                         gen[i]["fam"], gen[i]["ord"], P, D) for i in sub]))
    tot, dp_err = {}, 0.0
    for S in itertools.product((0, 1), repeat=len(sub)):
        S = np.array(S, bool)
        sc = set_scores(lq, l1mq, S)
        tot[int(S.sum())] = tot.get(int(S.sum()), 0.0) + math.exp(sc["conditional"])
    for d in range(len(sub) + 1):
        brute = np.zeros(lq.shape[1])
        for S in itertools.combinations(range(len(sub)), d):
            m_ = np.zeros(len(sub), bool); m_[list(S)] = True
            brute += np.exp(np.sum(np.where(m_[:, None], lq, l1mq), axis=0))
        dp_err = max(dp_err, float(np.max(np.abs(np.exp(log_count_pmf(lq, l1mq, d)) - brute))))
    out["S3_conditional_set_law_total_by_D_max_abs_minus_1"] = max(abs(v - 1) for v in tot.values())
    out["S3_count_dp_vs_brute_max_abs"] = dp_err
    # S4: timing of one event's O and B scores over 400 draws (truth-perturbed draws stand in for a posterior)
    p400 = stack([core.truth_params(np.random.default_rng(1000 + j), D, man["omega_calibrated"]) for j in range(400)])
    t0 = time.perf_counter()
    sc = score_event(gen, 38, p400, D)
    out["S4_event38_scores_400_draws_per_class"] = dict(seconds=time.perf_counter() - t0, **sc)
    # S5: two-class uniform null (Codex 76/2247): pooled scoring earns gain without within-class selectivity
    q4 = np.array([0.2, 0.2, 0.8, 0.8]); lq4, l1q4 = np.log(q4)[:, None], np.log1p(-q4)[:, None]
    pooled, within = 0.0, 0.0
    for S in itertools.combinations(range(4), 2):
        m_ = np.zeros(4, bool); m_[list(S)] = True
        wS = float(np.prod(np.where(m_, q4, 1 - q4)))
        pooled += wS * set_scores(lq4, l1q4, m_)["gain_per_genus"]
    norm = sum(float(np.prod(np.where(np.isin(range(4), S), q4, 1 - q4))) for S in itertools.combinations(range(4), 2))
    pooled /= norm
    for cls_idx in ((0, 1), (2, 3)):                    # within class, every set has the same probability: gain 0
        for S in itertools.combinations(range(2), 1):
            m_ = np.zeros(2, bool); m_[list(S)] = True
            within = max(within, abs(set_scores(lq4[list(cls_idx)], l1q4[list(cls_idx)], m_)["gain_per_genus"]))
    out["S5_pooled_expected_gain"] = pooled
    out["S5_within_class_max_abs_gain"] = within
    # S6: rare counts in log space; S7: endpoints are exactly zero
    lq6, l1q6 = np.full((1000, 3), math.log(0.99)), np.full((1000, 3), math.log1p(-0.99))
    m6 = np.zeros(1000, bool); m6[0] = True
    out["S6_N1000_q099_D1"] = set_scores(lq6, l1q6, m6)["conditional"]
    out["S6_expected"] = -math.log(1000)
    out["S7_endpoints"] = [set_scores(lq4, l1q4, np.zeros(4, bool))["conditional"], set_scores(lq4, l1q4, np.ones(4, bool))["conditional"]]
    out["ok"] = bool(worst < 1e-12 and out["S2_complement_max_abs"] < 1e-12
                     and abs(pooled - 0.248857705) < 1e-8 and within < 1e-12
                     and abs(out["S6_N1000_q099_D1"] - out["S6_expected"]) < 1e-9 and out["S7_endpoints"] == [0.0, 0.0]
                     and out["S3_conditional_set_law_total_by_D_max_abs_minus_1"] < 1e-12 and dp_err < 1e-14)
    (HERE / "score_checks.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    {"checks": checks}[sys.argv[1]]()
