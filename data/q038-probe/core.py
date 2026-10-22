"""Q-038 primary probe (contract v3, data/q038-predictor-contract/contract.md; cleared by Codex 76/2195).

One feature convention for generator, likelihood, fold builder and forecast (Codex's implementation requirement):
- Stages t = 1..T. A genus alive in stage t emits a reference count Binomial(E_t, 1 - exp(-theta_t)) (epsilon = 1), then
  survives the transition t -> t+1 with probability phi_t. A dead genus emits zero.
- The CJS likelihood conditions on the first record f and on its count (declared convention). A LOEO restart conditions
  on its capture and count but keeps the genus's earlier observed history for covariates (origin = first record).
- Hazard covariates for the transition s -> s+1 use records in stages < s, with the first-record stage always included
  (so the transition out of f uses f's own record). Detection at stage t uses w = log mean count over recorded stages < t.
- Covariates use FIXED affine transforms frozen from the deposit (deposit_constants.json), never data-dependent z-scores,
  so a coefficient means the same thing in generator, fit and forecast.
- Before the first record (generator only) covariates are 0 and w = 0.
"""
import json
import math
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EVENTS = (7, 21, 38, 45, 68)
CLASSES = ("Rhynchonellata", "Bivalvia")
N_FAM, FAM_PER_ORD = 40, 5          # per class: 40 families in 8 orders


def load_design():
    st = np.genfromtxt(ROOT / "data/q038-predictor-contract/stages.tsv", delimiter="\t", names=True, dtype=None, encoding=None)
    ex = np.genfromtxt(ROOT / "data/q038-predictor-contract/exposure.tsv", delimiter="\t", names=True, dtype=None, encoding=None)
    dc = json.loads((HERE / "deposit_constants.json").read_text())
    T = int(st["s"].max())
    maxma, minma, E = np.zeros(T + 1), np.zeros(T + 1), np.zeros(T + 1, dtype=int)
    maxma[st["s"]], minma[st["s"]] = st["max_ma"], st["min_ma"]
    E[ex["s"]] = ex["refs_other_classes"]
    return dict(T=T, maxma=maxma, minma=minma, E=E, tf=dc["transform"],
                entries={c: np.array([0] + dc["first_record_counts"][c]) for c in CLASSES})


# ---------------------------------------------------------------- features (one convention)
class History:
    """Observed record history of one genus from its first record: counts by stage (dict)."""
    def __init__(self, f, cf):
        self.f, self.counts = f, {f: cf}

    def add(self, t, c):
        if c > 0:
            self.counts[t] = c

    def hazard_features(self, s, D):
        """(x_occ, recency, age, completeness), fixed-transformed, for the transition s -> s+1."""
        rec = sorted(t for t in self.counts if t < s or t == self.f)
        l = rec[-1]
        tf = D["tf"]
        x = (math.log(self.counts[l]) - tf["log_refs"]["mean"]) / tf["log_refs"]["sd"]
        r = (max(0.0, D["minma"][l] - D["maxma"][s]) - tf["rec"]["mean"]) / tf["rec"]["sd"]
        a = (D["maxma"][self.f] - D["maxma"][s] - tf["age"]["mean"]) / tf["age"]["sd"]
        c = (len(rec) / (l - self.f + 1) - tf["comp"]["mean"]) / tf["comp"]["sd"]
        return x, r, a, c

    def w(self, t):
        rec = [c for u, c in self.counts.items() if u < t]
        return math.log(sum(rec) / len(rec)) if rec else 0.0


def history_from_counts(counts, f, upto):
    """History built from an array of counts, using stages f..upto only (the fold builder's truncation point)."""
    h = History(f, int(counts[f]))
    for t in range(f + 1, upto + 1):
        h.add(t, int(counts[t]))
    return h


def component_history(counts, f):
    """Observed history through a component's conditioning start f, from the genus's own first record. A LOEO restart
    conditions on its capture at f but keeps the earlier observed marks as covariates (Codex 76/2213)."""
    return history_from_counts(counts, int(np.flatnonzero(counts)[0]), f)


# ---------------------------------------------------------------- hazard and detection given parameters
def eta(params, cls, fam, ordr, s, feats):
    """logit(1 - phi) for the transition s -> s+1."""
    x, r, a, c = feats
    g = params["gamma"][cls]
    base = params["alpha"][cls][s] + g[0] * r + g[1] * a + g[2] * c + params["f_fam"][cls][fam] + params["g_ord"][cls][ordr]
    if s in EVENTS:
        k = EVENTS.index(s)
        return base + params["omega"][cls][k] + (params["beta_e"][cls] + params["delta"][k]) * x
    return base + params["beta_b"][cls] * x


def theta(params, cls, fam, t, w):
    return math.exp(params["gd0"][cls] + params["gd"][cls] * w + params["b_fam"][cls][fam] + params["nu"][cls][t])


def plogis(z):
    return 1 / (1 + math.exp(-z)) if z > -700 else 0.0


# ---------------------------------------------------------------- CJS component likelihood (Python reference for Stan)
def log_binom(y, n, th):
    """log Binomial(y | n, 1 - exp(-th))."""
    if y == 0:
        return -th * n
    return math.lgamma(n + 1) - math.lgamma(y + 1) - math.lgamma(n - y + 1) + y * math.log(-math.expm1(-th)) - (n - y) * th


def component_loglik(counts, f, C, cls, fam, ordr, params, D):
    """log P(counts at f+1..C | capture at f with its count and the observed history before f), censored after C."""
    h = component_history(counts, f)
    logphi, log1mphi, logp0, ll_em = {}, {}, {}, {}
    for t in range(f, C):
        e = eta(params, cls, fam, ordr, t, h.hazard_features(t, D))     # transition t -> t+1 uses records < t (+ f)
        log1mphi[t] = -math.log1p(math.exp(-e)) if e > -700 else e        # log(1 - phi) = log inv_logit(eta)
        logphi[t] = -math.log1p(math.exp(e)) if e < 700 else -e
        th = theta(params, cls, fam, t + 1, h.w(t + 1))
        logp0[t + 1] = -th * D["E"][t + 1]
        ll_em[t + 1] = log_binom(int(counts[t + 1]), int(D["E"][t + 1]), th)
        h.add(t + 1, int(counts[t + 1]))
    rec = [t for t in range(f, C + 1) if counts[t] > 0]
    l = rec[-1]
    ll = sum(logphi[s] for s in range(f, l)) + sum(ll_em[t] for t in range(f + 1, l + 1))
    logchi = 0.0
    for t in range(C - 1, l - 1, -1):
        logchi = np.logaddexp(log1mphi[t], logphi[t] + logp0[t + 1] + logchi)
    return ll + logchi


# ---------------------------------------------------------------- truth and generator
TRUTH_S2 = dict(alpha=dict(Rhynchonellata=0.19, Bivalvia=0.05), beta_b=0.3, beta_e=0.5, tau=0.3, gamma=0.2, s_fam=0.3,
                s_ord=0.3, gd0=math.log(0.01), gd=0.5, s_b=0.3, s_nu=0.2)
TRUTH = dict(S2=TRUTH_S2, S1=dict(TRUTH_S2, beta_e=0.0),
             S0=dict(TRUTH_S2, beta_e=0.0, tau=0.0, gamma=0.0, s_fam=0.0, s_ord=0.0))
# S0 zeroes the shared nuisance and clade effects globally (Codex 76/2195, first option), so at events eta = alpha + omega;
# background occupancy (beta_b) and detection heterogeneity are kept. S3 and S4 perturb observation only (simulate obs=).
S3_WINDOW, S4_SD = 3, 0.5
TARGET_LOSS = dict(Rhynchonellata=(26 / 98, 76 / 144, 99 / 128, 40 / 76, 27 / 55),
                   Bivalvia=(10 / 48, 6 / 67, 42 / 124, 34 / 181, 101 / 340))   # deposit class-event D/N (events.tsv)


def truth_params(rng, D, omega, scenario="S2", draw=True):
    """Truth parameter dict. Random effects are drawn from rng when draw=True (archived); omega is supplied (calibrated).
    A zero scale draws zeros but consumes the same stream."""
    T, tr = D["T"], TRUTH[scenario]
    p = dict(alpha={}, omega={}, gamma={}, f_fam={}, g_ord={}, b_fam={}, nu={}, beta_b={}, beta_e={}, gd0={}, gd={})
    zf = lambda n, s: rng.normal(0, s, n) if draw else np.zeros(n)
    p["delta"] = list(zf(5, tr["tau"]))
    for c in CLASSES:
        p["alpha"][c] = np.full(T + 1, math.log(tr["alpha"][c] / (1 - tr["alpha"][c])))
        p["omega"][c] = list(omega[c])
        p["gamma"][c] = [tr["gamma"]] * 3
        p["g_ord"][c] = zf(N_FAM // FAM_PER_ORD, tr["s_ord"])
        p["f_fam"][c] = zf(N_FAM, tr["s_fam"])
        p["b_fam"][c] = zf(N_FAM, tr["s_b"])
        p["nu"][c] = zf(T + 1, tr["s_nu"])
        p["beta_b"][c], p["beta_e"][c] = tr["beta_b"], tr["beta_e"]
        p["gd0"][c], p["gd"][c] = tr["gd0"], tr["gd"]
    return p


def s3_scale():
    """S3: true opportunity E_t x (1 - L_ck) for t = k+1..k+S3_WINDOW after each event, with L_ck the calibrated (target)
    class event loss; the fit still uses E_t."""
    return {(c, t): 1 - TARGET_LOSS[c][i] for c in CLASSES for i, k in enumerate(EVENTS) for t in range(k + 1, k + S3_WINDOW + 1)}


def simulate(rng, D, params, record_members=False, obs=None):
    """Forward simulation. Returns genera with observed counts from their first record, latent death stage, and (if
    asked) each event's members with their event eta excluding omega (for calibration). obs: None (the fitted
    observation model), "S3" (survivor-tracking exposure) or "S4" (reference-level clustering, one zeta per reference
    and stage shared by all genera)."""
    T, E = D["T"], D["E"]
    genera, members = [], {(c, k): [] for c in CLASSES for k in EVENTS}
    sc = s3_scale() if obs == "S3" else {}
    zeta = {t: rng.normal(0, S4_SD, int(E[t])) for t in range(1, T + 1)} if obs == "S4" else {}

    def detect(c, t, th):
        if obs == "S4":
            return int(np.sum(rng.random(int(E[t])) < -np.expm1(-th * np.exp(zeta[t]))))
        return int(rng.binomial(int(round(E[t] * sc.get((c, t), 1.0))) if sc else E[t], -math.expm1(-th)))
    for c in CLASSES:
        n_entry = rng.poisson(D["entries"][c][1:])
        for e, n in enumerate(n_entry, start=1):
            for _ in range(n):
                fam = int(rng.integers(N_FAM)); ordr = fam // FAM_PER_ORD
                counts = np.zeros(T + 1, dtype=int)
                h, death = None, T
                for t in range(e, T + 1):
                    th = theta(params, c, fam, t, h.w(t) if h else 0.0)
                    y = detect(c, t, th)
                    if h is None and y > 0:
                        h = History(t, y)
                    counts[t] = y if h else 0
                    if t == T:
                        break
                    feats = h.hazard_features(t, D) if h else (0.0, 0.0, 0.0, 0.0)
                    et = eta(params, c, fam, ordr, t, feats)
                    if record_members and t in EVENTS:
                        k = EVENTS.index(t)
                        members[(c, t)].append(et - params["omega"][c][k])
                    if h is not None:
                        h.add(t, y)
                    if rng.random() < plogis(et):
                        death = t
                        break
                if h is not None:
                    genera.append(dict(cls=c, fam=fam, ord=ordr, entry=e, f=h.f, death=death, counts=counts))
    return (genera, members) if record_members else genera


def calibrate_omega(D, seed=38000, scenario="S2"):
    """Event excesses solved sequentially (event order) so the mean event loss among members at the design covariates,
    with random effects at zero, equals the deposit class-event D/N. Deterministic given the seed."""
    omega = {c: [0.0] * 5 for c in CLASSES}
    from scipy.optimize import brentq
    for k_i, k in enumerate(EVENTS):
        rng = np.random.default_rng(seed)
        p = truth_params(np.random.default_rng(0), D, omega, scenario, draw=False)
        _, mem = simulate(rng, D, p, record_members=True)
        for c in CLASSES:
            et = np.array(mem[(c, k)])
            tgt = TARGET_LOSS[c][k_i]
            omega[c][k_i] = brentq(lambda w: float(np.mean(1 / (1 + np.exp(-(et + w))))) - tgt, -20, 20)
    return omega


# ---------------------------------------------------------------- folds and Stan data (the fold builder)
def components(genera, fold, D, W=3):
    """Likelihood components (genus index, f, C) for a fold. fold: ('full',), ('forward', k) or ('loeo', k).
    Forward: every genus first recorded by k-1, censored at k-1. Leave-one-event-out (epsilon = 1, contract v2 section 5):
    the prefix risk set of k is truncated at k-1; every other component beginning at or before k is censored at k; a genus
    with a record after k restarts at its first post-boundary record; held-out genera never restart."""
    T = D["T"]
    out = []
    for gi, g in enumerate(genera):
        f, cnt = g["f"], g["counts"]
        if fold[0] == "full":
            out.append((gi, f, T))
        elif fold[0] == "forward":
            k = fold[1]
            if f <= k - 1:
                out.append((gi, f, k - 1))
        else:
            k = fold[1]
            if f > k:
                out.append((gi, f, T))
                continue
            pre = [t for t in range(f, k) if cnt[t] > 0]
            held = bool(pre) and pre[-1] >= k - W
            if held:
                out.append((gi, f, k - 1))
                continue
            out.append((gi, f, k))
            later = [t for t in range(k + 1, T + 1) if cnt[t] > 0]
            if later:
                out.append((gi, later[0], T))
    return out


def stan_data(genera, comps, D, likelihood_only=0, grainsize=50):
    cl = {c: i + 1 for i, c in enumerate(CLASSES)}
    d = dict(T=D["T"], N=len(comps), c_cls=[], c_fam=[], c_ord=[], c_f=[], c_C=[], c_last=[], c_tr0=[], c_em0=[],
             tr_s=[], tr_feat=[], em_y=[], em_E=[], em_w=[], NF=N_FAM, NO=N_FAM // FAM_PER_ORD,
             ev_of=[EVENTS.index(s) + 1 if s in EVENTS else 0 for s in range(1, D["T"] + 1)],
             likelihood_only=likelihood_only, grainsize=grainsize)
    for gi, f, C in comps:
        g = genera[gi]
        cnt = g["counts"]
        h = component_history(cnt, f)
        d["c_cls"].append(cl[g["cls"]]); d["c_fam"].append(g["fam"] + 1); d["c_ord"].append(g["ord"] + 1)
        d["c_f"].append(f); d["c_C"].append(C)
        d["c_last"].append(max(t for t in range(f, C + 1) if cnt[t] > 0))
        d["c_tr0"].append(len(d["tr_s"]) + 1); d["c_em0"].append(len(d["em_y"]) + 1)
        for s in range(f, C):
            d["tr_s"].append(s); d["tr_feat"].append(list(h.hazard_features(s, D)))
            d["em_y"].append(int(cnt[s + 1])); d["em_E"].append(int(D["E"][s + 1])); d["em_w"].append(h.w(s + 1))
            h.add(s + 1, int(cnt[s + 1]))
    d["R"] = len(d["tr_s"])
    if d["R"] == 0:
        d["tr_feat"] = np.zeros((0, 4))
    return d


# ---------------------------------------------------------------- forecast (marked-history predictive, contract v3 A)
def membership(h, k, cls, fam, ordr, params, D):
    """P(alive at k-1 | records up to k-1), the CJS filter censored at k-1."""
    l = max(h.counts)
    if l == k - 1:
        return 1.0
    num, logchi = 0.0, 0.0
    hh = History(h.f, h.counts[h.f]); [hh.add(t, c) for t, c in h.counts.items() if t != h.f]
    lphi, l1m, lp0 = {}, {}, {}
    for s in range(l, k - 1):
        e = eta(params, cls, fam, ordr, s, hh.hazard_features(s, D))
        l1m[s] = -math.log1p(math.exp(-e)); lphi[s] = -math.log1p(math.exp(e))
        lp0[s + 1] = -theta(params, cls, fam, s + 1, hh.w(s + 1)) * D["E"][s + 1]
    num = sum(lphi[s] for s in range(l, k - 1)) + sum(lp0[t] for t in range(l + 1, k))
    for s in range(k - 2, l - 1, -1):
        logchi = np.logaddexp(l1m[s], lphi[s] + lp0[s + 1] + logchi)
    return math.exp(num - logchi)


def predict_q(h, k, M, cls, fam, ordr, params, D, n=2000, rng=None, exact=False):
    """q = P(no record in k+1..k+M | records up to k-1), integrating the genus's own future counts (stage k onward)."""
    pi = membership(h, k, cls, fam, ordr, params, D)

    def step_paths(hh, t, prob):          # exact enumeration: alive at t-1, transition t-1 -> t, emission at t
        e = eta(params, cls, fam, ordr, t - 1, hh.hazard_features(t - 1, D))
        phi = 1 - plogis(e)
        tot = prob * (1 - phi)
        th = theta(params, cls, fam, t, hh.w(t)); r = -math.expm1(-th)
        for y in range(int(D["E"][t]) + 1):
            if t > k and y > 0:
                continue
            py = math.comb(int(D["E"][t]), y) * r ** y * (1 - r) ** (int(D["E"][t]) - y)
            h2 = History(hh.f, hh.counts[hh.f]); [h2.add(u, c) for u, c in hh.counts.items() if u != hh.f]; h2.add(t, y)
            tot += prob * phi * py if t == k + M else step_paths(h2, t + 1, prob * phi * py)
        return tot
    if exact:
        return (1 - pi) + step_paths(h, k, pi)
    rng = rng or np.random.default_rng(0)
    miss = 0
    for _ in range(n):
        if rng.random() >= pi:
            miss += 1; continue
        hh = History(h.f, h.counts[h.f]); [hh.add(u, c) for u, c in h.counts.items() if u != h.f]
        seen = False
        for t in range(k, k + M + 1):
            if rng.random() < plogis(eta(params, cls, fam, ordr, t - 1, hh.hazard_features(t - 1, D))):
                break
            y = int(rng.binomial(int(D["E"][t]), -math.expm1(-theta(params, cls, fam, t, hh.w(t)))))
            if t > k and y > 0:
                seen = True; break
            hh.add(t, y)
        miss += not seen
    return miss / n
