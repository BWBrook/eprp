# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 oracle run 3: the bounded reference repair declared in collapsed_oracle.md (6281f84, ab8f558).
16 cells (six named states and two controls, T2 and T3); unchanged evaluator re-run for full 35-coordinate vectors;
an independent nested adaptive QUADPACK reference with strong-concavity envelope domains; staged decisions.
    uv run --python 3.12 data/q012-pilot/collapsed_oracle_refrepair.py fixtures | benchmark | run | adjudicate"""
import importlib.util
import json
import math
import multiprocessing as mp
import pathlib
import sys
import time
import warnings

import numpy as np
from scipy import integrate, optimize, special

ARGS = sys.argv[1:]
HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("orc", HERE / "collapsed_oracle.py")
O = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(O)
pilot = O.pilot
LOG2PI = math.log(2 * math.pi)
POINTS = ["stress_s3_r09_kbm15", "c4_previous", "c1_failing", "holdout_c1f_sigma6", "holdout_c1f_sigma20",
          "holdout_c4f_sigma15", "central0", "holdout_9707_sigma8"]
FORESTS = ["T2_pair", "T3_root_two_daughters"]
EVAL_SETTINGS = {"primary": (200, 200, 50.0), "resolution": (400, 400, 50.0), "domain": (200, 200, 70.0)}
REF_SETTINGS = {"primary": (1e-13, 1e-12, 0.0), "tightened": (1.2e-14, 1e-13, 4.0)}   # inner epsrel, outer epsrel, extra R
H = 1e-4
CELLS_FILE = HERE / "collapsed_oracle_run3_cells.jsonl"
TOL = dict(value=1e-4, deriv=1e-3, self_value=1e-6, self_deriv=1e-5, ref_rel=1e-11, tail_rel=1e-14, tightened=1e-10,
           ref_disagreement=1e-6)


class RefFail(Exception):
    pass


# ---------------------------------------------------------------- independent reference
def _quad(f, lo, hi, anchor, epsrel):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        r = integrate.quad(f, lo, hi, points=[anchor], epsabs=0, epsrel=epsrel, limit=1000, full_output=1)
    iw = [str(x.message)[:200] for x in w if issubclass(x.category, integrate.IntegrationWarning)]
    return r[0], r[1], int(r[2]["neval"]), iw


def envelope_integral(logf, c, start, scale, epsrel, extra_R=0.0):
    """Integral of exp(logf) for a concave logf with curvature at least c, over a box from the strong-concavity
    envelope h(x) <= h(a) + g^2/(2c) - (c/2)(x - a - g/c)^2 (Codex 76/2189). Returns log value and receipts."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        r = optimize.minimize_scalar(lambda x: -logf(x), bracket=(start - scale, start + scale), method="brent",
                                     options=dict(xtol=1e-12))
        a = float(r.x)
        ha = logf(a)
        if not math.isfinite(ha):
            raise RefFail("non-finite anchor value")
        d = 1e-5 / math.sqrt(c)
        g = (logf(a + d) - logf(a - d)) / (2 * d)
        if not math.isfinite(g):
            raise RefFail("non-finite anchor gradient")
        gi = 1.1 * abs(g) + 1e-8
        R = 12.0 + extra_R
        while True:
            half = R / math.sqrt(c) + gi / c
            lo, hi = a - half, a + half
            val, err, neval, iw = _quad(lambda x: math.exp(logf(x) - ha), lo, hi, a, epsrel)
            if not (val > 0 and math.isfinite(val)):
                raise RefFail("non-positive or non-finite integral")
            logI = ha + math.log(val)
            log_tail = ha + gi * gi / (2 * c) + 0.5 * math.log(2 * math.pi / c) + math.log(2.0) + special.log_ndtr(-R)
            tail_rel = math.exp(log_tail - logI)
            if tail_rel <= 1e-16:
                break
            R += 2.0
            if R > 60:
                raise RefFail("envelope tail bound not met by R = 60")
    return logI, dict(rel_err=err / val, tail_rel=tail_rel, a=a, g=g, R=R, lo=lo, hi=hi, neval=neval, warnings=iw)


def reference_value(p, forest, setting="primary"):
    eps_in, eps_out, extra = REF_SETTINGS[setting]
    nodes = O.FORESTS[forest]
    cfs = O.coefs(p, [lin for lin, _ in nodes], O.COHORT[forest], "full")
    sig, rho, kb, kap = p["sigma"], p["rho"], p["kappa_b"], p["kappa"]
    s2h, v = 0.5 * sig * sig, sig * sig * (1 - rho * rho)
    st = dict(max_inner_rel=0.0, max_inner_tail=0.0, inner_neval=0, inner_calls=0, inner_warnings=[])

    def leaf(cf, xr):
        lf = lambda x: -(x - rho * xr) ** 2 / (2 * v) - 0.5 * (LOG2PI + math.log(v)) + float(O.logF(cf, x, s2h, kb, kap))
        lv, rc = envelope_integral(lf, 1 / v, rho * xr, math.sqrt(v), eps_in, extra)
        st["max_inner_rel"] = max(st["max_inner_rel"], rc["rel_err"])
        st["max_inner_tail"] = max(st["max_inner_tail"], rc["tail_rel"])
        st["inner_neval"] += rc["neval"]
        st["inner_calls"] += 1
        if rc["warnings"] and len(st["inner_warnings"]) < 5:
            st["inner_warnings"] += rc["warnings"]
        return lv

    def Hroot(x):
        t = -x * x / (2 * sig * sig) - math.log(sig) - 0.5 * LOG2PI + float(O.logF(cfs[0], x, s2h, kb, kap))
        for cf in cfs[1:]:
            t += leaf(cf, x)
        return t
    logI, rc = envelope_integral(Hroot, 1 / sig ** 2, 0.0, sig, eps_out, extra)
    k = len(cfs) - 1
    total = rc["rel_err"] + rc["tail_rel"] + k * (st["max_inner_rel"] + st["max_inner_tail"])
    warn = rc["warnings"] + st["inner_warnings"]
    qualified = total <= TOL["ref_rel"] and not warn and rc["tail_rel"] <= TOL["tail_rel"] and st["max_inner_tail"] <= TOL["tail_rel"]
    return logI, dict(total_rel=total, outer=rc, inner=st, warnings=warn, qualified=bool(qualified))


# ---------------------------------------------------------------- tasks
def _stage(msg):
    for key, stage in (("joint", "joint_mode"), ("conditional", "conditional_mode"), ("level set", "level_bounds"),
                       ("line search", "line_search"), ("interior", "interior_nodes")):
        if key in msg:
            return stage
    return "other"


def tasks():
    out = []
    for pt in POINTS:
        for fo in FORESTS:
            for j in range(-1, 35):
                for sgn in ((0,) if j < 0 else (-1, 1)):
                    for st in EVAL_SETTINGS:
                        out.append((pt, fo, "evaluator", st, j, sgn))
                    out.append((pt, fo, "reference", "primary", j, sgn))
            out.append((pt, fo, "reference", "tightened", -1, 0))
    return out


def key(t):
    return "|".join(map(str, t))


_PTS = None


def run_task(t):
    global _PTS
    pt, fo, kind, st, j, sgn = t
    u = O.p_to_u(_PTS[pt]).copy()
    if j >= 0:
        u[j] += sgn * H
    p = O.u_to_p(u)
    t0 = time.perf_counter()
    rec = dict(key=key(t), point=pt, forest=fo, kind=kind, setting=st, coord=j, sign=sgn)
    try:
        if kind == "evaluator":
            rec["value"] = O.evaluator(p, fo, "full", *EVAL_SETTINGS[st])
            rec["ok"] = True
        else:
            v, rc = reference_value(p, fo, st)
            rec.update(value=v, ok=True, qualified=rc["qualified"], total_rel=rc["total_rel"], receipt=rc)
    except (O.Unresolved, NotImplementedError) as e:
        rec.update(ok=False, stage=_stage(str(e)), error=str(e))
    except RefFail as e:
        rec.update(ok=False, stage="reference", error=str(e))
    rec["seconds"] = time.perf_counter() - t0
    return rec


def run(limit_seconds=None):
    global _PTS
    _PTS = O.points()
    done = set()
    if CELLS_FILE.exists():
        done = {json.loads(ln)["key"] for ln in CELLS_FILE.read_text().splitlines() if ln.strip()}
    todo = [t for t in tasks() if key(t) not in done]
    print(f"{len(done)} done, {len(todo)} to do, workers {pilot.workers(len(todo))}", flush=True)
    t0 = time.time()
    with mp.get_context("fork").Pool(pilot.workers(len(todo))) as pool, CELLS_FILE.open("a") as fh:
        for rec in pool.imap_unordered(run_task, todo, chunksize=1):
            fh.write(json.dumps(rec, default=float) + "\n")
            fh.flush()
            if limit_seconds and time.time() - t0 > limit_seconds:
                print("execution limit reached; completed tasks are saved", flush=True)
                pool.terminate()
                break
    print(f"wall {time.time() - t0:.0f} s", flush=True)


# ---------------------------------------------------------------- decisions
def adjudicate_cell(c):
    """c: dict with evaluator[setting] = (ok, stage, value, grad) and reference = (ok, reason, value, grad, all_qualified,
    tightened_change), second_reference = optional (qualified, value), identities and decomposition flags."""
    for st in ("primary", "resolution", "domain"):
        ok, stage = c["evaluator"][st][:2]
        if not ok:
            return f"fail (evaluator: {stage})"
    pv, pg = c["evaluator"]["primary"][2:]
    for st in ("resolution", "domain"):
        v, g = c["evaluator"][st][2:]
        if abs(v - pv) > TOL["self_value"] or np.max(np.abs(np.asarray(g) - pg)) > TOL["self_deriv"]:
            return "fail (evaluator: self-convergence)"
    rok, reason, rv, rg, allq, tchg = c["reference"]
    if not rok:
        return f"unresolved (reference: {reason})"
    if not allq:
        return "unresolved (reference: a value not qualified)"
    if tchg is None or abs(tchg) > TOL["tightened"]:
        return "unresolved (reference: tightened rerun disagrees)"
    sec = c.get("second_reference")
    if sec and sec[0] and abs(sec[1] - rv) > TOL["ref_disagreement"]:
        return "unresolved (reference disagreement)"
    if abs(pv - rv) > TOL["value"] or np.max(np.abs(np.asarray(pg) - rg)) > TOL["deriv"]:
        return "fail (accuracy)"
    if not (c["identities"]["I1"] and c["identities"]["I2"]):
        return "fail (identity)"
    return "pass"


def all_pass(statuses, decomposition_pass):
    return bool(decomposition_pass and statuses and all(s == "pass" for s in statuses))


def fixtures():
    g0 = np.zeros(35)
    good = dict(evaluator={s: (True, None, -10.0, g0) for s in ("primary", "resolution", "domain")},
                reference=(True, None, -10.0, g0, True, 0.0), identities=dict(I1=True, I2=True))
    out = dict(good_passes=adjudicate_cell(good) == "pass")
    c = dict(good, second_reference=(True, -10.0 + 0.01))
    out["independent_disagreement_0.01_not_pass"] = adjudicate_cell(c) != "pass"
    c2 = dict(good, evaluator=dict(good["evaluator"], primary=(False, "joint_mode", None, None)))
    out["injected_mode_failure_is_evaluator_fail"] = adjudicate_cell(c2) == "fail (evaluator: joint_mode)"
    out["staging_from_message"] = _stage("joint mode not converged in 200 iterations") == "joint_mode"
    out["decomposition_false_blocks_all_pass"] = all_pass(["pass", "pass"], False) is False
    c3 = dict(good, reference=(True, None, -10.0, g0, False, 0.0))
    out["unqualified_reference_is_unresolved"] = adjudicate_cell(c3).startswith("unresolved (reference")
    c4 = dict(good, reference=(True, None, -10.0 + 0.01, g0, True, 0.0))
    out["accuracy_beyond_gate_fails"] = adjudicate_cell(c4) == "fail (accuracy)"
    out["all_ok"] = all(out.values())
    print(json.dumps(out, indent=1))
    return out


def benchmark():
    global _PTS
    _PTS = O.points()
    res = {}
    for pt in ("central0", "c1_failing", "holdout_c1f_sigma20"):
        t0 = time.perf_counter(); v, rc = reference_value(_PTS[pt], "T3_root_two_daughters"); t = time.perf_counter() - t0
        t1 = time.perf_counter(); ev = O.evaluator(_PTS[pt], "T3_root_two_daughters"); te = time.perf_counter() - t1
        res[pt] = dict(ref_seconds=t, ref_value=v, qualified=rc["qualified"], total_rel=rc["total_rel"], eval_seconds=te,
                       eval_minus_ref=ev - v, inner_calls=rc["inner"]["inner_calls"], outer_neval=rc["outer"]["neval"])
    n = len(tasks())
    per = max(r["ref_seconds"] for r in res.values()) + max(r["eval_seconds"] for r in res.values()) * 3
    w = pilot.workers(n)
    res["forecast"] = dict(tasks=n, workers=w, worst_seconds_per_value_set=per,
                           forecast_wall_seconds=16 * 72 * per / w, limit_seconds=4 * 16 * 72 * per / w)
    print(json.dumps(res, indent=1, default=float))
    return res


def assemble():
    recs = {}
    for ln in CELLS_FILE.read_text().splitlines():
        if ln.strip():
            r = json.loads(ln); recs[r["key"]] = r
    run2 = json.loads((HERE / "collapsed_oracle_results_run2.json").read_text())
    post = json.loads((HERE / "oracle_posthoc" / "selection_vs_qualified_reference.json").read_text())
    r2 = {(r["point"], r["forest"]): r for r in run2["rows"]}
    cells, missing = [], []
    for pt in POINTS:
        for fo in FORESTS:
            def get(kind, st, j, s):
                k = key((pt, fo, kind, st, j, s))
                if k not in recs:
                    missing.append(k)
                return recs.get(k)
            ev = {}
            for st in EVAL_SETTINGS:
                c0 = get("evaluator", st, -1, 0)
                rows = [(get("evaluator", st, j, -1), get("evaluator", st, j, 1)) for j in range(35)]
                if c0 is None or any(a is None or b is None for a, b in rows):
                    ev[st] = (False, "incomplete", None, None)
                    continue
                bad = [x for x in [c0] + [y for ab in rows for y in ab] if not x["ok"]]
                if bad:
                    ev[st] = (False, bad[0]["stage"], None, None)
                    continue
                ev[st] = (True, None, c0["value"], np.array([(b["value"] - a["value"]) / (2 * H) for a, b in rows]))
            c0 = get("reference", "primary", -1, 0)
            rows = [(get("reference", "primary", j, -1), get("reference", "primary", j, 1)) for j in range(35)]
            tg = get("reference", "tightened", -1, 0)
            if c0 is None or tg is None or any(a is None or b is None for a, b in rows):
                ref = (False, "incomplete", None, None, False, None)
            else:
                allr = [c0] + [y for ab in rows for y in ab]
                bad = [x for x in allr + [tg] if not x["ok"]]
                if bad:
                    ref = (False, bad[0]["error"], None, None, False, None)
                else:
                    ref = (True, None, c0["value"], np.array([(b["value"] - a["value"]) / (2 * H) for a, b in rows]),
                           all(x["qualified"] for x in allr) and tg["qualified"], tg["value"] - c0["value"])
            q = r2[(pt, fo)]
            i2 = abs(post[pt]["T2_pair"]["eval_minus_qualified_ref"]) <= 1e-6 and post[pt]["T2_pair"]["qualified"]
            cell = dict(evaluator=ev, reference=ref, identities=dict(I1=q["I1_unit_log_numerator"] <= 1e-8, I2=bool(i2)))
            status = adjudicate_cell(cell)
            out = dict(point=pt, forest=fo, run2_frozen_status=q["status"], amended_status=status,
                       evaluator_value=ev["primary"][2], reference_value=ref[2],
                       evaluator_gradient=None if ev["primary"][3] is None else ev["primary"][3].tolist(),
                       reference_gradient=None if ref[3] is None else ref[3].tolist(),
                       reference_all_values_qualified=ref[4], reference_tightened_change=ref[5])
            if ev["primary"][0] and ref[0]:
                dg = np.abs(ev["primary"][3] - ref[3])
                out.update(value_abs_diff=abs(ev["primary"][2] - ref[2]), max_derivative_abs_diff=float(dg.max()),
                           worst_coordinate=O.NAMES[int(dg.argmax())])
            for st in ("resolution", "domain"):
                if ev[st][0] and ev["primary"][0]:
                    out[f"evaluator_self_{st}"] = dict(value=abs(ev[st][2] - ev["primary"][2]),
                                                      deriv=float(np.max(np.abs(ev[st][3] - ev["primary"][3]))))
            cells.append(out)
    statuses = [c["amended_status"] for c in cells]
    res = dict(spec="collapsed_oracle.md run 3 (6281f84, ab8f558)", cells=cells, missing_tasks=len(missing),
               decomposition_pass=run2["decomposition_pass"],
               amended_status_counts={s: statuses.count(s) for s in sorted(set(statuses))},
               all_pass=all_pass(statuses, run2["decomposition_pass"]),
               note="Run-1 and run-2 frozen outcomes are unchanged; this is an amended adjudication of 16 cells only.")
    (HERE / "collapsed_oracle_results_run3.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "cells"}, indent=1))
    for c in cells:
        print(c["point"], c["forest"][:2], c["run2_frozen_status"][:10], "->", c["amended_status"],
              {k: c.get(k) for k in ("value_abs_diff", "max_derivative_abs_diff", "worst_coordinate")})
    return res


if __name__ == "__main__":
    cmd = ARGS[0] if ARGS else "fixtures"
    if cmd == "fixtures":
        fixtures()
    elif cmd == "benchmark":
        benchmark()
    elif cmd == "run":
        run(float(ARGS[1]) if len(ARGS) > 1 else None)
    elif cmd == "adjudicate":
        assemble()
