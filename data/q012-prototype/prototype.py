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

import importlib.util

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("quadrature", HERE / "quadrature.py")
QD = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(QD)
ROOT = HERE.parents[1]
CFG = json.loads((HERE / "config.json").read_text())
OUT = ROOT / "scratch/q012-prototype"
CMDSTAN = pathlib.Path.home() / ".cmdstan/cmdstan-2.38.0"
H = 75.0
C = 75.0 - 66.05


# ---------------------------------------------------------------- generator
def h0_at(u, h0):
    return h0[min(int((H - u) // 3), 24)]


def generate(seed, overrides=None):
    g = dict(CFG["generator"], **(overrides or {}))
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
    tO, tE, cnt = round_dates(L, ids, par)
    label = end_labels(ids, par, tO, tE)
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


def end_labels(ids, par, tO, tE):
    """End labels from recorded data only: daughters starting exactly at a parent's end."""
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
    return label


def round_dates(L, ids, par):
    """Round recorded dates to 0.01 Ma under the declared precedence (finite contract 8.2, as
    corrected after Codex 76/1720 and 76/1737):
    1. present censors stay at 0; an observed termination that rounds to 0 keeps its label and
       becomes 0.005 Ma;
    2. a shared event (a parent's end and its attached daughters' origins at the same true time)
       is rounded once and moved as one time;
    3. a short interval moves its origin older to end + 0.005; for a shared-event daughter the
       whole event moves;
    4. links must satisfy parent end <= daughter origin <= parent origin; a daughter older than its
       parent becomes a tie; any component still violating a constraint keeps unrounded dates."""
    groups = {}
    for i in ids:
        p = par[i]
        if p >= 0 and L[i]["o"] == L[p]["end"]:
            groups.setdefault(p, []).append(i)
    in_group = {d: p for p, ds in groups.items() for d in ds}
    cnt = dict(short_interval_moves=0, shared_event_moves=0, origin_ties=0, ext_near_present=0,
               fallback_components=0)
    tO, tE = {}, {}
    for i in ids:
        tO[i] = round(H - L[i]["o"], 2)
        if L[i]["end"] >= H:
            tE[i] = 0.0
        else:
            e = round(H - L[i]["end"], 2)
            if e == 0.0:
                e = 0.005
                cnt["ext_near_present"] += 1
            tE[i] = e
    for p, ds in groups.items():
        for d in ds:
            tO[d] = tE[p]

    def unround(comp):
        for j in comp:
            tO[j] = H - L[j]["o"]
            tE[j] = 0.0 if L[j]["end"] >= H else H - L[j]["end"]
        for pp, ds in groups.items():  # keep shared events shared after unrounding
            if pp in comp:
                for d in ds:
                    tO[d] = tE[pp]

    for _ in range(5):
        changed = False
        for i in sorted(ids, key=lambda j: L[j]["o"]):
            if tO[i] > tE[i]:
                continue
            if i in in_group:
                p = in_group[i]
                tE[p] = round(tE[i] + 0.005, 3)
                for d in groups[p]:
                    tO[d] = tE[p]
                cnt["shared_event_moves"] += 1
            else:
                tO[i] = round(tE[i] + 0.005, 3)
                cnt["short_interval_moves"] += 1
            changed = True
        for i in sorted(ids, key=lambda j: L[j]["o"]):
            p = par[i]
            if p < 0:
                continue
            if tO[i] > tO[p]:
                tO[i] = tO[p]
                cnt["origin_ties"] += 1
                changed = True
            comp = {p} | set(groups.get(p, [])) | {i}
            if not (tO[i] > tE[i] and tO[p] > tE[p] and tE[p] <= tO[i] <= tO[p]):
                unround(comp)
                cnt["fallback_components"] += 1
                changed = True
        if not changed:
            break
    for i in ids:  # final validation: every constraint holds
        assert tO[i] > tE[i], ("duration", i)
        if par[i] >= 0:
            assert tE[par[i]] <= tO[i] <= tO[par[i]], ("link", i)
    return tO, tE, cnt


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
    seg_start, seg_len = [], []
    term_bin, term_a, term_E, term_miss = [], [], [], []
    for k, i in enumerate(order):
        seg_start.append(len(seg["lin"]) + 1)
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
        seg_len.append(len(seg["lin"]) + 1 - seg_start[-1])
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
    VER = CFG[CFG.get("active", "v2")]
    t, w = np.polynomial.hermite.hermgauss(VER["quadrature_nodes"])
    data = dict(N=N, parent=parent, o=o, v=v, r=r, ext=ext, bif=bif, mplus=mplus,
                S=len(seg["lin"]), seg_lin=seg["lin"], seg_start=seg_start, seg_len=seg_len, seg_bin=seg["bin"], seg_a0=seg["a0"], seg_a1=seg["a1"],
                seg_E=seg["E"], seg_miss=seg["miss"], term_bin=term_bin, term_a=term_a, term_E=term_E, term_miss=term_miss,
                SP=len(pre["lin"]), pre_lin=pre["lin"], pre_bin=pre["bin"], pre_a0=pre["a0"], pre_a1=pre["a1"], c=C,
                NC=len(coh), coh=[k + 1 for k in coh], C1=len(singles), c1_lin=[k + 1 for k in singles],
                C2=len(pairs), c2_par=[a + 1 for a, _ in pairs], c2_dau=[b + 1 for _, b in pairs],
                Q=len(t), gh_t=list(t), gh_w=list(w))
    if "solver" in VER:
        data.update(solver_data(VER["solver"]), check_tol=VER["check_tol"])
    return data


def solver_data(sv):
    """Stan data for the mode solver: Newton (v3) takes a step tolerance, Powell (v4) a relative solution tolerance."""
    tol = {"solver_rel_tol": sv["rel_tol"]} if "rel_tol" in sv else {"solver_step_tol": sv["step_tol"]}
    return dict(tol, solver_f_tol=sv["f_tol"], solver_max_steps=sv["max_steps"])


# ---------------------------------------------------------------- independent Python target
def log_h0_of(p):
    if "log_h0" in p:
        return np.array(p["log_h0"])
    h = [p["log_h0_1"]]
    for zz in p["z_rw"]:
        h.append(h[-1] + p["tau"] * zz)
    return np.array(h)


def pieces(d, p):
    k = math.exp(p["log_k"])
    h = log_h0_of(p)
    x = np.zeros(d["N"])
    for i in range(d["N"]):
        x[i] = p["sigma"] * p["eps"][i] if d["parent"][i] == 0 else \
            p["rho"] * x[d["parent"][i] - 1] + p["sigma"] * math.sqrt(1 - p["rho"] ** 2) * p["eps"][i]
    A = np.zeros(d["N"])
    for s in range(d["SP"]):
        A[d["pre_lin"][s] - 1] += math.exp(h[d["pre_bin"][s] - 1] + p["gamma"]) * (d["pre_a1"][s] ** k - d["pre_a0"][s] ** k)
    return k, x, A


def log_surv_pre(x, sig, A, b0, kb, dpre):
    lz = x - 0.5 * sig ** 2
    return -np.exp(lz) * A - b0 * np.exp(kb * lz) * dpre


def cohort_terms(d, p, A):
    b0 = math.exp(p["log_b0"])
    singles = [(A[i - 1], b0 * (d["c"] - d["o"][i - 1])) for i in d["c1_lin"]]
    pairs = [(A[a - 1], b0 * (d["c"] - d["o"][a - 1]), A[b - 1], b0 * (d["c"] - d["o"][b - 1]))
             for a, b in zip(d["c2_par"], d["c2_dau"])]
    return singles, pairs


def log_norm_agh(d, p, A, Q=None):
    t, w = (np.array(d["gh_t"]), np.array(d["gh_w"])) if Q is None else np.polynomial.hermite.hermgauss(Q)
    s, pr = cohort_terms(d, p, A)
    sig, rho, kb = p["sigma"], p["rho"], p["kappa_b"]
    return sum(QD.log_pi_1d(sig, a, b, kb, t, w) for a, b in s) + sum(QD.log_pi_2d(sig, rho, *c, kb, t, w) for c in pr)


def log_norm_ref(d, p, A, n=1600):
    s, pr = cohort_terms(d, p, A)
    sig, rho, kb = p["sigma"], p["rho"], p["kappa_b"]
    return sum(QD.reference_1d(sig, a, b, kb, n) for a, b in s) + sum(QD.reference_2d(sig, rho, *c, kb, n) for c in pr)


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
    """Independent implementation of model_v2.stan (normal priors without constants)."""
    k, x, A = pieces(d, p)
    h = log_h0_of(p)
    sig, lam0, b0 = p["sigma"], math.exp(p["log_lambda0"]), math.exp(p["log_b0"])
    lz = x - 0.5 * sig ** 2
    lp = -0.5 * (p["log_h0_1"] - math.log(0.065)) ** 2 - 0.5 * float(np.sum(np.array(p["z_rw"]) ** 2))
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
    lp -= log_norm_agh(d, p, A)
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
    name = CFG[CFG.get("active", "v2")]["stan_file"]
    src = OUT / name
    if not src.exists() or src.read_text() != (HERE / name).read_text():
        src.write_text((HERE / name).read_text())
    return cmdstanpy.CmdStanModel(stan_file=str(src))


def test_point(d, j):
    rng = np.random.default_rng(300 + j)
    tau = [0.2, 0.35][j]
    h = np.log(0.065) + 0.2 * rng.standard_normal(25)
    return dict(log_h0_1=float(h[0]), z_rw=list((h[1:] - h[:-1]) / tau), tau=tau,
                log_k=[0.05, -0.1][j], log_lambda0=math.log([0.07, 0.08][j]), kappa=[0.1, -0.2][j],
                log_b0=math.log([0.008, 0.01][j]), kappa_b=[0.2, -0.1][j], beta=[0.1, -0.2][j], gamma=[0.05, -0.1][j],
                sigma=[0.5, 0.8][j], rho=[0.4, 0.7][j], eps=list(rng.standard_normal(d["N"])))


def stress_points(d):
    b = test_point(d, 0)
    return {"central0": b, "central1": test_point(d, 1),
            "stress_s3_r09_kbm15": dict(b, sigma=3.0, rho=0.9, kappa_b=-1.5),
            "stress_s18_r09_kbm15": dict(b, sigma=1.8, rho=0.9, kappa_b=-1.5),
            "stress_s3_r09_kbp15": dict(b, sigma=3.0, rho=0.9, kappa_b=1.5),
            "small_sigma": dict(b, sigma=0.05)}


def saved_draws(n=40):
    """A fixed subset of saved states from the v1 fit (evenly spaced over all chains)."""
    import pandas as pd
    files = sorted((OUT / "fit").glob("*.csv"))
    df = pd.concat([pd.read_csv(f, comment="#") for f in files], ignore_index=True)
    idx = np.linspace(0, len(df) - 1, n).astype(int)
    out = []
    for i in idx:
        r = df.iloc[i]
        out.append(dict(log_h0=[float(r[f"log_h0.{j}"]) for j in range(1, 26)], log_k=float(r["log_k"]), gamma=float(r["gamma"]),
                        log_b0=float(r["log_b0"]), kappa_b=float(r["kappa_b"]), sigma=float(r["sigma"]), rho=float(r["rho"]),
                        eps=[0.0] * 1))
    return out


def gate(d, p, h=1e-4):
    """AGH against the dense Simpson reference: value and d/dsigma, d/dkappa_b (and d/drho with a pair)."""
    def val(q, ref):
        A = cohort_A(d, q)
        return log_norm_ref(d, q, A) if ref else log_norm_agh(d, q, A)
    res = dict(log_err=abs(val(p, False) - val(p, True)))
    for name in ("sigma", "kappa_b") + (("rho",) if d["C2"] else ()):
        hi, lo = dict(p, **{name: p[name] + h}), dict(p, **{name: p[name] - h})
        da = (val(hi, False) - val(lo, False)) / (2 * h)
        dr = (val(hi, True) - val(lo, True)) / (2 * h)
        res[f"d_{name}_err"] = abs(da - dr)
    return res


def cohort_A(d, p):
    k = math.exp(p["log_k"])
    hh = log_h0_of(p)
    A = np.zeros(d["N"])
    for s in range(d["SP"]):
        A[d["pre_lin"][s] - 1] += math.exp(hh[d["pre_bin"][s] - 1] + p["gamma"]) * (d["pre_a1"][s] ** k - d["pre_a0"][s] ** k)
    return A


def rounding_fixtures():
    """Codex 76/1737: shared bifurcation event with a short daughter; an extinction near the present."""
    Ma = lambda a: H - a
    L = [dict(parent=-1, o=Ma(10.0), end=Ma(1.004), cause="bif"),
         dict(parent=0, o=Ma(1.004), end=Ma(1.001), cause="ext"),
         dict(parent=0, o=Ma(1.004), end=H, cause="cens"),
         dict(parent=-1, o=Ma(5.0), end=Ma(0.003), cause="ext")]
    L[1]["o"] = L[0]["end"]; L[2]["o"] = L[0]["end"]
    ids, par = [0, 1, 2, 3], [-1, 0, 0, -1]
    tO, tE, cnt = round_dates(L, ids, par)
    lab = end_labels(ids, par, tO, tE)
    got = dict(A=(tO[0], tE[0], lab[0]), B=(tO[1], tE[1], lab[1]), D=(tO[2], tE[2], lab[2]), E=(tO[3], tE[3], lab[3]))
    want = dict(A=(10.0, 1.005, "bif"), B=(1.005, 1.0, "ext"), D=(1.005, 0.0, "present"), E=(5.0, 0.005, "ext"))
    ok = all(abs(got[k][0] - want[k][0]) < 1e-12 and abs(got[k][1] - want[k][1]) < 1e-12 and got[k][2] == want[k][2] for k in want)
    assert ok, got
    return dict(result=got, counts=cnt, budding_links_from_B_or_D=0)


def unconstrained_target(d, p):
    """Python target plus the log Jacobian of Stan's transforms (sigma, tau: log; rho: logit)."""
    return python_target(d, p) + math.log(p["sigma"]) + math.log(p["tau"]) + math.log(p["rho"]) + math.log(1 - p["rho"])


def fd_unconstrained(d, p, name, h=1e-6, idx=None):
    def shift(q, s):
        q = dict(q)
        if name in ("sigma", "tau"):
            q[name] = q[name] * math.exp(s)
        elif name == "rho":
            u = math.log(q["rho"] / (1 - q["rho"])) + s
            q["rho"] = 1 / (1 + math.exp(-u))
        elif idx is not None:
            v = list(q[name]); v[idx] += s; q[name] = v
        else:
            q[name] = q[name] + s
        return q
    return (unconstrained_target(d, shift(p, h)) - unconstrained_target(d, shift(p, -h))) / (2 * h)


def stan_grads(mdl, d, p):
    df = mdl.log_prob(p, data=d, jacobian=True, sig_figs=15)
    return df.iloc[0].to_dict()


def gradient_check(mdl, d, p):
    g = stan_grads(mdl, d, p)
    coh_eps = d["coh"][0]  # a cohort lineage: its frailty enters the pre-entry survival and the normaliser
    rows = {}
    for name, col, idx in (("sigma", "g_sigma", None), ("rho", "g_rho", None), ("kappa_b", "g_kappa_b", None),
                           ("log_h0_1", "g_log_h0_1", None), ("log_k", "g_log_k", None), ("gamma", "g_gamma", None),
                           ("log_b0", "g_log_b0", None), ("tau", "g_tau", None), ("eps", f"g_eps.{coh_eps}", coh_eps - 1)):
        fd = fd_unconstrained(d, p, name, idx=idx)
        rows[col] = dict(stan=round(g[col], 7), fd=round(fd, 7), abs_err=abs(g[col] - fd))
    ok = all(r["abs_err"] <= 1e-4 * max(1.0, abs(r["fd"])) for r in rows.values())
    return rows, ok


def solver_stability(mdl, d, p):
    dt = dict(d, **solver_data(CFG[CFG["active"]]["solver_tight"]))
    a = float(mdl.log_prob(p, data=d, jacobian=False, sig_figs=15)["lp__"].iloc[0])
    b = float(mdl.log_prob(p, data=dt, jacobian=False, sig_figs=15)["lp__"].iloc[0])
    return dict(lp_default=round(a, 10), lp_tight=round(b, 10), abs_diff=abs(a - b))


def gradient_benchmark(d, reps=200):
    """Repeated log-density-and-gradient evaluations at identical points: the comparison version against the active one."""
    import subprocess
    import cmdstanpy
    from cmdstanpy.utils import write_stan_json
    work = OUT / "bench"
    work.mkdir(parents=True, exist_ok=True)
    ver_a, ver_b = CFG[CFG["active"]].get("benchmark_against", "v2"), CFG["active"]
    base = {k: v for k, v in d.items() if not k.startswith("solver_")}
    data_files = {}
    for ver in (ver_a, ver_b):
        data_files[ver] = work / f"data_{ver}.json"
        write_stan_json(str(data_files[ver]), dict(base, **solver_data(CFG[ver]["solver"])) if "solver" in CFG[ver] else base)
    src = sorted((OUT / "fit_v2").glob("*_1.csv"))[0]
    lines = src.read_text().splitlines()
    head = [l for l in lines if l.startswith("#")][:60]
    hdr_i = next(i for i, l in enumerate(lines) if not l.startswith("#"))
    header = lines[hdr_i].split(",")
    body = [l for l in lines[hdr_i + 1:] if l and not l.startswith("#")]
    pts = {"saved_draw_a": body[100].split(","), "saved_draw_b": body[500].split(",")}
    st = list(body[100].split(","))
    for k, v in (("sigma", "3.0"), ("rho", "0.9"), ("kappa_b", "-1.5")):
        st[header.index(k)] = v
    pts["stress_from_saved_a"] = st
    exes = {ver: OUT / CFG[ver]["stan_file"].removesuffix(".stan") for ver in (ver_a, ver_b)}
    res = {}
    for pname, row in pts.items():
        res[pname] = {}
        for n in (1, reps):
            f = work / f"{pname}_{n}.csv"
            f.write_text("\n".join(head + [",".join(header)] + [",".join(row)] * n) + "\n")
        for ver, exe in exes.items():
            times = {}
            for n in (1, reps):
                t0 = time.time()
                r = subprocess.run([str(exe), "log_prob", f"constrained_params={work / f'{pname}_{n}.csv'}", "jacobian=1",
                                    "data", f"file={data_files[ver]}", "output", f"file={work / f'out_{ver}_{pname}_{n}.csv'}"],
                                   capture_output=True, text=True)
                times[n] = time.time() - t0
                if r.returncode != 0:
                    times[n] = None
                    res[pname][ver + "_error"] = (r.stdout + r.stderr)[-300:]
            if None not in times.values():
                res[pname][ver + "_ms_per_gradient"] = round(1000 * (times[reps] - times[1]) / (reps - 1), 3)
        if f"{ver_a}_ms_per_gradient" in res[pname] and f"{ver_b}_ms_per_gradient" in res[pname]:
            res[pname][f"{ver_b}_over_{ver_a}"] = round(res[pname][f"{ver_b}_ms_per_gradient"] / res[pname][f"{ver_a}_ms_per_gradient"], 3)
    return res


def checks_solver():
    VER = CFG[CFG["active"]]
    out = dict(rounding_fixtures=rounding_fixtures())
    mdl = model()
    for label, seed in (("frozen_seed", CFG["seed"]), ("fit_seed", CFG["fit_seed"])):
        d, ginfo, oinfo = dataset(seed)
        r = dict(seed=seed, observation=oinfo, adapted=dict(N=d["N"], cohort=d["NC"], singles=d["C1"], pairs=d["C2"]))
        sp = stress_points(d)
        sp.update({"small_sigma_002": dict(sp["central0"], sigma=0.02), "near_one_rho_099": dict(sp["central0"], rho=0.99),
                   "near_one_rho_0999_s3": dict(sp["central0"], rho=0.999, sigma=3.0)})
        G = {k: gate(d, p) for k, p in sp.items()}
        if label == "fit_seed":
            gs = [gate(d, q) for q in saved_draws(40)]
            G["saved_draws_40_max"] = {k: max(g[k] for g in gs) for k in gs[0]}
        r["precision_gate"] = {k: {kk: float(f"{vv:.3g}") for kk, vv in g.items()} for k, g in G.items()}
        r["precision_gate_pass"] = all(g["log_err"] <= 1e-4 and all(v <= 1e-3 for kk, v in g.items() if kk.startswith("d_")) for g in G.values())
        q = sp["near_one_rho_0999_s3"]
        A = cohort_A(d, q)
        r["reference_precision_extreme"] = dict(n1600=round(log_norm_ref(d, q, A, 1600), 10), n3200=round(log_norm_ref(d, q, A, 3200), 10))
        names = ["central0", "central1", "stress_s3_r09_kbm15", "near_one_rho_0999_s3"]
        slp = {n: float(mdl.log_prob(sp[n], data=d, jacobian=False, sig_figs=15)["lp__"].iloc[0]) for n in names}
        plp = {n: python_target(d, sp[n]) for n in names}
        r["stan_vs_python_lp_differences"] = {f"central0-{n}": abs((slp["central0"] - slp[n]) - (plp["central0"] - plp[n])) for n in names[1:]}
        r["solver_stability"] = {n: solver_stability(mdl, d, sp[n]) for n in ("central0", "stress_s3_r09_kbm15")}
        r["automatic_gradients"] = {}
        ok_all = True
        for n in ("central0", "stress_s3_r09_kbm15"):
            rows, ok = gradient_check(mdl, d, sp[n])
            r["automatic_gradients"][n] = rows
            ok_all &= ok
        r["automatic_gradients_pass"] = ok_all
        out[label] = r
    d, _, _ = dataset(CFG["fit_seed"])
    out["gradient_benchmark"] = gradient_benchmark(d)
    passed = all(out[k]["precision_gate_pass"] and out[k]["automatic_gradients_pass"] for k in ("frozen_seed", "fit_seed")) and \
        all(v < 1e-6 for k in ("frozen_seed", "fit_seed") for v in out[k]["stan_vs_python_lp_differences"].values()) and \
        all(s["abs_diff"] < 1e-8 for k in ("frozen_seed", "fit_seed") for s in out[k]["solver_stability"].values())
    if "probes" in VER:
        paths, starts = make_inits(d)
        out["probes"] = probes(d, starts)
        out["smoke"] = smoke(paths) if out["probes"]["pass"] else "not run: probes failed"
        passed = passed and out["probes"]["pass"] and isinstance(out["smoke"], dict) and out["smoke"]["pass"]
    out["all_prefit_checks_pass"] = passed
    (HERE / VER["checks_file"]).write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(out, indent=1, default=float))


def checks():
    if CFG.get("active") in ("v3", "v4"):
        return checks_solver()
    out = dict(rounding_fixtures=rounding_fixtures())
    for label, seed in (("frozen_seed", CFG["seed"]), ("fit_seed", CFG["fit_seed"])):
        out[label] = check_one(seed, saved=(label == "fit_seed"))
    (HERE / CFG["v2"]["checks_file"]).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


def check_one(seed, saved=False):
    t0 = time.time()
    d, ginfo, oinfo = dataset(seed)
    res = dict(seed=seed, generator=ginfo, observation=oinfo, seconds_generate_observe_adapt=round(time.time() - t0, 2))
    if d is None:
        return res
    res["adapted"] = dict(N=d["N"], segments=d["S"], pre_segments=d["SP"], cohort=d["NC"], singles=d["C1"], pairs=d["C2"],
                          ext=sum(d["ext"]), bif=sum(d["bif"]), buds_after_entry=sum(d["mplus"]),
                          missing_share_segments=round(float(np.mean(d["seg_miss"])), 3))
    # reference convergence (its own numerical error)
    p0 = stress_points(d)["stress_s3_r09_kbm15"]
    A0 = cohort_A(d, p0)
    res["reference_convergence"] = dict(n800=round(log_norm_ref(d, p0, A0, 800), 10), n1600=round(log_norm_ref(d, p0, A0, 1600), 10),
                                        n3200=round(log_norm_ref(d, p0, A0, 3200), 10))
    # precision gate: |log pi error| <= 1e-4 and derivative errors <= 1e-3
    G = {k: gate(d, p) for k, p in stress_points(d).items()}
    if saved:
        sd = saved_draws(40)
        gs = [gate(d, q) for q in sd]
        G["saved_draws_40_max"] = {k: max(g[k] for g in gs) for k in gs[0]}
    res["precision_gate"] = {k: {kk: float(f"{vv:.3g}") for kk, vv in g.items()} for k, g in G.items()}
    res["precision_gate_pass"] = all(g["log_err"] <= 1e-4 and all(v <= 1e-3 for kk, v in g.items() if kk.startswith("d_")) for g in G.values())
    assert res["precision_gate_pass"], res["precision_gate"]
    # Monte Carlo cross-check at the central points
    mcs = []
    for j in range(2):
        p = test_point(d, j)
        A = cohort_A(d, p)
        ag = log_norm_agh(d, p, A)
        mc = log_norm_mc(d, p, A, 1_000_000, 900 + j)
        mc_log = sum(math.log(m) for m, _ in mc)
        mc_se = math.sqrt(sum((s / m) ** 2 for m, s in mc))
        mcs.append(dict(point=j, log_pi_agh=round(ag, 8), log_pi_mc=round(mc_log, 8), z=round((ag - mc_log) / mc_se, 2)))
        assert abs(ag - mc_log) < 4 * mc_se
    res["normaliser_agh_vs_mc"] = mcs
    # Stan target against the Python target: differences at central and stress points, and d/dsigma
    mdl = model()
    sp = stress_points(d)
    names = ["central0", "central1", "stress_s3_r09_kbm15"]
    stan_lp = {n: float(mdl.log_prob(sp[n], data=d, jacobian=False, sig_figs=15)["lp__"].iloc[0]) for n in names}
    py_lp = {n: python_target(d, sp[n]) for n in names}
    res["logdensity_differences"] = {f"{a}-{b}": dict(stan=round(stan_lp[a] - stan_lp[b], 8), python=round(py_lp[a] - py_lp[b], 8),
                                                      abs_err=abs((stan_lp[a] - stan_lp[b]) - (py_lp[a] - py_lp[b])))
                                     for a, b in (("central0", "central1"), ("central0", "stress_s3_r09_kbm15"))}
    for v in res["logdensity_differences"].values():
        assert v["abs_err"] < 1e-6 * max(1.0, abs(v["python"])), v
    h = 1e-5
    p = sp["central0"]
    ls = [float(mdl.log_prob(dict(p, sigma=p["sigma"] + s), data=d, jacobian=False, sig_figs=15)["lp__"].iloc[0]) for s in (h, -h)]
    lpy = [python_target(d, dict(p, sigma=p["sigma"] + s)) for s in (h, -h)]
    res["dlp_dsigma_central0"] = dict(stan=round((ls[0] - ls[1]) / (2 * h), 6), python=round((lpy[0] - lpy[1]) / (2 * h), 6))
    assert abs(res["dlp_dsigma_central0"]["stan"] - res["dlp_dsigma_central0"]["python"]) < 1e-4
    return res


def cause(line):
    """Label an exception message by source; Q012-labelled rejections come from the explicit guards."""
    low = line.lower()
    for tag, lab in (("Q012 input failure", "input"), ("Q012 solver failure", "solver"),
                     ("Q012 Hessian failure", "hessian"), ("Q012 factorisation failure", "factorisation")):
        if tag in line:
            return lab
    if "algebra_solver" in low or "newton" in low or "kinsol" in low:
        return "solver_internal"
    if "log(0)" in low or "not finite" in low:
        return "nonfinite_lp_or_gradient"
    return "other"


def init_points(rule, seed, n, N, pert):
    """Prior-centred points by the declared init rule (normal: location + pert*scale*z; half-normal: median*exp(pert*z);
    rho: inv_logit(pert*z); z_rw, eps: pert*z), one numpy stream per point."""
    out = []
    for k in range(1, n + 1):
        rng = np.random.default_rng([seed, k])
        q = {name: loc + pert * sc * float(rng.standard_normal()) for name, (loc, sc) in rule["normal"].items()}
        q.update({name: med * math.exp(pert * float(rng.standard_normal())) for name, med in rule["half_normal_median"].items()})
        q["rho"] = 1 / (1 + math.exp(-pert * float(rng.standard_normal())))
        q["z_rw"] = list(pert * rng.standard_normal(24))
        q["eps"] = list(pert * rng.standard_normal(N))
        out.append(q)
    return out


def make_inits(d):
    """Write the four frozen v4 initial-value files for the fit dataset."""
    from cmdstanpy.utils import write_stan_json
    I = CFG[CFG["active"]]["inits"]
    pts = init_points(I, I["seed"], 4, d["N"], I["perturbation"])
    folder = HERE / I["dir"]
    folder.mkdir(exist_ok=True)
    paths = []
    for k, q in enumerate(pts, start=1):
        paths.append(folder / f"chain{k}.json")
        write_stan_json(str(paths[-1]), q)
    return paths, pts


def draw_to_params(row, N):
    return dict(log_h0_1=float(row["log_h0_1"]), z_rw=[float(row[f"z_rw.{j}"]) for j in range(1, 25)], tau=float(row["tau"]),
                **{k: float(row[k]) for k in ("log_k", "log_lambda0", "kappa", "log_b0", "kappa_b", "beta", "gamma", "sigma", "rho")},
                eps=[float(row[f"eps.{j}"]) for j in range(1, N + 1)])


def probes(d, starts):
    """Fixed initialisation-like points through Stan's own initialisation, which reports a domain error as
    'Rejecting initial value' and any other exception as 'Unrecoverable error'. Bounded per point and in total."""
    import subprocess
    from concurrent.futures import ThreadPoolExecutor
    import pandas as pd
    from cmdstanpy.utils import write_stan_json
    VER = CFG[CFG["active"]]
    P = VER["probes"]
    exe = OUT / VER["stan_file"].removesuffix(".stan")
    work = OUT / "probes_v4"
    work.mkdir(parents=True, exist_ok=True)
    data_file = work / "data.json"
    write_stan_json(str(data_file), d)
    pts = [(f"start_chain{k}", "start", q) for k, q in enumerate(starts, start=1)]
    sp = stress_points(d)
    est = {"central0": sp["central0"], "central1": sp["central1"], "stress_s3_r09_kbm15": sp["stress_s3_r09_kbm15"],
           "near_one_rho_099": dict(sp["central0"], rho=0.99), "near_one_rho_0999_s3": dict(sp["central0"], rho=0.999, sigma=3.0),
           "small_sigma_002": dict(sp["central0"], sigma=0.02)}
    pts += [(k, "established", q) for k, q in est.items()]
    for ch in (3, 4):
        df = pd.read_csv(sorted((OUT / "fit_v3").glob(f"*_{ch}.csv"))[0], comment="#")
        pts += [(f"saved_v3_chain{ch}_draw{i}", "saved", draw_to_params(df.iloc[i], d["N"])) for i in (250, 750)]
    rng = np.random.default_rng(P["seed"])
    n_broad = (P["max_points"] - len(pts)) // 2
    for k in range(n_broad):
        u = rng.uniform(-2, 2, size=12 + 24 + d["N"])
        q = dict(zip(["log_h0_1", "tau", "log_k", "log_lambda0", "kappa", "log_b0", "kappa_b", "beta", "gamma", "sigma", "rho"],
                     map(float, u[:11])))
        q.update(tau=math.exp(q["tau"]), sigma=math.exp(q["sigma"]), rho=1 / (1 + math.exp(-q["rho"])),
                 z_rw=list(u[12:36]), eps=list(u[36:]))
        pts.append((f"uniform2_{k}", "uniform2", q))
    for k, q in enumerate(init_points(VER["inits"], P["seed"], n_broad, d["N"], 1.0)):
        pts.append((f"prior_scale_{k}", "prior_scale", q))
    assert len(pts) <= P["max_points"]
    t0 = time.time()

    def run(item):
        j, (label, kind, q) = item
        if time.time() - t0 > P["budget_seconds"]:
            return dict(label=label, kind=kind, outcome="not_run_budget")
        f = work / f"p{j}.json"
        write_stan_json(str(f), q)
        try:
            r = subprocess.run([str(exe), "sample", "num_samples=1", "num_warmup=0", "adapt", "engaged=0", "algorithm=hmc",
                                "engine=nuts", "max_depth=1", "stepsize=" + str(VER["init_step_size"]), "init=" + str(f),
                                "random", f"seed={P['seed']}", "data", f"file={data_file}", "output", f"file={work / f'p{j}.csv'}",
                                "refresh=0"], capture_output=True, text=True, timeout=P["per_point_timeout_seconds"])
        except subprocess.TimeoutExpired:
            return dict(label=label, kind=kind, outcome="timeout")
        txt = r.stdout + r.stderr
        lines = txt.splitlines()
        if "Unrecoverable error" in txt:
            msg = next((l for l in lines if l.startswith("Exception")), "")
            return dict(label=label, kind=kind, outcome="unrecoverable", cause=cause(msg), message=msg[:240])
        if "Rejecting initial value" in txt:
            i = lines.index(next(l for l in lines if "Rejecting initial value" in l))
            msg = next((l for l in lines[i + 1:i + 4] if l.startswith("Exception") or "log(0)" in l or "not finite" in l), lines[i + 1])
            return dict(label=label, kind=kind, outcome="domain_rejection", cause=cause(msg), message=msg.strip()[:240])
        if r.returncode != 0:
            return dict(label=label, kind=kind, outcome="unexpected_exit", returncode=r.returncode, tail=txt[-240:])
        return dict(label=label, kind=kind, outcome="initialised", transition_rejected="about to be rejected" in txt)

    with ThreadPoolExecutor(P["workers"]) as ex:
        rows = list(ex.map(run, enumerate(pts)))
    secs = round(time.time() - t0, 1)
    tally = {}
    for r in rows:
        key = r["kind"] + ":" + r["outcome"] + (":" + r["cause"] if "cause" in r else "")
        tally[key] = tally.get(key, 0) + 1
    must = [r for r in rows if r["kind"] in ("start", "established", "saved")]
    bad_rows = [r for r in rows if r["outcome"] in ("unrecoverable", "unexpected_exit", "timeout", "not_run_budget")]
    ok = all(r["outcome"] == "initialised" for r in must) and not bad_rows and secs <= P["budget_seconds"]
    return dict(points=len(rows), seconds=secs, tally=tally, must_pass=[(r["label"], r["outcome"]) for r in must],
                unexpected=bad_rows, domain_rejection_examples=[r for r in rows if r["outcome"] == "domain_rejection"][:6],
                **{"pass": ok})


def smoke(paths):
    """Four real chains from the selected starts and step size: initialisation, step-size search, ten warmup iterations."""
    VER = CFG[CFG["active"]]
    S, s = VER["smoke"], CFG["sampler"]
    d, _, _ = dataset(CFG["fit_seed"])
    mdl = model()
    odir = OUT / S["output_dir"]
    t0 = time.time()
    status = "finished"
    try:
        mdl.sample(data=d, chains=S["chains"], parallel_chains=S["chains"], iter_warmup=S["iter_warmup"],
                   iter_sampling=S["iter_sampling"], adapt_delta=s["adapt_delta"], max_treedepth=s["max_treedepth"],
                   seed=s["seed"], inits=[str(x) for x in paths], step_size=VER["init_step_size"], show_progress=False,
                   output_dir=str(odir), timeout=S["timeout_seconds"])
    except TimeoutError:
        status = "timeout"
    except RuntimeError as e:
        status = "error: " + str(e)[:200]
    rec = chain_record(odir)
    fatal = [c["fatal"] for c in rec["chains"].values() if c.get("fatal")]
    done = sum(1 for c in rec["chains"].values() if c.get("complete"))
    return dict(status=status, seconds=round(time.time() - t0, 1), completed_chains=done, fatal=fatal,
                rejections=rec["rejections_total"],
                **{"pass": status == "finished" and done == S["chains"] and not fatal})


def chain_record(outdir):
    """Per-chain record from CmdStan output alone: progress, saved draws, timing, and rejected proposals versus
    fatal exceptions by cause. A rejection follows Stan's 'about to be rejected' message, or a rejected initial value
    (which Stan redraws); any other exception ends the chain. Phase is 'init' before the first progress line, then
    taken from the latest progress line."""
    import pandas as pd
    outdir = pathlib.Path(outdir)
    chains, rej_tot = {}, {}
    for k, f in enumerate(sorted(outdir.glob("*-stdout.txt")), start=1):
        phase, prev, rej, fatal, progress = "init", "", {}, [], None
        for line in f.read_text(errors="replace").splitlines():
            if line.startswith("Iteration:"):
                phase = "sampling" if "(Sampling)" in line else "warmup"
                progress = " ".join(line.split())
            elif line.startswith("Exception:"):
                if prev.startswith("Informational Message") or "Error evaluating the log probability at the initial" in prev:
                    key = f"{cause(line)}_{'init_value' if 'initial' in prev else phase}"
                    rej[key] = rej.get(key, 0) + 1
                    rej_tot[key] = rej_tot.get(key, 0) + 1
                else:
                    fatal.append(dict(phase=phase, cause=cause(line), after=prev.strip(), message=line.strip()[:240]))
            if line.strip():
                prev = line
        chains[f"chain{k}"] = dict(stdout=f.name, last_progress=progress, rejections=rej, fatal=fatal)
    for k, f in enumerate(sorted(outdir.glob("*.csv")), start=1):
        txt = f.read_text(errors="replace")
        el = [ln for ln in txt.splitlines() if ln.startswith("#") and "seconds (" in ln]
        try:
            dr = pd.read_csv(f, comment="#")
        except pd.errors.EmptyDataError:
            dr = pd.DataFrame()
        c = chains.setdefault(f"chain{k}", {})
        c.update(csv=f.name, saved_draws=len(dr), complete="seconds (Total)" in txt)
        if len(dr):
            c.update(divergences=int(dr["divergent__"].sum()), treedepth_median=float(dr["treedepth__"].median()),
                     n_leapfrog_median=float(dr["n_leapfrog__"].median()))
        if el:
            secs = {ln.split("(")[1].split(")")[0].lower(): float(ln.split()[-3] if ln.split()[-3] != "=" else ln.split()[-2])
                    for ln in el}
            c["seconds"] = secs
            if len(dr) and "sampling" in secs:
                c["seconds_per_gradient_sampling"] = round(secs["sampling"] / float(dr["n_leapfrog__"].sum()), 6)
    return dict(chains=chains, rejections_total=rej_tot)


def fit():
    d, ginfo, oinfo = dataset(CFG["fit_seed"])
    assert d is not None, "capped dataset"
    mdl = model()
    s, lim = CFG["sampler"], CFG["compute_limit"]
    t0 = time.time()
    VER = CFG[CFG.get("active", "v2")]
    row = dict(seed=CFG["fit_seed"], N=d["N"], model=VER["stan_file"], observation=oinfo)
    odir = OUT / VER.get("output_dir", "fit_v2")
    start = {}
    if "inits" in VER:
        assert json.loads((HERE / VER["checks_file"]).read_text())["all_prefit_checks_pass"], "prefit checks have not passed"
        start = dict(inits=[str(HERE / VER["inits"]["dir"] / f"chain{k}.json") for k in range(1, s["chains"] + 1)],
                     step_size=VER["init_step_size"])
    try:
        f = mdl.sample(data=d, chains=s["chains"], parallel_chains=lim["parallel_chains"], iter_warmup=s["iter_warmup"],
                       iter_sampling=s["iter_sampling"], adapt_delta=s["adapt_delta"], max_treedepth=s["max_treedepth"],
                       seed=s["seed"], show_progress=False, output_dir=str(odir),
                       timeout=lim["fit_timeout_seconds"], **start)
    except (TimeoutError, RuntimeError) as e:
        row.update(status="timeout" if isinstance(e, TimeoutError) else "chain_failure",
                   seconds=round(time.time() - t0, 1), **partial_summary(odir))
        (HERE / VER["fit_file"]).write_text(json.dumps(row, indent=1) + "\n")
        print(json.dumps(row, indent=1)); return
    secs = time.time() - t0
    dr = f.draws_pd()
    summ = f.summary()
    rh = [c for c in summ.columns if c.lower().startswith("r_hat")][0]
    ess = [c for c in summ.columns if c.lower() in ("ess_bulk", "n_eff")][0]
    core = ["sigma", "rho", "eta", "kappa", "kappa_b", "beta", "gamma", "log_k", "log_lambda0", "log_b0", "tau"]
    g = CFG["generator"]
    truth = dict(sigma=g["sigma"], rho=g["rho"], eta=g["sigma"] * g["rho"], kappa=g["kappa"], kappa_b=g["kappa_b"],
                 beta=g["beta"], log_k=0.0, log_lambda0=math.log(g["lambda0"]), log_b0=math.log(g["b0"]))
    chain_secs = None
    try:
        chain_secs = [round(float(x), 1) for x in f.time_info()] if hasattr(f, "time_info") else None
    except Exception:
        chain_secs = None
    row.update(status="fitted", seconds=round(secs, 1), divergences=int(f.method_variables()["divergent__"].sum()),
               treedepth_hits=int((dr["treedepth__"] >= s["max_treedepth"]).sum()),
               max_rhat_core=round(float(summ.loc[core, rh].max()), 4), min_ess_core=round(float(summ.loc[core, ess].min()), 0),
               max_rhat_all=round(float(summ[rh].max()), 4), min_ess_all=round(float(summ[ess].min()), 0),
               worst_rhat_param=str(summ[rh].idxmax()), worst_ess_param=str(summ[ess].idxmin()),
               chain_record=chain_record(odir))
    row["intervals_90"] = {v: [round(float(q), 3) for q in np.quantile(dr[v], [0.05, 0.5, 0.95])] + [truth.get(v)] for v in core}
    (HERE / VER["fit_file"]).write_text(json.dumps(row, indent=1) + "\n")
    print(json.dumps(row, indent=1))


CORE = ["sigma", "rho", "eta", "kappa", "kappa_b", "beta", "gamma", "log_k", "log_lambda0", "log_b0", "tau"]


def partial_summary(odir):
    """Chain record plus, when at least two chains completed, R-hat, ESS and 90% intervals over those chains only."""
    import cmdstanpy
    out = dict(chain_record=chain_record(odir))
    done = [str(pathlib.Path(odir) / c["csv"]) for c in out["chain_record"]["chains"].values() if c.get("complete")]
    out["completed_chains"] = len(done)
    if len(done) >= 2:
        f = cmdstanpy.from_csv(done)
        summ, dr = f.summary(), f.draws_pd()
        rh = [c for c in summ.columns if c.lower().startswith("r_hat")][0]
        ess = [c for c in summ.columns if c.lower() in ("ess_bulk", "n_eff")][0]
        g = CFG["generator"]
        truth = dict(sigma=g["sigma"], rho=g["rho"], eta=g["sigma"] * g["rho"], kappa=g["kappa"], kappa_b=g["kappa_b"],
                     beta=g["beta"], log_k=0.0, log_lambda0=math.log(g["lambda0"]), log_b0=math.log(g["b0"]))
        out["completed_chains_summary"] = dict(
            max_rhat_core=round(float(summ.loc[CORE, rh].max()), 4), min_ess_core=round(float(summ.loc[CORE, ess].min()), 0),
            max_rhat_all=round(float(summ[rh].max()), 4), min_ess_all=round(float(summ[ess].min()), 0),
            worst_rhat_param=str(summ[rh].idxmax()), worst_ess_param=str(summ[ess].idxmin()),
            intervals_90={v: [round(float(q), 3) for q in np.quantile(dr[v], [0.05, 0.5, 0.95])] + [truth.get(v)] for v in CORE})
    return out


def record():
    """Rebuild the fit record from the active version's output directory alone (no sampling)."""
    VER = CFG[CFG["active"]]
    odir = OUT / VER["output_dir"]
    stamps = sorted(odir.glob("*.csv"))
    start = time.mktime(time.strptime(stamps[0].stem.split("-")[1].split("_")[0], "%Y%m%d%H%M%S"))
    end = max(f.stat().st_mtime for f in odir.iterdir())
    s = partial_summary(odir)
    fatal = any(c.get("fatal") for c in s["chain_record"]["chains"].values())
    rec = dict(note="Supersedes the run-time 'rejections' field, whose counter (since replaced) labelled every exception "
                    "as a warmup rejection, including fatal ones and rejected initial values.",
               chain_failure=fatal, completed_chains=s.pop("completed_chains"),
               seconds_from_file_times=round(end - start, 1), **s)
    path = HERE / VER["fit_file"]
    row = json.loads(path.read_text()) if path.exists() else dict(seed=CFG["fit_seed"], model=VER["stan_file"])
    row["record_from_output"] = rec
    path.write_text(json.dumps(row, indent=1) + "\n")
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    {"checks": checks, "fit": fit, "record": record}[sys.argv[1]]()
