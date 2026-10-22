# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 oracle run 4: reference v2 declared in collapsed_oracle.md (f863277; Codex 76/2194). Full QUADPACK diagnostics,
a standardised narrow-kernel leaf coordinate, a 1e-10 budget; 1,152 reference values for the 16 run-3 cells, reusing the
run-3 evaluator vectors unchanged.
    uv run --python 3.12 data/q012-pilot/collapsed_oracle_refrepair_v2.py fixtures | smoke | run [limit] | adjudicate"""
import gzip
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
_spec = importlib.util.spec_from_file_location("rr1", HERE / "collapsed_oracle_refrepair.py")
R1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R1)
O, pilot = R1.O, R1.pilot
LOG2PI = math.log(2 * math.pi)
VERSION = "refv2"
SETTINGS = {"primary": (1e-12, 1e-11, 0.0), "tightened": (2e-13, 2e-12, 4.0)}   # inner epsrel, outer epsrel, extra R
BUDGET, TAIL, TIGHT = 1e-10, 1e-14, 1e-10
OUT = HERE / "collapsed_oracle_run4_reference.jsonl"


class RefFail(Exception):
    pass


def _quad(f, lo, hi, anchor, epsrel, limit=1000):
    """quad with its complete return kept: a non-success message (4th element) or an IntegrationWarning is a diagnostic."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        r = integrate.quad(f, lo, hi, points=[anchor], epsabs=0, epsrel=epsrel, limit=limit, full_output=1)
    diag = [str(x.message)[:200] for x in w if issubclass(x.category, integrate.IntegrationWarning)]
    if len(r) > 3:
        diag.append(f"ier={r[2].get('ier', '?')}: " + str(r[3])[:200])
    return r[0], r[1], int(r[2]["neval"]), diag


def envelope_integral(logf, c, start, scale, epsrel, extra_R=0.0):
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
            val, err, neval, diag = _quad(lambda x: math.exp(logf(x) - ha), lo, hi, a, epsrel)
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
    return logI, dict(rel_err=err / val, tail_rel=tail_rel, a=a, g=g, R=R, lo=lo, hi=hi, neval=neval, diagnostics=diag)


def reference_value(p, forest, setting="primary"):
    eps_in, eps_out, extra = SETTINGS[setting]
    nodes = O.FORESTS[forest]
    cfs = O.coefs(p, [lin for lin, _ in nodes], O.COHORT[forest], "full")
    sig, rho, kb, kap = p["sigma"], p["rho"], p["kappa_b"], p["kappa"]
    s2h, s = 0.5 * sig * sig, sig * math.sqrt(1 - rho * rho)
    st = dict(max_inner_rel=0.0, max_inner_tail=0.0, inner_neval=0, inner_calls=0, inner_diagnostic_calls=0, inner_diagnostics=[])

    def leaf(cf, xr):
        # standardised leaf: x = rho*xr + s*u, N(x; rho*xr, s^2) dx = phi(u) du, curvature bound 1 in u (Codex 76/2194)
        lf = lambda u: -0.5 * u * u - 0.5 * LOG2PI + float(O.logF(cf, rho * xr + s * u, s2h, kb, kap))
        lv, rc = envelope_integral(lf, 1.0, 0.0, 1.0, eps_in, extra)
        st["max_inner_rel"] = max(st["max_inner_rel"], rc["rel_err"])
        st["max_inner_tail"] = max(st["max_inner_tail"], rc["tail_rel"])
        st["inner_neval"] += rc["neval"]
        st["inner_calls"] += 1
        if rc["diagnostics"]:
            st["inner_diagnostic_calls"] += 1
            if len(st["inner_diagnostics"]) < 5:
                st["inner_diagnostics"] += rc["diagnostics"]
        return lv

    def Hroot(x):
        t = -x * x / (2 * sig * sig) - math.log(sig) - 0.5 * LOG2PI + float(O.logF(cfs[0], x, s2h, kb, kap))
        for cf in cfs[1:]:
            t += leaf(cf, x)
        return t
    logI, rc = envelope_integral(Hroot, 1 / sig ** 2, 0.0, sig, eps_out, extra)
    k = len(cfs) - 1
    total = rc["rel_err"] + rc["tail_rel"] + k * (st["max_inner_rel"] + st["max_inner_tail"])
    diag = rc["diagnostics"] + st["inner_diagnostics"]
    qualified = (total <= BUDGET and not rc["diagnostics"] and st["inner_diagnostic_calls"] == 0
                 and rc["tail_rel"] <= TAIL and st["max_inner_tail"] <= TAIL)
    return logI, dict(version=VERSION, total_rel=total, outer=rc, inner=st, diagnostics=diag, qualified=bool(qualified))


def tasks():
    out = []
    for pt in R1.POINTS:
        for fo in R1.FORESTS:
            for j in range(-1, 35):
                for sgn in ((0,) if j < 0 else (-1, 1)):
                    out.append((VERSION, pt, fo, "reference", "primary", j, sgn))
            out.append((VERSION, pt, fo, "reference", "tightened", -1, 0))
    return out


key = R1.key
_PTS = None


def run_task(t):
    _, pt, fo, kind, st, j, sgn = t
    u = O.p_to_u(_PTS[pt]).copy()
    if j >= 0:
        u[j] += sgn * R1.H
    t0 = time.perf_counter()
    rec = dict(key=key(t), version=VERSION, point=pt, forest=fo, kind=kind, setting=st, coord=j, sign=sgn)
    try:
        v, rc = reference_value(O.u_to_p(u), fo, st)
        rec.update(value=v, ok=True, qualified=rc["qualified"], total_rel=rc["total_rel"], receipt=rc)
    except RefFail as e:
        rec.update(ok=False, stage="reference", error=str(e))
    rec["seconds"] = time.perf_counter() - t0
    return rec


def run(limit_seconds=None):
    global _PTS
    _PTS = O.points()
    done = set()
    if OUT.exists():
        done = {json.loads(ln)["key"] for ln in OUT.read_text().splitlines() if ln.strip()}
    todo = [t for t in tasks() if key(t) not in done]
    print(f"{len(done)} done, {len(todo)} to do, workers {pilot.workers(len(todo))}", flush=True)
    t0 = time.time()
    with mp.get_context("fork").Pool(pilot.workers(len(todo))) as pool, OUT.open("a") as fh:
        for rec in pool.imap_unordered(run_task, todo, chunksize=1):
            fh.write(json.dumps(rec, default=float) + "\n")
            fh.flush()
            if limit_seconds and time.time() - t0 > limit_seconds:
                print("execution limit reached; completed tasks are saved", flush=True)
                pool.terminate()
                break
    print(f"wall {time.time() - t0:.0f} s", flush=True)


def fixtures():
    global _quad
    out = {}
    # 1. a subdivision-limited integral returns a non-success message that _quad keeps
    v, e, n, d = _quad(lambda x: math.sin(40 * x) ** 2, 0.0, 10.0, 5.0, 1e-12, limit=2)
    out["subdivision_limit_message_captured"] = bool(d) and any("ier=" in m for m in d)
    # 2. the message reaches qualification: patch _quad for one inner call
    real = _quad
    calls = {"n": 0}

    def patched(f, lo, hi, anchor, epsrel, limit=1000):
        calls["n"] += 1
        v, e, n, d = real(f, lo, hi, anchor, epsrel, limit)
        return (v, e, n, d + ["ier=2: injected roundoff"]) if calls["n"] == 1 else (v, e, n, d)
    pts = O.points()
    _quad = patched
    try:
        _, rc = reference_value(pts["central0"], "T2_pair")
    finally:
        _quad = real
    out["injected_inner_message_unqualifies"] = rc["qualified"] is False and rc["inner"]["inner_diagnostic_calls"] >= 1
    _, rc2 = reference_value(pts["central0"], "T2_pair")
    out["clean_central0_T2_qualifies"] = rc2["qualified"] is True and not rc2["diagnostics"]
    # 3. keys are version-bound and cannot collide with run-3 keys
    out["keys_version_bound"] = all(k.startswith(VERSION + "|") for k in map(key, tasks()))
    out["task_count_1152"] = len(tasks()) == 1152
    out["all_ok"] = all(out.values())
    print(json.dumps(out, indent=1))
    return out


def smoke():
    pts = O.points()
    t0 = time.perf_counter()
    v, rc = reference_value(pts["holdout_9707_sigma8"], "T3_root_two_daughters")
    t = time.perf_counter() - t0
    ev3 = [json.loads(l) for l in gzip.open(HERE / "collapsed_oracle_run3_cells.jsonl.gz", "rt")]
    e = next(r for r in ev3 if r["point"] == "holdout_9707_sigma8" and r["forest"] == "T3_root_two_daughters"
             and r["kind"] == "evaluator" and r["setting"] == "primary" and r["coord"] == -1)
    res = dict(seconds=t, value=v, evaluator_minus_ref=e["value"] - v, qualified=rc["qualified"], total_rel=rc["total_rel"],
               outer_rel=rc["outer"]["rel_err"], max_inner_rel=rc["inner"]["max_inner_rel"],
               inner_calls=rc["inner"]["inner_calls"], inner_diagnostic_calls=rc["inner"]["inner_diagnostic_calls"],
               outer_diagnostics=rc["outer"]["diagnostics"], tails=(rc["outer"]["tail_rel"], rc["inner"]["max_inner_tail"]))
    print(json.dumps(res, indent=1, default=float))
    return res


def adjudicate():
    ev3 = {}
    for l in gzip.open(HERE / "collapsed_oracle_run3_cells.jsonl.gz", "rt"):
        r = json.loads(l)
        if r["kind"] == "evaluator":
            ev3[r["key"]] = r
    ref = {}
    for l in OUT.read_text().splitlines():
        if l.strip():
            r = json.loads(l); ref[r["key"]] = r
    run2 = json.loads((HERE / "collapsed_oracle_results_run2.json").read_text())
    post = json.loads((HERE / "oracle_posthoc" / "selection_vs_qualified_reference.json").read_text())
    r2 = {(r["point"], r["forest"]): r for r in run2["rows"]}
    cells, missing = [], 0
    for pt in R1.POINTS:
        for fo in R1.FORESTS:
            ev = {}
            for st in R1.EVAL_SETTINGS:
                c0 = ev3.get(R1.key((pt, fo, "evaluator", st, -1, 0)))
                rows = [(ev3.get(R1.key((pt, fo, "evaluator", st, j, -1))), ev3.get(R1.key((pt, fo, "evaluator", st, j, 1)))) for j in range(35)]
                if c0 is None or any(a is None or b is None for a, b in rows) or not c0["ok"] or not all(a["ok"] and b["ok"] for a, b in rows):
                    ev[st] = (False, "incomplete or failed run-3 evaluator task", None, None)
                    continue
                ev[st] = (True, None, c0["value"], np.array([(b["value"] - a["value"]) / (2 * R1.H) for a, b in rows]))
            g = lambda st_, j, s_: ref.get(key((VERSION, pt, fo, "reference", st_, j, s_)))
            c0, tg = g("primary", -1, 0), g("tightened", -1, 0)
            rows = [(g("primary", j, -1), g("primary", j, 1)) for j in range(35)]
            if c0 is None or tg is None or any(a is None or b is None for a, b in rows):
                missing += 1
                refv = (False, "incomplete", None, None, False, None)
            else:
                allr = [c0] + [y for ab in rows for y in ab]
                bad = [x for x in allr + [tg] if not x["ok"]]
                if bad:
                    refv = (False, bad[0]["error"], None, None, False, None)
                else:
                    refv = (True, None, c0["value"], np.array([(b["value"] - a["value"]) / (2 * R1.H) for a, b in rows]),
                            all(x["qualified"] for x in allr) and tg["qualified"], tg["value"] - c0["value"])
            q = r2[(pt, fo)]
            i2 = abs(post[pt]["T2_pair"]["eval_minus_qualified_ref"]) <= 1e-6 and post[pt]["T2_pair"]["qualified"]
            cell = dict(evaluator=ev, reference=refv, identities=dict(I1=q["I1_unit_log_numerator"] <= 1e-8, I2=bool(i2)))
            status = R1.adjudicate_cell(cell)
            diag_vals = sum(1 for x in ([c0, tg] + [y for ab in rows for y in ab]) if x and x.get("receipt", {}).get("diagnostics"))
            out = dict(point=pt, forest=fo, run2_frozen_status=q["status"], status_run4=status,
                       reference_values_with_diagnostics=diag_vals,
                       max_total_rel=max((x["total_rel"] for x in [c0, tg] + [y for ab in rows for y in ab] if x and x.get("ok")), default=None),
                       reference_tightened_change=refv[5])
            if ev["primary"][0] and refv[0]:
                dg = np.abs(ev["primary"][3] - refv[3])
                out.update(value_abs_diff=abs(ev["primary"][2] - refv[2]), max_derivative_abs_diff=float(dg.max()),
                           worst_coordinate=O.NAMES[int(dg.argmax())], reference_gradient=refv[3].tolist())
            cells.append(out)
    statuses = [c["status_run4"] for c in cells]
    res = dict(spec="collapsed_oracle.md run 4 (f863277)", version=VERSION, cells=cells, missing_cells=missing,
               decomposition_pass=run2["decomposition_pass"], status_counts={s: statuses.count(s) for s in sorted(set(statuses))},
               all_pass=R1.all_pass(statuses, run2["decomposition_pass"]),
               note="Run-1, run-2 and run-3 records are unchanged; evaluator vectors are run 3's.")
    (HERE / "collapsed_oracle_results_run4.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "cells"}, indent=1))
    for c in cells:
        print(c["point"], c["forest"][:2], "->", c["status_run4"], {k: c.get(k) for k in
              ("value_abs_diff", "max_derivative_abs_diff", "reference_values_with_diagnostics", "max_total_rel")})
    return res


if __name__ == "__main__":
    cmd = ARGS[0] if ARGS else "fixtures"
    {"fixtures": fixtures, "smoke": smoke, "adjudicate": adjudicate}.get(cmd, lambda: run(float(ARGS[1]) if len(ARGS) > 1 else None))()
