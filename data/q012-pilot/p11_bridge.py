# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 P11 full-target bridge (p11_fixedpoint.md, 'Full-target bridge'): collapsed log target on Stan's
unconstrained coordinates = sum of tree log numerators - log pi_Q80 + model_v6 non-frailty priors + Jacobians;
gradient = Fisher numerator - FD grad log pi_Q80 + analytic prior/Jacobian. Checks B1-B5. No fit.
    uv run --python 3.12 data/q012-pilot/p11_bridge.py benchmark | run"""
import gzip
import hashlib
import importlib.util
import json
import math
import pathlib
import platform
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ARGS = sys.argv[1:]
sys.argv = sys.argv[:1]
_s = importlib.util.spec_from_file_location("ft", HERE / "fisher_tree.py")
FT = importlib.util.module_from_spec(_s)
_s.loader.exec_module(FT)
F, O = FT.F, FT.O
NAMES = O.NAMES
IX = {n: i for i, n in enumerate(NAMES)}
Z = [IX[f"z_rw.{j}"] for j in range(1, 25)]
POINTS = ("central0", "high_rho_9707", "holdout_c4f_sigma15")
TOL = dict(B1=1e-5, B2=1e-5, B3_rel=1e-4, B3_abs=1e-5, B4=1e-12, B5=1e-10)


def prior_jac(u):
    p = O.u_to_p(u)
    z = np.array(p["z_rw"])
    lp = (-0.5 * (p["log_h0_1"] - math.log(0.065)) ** 2 - 0.5 * float(z @ z) - 0.5 * (p["tau"] / 0.5) ** 2
          - 0.5 * (p["log_k"] / 0.5) ** 2 - 0.5 * (p["log_lambda0"] - math.log(0.0708)) ** 2 - 0.5 * p["kappa"] ** 2
          - 0.5 * (p["log_b0"] - math.log(0.0082)) ** 2 - 0.5 * p["kappa_b"] ** 2 - 0.5 * p["beta"] ** 2
          - 0.5 * p["gamma"] ** 2 - 0.5 * p["sigma"] ** 2)
    return lp + math.log(p["tau"]) + math.log(p["sigma"]) + math.log(p["rho"]) + math.log1p(-p["rho"])


def prior_jac_grad(u):
    p = O.u_to_p(u)
    g = np.zeros(len(u))
    g[IX["log_h0_1"]] = -(p["log_h0_1"] - math.log(0.065))
    g[Z] = -np.array(p["z_rw"])
    g[IX["tau"]] = -4 * p["tau"] ** 2 + 1
    g[IX["log_k"]] = -4 * p["log_k"]
    g[IX["log_lambda0"]] = -(p["log_lambda0"] - math.log(0.0708))
    g[IX["log_b0"]] = -(p["log_b0"] - math.log(0.0082))
    for k in ("kappa", "kappa_b", "beta", "gamma"):
        g[IX[k]] = -p[k]
    g[IX["sigma"]] = -p["sigma"] ** 2 + 1
    g[IX["rho"]] = 1 - 2 * p["rho"]
    return g


def numerator_fisher(p, setting):
    s = F.SETTINGS[setting]
    t0 = time.perf_counter()
    tot, val = np.zeros(len(NAMES)), 0.0
    for nodes in F.TREES.values():
        v, g = FT.FisherTree(p, nodes, F.COH, *s).gradient()
        tot += g; val += v
    return val, tot, time.perf_counter() - t0


def full_value(u):
    p = O.u_to_p(u)
    return sum(F.trees_log(p, "full", "primary").values()) - F.log_pi_p11(p) + prior_jac(u)


def fd_logpi(u, h=1e-4):
    t0 = time.perf_counter()
    g = np.array([(F.log_pi_p11(O.u_to_p(u + h * e)) - F.log_pi_p11(O.u_to_p(u - h * e))) / (2 * h) for e in np.eye(len(u))])
    return g, time.perf_counter() - t0


def archived():
    recs = {}
    with gzip.open(HERE / "p11_fixedpoint_run.jsonl.gz", "rt") as fh:
        for l in fh:
            r = json.loads(l)
            if r["kind"] == "cand" and r["arg"] == "primary" and r["point"] in POINTS:
                recs[r["point"]] = r
    return recs


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def benchmark():
    p = F.load_bank()["central0"]
    u = O.p_to_u(p)
    t0 = time.perf_counter(); full_value(u); tv = time.perf_counter() - t0
    _, _, tf = numerator_fisher(p, "primary")
    _, tl = fd_logpi(u)
    out = dict(value_seconds=tv, fisher_seconds=tf, fd_logpi_seconds=tl, host=platform.node())
    (HERE / "p11_bridge_benchmark.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out))


def run():
    t_start = time.time()
    bank, arch = F.load_bank(), archived()
    out = dict(points={}, tolerances=TOL, host=platform.node(), python=platform.python_version(), numpy=np.__version__,
               sources={f: sha(HERE / f) for f in ("p11_bridge.py", "fisher_tree.py", "fisher_gradient_probe.py",
                                                    "p11_fixedpoint.py", "collapsed_oracle.py", "pilot.py",
                                                    "p11_fixedpoint_bank.json", "p11_fixedpoint_run.jsonl.gz")})
    # internal check of the analytic prior/Jacobian gradient against its own central difference
    for name in POINTS:
        p = bank[name]; u = O.p_to_u(p)
        pj = prior_jac_grad(u)
        pj_fd = np.array([(prior_jac(u + 1e-5 * e) - prior_jac(u - 1e-5 * e)) / 2e-5 for e in np.eye(len(u))])
        fish = {s: numerator_fisher(p, s) for s in ("primary", "resolution", "domain")}
        g_logpi, t_logpi = fd_logpi(u)
        a = arch[name]
        arch_num = np.sum([np.array(a["grad"][k]) for k in a["per_tree"]], axis=0)
        arch_logpi = np.array(a["log_pi_grad"])
        grad_full = fish["primary"][1] - g_logpi + pj
        ref_full = arch_num - arch_logpi + pj
        b1 = grad_full - ref_full
        b2 = {s: float(np.max(np.abs(fish[s][1] - fish["primary"][1]))) for s in ("resolution", "domain")}
        b5 = float(np.max(np.abs(g_logpi - arch_logpi)))
        # B4: ridge identity at the coefficient level and for log pi
        b4 = 0.0
        lins = list(range(1, O.N + 1))
        c0 = np.array(O.coefs(p, lins, F.COH))
        for c in (0.5, 2.0):
            uc = u.copy(); uc[IX["tau"]] += math.log(c); uc[Z] = u[Z] / c
            pc = O.u_to_p(uc)
            b4 = max(b4, float(np.max(np.abs(np.array(O.coefs(pc, lins, F.COH)) - c0) / np.maximum(1, np.abs(c0)))),
                     abs(F.log_pi_p11(pc) - F.log_pi_p11(p)))
        # B3: directional checks on the whole-forest target
        d1 = np.zeros(len(u)); d1[IX["tau"]] = 1.0; d1[Z] = -u[Z]; d1 /= np.linalg.norm(d1)
        d2 = np.zeros(len(u)); d2[[IX["sigma"], IX["rho"], IX["kappa"]]] = 1.0; d2 /= np.linalg.norm(d2)
        b3 = {}
        for dname, d in (("d1_tau_zrw_ridge", d1), ("d2_sigma_rho_kappa", d2)):
            D = {}
            for eps in (1e-3, 5e-4):
                D[eps] = (full_value(u + eps * d) - full_value(u - eps * d)) / (2 * eps)
            rich = (4 * D[5e-4] - D[1e-3]) / 3
            pred = float(grad_full @ d)
            err = abs(rich - pred)
            b3[dname] = dict(fd_1e3=D[1e-3], fd_5e4=D[5e-4], richardson=rich, predicted=pred, abs_err=err,
                             numerator_dot_d=float(fish["primary"][1] @ d),
                             ok=bool(err <= max(TOL["B3_abs"], TOL["B3_rel"] * abs(pred))))
        out["points"][name] = dict(
            value=full_value(u), log_numerator=fish["primary"][0], log_pi=F.log_pi_p11(p), prior_jac=prior_jac(u),
            grad_full=grad_full.tolist(), grad_numerator_fisher=fish["primary"][1].tolist(), grad_logpi_fd=g_logpi.tolist(),
            grad_prior_jac=pj.tolist(), prior_jac_grad_vs_own_fd=float(np.max(np.abs(pj - pj_fd))),
            B1_max_abs=float(np.max(np.abs(b1))), B1_signed=b1.tolist(), B1_worst=NAMES[int(np.argmax(np.abs(b1)))],
            B2=b2, B3=b3, B4=b4, B5=b5,
            seconds=dict(fisher={s: fish[s][2] for s in fish}, fd_logpi=t_logpi),
            ok=dict(B1=bool(np.max(np.abs(b1)) <= TOL["B1"]), B2=bool(max(b2.values()) <= TOL["B2"]),
                    B3=bool(all(x["ok"] for x in b3.values())), B4=bool(b4 <= TOL["B4"]), B5=bool(b5 <= TOL["B5"])))
        print(name, {k: v for k, v in out["points"][name]["ok"].items()}, "B1", out["points"][name]["B1_max_abs"],
              "B2", b2, "B5", b5, "B4", b4, {k: (round(v["richardson"], 8), round(v["predicted"], 8), v["abs_err"]) for k, v in b3.items()},
              flush=True)
    out["all_pass"] = bool(all(all(v["ok"].values()) for v in out["points"].values()))
    out["wall_seconds"] = time.time() - t_start
    (HERE / "p11_bridge_results.json").write_text(json.dumps(out, indent=1) + "\n")
    print("all_pass", out["all_pass"], "wall", round(out["wall_seconds"]))


if __name__ == "__main__":
    {"benchmark": benchmark, "run": run}[ARGS[0]]()
