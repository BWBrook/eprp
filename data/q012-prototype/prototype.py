# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4"]
# ///
"""Q-012 timed one-dataset prototype of the full working likelihood.

Run from the repository root:
  uv run --python 3.12 data/q012-prototype/prototype.py checks   # generate, map, adapt; normaliser and log-density checks
  uv run --python 3.12 data/q012-prototype/prototype.py fit      # one timed fit under the declared limit

Implements the finite contract with Amendment 1
(literature/2026-10-16-q012-finite-contract.md): a generator with the forced-design
boundary cohort, the observation map (thinning, compatible-parent pruning, acyclic
reassignment, rounding precedence, Markov exposure observation, past-only lag), the
data adapter, an independent Python implementation of the Stan target, and the
cohort normaliser checked by Gauss-Hermite quadrature against Monte Carlo.
"""

import json
import math
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CFG = json.loads((HERE / "config.json").read_text())
OUT = ROOT / "scratch/q012-prototype"
CMDSTAN = pathlib.Path.home() / ".cmdstan/cmdstan-2.38.0"
H = 75.0
C = 75.0 - 66.05


# ---------------------------------------------------------------- generator
def h0_at(u, h0):
    return h0[min(int((H - u) // 3), 24)]


def generate(seed):
    g = CFG["generator"]
    rng = np.random.default_rng(seed)
    sig, rho, kap, kapb, beta = g["sigma"], g["rho"], g["kappa"], g["kappa_b"], g["beta"]
    lam0, b0, h0 = g["lambda0"], g["b0"], g["h0_by_3Myr_bin_Ma"]
    ep = g["E_process"]

    def ma_bin(u):  # 1-Myr Ma bin containing forward time u (u in [n, n+1) -> 74 - n)
        return 74 - min(int(math.floor(u)), 74)

    def e_next(prev):
        val = ep["mean"] + ep["phi"] * (prev - ep["mean"]) + rng.normal(0, ep["sd"] * math.sqrt(1 - ep["phi"] ** 2))
        return min(max(val, ep["truncate"][0]), ep["truncate"][1])

    def e_start(parent_val):
        if parent_val is None:
            val = rng.normal(ep["mean"], ep["sd"])
        else:
            val = ep["mean"] + ep["rho_E"] * (parent_val - ep["mean"]) + rng.normal(0, ep["sd"] * math.sqrt(1 - ep["rho_E"] ** 2))
        return min(max(val, ep["truncate"][0]), ep["truncate"][1])

    def new_lineage(parent, o, x, parent_E=None):
        b = ma_bin(o)
        return dict(parent=parent, o=o, x=x, E={b: e_start(parent_E)})

    def E_at(lin, b):
        while b not in lin["E"]:
            last = min(lin["E"])
            lin["E"][last - 1] = e_next(lin["E"][last])
        return lin["E"][b]

    def terminate(lin):
        """Piecewise-exponential termination (k = 1) from origin; sets end and cause."""
        z = math.exp(lin["x"] - 0.5 * sig ** 2)
        bif = b0 * z ** kapb
        u = lin["o"]
        while u < H:
            seg_end = min(math.floor(u) + 1.0, H)
            Eb = (E_at(lin, ma_bin(u)) - CFG["observation"]["E_standardise"]["mean"]) / CFG["observation"]["E_standardise"]["sd"]
            mu = z * h0_at(0.5 * (u + seg_end), h0) * math.exp(beta * Eb)
            t = u + rng.exponential(1.0 / (mu + bif))
            if t < seg_end:
                lin["end"], lin["cause"] = t, ("ext" if rng.random() < mu / (mu + bif) else "bif")
                return
            u = seg_end
        lin["end"], lin["cause"] = H, "cens"

    roots = [H - t for t in g["roots_Ma"]]
    coh = g["cohort"]
    attempts = 0
    while True:  # forced-design cohort, conditioned on all six surviving to c
        attempts += 1
        L = [new_lineage(-1, roots[i], sig * rng.standard_normal()) for i in coh["root_indices"]]
        p = coh["design_daughter_parent_index"]
        od = H - coh["design_daughter_Ma"]
        L.append(new_lineage(p, od, rho * L[p]["x"] + sig * math.sqrt(1 - rho ** 2) * rng.standard_normal(),
                             parent_E=E_at(L[p], ma_bin(od))))
        for lin in L:
            terminate(lin)
        if all(lin["end"] > C for lin in L):
            break
    for lin in L:
        lin["cohort"] = True
    for i in range(len(coh["root_indices"]), len(roots)):
        lin = new_lineage(-1, roots[i], sig * rng.standard_normal())
        terminate(lin)
        lin["cohort"] = False
        L.append(lin)
    i, capped = 0, False
    while i < len(L):
        lin = L[i]
        z = math.exp(lin["x"] - 0.5 * sig ** 2)
        start = max(lin["o"], C)
        t, buds = start, []
        while True:
            t += rng.exponential(1.0 / (lam0 * z ** kap))
            if t >= lin["end"]:
                break
            buds.append(t)
        kids = [(b, False) for b in buds]
        if lin["cause"] == "bif":
            kids += [(lin["end"], True), (lin["end"], True)]
        lin["true_buds"] = len(buds)
        if len(L) + len(kids) > g["lineage_cap"]:
            capped = True
            break
        for o, _ in kids:
            d = new_lineage(i, o, rho * lin["x"] + sig * math.sqrt(1 - rho ** 2) * rng.standard_normal(),
                            parent_E=E_at(lin, ma_bin(min(o, H - 1e-9))))
            terminate(d)
            d["cohort"] = False
            L.append(d)
        i += 1
    return L, dict(cohort_attempts=attempts, capped=capped, true_lineages=len(L))


# ---------------------------------------------------------------- observation map
def observe(L, seed):
    ob = CFG["observation"]
    rng = np.random.default_rng(seed + 1)
    n = len(L)
    rec = [rng.random() < 1 - math.exp(-ob["psi"] * (l["end"] - l["o"])) for l in L]
    par = [-1] * n
    lost = 0
    for i in range(n):
        if not rec[i]:
            continue
        p = L[i]["parent"]
        while p >= 0:
            if rec[p] and L[p]["o"] <= L[i]["o"] <= L[p]["end"]:
                break
            p = L[p]["parent"]
        par[i] = p
        if p < 0 and L[i]["parent"] >= 0:
            lost += 1
    ids = [i for i in range(n) if rec[i]]

    def root_of(i):
        while par[i] >= 0:
            i = par[i]
        return i

    def descendants(i):
        out, stack = set(), [i]
        while stack:
            a = stack.pop()
            for j in ids:
                if par[j] == a and j not in out:
                    out.add(j)
                    stack.append(j)
        return out

    reassigned = 0
    for i in sorted(ids, key=lambda j: L[j]["o"]):
        if par[i] < 0 or rng.random() >= ob["epsilon"]:
            continue
        rt, desc = root_of(i), descendants(i)
        cands = [j for j in ids if j != i and j not in desc and root_of(j) == rt
                 and L[j]["o"] <= L[i]["o"] <= L[j]["end"]]
        if cands:
            best = sorted(cands, key=lambda j: (-(L[j]["end"] - L[j]["o"]), L[j]["o"], j))[0]
            if best != par[i]:
                par[i] = best
                reassigned += 1
    # rounding precedence (Ma), applied jointly
    tO = {i: round(H - L[i]["o"], 2) for i in ids}
    tE = {i: (0.0 if L[i]["end"] >= H else round(H - L[i]["end"], 2)) for i in ids}
    cnt = dict(short_interval_moves=0, origin_ties=0, unroundable=0)
    for i in ids:
        if tO[i] <= tE[i]:
            tO[i] = round(tE[i] + 0.005, 3)
            cnt["short_interval_moves"] += 1
    for i in sorted(ids, key=lambda j: L[j]["o"]):
        p = par[i]
        if p < 0:
            continue
        if tO[i] > tO[p]:
            tO[i] = tO[p]
            cnt["origin_ties"] += 1
        if not (tO[i] > tE[i] and tE[p] <= tO[i] <= tO[p]):
            for j in (i, p):
                tO[j] = H - L[j]["o"]
                tE[j] = 0.0 if L[j]["end"] >= H else H - L[j]["end"]
            cnt["unroundable"] += 1
    # end labels from recorded data only
    at_end = {i: 0 for i in ids}
    for i in ids:
        if par[i] >= 0 and abs(tO[i] - tE[par[i]]) < 1e-9:
            at_end[par[i]] += 1
    label = {}
    for i in ids:
        if tE[i] == 0.0:
            label[i] = "present"
        elif at_end[i] >= 2:
            label[i] = "bif"
        elif at_end[i] == 1:
            label[i] = "single"
        else:
            label[i] = "ext"
    # exposure observation: coverage, Markov chain after 66 Ma, then past-only lag
    mk = ob["E_markov"]
    used = {}
    for i in ids:
        covered = rng.random() < mk["pi_L"]
        top, bot = int(math.floor(tO[i] - 1e-12)), int(math.floor(tE[i]))
        bins = list(range(top, bot - 1, -1))  # oldest first
        obs, prev = {}, None
        for b in bins:
            if b >= 66 or not covered:
                o = False
            elif prev is None:
                o = rng.random() < mk["p_first"]
            else:
                o = rng.random() < (mk["p_obs_given_obs"] if prev else mk["p_obs_given_missing"])
            if b < 66 and covered:
                prev = o
            obs[b] = L[i]["E"].get(b) if o else None
        u = {}
        for b in bins:
            u[b] = obs.get(b + 1) if obs.get(b + 1) is not None else obs.get(b + 2)
        used[i] = u
    labels = dict(ext=0, bif=0, single=0, present=0)
    for v in label.values():
        labels[v] += 1
    info = dict(recorded=len(ids), ancestry_lost=lost, reassigned=reassigned, labels=labels, **cnt)
    return dict(ids=ids, par=par, tO=tO, tE=tE, label=label, used=used), info


# ---------------------------------------------------------------- adapter
def adapt(obsd):
    ids, par, tO, tE, label, used = (obsd[k] for k in ("ids", "par", "tO", "tE", "label", "used"))
    sd = CFG["observation"]["E_standardise"]

    def depth(i):
        d = 0
        while par[i] >= 0:
            i, d = par[i], d + 1
        return d

    order = sorted(ids, key=lambda i: (H - tO[i], depth(i)))
    pos = {i: k for k, i in enumerate(order)}
    N = len(order)
    o = [H - tO[i] for i in order]
    v = [H - tE[i] for i in order]
    coh = [k for k in range(N) if o[k] < C < v[k]]
    r = [max(o[k], C) if k in coh else o[k] for k in range(N)]
    parent = [pos[par[i]] + 1 if par[i] >= 0 else 0 for i in order]
    for k in range(N):
        assert parent[k] == 0 or parent[k] - 1 < k, "parents must precede daughters"
    ext = [int(label[i] == "ext") for i in order]
    bif = [int(label[i] == "bif") for i in order]
    mplus = [0] * N
    for k, i in enumerate(order):
        p = parent[k] - 1
        if p >= 0 and o[k] < v[p] - 1e-9 and o[k] >= r[p]:
            mplus[p] += 1

    def bin3(u):
        return min(int((H - u) // 3), 24) + 1

    def ebin(i, b):
        val = used[i].get(b)
        return (0.0, 1.0) if val is None else ((val - sd["mean"]) / sd["sd"], 0.0)

    seg = dict(lin=[], bin=[], a0=[], a1=[], E=[], miss=[])
    term_bin, term_a, term_E, term_miss = [], [], [], []
    for k, i in enumerate(order):
        cuts = sorted({r[k], v[k]} | {float(n) for n in range(math.ceil(r[k]), math.floor(v[k]) + 1) if r[k] < n < v[k]})
        last = None
        for s0, s1 in zip(cuts, cuts[1:]):
            mid = 0.5 * (s0 + s1)
            Eb, mb = ebin(i, 74 - min(int(math.floor(mid)), 74))
            seg["lin"].append(k + 1); seg["bin"].append(bin3(mid)); seg["a0"].append(s0 - o[k]); seg["a1"].append(s1 - o[k])
            seg["E"].append(Eb); seg["miss"].append(mb)
            last = (bin3(mid), Eb, mb)
        if last is None:  # zero-length post-entry interval cannot occur after rounding rules
            raise ValueError("empty post-entry interval")
        term_bin.append(last[0]); term_a.append(v[k] - o[k]); term_E.append(last[1]); term_miss.append(last[2])
    pre = dict(lin=[], bin=[], a0=[], a1=[])
    for k in coh:
        cuts = sorted({o[k], C} | {float(n) for n in range(math.ceil(o[k]), math.floor(C) + 1) if o[k] < n < C})
        for s0, s1 in zip(cuts, cuts[1:]):
            pre["lin"].append(k + 1); pre["bin"].append(bin3(0.5 * (s0 + s1)))
            pre["a0"].append(s0 - o[k]); pre["a1"].append(s1 - o[k])
    cohset = set(coh)
    pairs = [(parent[k] - 1, k) for k in coh if parent[k] > 0 and parent[k] - 1 in cohset]
    paired = {a for a, _ in pairs} | {b for _, b in pairs}
    assert len({a for a, _ in pairs}) == len(pairs), "a cohort parent with two cohort daughters is not supported"
    singles = [k for k in coh if k not in paired]
    t, w = np.polynomial.hermite.hermgauss(CFG["quadrature_nodes"])
    data = dict(N=N, parent=parent, o=o, v=v, r=r, ext=ext, bif=bif, mplus=mplus,
                S=len(seg["lin"]), seg_lin=seg["lin"], seg_bin=seg["bin"], seg_a0=seg["a0"], seg_a1=seg["a1"],
                seg_E=seg["E"], seg_miss=seg["miss"], term_bin=term_bin, term_a=term_a, term_E=term_E, term_miss=term_miss,
                SP=len(pre["lin"]), pre_lin=pre["lin"], pre_bin=pre["bin"], pre_a0=pre["a0"], pre_a1=pre["a1"], c=C,
                NC=len(coh), coh=[k + 1 for k in coh], C1=len(singles), c1_lin=[k + 1 for k in singles],
                C2=len(pairs), c2_par=[a + 1 for a, _ in pairs], c2_dau=[b + 1 for _, b in pairs],
                Q=len(t), gh_t=list(t), gh_w=list(w))
    return data


# ---------------------------------------------------------------- independent Python target
def pieces(d, p):
    k = math.exp(p["log_k"])
    x = np.zeros(d["N"])
    for i in range(d["N"]):
        x[i] = p["sigma"] * p["eps"][i] if d["parent"][i] == 0 else \
            p["rho"] * x[d["parent"][i] - 1] + p["sigma"] * math.sqrt(1 - p["rho"] ** 2) * p["eps"][i]
    A = np.zeros(d["N"])
    for s in range(d["SP"]):
        A[d["pre_lin"][s] - 1] += math.exp(p["log_h0"][d["pre_bin"][s] - 1] + p["gamma"]) * (d["pre_a1"][s] ** k - d["pre_a0"][s] ** k)
    return k, x, A


def log_surv_pre(x, sig, A, b0, kb, dpre):
    lz = x - 0.5 * sig ** 2
    return -np.exp(lz) * A - b0 * np.exp(kb * lz) * dpre


def log_norm_gh(d, p, A):
    """Sum over components of log pi, by Gauss-Hermite quadrature."""
    t, w = np.array(d["gh_t"]), np.array(d["gh_w"])
    sig, rho, b0, kb = p["sigma"], p["rho"], math.exp(p["log_b0"]), p["kappa_b"]
    total = 0.0
    for i in d["c1_lin"]:
        i -= 1
        total += math.log(np.sum(w / math.sqrt(math.pi) * np.exp(log_surv_pre(math.sqrt(2) * sig * t, sig, A[i], b0, kb, d["c"] - d["o"][i]))))
    for ip, idd in zip(d["c2_par"], d["c2_dau"]):
        ip, idd = ip - 1, idd - 1
        xp = math.sqrt(2) * sig * t
        sp = np.exp(log_surv_pre(xp, sig, A[ip], b0, kb, d["c"] - d["o"][ip]))
        xd = rho * xp[:, None] + math.sqrt(2) * sig * math.sqrt(1 - rho ** 2) * t[None, :]
        sd_ = np.exp(log_surv_pre(xd, sig, A[idd], b0, kb, d["c"] - d["o"][idd]))
        total += math.log(np.sum((w[:, None] * w[None, :] / math.pi) * sp[:, None] * sd_))
    return total


def log_norm_mc(d, p, A, n, seed):
    rng = np.random.default_rng(seed)
    sig, rho, b0, kb = p["sigma"], p["rho"], math.exp(p["log_b0"]), p["kappa_b"]
    out = []
    for i in d["c1_lin"]:
        i -= 1
        s = np.exp(log_surv_pre(sig * rng.standard_normal(n), sig, A[i], b0, kb, d["c"] - d["o"][i]))
        out.append((float(s.mean()), float(s.std() / math.sqrt(n))))
    for ip, idd in zip(d["c2_par"], d["c2_dau"]):
        ip, idd = ip - 1, idd - 1
        xp = sig * rng.standard_normal(n)
        xd = rho * xp + sig * math.sqrt(1 - rho ** 2) * rng.standard_normal(n)
        s = np.exp(log_surv_pre(xp, sig, A[ip], b0, kb, d["c"] - d["o"][ip]) + log_surv_pre(xd, sig, A[idd], b0, kb, d["c"] - d["o"][idd]))
        out.append((float(s.mean()), float(s.std() / math.sqrt(n))))
    return out


def python_target(d, p):
    k, x, A = pieces(d, p)
    sig, lam0, b0 = p["sigma"], math.exp(p["log_lambda0"]), math.exp(p["log_b0"])
    lz = x - 0.5 * sig ** 2
    h = np.array(p["log_h0"])
    lp = -0.5 * (h[0] - math.log(0.065)) ** 2 - 24 * math.log(p["tau"]) - 0.5 * np.sum(((h[1:] - h[:-1]) / p["tau"]) ** 2)
    lp += -0.5 * (p["tau"] / 0.5) ** 2 - 0.5 * (p["log_k"] / 0.5) ** 2 - 0.5 * (p["log_lambda0"] - math.log(0.0708)) ** 2
    lp += -0.5 * p["kappa"] ** 2 - 0.5 * (p["log_b0"] - math.log(0.0082)) ** 2 - 0.5 * p["kappa_b"] ** 2
    lp += -0.5 * p["beta"] ** 2 - 0.5 * p["gamma"] ** 2 - 0.5 * sig ** 2 - 0.5 * float(np.sum(np.array(p["eps"]) ** 2))
    cum = np.zeros(d["N"])
    for s in range(d["S"]):
        cum[d["seg_lin"][s] - 1] += math.exp(h[d["seg_bin"][s] - 1] + p["beta"] * d["seg_E"][s] + p["gamma"] * d["seg_miss"][s]) \
            * (d["seg_a1"][s] ** k - d["seg_a0"][s] ** k)
    for i in range(d["N"]):
        dp = d["v"][i] - d["r"][i]
        lp += -math.exp(lz[i]) * cum[i] - b0 * math.exp(p["kappa_b"] * lz[i]) * dp
        if d["ext"][i]:
            lp += lz[i] + h[d["term_bin"][i] - 1] + p["log_k"] + (k - 1) * math.log(d["term_a"][i]) \
                + p["beta"] * d["term_E"][i] + p["gamma"] * d["term_miss"][i]
        if d["bif"][i]:
            lp += p["log_b0"] + p["kappa_b"] * lz[i]
        lp += d["mplus"][i] * (p["log_lambda0"] + p["kappa"] * lz[i]) - lam0 * math.exp(p["kappa"] * lz[i]) * dp
    for i in d["coh"]:
        i -= 1
        lp += float(log_surv_pre(x[i], sig, A[i], b0, p["kappa_b"], d["c"] - d["o"][i]))
    lp -= log_norm_gh(d, p, A)
    return lp


# ---------------------------------------------------------------- runs
def dataset(seed):
    L, ginfo = generate(seed)
    if ginfo["capped"]:
        return None, ginfo, None
    obsd, oinfo = observe(L, seed)
    return adapt(obsd), ginfo, oinfo


def model():
    import cmdstanpy
    cmdstanpy.set_cmdstan_path(str(CMDSTAN))
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / "model.stan"
    if not src.exists() or src.read_text() != (HERE / "model.stan").read_text():
        src.write_text((HERE / "model.stan").read_text())
    return cmdstanpy.CmdStanModel(stan_file=str(src))


def test_point(d, j):
    rng = np.random.default_rng(300 + j)
    return dict(log_h0=list(np.log(0.065) + 0.2 * rng.standard_normal(25)), tau=[0.2, 0.35][j],
                log_k=[0.05, -0.1][j], log_lambda0=math.log([0.07, 0.08][j]), kappa=[0.1, -0.2][j],
                log_b0=math.log([0.008, 0.01][j]), kappa_b=[0.2, -0.1][j], beta=[0.1, -0.2][j], gamma=[0.05, -0.1][j],
                sigma=[0.5, 0.8][j], rho=[0.4, 0.7][j], eps=list(rng.standard_normal(d["N"])))


def checks():
    out = {}
    for label, seed in (("frozen_seed", CFG["seed"]), ("fit_seed", CFG["fit_seed"])):
        out[label] = check_one(seed)
    (HERE / "checks.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


def check_one(seed):
    t0 = time.time()
    d, ginfo, oinfo = dataset(seed)
    res = dict(seed=seed, generator=ginfo, observation=oinfo, seconds_generate_observe_adapt=round(time.time() - t0, 2))
    if d is None:
        return res
    res["adapted"] = dict(N=d["N"], segments=d["S"], pre_segments=d["SP"], cohort=d["NC"], singles=d["C1"], pairs=d["C2"],
                          ext=sum(d["ext"]), bif=sum(d["bif"]), buds_after_entry=sum(d["mplus"]),
                          missing_share_segments=round(float(np.mean(d["seg_miss"])), 3))
    # normaliser: quadrature against Monte Carlo at two parameter points
    norm = []
    for j in range(2):
        p = test_point(d, j)
        _, _, A = pieces(d, p)
        gh = log_norm_gh(d, p, A)
        mc = log_norm_mc(d, p, A, 1_000_000, 900 + j)
        mc_log = sum(math.log(m) for m, _ in mc)
        mc_se = math.sqrt(sum((s / m) ** 2 for m, s in mc))
        norm.append(dict(point=j, log_pi_gh=round(gh, 8), log_pi_mc=round(mc_log, 8), mc_se_log=round(mc_se, 8),
                         z=round((gh - mc_log) / mc_se, 2) if mc_se > 0 else None))
        assert mc_se == 0 or abs(gh - mc_log) < 4 * mc_se, norm[-1]
    res["normaliser_gh_vs_mc"] = norm
    # Stan target against the independent Python target, as a difference of two points
    mdl = model()
    pts = [test_point(d, j) for j in range(2)]
    stan_lp = [float(mdl.log_prob(p, data=d, jacobian=False, sig_figs=15)["lp__"].iloc[0]) for p in pts]
    py_lp = [python_target(d, p) for p in pts]
    diff_s, diff_p = stan_lp[0] - stan_lp[1], py_lp[0] - py_lp[1]
    res["logdensity_difference"] = dict(stan=round(diff_s, 8), python=round(float(diff_p), 8), abs_err=float(abs(diff_s - diff_p)))
    assert abs(diff_s - diff_p) < 1e-7 * max(1.0, abs(diff_p)), res["logdensity_difference"]
    return res


def fit():
    d, ginfo, oinfo = dataset(CFG["fit_seed"])
    assert d is not None, "capped dataset"
    mdl = model()
    s, lim = CFG["sampler"], CFG["compute_limit"]
    t0 = time.time()
    row = dict(seed=CFG["fit_seed"], N=d["N"], observation=oinfo)
    try:
        f = mdl.sample(data=d, chains=s["chains"], parallel_chains=lim["parallel_chains"], iter_warmup=s["iter_warmup"],
                       iter_sampling=s["iter_sampling"], adapt_delta=s["adapt_delta"], max_treedepth=s["max_treedepth"],
                       seed=s["seed"], show_progress=False, output_dir=str(OUT / "fit"), timeout=lim["fit_timeout_seconds"])
    except TimeoutError:
        row.update(status="timeout", seconds=round(time.time() - t0, 1))
        (HERE / "fit_result.json").write_text(json.dumps(row, indent=1) + "\n")
        print(row); return
    secs = time.time() - t0
    dr = f.draws_pd()
    summ = f.summary()
    rh = [c for c in summ.columns if c.lower().startswith("r_hat")][0]
    ess = [c for c in summ.columns if c.lower() in ("ess_bulk", "n_eff")][0]
    core = ["sigma", "rho", "eta", "kappa", "kappa_b", "beta", "gamma", "log_k", "log_lambda0", "log_b0", "tau"]
    g = CFG["generator"]
    truth = dict(sigma=g["sigma"], rho=g["rho"], eta=g["sigma"] * g["rho"], kappa=g["kappa"], kappa_b=g["kappa_b"],
                 beta=g["beta"], log_k=0.0, log_lambda0=math.log(g["lambda0"]), log_b0=math.log(g["b0"]))
    row.update(status="fitted", seconds=round(secs, 1), divergences=int(f.method_variables()["divergent__"].sum()),
               treedepth_hits=int((dr["treedepth__"] >= s["max_treedepth"]).sum()),
               max_rhat_core=round(float(summ.loc[core, rh].max()), 4), min_ess_core=round(float(summ.loc[core, ess].min()), 0),
               max_rhat_all=round(float(summ[rh].max()), 4), min_ess_all=round(float(summ[ess].min()), 0))
    row["intervals_90"] = {v: [round(float(q), 3) for q in np.quantile(dr[v], [0.05, 0.5, 0.95])] + [truth.get(v)]
                           for v in core}
    (HERE / "fit_result.json").write_text(json.dumps(row, indent=1) + "\n")
    print(json.dumps(row, indent=1))


if __name__ == "__main__":
    {"checks": checks, "fit": fit}[sys.argv[1]]()
