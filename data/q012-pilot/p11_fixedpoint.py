# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 P11 fixed-point check (p11_fixedpoint.md): the collapsed likelihood on the whole P11 forest by tree message
passing with Hermite-interpolated interior messages; R1 exact-node interpolation check; R2 tensor reference on the
4-9-12 chain; identities; cost. No optimiser, MCMC, bootstrap or empirical fit.
    uv run --python 3.12 data/q012-pilot/p11_fixedpoint.py bank        # write p11_fixedpoint_bank.json (needs scratch)
    uv run --python 3.12 data/q012-pilot/p11_fixedpoint.py fixtures    # regression, I1, I2, I3 at three points
    uv run --python 3.12 data/q012-pilot/p11_fixedpoint.py benchmark   # one value of each kind at central0
    uv run --python 3.12 data/q012-pilot/p11_fixedpoint.py run         # the frozen batch (section 6)"""
import importlib.util
import json
import math
import multiprocessing as mp
import pathlib
import resource
import sys
import time

import numpy as np
from scipy.interpolate import CubicHermiteSpline

ARGS = sys.argv[1:]
HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("collapsed_oracle", HERE / "collapsed_oracle.py")
O = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(O)
D, N, P, LOG2PI, Unresolved = O.D, O.N, O.P, O.LOG2PI, O.Unresolved
COH = set(D["coh"])
SETTINGS = {"primary": (200, 200, 400, 50.0), "resolution": (400, 400, 800, 50.0), "domain": (200, 200, 400, 70.0)}
TAB_SLACK = 40.0
CHUNK = 20000
BANK = HERE / "p11_fixedpoint_bank.json"


def p11_trees():
    """P11's trees, each a list of (lineage, parent index within the tree) in breadth-first order."""
    kids = {i: [] for i in range(1, N + 1)}
    for i in range(1, N + 1):
        if D["parent"][i - 1]:
            kids[D["parent"][i - 1]].append(i)
    trees = {}
    for r in range(1, N + 1):
        if D["parent"][r - 1] == 0:
            nodes, idx, queue = [], {}, [r]
            while queue:
                i = queue.pop(0)
                idx[i] = len(nodes)
                nodes.append((i, idx[D["parent"][i - 1]] if D["parent"][i - 1] else None))
                queue += kids[i]
            trees["-".join(str(l) for l, _ in nodes)] = nodes
    return trees


TREES = p11_trees()
INTERIOR_TREES = [k for k, v in TREES.items() if any(pa is not None and v[pa][1] is not None for _, pa in v)]
CHAIN = "4-9-12"
O.FORESTS["C_chain_4_9_12"], O.COHORT["C_chain_4_9_12"] = TREES[CHAIN], {4}


class Tree:
    """One tree's log integral. Interior nodes carry Hermite tables of their children's log messages (section 2)."""

    def __init__(self, p, nodes, coh, mode, n_node, n_cond, n_tab, delta, cfs=None):
        self.par = [pa for _, pa in nodes]
        n = len(nodes)
        self.cfs = cfs if cfs is not None else O.coefs(p, [l for l, _ in nodes], coh, mode)
        self.sig, self.rho, self.kb, self.kap = p["sigma"], p["rho"], p["kappa_b"], p["kappa"]
        self.s2h, self.v = 0.5 * self.sig ** 2, self.sig ** 2 * (1 - self.rho ** 2)
        self.kids = [[c for c in range(n) if self.par[c] == j] for j in range(n)]
        self.depth = [0] * n
        for c in range(1, n):
            self.depth[c] = self.depth[self.par[c]] + 1
        self.n_node, self.n_cond, self.n_tab, self.delta = n_node, n_cond, n_tab, delta
        self.coverage = {}
        self.m, self.s = O.joint_mode(self.par, self.cfs, self.sig, self.rho, self.kb, self.kap)
        self.Lam = O.forest_precision(self.par, self.sig, self.rho)
        self.tables = {}
        for j in reversed(range(1, n)):            # breadth-first order reversed: children before parents
            if self.kids[j]:
                self.build_table(j)

    # ------------------------------------------------------------ interior tables
    def profile(self, j, z):
        return np.array([self._profile1(j, float(zz)) for zz in np.atleast_1d(z)])

    def _profile1(self, j, zj):
        fj = float(O.logF(self.cfs[j], zj, self.s2h, self.kb, self.kap))
        if not math.isfinite(fj):
            return -math.inf
        free = np.array([i != j for i in range(len(self.par))])
        x = self.m.copy()
        x[j] = zj
        cf = [c for i, c in enumerate(self.cfs) if i != j]

        def obj(z):
            return -0.5 * float(z @ self.Lam @ z) + fj + sum(float(O.logF(c, zi, self.s2h, self.kb, self.kap))
                                                             for c, zi in zip(cf, z[free]))
        for _ in range(200):
            g = (-self.Lam @ x)[free] + np.array([O.dlogF(c, xi, self.s2h, self.kb, self.kap) for c, xi in zip(cf, x[free])])
            H = self.Lam[np.ix_(free, free)] - np.diag([O.d2logF(c, xi, self.s2h, self.kb, self.kap) for c, xi in zip(cf, x[free])])
            if not (np.all(np.isfinite(g)) and np.all(np.isfinite(H))):
                raise Unresolved("non-finite profile gradient or curvature")
            dl = np.linalg.solve(H, g)
            dec2 = float(g @ dl)
            if not (math.isfinite(dec2) and np.all(np.isfinite(dl))) or dec2 < 0:
                raise Unresolved("invalid profile Newton step")
            if np.max(np.abs(dl)) < 1e-14 or dec2 <= 1e-20:
                break
            t, f0 = 1.0, obj(x)
            for _ in range(60):
                y = x.copy(); y[free] += t * dl
                f1 = obj(y)
                if dec2 <= 1e-8 or (math.isfinite(f1) and f1 >= f0 + 1e-4 * t * dec2):
                    break
                t *= 0.5
            else:
                raise Unresolved("profile line search failed")
            x[free] += t * dl
        else:
            raise Unresolved("profile not converged in 200 iterations")
        return obj(x)

    def build_table(self, j):
        dl = (self.depth[j] + 1) * self.delta + TAB_SLACK
        lo, hi = O.level_bounds(lambda z: self.profile(j, z), np.array([self.m[j]]), np.array([self.s[j]]), dl)
        c0, sc = self.m[j], self.s[j]
        U = np.linspace(np.arcsinh((lo[0] - c0) / sc), np.arcsinh((hi[0] - c0) / sc), self.n_tab + 1)
        X = c0 + sc * np.sinh(U)
        spl = {}
        for c in self.kids[j]:
            lv, d1 = self.message(c, X)
            if not (np.all(np.isfinite(lv)) and np.all(np.isfinite(d1))):
                raise Unresolved("non-finite table value")
            spl[c] = (CubicHermiteSpline(X, lv, d1), lv[0], d1[0], lv[-1], d1[-1])
        self.tables[j] = dict(X=X, lo=X[0], hi=X[-1], spl=spl)

    def interp(self, j, c, x, d):
        tb = self.tables[j]
        s, v0, g0, v1, g1 = tb["spl"][c]
        lo, hi = tb["lo"], tb["hi"]
        xin = np.clip(x, lo, hi)
        if d == 0:
            return s(xin) + np.where(x < lo, g0 * (x - lo), 0.0) + np.where(x > hi, g1 * (x - hi), 0.0)
        if d == 1:
            return np.where(x < lo, g0, np.where(x > hi, g1, s(xin, 1)))
        return np.where((x < lo) | (x > hi), 0.0, s(xin, 2))

    def logM(self, j, x, d=0):
        f = (O.logF, O.dlogF, O.d2logF)[d](self.cfs[j], x, self.s2h, self.kb, self.kap)
        for c in self.kids[j]:
            f = f + self.interp(j, c, x, d)
        return f

    # ------------------------------------------------------------ messages
    def placement(self, j, xp):
        """Conditional grid placement for node j at parent points xp: mode, curvature scale and Delta-level bounds."""
        rho, v = self.rho, self.v
        xp = np.asarray(xp, float)
        hobj = lambda z: -(z - rho * xp) ** 2 / (2 * v) + self.logM(j, z)
        x = rho * xp
        if j in self.tables:
            x = np.clip(x, self.tables[j]["lo"], self.tables[j]["hi"])
        for _ in range(200):
            g = -(x - rho * xp) / v + self.logM(j, x, 1)
            h2 = -1 / v + self.logM(j, x, 2)
            if not (np.all(np.isfinite(g)) and np.all(np.isfinite(h2))) or np.any(h2 >= 0):
                raise Unresolved("invalid conditional curvature")
            step = -g / h2
            dec2 = -g * g / h2
            done = (np.abs(step) < 1e-14) | (dec2 <= 1e-20)
            t, f0 = np.ones_like(x), hobj(x)
            for _ in range(60):
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
        sc = 1 / np.sqrt(-(-1 / v + self.logM(j, x, 2)))
        lo, hi = O.level_bounds(lambda X: self.hc(j, xp, X), x, sc, self.delta)
        return x, sc, lo, hi

    def hc(self, j, xp, X):
        c = xp if X.ndim == 1 else xp[:, None]
        return -(X - self.rho * c) ** 2 / (2 * self.v) - 0.5 * (LOG2PI + math.log(self.v)) + self.logM(j, X)

    def message(self, j, xp, exact=False):
        """(log m_j, d log m_j / d xp) at parent points xp; exact=True replaces every interpolated child message at the
        quadrature nodes by its exact recursive value (R1), keeping the same nodes and weights."""
        xp = np.asarray(xp, float)
        if xp.size > CHUNK:
            parts = [self.message(j, xp[a:a + CHUNK], exact) for a in range(0, xp.size, CHUNK)]
            return np.concatenate([q[0] for q in parts]), np.concatenate([q[1] for q in parts])
        rho, v = self.rho, self.v
        x, sc, lo, hi = self.placement(j, xp)
        X, lw = O.sinh_simpson(self.n_cond, x, sc, lo, hi)
        if exact and self.kids[j]:
            a = lw - (X - rho * xp[:, None]) ** 2 / (2 * v) - 0.5 * (LOG2PI + math.log(v)) \
                + O.logF(self.cfs[j], X, self.s2h, self.kb, self.kap)
            for c in self.kids[j]:
                a = a + self.message(c, X.ravel(), True)[0].reshape(X.shape)
        else:
            a = lw + self.hc(j, xp, X)
        lm = O.lse(a, axis=1)
        ex = np.sum(np.exp(a - lm[:, None]) * X, axis=1)
        return lm, rho / v * (ex - rho * xp)

    def log_integral(self, exact=False):
        sig = self.sig

        def hroot(x, ex=False):
            x = np.atleast_1d(np.asarray(x, float))
            tot = -x ** 2 / (2 * sig ** 2) - math.log(sig) - 0.5 * LOG2PI + O.logF(self.cfs[0], x, self.s2h, self.kb, self.kap)
            for c in self.kids[0]:
                tot = tot + self.message(c, x, ex)[0]
            return tot
        lo, hi = O.level_bounds(hroot, np.array([self.m[0]]), np.array([self.s[0]]), self.delta)
        self.check_coverage(lo[0], hi[0])
        X, lw = O.sinh_simpson(self.n_node, self.m[0], self.s[0], lo[0], hi[0])
        return float(O.lse(lw + hroot(X, exact)))

    def check_coverage(self, lo_root, hi_root):
        """Amendment 1: every interior table must contain the range its node's quadrature nodes can occupy. For rho > 0
        both ends of a conditional level set increase with the parent value, so that range is the lower bound at the
        parent's lowest needed point and the upper bound at its highest. A parent's needed range is widened to its own
        enclosing table nodes, which are the entries its Hermite interpolant reads."""
        need = {0: (lo_root, hi_root)}
        for j in range(1, len(self.par)):
            p = self.par[j]
            if j not in self.tables or p not in need:
                continue
            a, b = need[p]
            if p in self.tables:
                Xp = self.tables[p]["X"]
                a, b = Xp[Xp <= a].max(initial=Xp[0]), Xp[Xp >= b].min(initial=Xp[-1])
            _, _, l, h = self.placement(j, np.array([a, b]))
            need[j] = (float(l[0]), float(h[1]))
            tb = self.tables[j]
            self.coverage[j] = dict(needed=need[j], table=(float(tb["lo"]), float(tb["hi"])))
            if need[j][0] < tb["lo"] or need[j][1] > tb["hi"]:
                raise Unresolved(f"interpolation table of node {j} does not cover its needed range")


# ---------------------------------------------------------------- P11 quantities
def trees_log(p, mode="full", setting="primary", exact=False, only=None):
    """Per-tree log integrals; exact=True (R1) is computed only for trees with interior nodes."""
    n_node, n_cond, n_tab, delta = SETTINGS[setting]
    out = {}
    for k, nodes in TREES.items():
        if only is not None and k not in only:
            continue
        out[k] = Tree(p, nodes, COH, mode, n_node, n_cond, n_tab, delta).log_integral(exact)
    return out


def log_pi_p11(p):
    t, w = np.array(D["gh_t"]), np.array(D["gh_w"])
    A = P.cohort_A(D, p)
    b0, c = math.exp(p["log_b0"]), D["c"]
    tot = sum(float(P.QD.log_pi_1d(p["sigma"], A[i - 1], b0 * (c - D["o"][i - 1]), p["kappa_b"], t, w)) for i in D["c1_lin"])
    for a, b in zip(D["c2_par"], D["c2_dau"]):
        tot += float(P.QD.log_pi_2d(p["sigma"], p["rho"], A[a - 1], b0 * (c - D["o"][a - 1]), A[b - 1],
                                    b0 * (c - D["o"][b - 1]), p["kappa_b"], t, w))
    return tot


def fd_trees(fun, u0):
    """Central differences of a per-tree dict function: base dict, gradient dict, seconds."""
    t0 = time.perf_counter()
    base = fun(u0)
    t1 = time.perf_counter()
    g = {k: np.zeros(len(u0)) for k in base}
    for j in range(len(u0)):
        e = np.zeros(len(u0)); e[j] = O.H_FD
        a, b = fun(u0 + e), fun(u0 - e)
        for k in base:
            g[k][j] = (a[k] - b[k]) / (2 * O.H_FD)
    return base, g, dict(value_seconds=t1 - t0, gradient_seconds=time.perf_counter() - t0)


def selection_identity(p):
    """I2 (Amendment 2): selection-mode candidate against the qualified local selection reference (the oracle's
    post-hoc method: n = 800 and 1600 at L = 12, and n = 1600 at L = 16, agreeing to 1e-6); Q80 recorded, not gated."""
    sel = sum(trees_log(p, "selection").values())
    a, b, c = (O.pilot.local_reference(D, p, n, L) for n, L in ((800, 12.0), (1600, 12.0), (1600, 16.0)))
    return dict(selection_minus_ref=sel - b, ref_resolution=a - b, ref_domain=c - b,
                ref_qualified=bool(abs(a - b) <= 1e-6 and abs(c - b) <= 1e-6), selection_minus_q80=sel - log_pi_p11(p))


def tilt_closed_form(p, nodes, b):
    Sig = np.linalg.inv(O.forest_precision([pa for _, pa in nodes], p["sigma"], p["rho"]))
    return 0.5 * float(b @ Sig @ b) - 0.5 * p["sigma"] ** 2 * float(np.sum(b))


def load_bank():
    return {k: v for k, v in json.loads(BANK.read_text()).items()}


# ---------------------------------------------------------------- commands
def bank():
    pts = O.points()
    BANK.write_text(json.dumps({k: {kk: (list(map(float, vv)) if isinstance(vv, (list, np.ndarray)) else float(vv))
                                    for kk, vv in v.items() if kk in ("log_h0_1", "z_rw", "tau", "log_k", "log_lambda0",
                                                                      "kappa", "log_b0", "kappa_b", "beta", "gamma",
                                                                      "sigma", "rho")}
                                for k, v in pts.items()}, indent=1) + "\n")
    chk = load_bank()
    print(len(chk), "points;", "max |u - u_bank| =", max(float(np.max(np.abs(O.p_to_u(pts[k]) - O.p_to_u(chk[k])))) for k in pts))


def fixtures():
    pts = load_bank()
    out = {}
    # regression: the generic tree code reproduces the frozen evaluator on T1-T3
    reg = {}
    for name in ("central0", "central1", "high_rho_9707"):
        for fo in ("T1_root", "T2_pair", "T3_root_two_daughters"):
            mine = Tree(pts[name], O.FORESTS[fo], O.COHORT[fo], "full", 200, 200, 400, 50.0).log_integral()
            reg[f"{name}/{fo}"] = abs(mine - O.evaluator(pts[name], fo))
    out["regression_max_abs"] = max(reg.values())
    out["regression"] = reg
    for name in ("central0", "stress_s3_r09_kbm15", "holdout_9707_sigma8"):
        p = pts[name]
        r = dict(I1_unit_max_abs=max(abs(v) for s in ("primary", "resolution") for v in trees_log(p, "unit", s).values()))
        r["I2"] = selection_identity(p)
        rng = np.random.default_rng(12)
        i3 = {}
        for k in INTERIOR_TREES + ["15-18"]:
            nodes = TREES[k]
            b = rng.uniform(0.2, 1.5, len(nodes))
            t = Tree(p, nodes, COH, "full", 200, 200, 400, 50.0, cfs=[(0.0, 0.0, 0.0, float(bi), 0.0) for bi in b])
            i3[k] = abs(t.log_integral() - tilt_closed_form(p, nodes, b))
        r["I3_tilt_abs"] = i3
        out[name] = r
    out["pass"] = bool(out["regression_max_abs"] <= 1e-12 and all(
        out[k]["I1_unit_max_abs"] <= 1e-8 and out[k]["I2"]["ref_qualified"] and abs(out[k]["I2"]["selection_minus_ref"]) <= 1e-6 and max(out[k]["I3_tilt_abs"].values()) <= 1e-8
        for k in ("central0", "stress_s3_r09_kbm15", "holdout_9707_sigma8")))
    (HERE / "p11_fixedpoint_fixtures.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(out, indent=1, default=float))


def benchmark():
    p = load_bank()["central0"]
    out = {}
    for s in SETTINGS:
        t0 = time.perf_counter()
        per = {}
        for k in TREES:
            t1 = time.perf_counter()
            per[k] = trees_log(p, "full", s, only={k})[k]
            out.setdefault(f"{s}_tree_seconds", {})[k] = time.perf_counter() - t1
        out[f"{s}_seconds"] = time.perf_counter() - t0
        out[f"{s}_log_numerator"] = sum(per.values())
        out[f"{s}_per_tree"] = per
    for k in INTERIOR_TREES:
        t0 = time.perf_counter()
        ex = trees_log(p, "full", "primary", exact=True, only={k})[k]
        out[f"R1_{k}_seconds"] = time.perf_counter() - t0
        out[f"R1_{k}_minus_candidate"] = ex - out["primary_per_tree"][k]
    t0 = time.perf_counter()
    box = O.ref_box(p, "C_chain_4_9_12", "full", 50.0)
    out["R2_box_seconds"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    rv = O.reference(p, "C_chain_4_9_12", box, "full", 200)
    out["R2_n200_seconds"] = time.perf_counter() - t0
    out["R2_n200_minus_candidate"] = rv - out["primary_per_tree"][CHAIN]
    t0 = time.perf_counter()
    out["log_pi"] = log_pi_p11(p)
    out["log_pi_seconds"] = time.perf_counter() - t0
    out["maxrss_kb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (HERE / "p11_fixedpoint_benchmark.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps(out, indent=1, default=float))


# ---------------------------------------------------------------- the frozen batch (p11_fixedpoint.md section 6)
BIG = "2-5-7-8-10-11-14"
R1_GRAD_POINTS = tuple(json.loads(BANK.read_text()))       # all 15 (section 6)
R2_SETTINGS = {"n200_L10": (200, 50.0), "n400_L10": (400, 50.0), "n400_L14": (400, 70.0)}
WALL_LIMIT = 10 * 3600
RESULTS = HERE / "p11_fixedpoint_run.jsonl"
SUMMARY = HERE / "p11_fixedpoint_results.json"
TOL = dict(O.TOL, interpolation_value=1e-6, interpolation_deriv=1e-5)


def tasks():
    out = []
    for name in json.loads(BANK.read_text()):
        if name in R1_GRAD_POINTS:
            out += [("R1big", name, j) for j in range(35)]
        out += [("R1big", name, "base"), ("R2", name, "n400_L10"), ("R2", name, "n400_L14")]
        out += [("cand", name, s) for s in SETTINGS] + [("R1chain", name, None), ("R2", name, "n200_L10"), ("ident", name, None)]
    first = [("ident", "central0", None), ("R1chain", "central0", None), ("R2", "central0", "n200_L10"),
             ("cand", "central0", "primary"), ("R1big", "central0", "base")]          # one of each kind early: smoke
    return first + [t for t in out if t not in first]


def _key(r):
    return f"{r[0]}|{r[1]}|{r[2]}"


def _lists(d):
    return {k: [float(x) for x in v] for k, v in d.items()}


def run_task(t):
    kind, name, arg = t
    p = load_bank()[name]
    u0 = O.p_to_u(p)
    rec = dict(key=_key(t), kind=kind, point=name, arg=arg, host=__import__("socket").gethostname())
    t0 = time.perf_counter()
    if time.time() > float(__import__("os").environ.get("P11_DEADLINE", "inf")):
        rec.update(skipped="execution ceiling reached before start")
        return rec
    try:
        if kind == "ident":
            rec["I1_unit_max_abs"] = max(abs(v) for s in ("primary", "resolution") for v in trees_log(p, "unit", s).values())
            rec["I2"] = selection_identity(p)
        elif kind == "cand":
            base, g, sec = fd_trees(lambda u: trees_log(O.u_to_p(u), "full", arg), u0)
            rec.update(per_tree=base, grad=_lists(g), **sec)
            if arg == "primary":
                lp, glp = O.grad(lambda u: log_pi_p11(O.u_to_p(u)), u0)
                rec.update(log_pi=lp, log_pi_grad=[float(x) for x in glp])
        elif kind == "R2":
            n, dl = R2_SETTINGS[arg]
            box = O.ref_box(p, "C_chain_4_9_12", "full", dl)
            v, g = O.grad(lambda u: O.reference(O.u_to_p(u), "C_chain_4_9_12", box, "full", n), u0)
            rec.update(value=v, grad=[float(x) for x in g])
        elif kind == "R1chain":
            base, g, sec = fd_trees(lambda u: trees_log(O.u_to_p(u), "full", "primary", exact=True, only={CHAIN}), u0)
            rec.update(value=base[CHAIN], grad=[float(x) for x in g[CHAIN]], **sec)
        elif kind == "R1big":
            f = lambda u: trees_log(O.u_to_p(u), "full", "primary", exact=True, only={BIG})[BIG]
            if arg == "base":
                rec["value"] = f(u0)
            else:
                e = np.zeros(len(u0)); e[arg] = O.H_FD
                rec.update(plus=f(u0 + e), minus=f(u0 - e))
    except Unresolved as e:
        rec["unresolved"] = str(e)
    rec["seconds"] = time.perf_counter() - t0
    rec["maxrss_kb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return rec


def run():
    import os
    done = set()
    if RESULTS.exists():
        done = {json.loads(l)["key"] for l in RESULTS.read_text().splitlines() if l.strip() and "skipped" not in json.loads(l)}
    todo = [t for t in tasks() if _key(t) not in done]
    os.environ["P11_DEADLINE"] = str(time.time() + WALL_LIMIT)
    nw = O.pilot.workers(len(todo))
    print(f"{len(todo)} tasks ({len(done)} already done), {nw} workers, deadline {WALL_LIMIT / 3600:.0f} h", flush=True)
    t0 = time.time()
    with mp.get_context("spawn").Pool(nw) as pool, RESULTS.open("a") as fh:
        for i, rec in enumerate(pool.imap_unordered(run_task, todo, chunksize=1), 1):
            fh.write(json.dumps(rec, default=float) + "\n"); fh.flush()
            print(f"{i}/{len(todo)} {rec['key']} {rec.get('seconds', 0):.0f}s {rec.get('unresolved', rec.get('skipped', ''))}"
                  f" elapsed {(time.time() - t0) / 3600:.2f} h", flush=True)


def assemble():
    recs = {}
    for l in RESULTS.read_text().splitlines():
        r = json.loads(l)
        if "skipped" not in r:
            recs[r["key"]] = r
    bank_ = json.loads(BANK.read_text())
    rows, cost = [], dict(core_seconds=sum(r["seconds"] for r in recs.values()), tasks=len(recs),
                          expected_tasks=len(tasks()), hosts=sorted({r["host"] for r in recs.values()}))
    for name in bank_:
        g = lambda kind, arg: recs.get(f"{kind}|{name}|{arg}")
        row = dict(point=name, sigma=bank_[name]["sigma"], rho=bank_[name]["rho"])
        unres = [r["key"] + ": " + r["unresolved"] for k, r in recs.items() if r["point"] == name and "unresolved" in r]
        missing = [_key(t) for t in tasks() if t[1] == name and _key(t) not in recs]
        row.update(unresolved=unres, missing=missing)
        cand_unres = [x for x in unres if not x.startswith("R2|")]          # R2 never decides the candidate's status
        cand_missing = [x for x in missing if not x.startswith("R2|")]
        c = {s: g("cand", s) for s in SETTINGS}
        if all(c.values()) and not any("unresolved" in v for v in c.values()):
            tot = {s: (sum(c[s]["per_tree"].values()), np.sum([c[s]["grad"][k] for k in c[s]["per_tree"]], axis=0)) for s in SETTINGS}
            pv, pg = tot["primary"]
            row["log_numerator"] = pv
            row["log_likelihood_collapsed"] = pv - c["primary"]["log_pi"]
            row["self_resolution"] = (abs(tot["resolution"][0] - pv), float(np.max(np.abs(tot["resolution"][1] - pg))))
            row["self_domain"] = (abs(tot["domain"][0] - pv), float(np.max(np.abs(tot["domain"][1] - pg))))
            row["candidate_seconds"] = {s: dict(value=c[s]["value_seconds"], gradient=c[s]["gradient_seconds"]) for s in SETTINGS}
            cg = {k: np.array(v) for k, v in c["primary"]["grad"].items()}
            cv = c["primary"]["per_tree"]
            r1c = g("R1chain", None)
            if r1c and "unresolved" not in r1c:
                row["R1_chain"] = (abs(r1c["value"] - cv[CHAIN]), float(np.max(np.abs(np.array(r1c["grad"]) - cg[CHAIN]))))
            r1b = g("R1big", "base")
            if r1b and "unresolved" not in r1b:
                row["R1_big_value"] = abs(r1b["value"] - cv[BIG])
                co = [g("R1big", j) for j in range(35)]
                if name in R1_GRAD_POINTS and all(co) and not any("unresolved" in x for x in co):
                    gr = np.array([(x["plus"] - x["minus"]) / (2 * O.H_FD) for x in co])
                    d = np.abs(gr - cg[BIG])
                    row["R1_big_deriv"] = float(np.max(d))
                    row["R1_big_worst_coordinate"] = O.NAMES[int(np.argmax(d))]
            r2 = {k: g("R2", k) for k in R2_SETTINGS}
            if all(r2.values()) and not any("unresolved" in v for v in r2.values()):
                rv, rg = r2["n400_L10"]["value"], np.array(r2["n400_L10"]["grad"])
                rres = (abs(r2["n200_L10"]["value"] - rv), float(np.max(np.abs(np.array(r2["n200_L10"]["grad"]) - rg))))
                rdom = (abs(r2["n400_L14"]["value"] - rv), float(np.max(np.abs(np.array(r2["n400_L14"]["grad"]) - rg))))
                row["R2_resolution"], row["R2_domain"] = rres, rdom
                row["R2_qualified"] = bool(rres[0] <= TOL["self_value"] and rres[1] <= TOL["self_deriv"]
                                           and rdom[0] <= TOL["self_value"] and rdom[1] <= TOL["self_deriv"])
                row["chain_vs_R2"] = (abs(cv[CHAIN] - rv), float(np.max(np.abs(cg[CHAIN] - rg))))
        idn = g("ident", None)
        if idn and "unresolved" not in idn:
            row["I1"], row["I2"] = idn["I1_unit_max_abs"], idn["I2"]
        ok = lambda pair, tv, td: pair[0] <= tv and pair[1] <= td
        checks = dict(
            self=("self_resolution" in row and ok(row["self_resolution"], TOL["self_value"], TOL["self_deriv"])
                  and ok(row["self_domain"], TOL["self_value"], TOL["self_deriv"])),
            interpolation=("R1_chain" in row and "R1_big_value" in row
                           and ok(row["R1_chain"], TOL["interpolation_value"], TOL["interpolation_deriv"])
                           and row["R1_big_value"] <= TOL["interpolation_value"]
                           and (name not in R1_GRAD_POINTS or row.get("R1_big_deriv", math.inf) <= TOL["interpolation_deriv"])),
            identities=("I1" in row and row["I1"] <= TOL["unit"] and row["I2"]["ref_qualified"]
                        and abs(row["I2"]["selection_minus_ref"]) <= TOL["selection"]))
        row["checks"] = checks
        r2_raised = any(x.startswith("R2|") for x in unres)
        row["R2_status"] = ("reference-unresolved (raised)" if r2_raised else "not run" if "R2_qualified" not in row
                            else "reference-unresolved" if not row["R2_qualified"]
                            else "pass" if ok(row["chain_vs_R2"], TOL["value"], TOL["deriv"]) else "fail")
        row["status"] = ("unresolved" if cand_unres or cand_missing else "pass" if all(checks.values())
                         else "interpolation fail" if not checks["interpolation"] else "fail")
        rows.append(row)
    out = dict(spec="p11_fixedpoint.md with Amendments 1-2 and section 6", tolerances=TOL, r1_gradient_points=R1_GRAD_POINTS,
               rows=rows, status_counts={s: sum(r["status"] == s for r in rows) for s in sorted({r["status"] for r in rows})},
               r2_counts={s: sum(r["R2_status"] == s for r in rows) for s in sorted({r["R2_status"] for r in rows})}, cost=cost)
    SUMMARY.write_text(json.dumps(out, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1, default=float))
    for r in rows:
        print(r["point"], r["status"], r["R2_status"], {k: v for k, v in r["checks"].items() if not v}, r["unresolved"][:2])


if __name__ == "__main__":
    {"bank": bank, "fixtures": fixtures, "benchmark": benchmark, "run": run, "assemble": assemble}[ARGS[0]]()
