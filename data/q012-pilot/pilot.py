# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3", "cmdstanpy==1.2.4", "arviz==0.20.0", "matplotlib==3.9.2",
#                 "xarray==2024.9.0", "scipy==1.14.1"]
# ///
"""Q-012 bounded kunanyi pilot (Codex 76/1750): package, control tests and screening.

  uv run --python 3.12 data/q012-pilot/pilot.py build                 # hash-bound payload from the frozen seed table
  uv run --python 3.12 data/q012-pilot/pilot.py selftest              # cap, timeout, chain-failure, resume, signal and stale-hash fixtures
  uv run --python 3.12 data/q012-pilot/pilot.py diagnose DIR SCEN     # screening of one fitted attempt directory
  uv run --python 3.12 data/q012-pilot/pilot.py compare A B OUT.json   # mapped comparison of two fits of one dataset

The cluster runs only CmdStan and bash (payload/pbs/); data generation and screening run locally.
"""
import hashlib
import importlib.util
import json
import math
import pathlib
import queue
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
PILOT = json.loads((HERE / "pilot.json").read_text())
CAND = PILOT["candidates"][PILOT["active_candidate"]]
PAY = HERE / CAND["payload_dir"]
_spec = importlib.util.spec_from_file_location("prototype", HERE.parent / "q012-prototype" / "prototype.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
CACHE = P.OUT.parent / "q012-pilot"
RUN_ENV = dict(CHAINS=4, WARMUP=PILOT["sampler"]["iter_warmup"], SAMPLING=PILOT["sampler"]["iter_sampling"],
               ADAPT_DELTA=PILOT["sampler"]["adapt_delta"], MAX_DEPTH=PILOT["sampler"]["max_treedepth"],
               STEPSIZE=PILOT["sampler"]["init_step_size"], SEED=77017, FIT_SECONDS=PILOT["resources"]["fit_seconds"],
               SMOKE_SECONDS=PILOT["resources"]["smoke_seconds"], MODEL_BIN="./" + CAND["stan_file"].removesuffix(".stan"),
               MODULE="HDF5/1.14.0-gompi-2023a", CMDSTAN_VERSION="2.38.0")
RUN_ENV.update(CAND.get("run_env", {}))


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def scenarios():
    lines = (HERE / PILOT["scenarios_file"]).read_text().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def _generate(q, seed, overrides):
    L, ginfo = P.generate(seed, overrides)
    if ginfo["capped"]:
        q.put(("capped", None, ginfo, None))
        return
    obsd, oinfo = P.observe(L, seed)
    q.put(("ok", P.adapt(obsd), ginfo, oinfo))


def generate(seed, overrides, timeout):
    """Generate, observe and adapt one dataset in a child process under a hard time limit.
    Returns (outcome, data, generator info, observation info); outcome is ok, capped, timeout or error."""
    import multiprocessing as mp
    ctx = mp.get_context("fork")
    q = ctx.Queue()
    proc = ctx.Process(target=_generate, args=(q, seed, overrides))
    t0 = time.time()
    proc.start()
    try:
        out = q.get(timeout=timeout)
    except queue.Empty:
        out = ("timeout" if proc.is_alive() else "error", None, None, None)
    proc.join(5)
    if proc.is_alive():
        proc.terminate()
        proc.join()
    return out + (round(time.time() - t0, 2),)


def write_starts(folder, N, mapped=False):
    """The four prior-centred starts by the declared rule; for a reparameterised candidate, mapped exactly to its coordinates."""
    from cmdstanpy.utils import write_stan_json
    rule = P.CFG[P.CFG["active"]]["inits"]
    folder.mkdir(parents=True, exist_ok=True)
    for k, q in enumerate(P.init_points(rule, rule["seed"], 4, N, rule["perturbation"]), start=1):
        write_stan_json(str(folder / f"chain{k}.json"), P.to_nc(q) if mapped else q)


def log_prob_csv(exe, params_file, data_file, out_file):
    r = subprocess.run([str(exe), "log_prob", "jacobian=1", f"constrained_params={params_file}", "data", f"file={data_file}",
                        "output", f"file={out_file}", "sig_figs=15"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-500:]


def start_check(exe, scen):
    """Each frozen start through Stan's own initialisation (one draw, adaptation off, depth 1) on its dataset."""
    out = {}
    work = CACHE / "start_check"
    work.mkdir(parents=True, exist_ok=True)
    for k in range(1, 5):
        r = subprocess.run([str(exe), "sample", "num_samples=1", "num_warmup=0", "adapt", "engaged=0", "algorithm=hmc",
                            "engine=nuts", "max_depth=1", f"stepsize={RUN_ENV['STEPSIZE']}", f"init={PAY / 'inits' / scen / f'chain{k}.json'}",
                            "random", f"seed={RUN_ENV['SEED']}", "data", f"file={PAY / 'data' / f'{scen}.json'}",
                            "output", f"file={work / f'{scen}_{k}.csv'}", "refresh=0"], capture_output=True, text=True, timeout=120)
        txt = r.stdout + r.stderr
        out[f"chain{k}"] = ("unrecoverable" if "Unrecoverable" in txt else "rejected" if "Rejecting initial value" in txt
                            else "initialised" if r.returncode == 0 else f"exit_{r.returncode}")
    return out


def write_manifest(root):
    files = sorted(f for f in root.rglob("*") if f.is_file() and f.name not in ("manifest.sha256", "manifest.json")
                   and not f.relative_to(root).parts[0] in ("runs", "build")
                   and not f.name.endswith((".tar.gz", ".hpp", ".o", ".d")) and f.name != RUN_ENV["MODEL_BIN"][2:])
    (root / "manifest.sha256").write_text("".join(f"{sha(f)}  {f.relative_to(root)}\n" for f in files))
    return len(files)


def cmdstan_tarball():
    """The CmdStan release tarball, downloaded once into scratch; never committed."""
    CACHE.mkdir(parents=True, exist_ok=True)
    tb = CACHE / f"cmdstan-{RUN_ENV['CMDSTAN_VERSION']}.tar.gz"
    if not tb.exists():
        subprocess.run(["curl", "-fsSL", "-o", str(tb), PILOT["runtime"]["cmdstan_url"]], check=True)
    return tb


def build():
    """Build the payload: refuse unless the prototype's checks pass and are bound to the current source and settings."""
    from cmdstanpy.utils import write_stan_json
    ver = P.CFG["active"]
    assert ver == CAND["prototype_version"], f"prototype active version is {ver}"
    chk = json.loads((HERE / CAND["checks_file"]).read_text())
    d_fit, _, _ = P.dataset(P.CFG["fit_seed"])
    assert chk["all_prefit_checks_pass"], "prototype checks have not passed"
    assert chk["binding"] == P.binding(d_fit), "stale prototype checks: rerun prototype.py checks"
    table_sha = sha(HERE / PILOT["scenarios_file"])
    if not (PAY / "pbs").exists():  # a further candidate's package starts from a previous package's runner scripts
        shutil.copytree(HERE / CAND.get("pbs_source", "payload/pbs"), PAY / "pbs")
    for sub in ("data", "inits", "preflight"):
        shutil.rmtree(PAY / sub, ignore_errors=True)
        (PAY / sub).mkdir(parents=True)
    rows = []
    for s in [s for s in scenarios() if CAND["scenarios"] == "all" or s["id"] in CAND["scenarios"]]:
        assert int(s["sampler_seed"]) == RUN_ENV["SEED"]
        ov = dict(lambda0=float(s["lambda0"]), sigma=float(s["sigma"]), rho=float(s["rho"]))
        outcome, d, ginfo, oinfo, secs = generate(int(s["gen_seed"]), ov, PILOT["generator"]["timeout_seconds"])
        row = dict(s, outcome=outcome, generator_seconds=secs, true_lineages=(ginfo or {}).get("true_lineages"))
        if outcome == "ok":
            d = dict(d, **CAND.get("data_overrides", {}))
            write_stan_json(str(PAY / "data" / f"{s['id']}.json"), d)
            write_starts(PAY / "inits" / s["id"], d["N"], "noncentring" in P.CFG[ver])
            row.update(N=d["N"], observation=oinfo, cohort=d["NC"], singles=d["C1"], pairs=d["C2"])
        rows.append(row)
        print(s["id"], outcome, row.get("N"), secs)
    # The replay dataset is the prototype's cost dataset at 64 nodes, and its starts are the frozen v4/v5 files.
    d_r00 = json.loads((PAY / "data" / "R00.json").read_text())
    ref = json.loads(json.dumps(dict(d_fit, **CAND.get("data_overrides", {})), default=float))
    assert all(np.allclose(np.asarray(d_r00[k], float), np.asarray(ref[k], float), rtol=0, atol=0) for k in ref), "R00 differs"
    for k in range(1, 5):
        assert (PAY / "inits" / "R00" / f"chain{k}.json").read_bytes() == \
            (P.HERE / P.CFG[ver]["inits"]["dir"] / f"chain{k}.json").read_bytes(), "R00 starts differ from the checked starts"
    # Preflight points and their local reference log density and gradients.
    sp = P.stress_points(d_fit)
    if "tail_states" in P.CFG[ver]:
        tail, _, imax = P.v4_states(d_fit)
        pts = dict(central0=sp["central0"], stress_s3_r09_kbm15=sp["stress_s3_r09_kbm15"], max_sigma_v4_state=tail[imax])
    else:
        r00 = P.r00_states(d_fit)
        pts = dict(central0=sp["central0"], stress_s3_r09_kbm15=sp["stress_s3_r09_kbm15"],
                   max_sigma_r00_state=max(r00.values(), key=lambda q: q["sigma"]))
    if "noncentring" in P.CFG[ver]:
        pts = {k: P.to_nc(q) for k, q in pts.items()}
    exe = P.OUT / P.CFG[ver]["stan_file"].removesuffix(".stan")
    for name, q in pts.items():
        write_stan_json(str(PAY / "preflight" / f"point_{name}.json"), q)
        log_prob_csv(exe, PAY / "preflight" / f"point_{name}.json", PAY / "data" / "R00.json",
                     PAY / "preflight" / f"ref_point_{name}.csv")
    if "controls" in CAND:  # deterministic solver controls (Codex 76/1895): one admitted point, one rejected point
        C = CAND["controls"]
        pdir = HERE.parents[1] / C["probe_dir"]
        shutil.copy(pdir / f"{C['accept']}.json", PAY / "preflight" / f"point_control_{C['accept']}.json")
        log_prob_csv(exe, PAY / "preflight" / f"point_control_{C['accept']}.json", PAY / "data" / "R00.json",
                     PAY / "preflight" / f"ref_point_control_{C['accept']}.csv")
        shutil.copy(pdir / f"{C['reject']}.json", PAY / "preflight" / f"reject_control_{C['reject']}.json")
        r = subprocess.run([str(exe), "log_prob", "jacobian=1", f"constrained_params={PAY / 'preflight' / f'reject_control_{C["reject"]}.json'}",
                            "data", f"file={PAY / 'data' / 'R00.json'}", "output", f"file={CACHE / 'reject_control.csv'}", "sig_figs=15"],
                           capture_output=True, text=True)
        assert r.returncode != 0 and "algebra_solver: the norm of the algebraic function" in r.stdout + r.stderr, "reject control was not rejected"
    for row in rows:
        if row["outcome"] == "ok":
            row["starts_initialise"] = start_check(exe, row["id"])
    shutil.copy(P.HERE / P.CFG[ver]["stan_file"], PAY / P.CFG[ver]["stan_file"])
    lines = (HERE / PILOT["scenarios_file"]).read_text().splitlines(keepends=True)
    (PAY / "scenarios.tsv").write_text(lines[0] + "".join(ln for ln in lines[1:] if CAND["scenarios"] == "all"
                                                          or ln.split("\t")[0] in CAND["scenarios"]))
    (PAY / "run.env").write_text("".join(f"{k}={v}\n" for k, v in RUN_ENV.items()))
    fits = CAND.get("fits", [s["id"] for s in scenarios()] if CAND["scenarios"] == "all" else CAND["scenarios"])
    (PAY / "fits.txt").write_text("".join(f"{s}\n" for s in fits))  # the only scenarios stage.sh / submit_fit.sh may submit
    tb = cmdstan_tarball()
    (PAY / "cmdstan.sha256").write_text(f"{sha(tb)}  {tb.name}\n")
    nfiles = write_manifest(PAY)
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    man = dict(created=time.strftime("%Y-%m-%dT%H:%M:%S%z"), git_head_at_build=head, files=nfiles,
               manifest_sha256=sha(PAY / "manifest.sha256"), pilot_json_sha256=sha(HERE / "pilot.json"),
               scenario_table=dict(file=PILOT["scenarios_file"], sha256=table_sha, frozen_commit="c93ea58"),
               candidate=PILOT["active_candidate"],
               prototype_checks=dict(file=CAND["checks_file"], sha256=sha(HERE / CAND["checks_file"]),
                                     binding=chk["binding"], all_prefit_checks_pass=chk["all_prefit_checks_pass"]),
               cmdstan=dict(version=RUN_ENV["CMDSTAN_VERSION"], url=PILOT["runtime"]["cmdstan_url"], tarball_sha256=sha(tb)),
               run_env=RUN_ENV, scenarios=rows)
    (PAY / "manifest.json").write_text(json.dumps(man, indent=1, default=float) + "\n")
    print(json.dumps({k: v for k, v in man.items() if k != "scenarios"}, indent=1))


# ---------------------------------------------------------------- screening
def _receipt(path):
    return dict(ln.split("=", 1) for ln in pathlib.Path(path).read_text().splitlines() if "=" in ln)


def settings_line(env):
    """The settings line fit.sh writes into every receipt, for the given run.env values."""
    e = {k: str(v) for k, v in env.items()}
    s = (f"chains {e['CHAINS']}; warmup {e['WARMUP']}; sampling {e['SAMPLING']}; adapt_delta {e['ADAPT_DELTA']}; "
         f"max_depth {e['MAX_DEPTH']}; stepsize {e['STEPSIZE']}; seed {e['SEED']}; fit_seconds {e['FIT_SECONDS']}")
    return s + (f"; refresh {e['REFRESH']}; log {e['LOG_FORMAT']}" if "LOG_FORMAT" in e else "")


def csv_meta(path):
    """CmdStan CSV header settings; 'file' is qualified by its section (data.file, output.file)."""
    meta, section = {}, ""
    with open(path, errors="replace") as f:
        for line in f:
            if not line.startswith("#"):
                break
            s = line[1:].strip()
            if "=" in s:
                k, v = (x.strip() for x in s.split("=", 1))
                v = v.replace("(Default)", "").strip()
                meta.setdefault(f"{section}.file" if k == "file" else k, v)
            elif s:
                section = s
    return meta


def csv_draws(path):
    with open(path, errors="replace") as f:
        rows = [ln for ln in f if ln.strip() and not ln.startswith("#")]
    return len(rows) - 1


def stdout_record(text):
    phase, prev, rej, fatal = "init", "", {}, []
    for line in text.splitlines():
        if line.startswith("Iteration:"):
            phase = "sampling" if "(Sampling)" in line else "warmup"
        elif line.startswith("Exception:"):
            if prev.startswith("Informational Message") or "Error evaluating the log probability at the initial" in prev:
                key = f"{P.cause(line)}_{'init_value' if 'initial' in prev else phase}"
                rej[key] = rej.get(key, 0) + 1
            else:
                fatal.append(dict(phase=phase, cause=P.cause(line), after=prev.strip(), message=line.strip()[:240]))
        elif "Unrecoverable" in line or "Exception initializing" in line:
            fatal.append(dict(phase=phase, cause="unrecoverable", after=prev.strip(), message=line.strip()[:240]))
        if line.strip():
            prev = line
    return rej, fatal


import re

LOG_RE = dict(
    config=re.compile(r"^\s*[A-Za-z_]\w*( = .*)?$"),
    grad=re.compile(r"^Gradient evaluation took [0-9.e+-]+ seconds$"),
    trans=re.compile(r"^\d+ transitions using \d+ leapfrog steps per transition would take [0-9.e+-]+ seconds\.$"),
    iteration=re.compile(r"^Iteration:\s+(\d+) / (\d+) \[\s*\d+%\]\s+\((Warmup|Sampling)\)$"),
    elapsed1=re.compile(r"^ Elapsed Time: [0-9.e+-]+ seconds \(Warm-up\)$"),
    elapsed2=re.compile(r"^\s+[0-9.e+-]+ seconds \(Sampling\)$"),
    elapsed3=re.compile(r"^\s+[0-9.e+-]+ seconds \(Total\)$"))
LOG_FIXED = dict(
    adjust="Adjust your expectations accordingly!",
    warn20a="WARNING: No variance estimation is", warn20b="         performed for num_warmup < 20",
    rej="Informational Message: The current Metropolis proposal is about to be rejected because of the following issue:",
    rej3="If this warning occurs sporadically, such as for highly constrained variable types like covariance matrices, then the sampler is fine,",
    rej4="but if this warning occurs often then your model may be either severely ill-conditioned or misspecified.",
    init="Rejecting initial value:", init_eval="  Error evaluating the log probability at the initial value.",
    init_log0="  Log probability evaluates to log(0), i.e. negative infinity.",
    init_grad="  Gradient evaluated at the initial value is not finite.",
    init_cant="  Stan can't start sampling from this initial value.")
RECOGNISED_CAUSES = {"input", "solver", "hessian", "factorisation", "solver_internal"}


def parse_log(text, warmup, sampling):
    """Fail-closed parse of one combined, ordered CmdStan sample log (stdout and stderr on one file, refresh = 1).
    Returns (failures, rejections). A failure is any unrecognised or malformed line, an incomplete rejection envelope,
    an unrecognised rejection cause, a missing, repeated, out-of-order or mislabelled iteration marker, or a missing
    completion block. Each rejection records its phase (init, stepsize_init, warmup, sampling) and transition."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    fails, rej = [], []
    total = warmup + sampling
    state, expect, cur, i = "header", 1, None, 0

    def phase():
        return {"header": "init", "init": "init", "prewarm": "stepsize_init"}.get(state, cur[1] if cur else "unknown")
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if state == "header" and LOG_RE["config"].match(ln):
            i += 1
            continue
        if ln == LOG_FIXED["init"]:
            if state not in ("header", "init"):
                fails.append(f"line {i + 1}: initial-value rejection after initialisation")
            state = "init"
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt == LOG_FIXED["init_eval"] and i + 2 < len(lines) and lines[i + 2].startswith("Exception: "):
                c = P.cause(lines[i + 2])
                rej.append(dict(phase="init", transition=None, cause=c, message=lines[i + 2][:200]))
                if c not in RECOGNISED_CAUSES:
                    fails.append(f"line {i + 3}: unrecognised initial-value rejection cause: {lines[i + 2][:120]!r}")
                i += 3
            elif nxt in (LOG_FIXED["init_log0"], LOG_FIXED["init_grad"]) and i + 2 < len(lines) and lines[i + 2] == LOG_FIXED["init_cant"]:
                rej.append(dict(phase="init", transition=None, cause="init_nonfinite", message=nxt.strip()))
                i += 3
            else:
                fails.append(f"line {i + 1}: incomplete initial-value rejection envelope")
                i += 1
            continue
        if LOG_RE["grad"].match(ln) or LOG_RE["trans"].match(ln) or ln == LOG_FIXED["adjust"]:
            if state not in ("header", "init", "prewarm"):
                fails.append(f"line {i + 1}: gradient-timing block out of place")
            state = "prewarm"
            i += 1
            continue
        if ln == LOG_FIXED["warn20a"]:
            if not (i + 1 < len(lines) and lines[i + 1] == LOG_FIXED["warn20b"] and warmup < 20 and state == "prewarm"):
                fails.append(f"line {i + 1}: unexpected low-warmup warning")
            i += 2
            continue
        m = LOG_RE["iteration"].match(ln)
        if m:
            k, n, lab = int(m.group(1)), int(m.group(2)), m.group(3)
            want = "Warmup" if k <= warmup else "Sampling"
            if state not in ("prewarm", "iter") or k != expect or n != total or lab != want:
                fails.append(f"line {i + 1}: iteration marker {k}/{n} ({lab}); expected {expect}/{total} ({want if k == expect else ''})")
            state, cur, expect = "iter", (k, lab.lower()), k + 1
            i += 1
            continue
        if ln == LOG_FIXED["rej"]:
            ok = (i + 3 < len(lines) and lines[i + 1].startswith("Exception: ") and lines[i + 2] == LOG_FIXED["rej3"]
                  and lines[i + 3] == LOG_FIXED["rej4"])
            if not ok:
                fails.append(f"line {i + 1}: incomplete rejection envelope")
                i += 1
                continue
            c = P.cause(lines[i + 1])
            ph = phase()
            if ph in ("init",):
                ph = "stepsize_init"
            rej.append(dict(phase=ph, transition=cur[0] if (cur and state == "iter") else None, cause=c, message=lines[i + 1][:200]))
            if c not in RECOGNISED_CAUSES:
                fails.append(f"line {i + 2}: unrecognised rejection cause: {lines[i + 1][:120]!r}")
            if state not in ("prewarm", "iter"):
                fails.append(f"line {i + 1}: rejection envelope before initialisation completed")
            i += 4
            continue
        if LOG_RE["elapsed1"].match(ln):
            if not (state == "iter" and expect == total + 1 and i + 2 < len(lines) and LOG_RE["elapsed2"].match(lines[i + 1])
                    and LOG_RE["elapsed3"].match(lines[i + 2])):
                fails.append(f"line {i + 1}: completion block out of place or malformed")
            state = "done"
            i += 3
            continue
        fails.append(f"line {i + 1}: unrecognised line {ln[:120]!r}")
        i += 1
    if state != "done":
        fails.append(f"no completion block; last marker {cur}")
    if expect != total + 1:
        fails.append(f"iteration markers end at {expect - 1}, expected {total}")
    return fails, rej


def qualify(attempt, scen, env, manifest_sha, build_receipt):
    """Structural qualification of one attempt, before any statistics. Returns the list of failures (empty if it qualifies)."""
    attempt = pathlib.Path(attempt)
    fails = []
    if not (attempt / "receipt.txt").exists():
        return ["no receipt"]
    rc = _receipt(attempt / "receipt.txt")
    bh = build_receipt.get("binary_sha256") or ""
    if not (len(bh) == 64 and all(ch in "0123456789abcdef" for ch in bh)):
        fails.append(f"build receipt has no valid binary hash ({bh!r})")
    want = dict(scenario=scen, attempt=attempt.name.removeprefix("attempt"), status="complete", manifest_sha256=manifest_sha,
                binary_sha256=build_receipt.get("binary_sha256"), settings=settings_line(env))
    fails += [f"receipt {k} is {rc.get(k)!r}, expected {v!r}" for k, v in want.items() if rc.get(k) != v]
    if build_receipt.get("status") != "ok":
        fails.append(f"build receipt status is {build_receipt.get('status')!r}")
    if build_receipt.get("manifest_sha256") != manifest_sha:
        fails.append("build receipt is for a different payload manifest")
    C = int(env["CHAINS"])
    combined = env.get("LOG_FORMAT") == "combined"
    streams = ("log",) if combined else ("stdout", "stderr")
    expected = {f"chain{k}.{x}" for k in range(1, C + 1) for x in ("csv", "exit") + streams}
    present = {f.name for f in attempt.iterdir()}
    fails += [f"missing {n}" for n in sorted(expected - present)]
    fails += [f"unexpected output file {n}" for n in sorted(present)
              if (n.endswith((".csv", ".stdout", ".stderr", ".log", ".exit")) and n not in expected)
              or (n.endswith(".time") and n.removesuffix(".time") + ".csv" not in expected)]
    for k in range(1, C + 1):
        c = attempt / f"chain{k}"
        if not all((attempt / f"chain{k}.{x}").exists() for x in ("csv", "exit") + streams):
            continue
        if (attempt / f"chain{k}.exit").read_text().strip() != "0" or rc.get(f"chain{k}_exit") != "0":
            fails.append(f"chain {k} exit {(attempt / f'chain{k}.exit').read_text().strip()!r}")
        if combined:
            lf, _ = parse_log((attempt / f"chain{k}.log").read_text(errors="replace"), int(env["WARMUP"]), int(env["SAMPLING"]))
            fails += [f"chain {k} log: {x}" for x in lf]
        else:
            err = (attempt / f"chain{k}.stderr").read_text(errors="replace").strip()
            if err:
                fails.append(f"chain {k} stderr not empty: {err.splitlines()[0][:160]!r}")
            _, fatal = stdout_record((attempt / f"chain{k}.stdout").read_text(errors="replace"))
            if fatal:
                fails.append(f"chain {k} fatal: {fatal[0]['message'][:160]!r}")
        if "seconds (Total)" not in pathlib.Path(f"{c}.csv").read_text(errors="replace"):
            fails.append(f"chain {k} CSV incomplete")
        m = csv_meta(f"{c}.csv")
        for key, val in (("num_samples", env["SAMPLING"]), ("num_warmup", env["WARMUP"]), ("delta", env["ADAPT_DELTA"]),
                         ("max_depth", env["MAX_DEPTH"]), ("stepsize", env["STEPSIZE"]), ("seed", env["SEED"]), ("id", k)):
            try:
                ok = float(m.get(key, "nan")) == float(val)
            except ValueError:
                ok = False
            if not ok:
                fails.append(f"chain {k} CSV {key} is {m.get(key)!r}, expected {val!r}")
        for key, val in (("data.file", f"data/{scen}.json"), ("init", f"inits/{scen}/chain{k}.json")):
            if m.get(key) != val:
                fails.append(f"chain {k} CSV {key} is {m.get(key)!r}, expected {val!r}")
        n = csv_draws(f"{c}.csv")
        if n != int(env["SAMPLING"]):
            fails.append(f"chain {k} has {n} retained draws, expected {env['SAMPLING']}")
    return fails


def ebfmi(e):
    """E-BFMI per chain as CmdStan's diagnose defines it (diagnose.cpp: mean squared successive energy difference
    over the sample variance, which equals the ratio of the two sums). A population-variance denominator gives values
    larger by n / (n - 1)."""
    return float(np.sum(np.diff(e) ** 2) / np.sum((e - e.mean()) ** 2))


def _finite(x):
    return x is not None and bool(np.isfinite(x))


def rhat_pass(rhat):
    return bool(rhat) and all(_finite(v) and v < PILOT["screening"]["rhat_max"] for v in rhat.values())


def ess_pass(ess):
    T = PILOT["screening"]["ess_bulk_and_tail_min_core"]
    return bool(ess) and all(_finite(v["bulk"]) and _finite(v["tail"]) and v["bulk"] >= T and v["tail"] >= T for v in ess.values())


def eta_block(q05, q95, m05, m95, truth):
    """Endpoints, raw D/X flags and Monte Carlo precision. Non-finite endpoints or MCSE leave the affected items unresolved
    (None), never passed."""
    D = PILOT["decision"]
    ends = _finite(q05) and _finite(q95)
    prec = _finite(m05) and _finite(m95) and m05 >= 0 and m95 >= 0
    return dict(q05=q05, q95=q95, mcse_q05=m05, mcse_q95=m95, endpoints_finite=ends, mcse_finite=prec,
                mcse_target_met=(max(m05, m95) <= D["mcse_target"]) if ends and prec else None, truth=truth,
                interval_covers_truth=(q05 <= truth <= q95) if ends and truth is not None else None,
                D=(q05 > D["eta0"]) if ends else None, X=(q95 < D["eta1"]) if ends else None,
                D_numerically_uncertain=(q05 - 2 * m05 < D["eta0"] < q05 + 2 * m05) if ends and prec else None,
                X_numerically_uncertain=(q95 - 2 * m95 < D["eta1"] < q95 + 2 * m95) if ends and prec else None)


def statistics(csvs, outs, truth, env=None):
    """Screening statistics on chain files of equal, already verified length. With a combined log format (env
    LOG_FORMAT=combined) the per-chain logs are parsed for phase-attributed rejections; otherwise stdout only."""
    import arviz as az
    import pandas as pd
    S = PILOT["screening"]
    dfs = [pd.read_csv(c, comment="#") for c in csvs]
    assert len({len(x) for x in dfs}) == 1, "unequal chain lengths"
    arr = lambda col: np.stack([x[col].to_numpy() for x in dfs])
    chains = []
    combined = bool(env) and env.get("LOG_FORMAT") == "combined"
    for c, o, x in zip(csvs, outs, dfs):
        if combined:
            lf, rl = parse_log(pathlib.Path(o).read_text(errors="replace"), int(env["WARMUP"]), int(env["SAMPLING"]))
            rej = {}
            for r in rl:
                rej[f"{r['cause']}_{r['phase']}"] = rej.get(f"{r['cause']}_{r['phase']}", 0) + 1
            fatal = [dict(message=f) for f in lf]
            extra = dict(rejection_events=rl, log_parse="complete" if not lf else "failed")
        else:
            rej, fatal = stdout_record(pathlib.Path(o).read_text(errors="replace"))
            se = pathlib.Path(o).with_suffix(".stderr")
            extra = dict(log_parse="stdout only", stderr_nonempty=se.exists() and bool(se.read_text(errors="replace").strip()))
        chains.append(dict(csv=pathlib.Path(c).name, draws=len(x), divergences=int(x["divergent__"].sum()),
                           depth_hits=int((x["treedepth__"] >= PILOT["sampler"]["max_treedepth"]).sum()),
                           ebfmi=ebfmi(x["energy__"].to_numpy()), rejections=rej, fatal=fatal,
                           sampling_phase_rejections=sum(v for k, v in rej.items() if k.endswith("_sampling")), **extra))
    cols = [c for c in dfs[0].columns if not c.endswith("__") or c == "lp__"]
    rhat = {c: float(az.rhat(arr(c))) for c in cols}
    ess = {c: dict(bulk=float(az.ess(arr(c), method="bulk")), tail=float(az.ess(arr(c), method="tail"))) for c in S["core"]}
    eta = arr("eta")
    q05, q95 = (float(v) for v in np.quantile(eta.ravel(), [0.05, 0.95]))
    m05, m95 = float(az.mcse(eta, method="quantile", prob=0.05)), float(az.mcse(eta, method="quantile", prob=0.95))
    crit = dict(
        zero_post_warmup_divergences=sum(c["divergences"] for c in chains) == S["post_warmup_divergences"],
        no_fatal_or_sampling_phase_failures=(not any(c["fatal"] or c["sampling_phase_rejections"] for c in chains))
        if combined or not any(c.get("stderr_nonempty") for c in chains) else None,  # separate stderr: phase unknown
        ebfmi_each_chain=all(_finite(c["ebfmi"]) and c["ebfmi"] >= S["ebfmi_min_per_chain"] for c in chains),
        rhat_all=rhat_pass(rhat), ess_bulk_tail_core=ess_pass(ess))
    worst = sorted(rhat.items(), key=lambda kv: -kv[1] if _finite(kv[1]) else -np.inf)
    verdict = False if any(v is False for v in crit.values()) else None if any(v is None for v in crit.values()) else True
    return dict(chains=chains, screening=crit, screening_pass=verdict, rhat_max=worst[0],
                rhat_over_threshold=[(k, v) for k, v in worst if not _finite(v) or v >= S["rhat_max"]][:20],
                rhat_core={c: rhat[c] for c in S["core"]}, ess_core=ess, eta=eta_block(q05, q95, m05, m95, truth))


def _clean(x):
    if isinstance(x, float) and not np.isfinite(x):
        return repr(x)
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    return x


def diagnose(attempt, scen, env=None, manifest_sha=None, build_receipt=None, write=True):
    """Pilot qualification and screening of one fetched attempt (Codex 76/1750, 76/1765). Structural failures leave the
    fit unresolved and no statistics are computed. Defaults: the local payload's run.env and manifest, and the build
    receipt fetched with the run (<fetch root>/build/receipt.txt)."""
    attempt = pathlib.Path(attempt)
    env = env or RUN_ENV
    manifest_sha = manifest_sha or sha(PAY / "manifest.sha256")
    if build_receipt is None:
        br = attempt.parents[2] / "build" / "receipt.txt"
        build_receipt = _receipt(br) if br.exists() else {}
    fails = qualify(attempt, scen, env, manifest_sha, build_receipt)
    truth = next((float(s["eta"]) for s in scenarios() if s["id"] == scen), None)
    res = dict(scenario=scen, attempt=str(attempt), qualified=not fails, qualification_failures=fails)
    if fails:
        res.update(status="unresolved", screening_pass=None)
    else:
        C = int(env["CHAINS"])
        st = statistics([attempt / f"chain{k}.csv" for k in range(1, C + 1)],
                        [attempt / f"chain{k}.{'log' if env.get('LOG_FORMAT') == 'combined' else 'stdout'}" for k in range(1, C + 1)],
                        truth, env)
        res.update(status="screened", **st)
        res["precision"] = ("met" if st["eta"]["mcse_target_met"] else "not met" if st["eta"]["mcse_target_met"] is False
                            else "unresolved")
    res = _clean(res)
    if write:
        (attempt / "diagnostics.json").write_text(json.dumps(res, indent=1) + "\n")
    return res


def summarise(folder):
    """Historical summary of older output (for example the v4 fit). Not pilot qualification: no receipts are checked."""
    folder = pathlib.Path(folder)
    csvs = sorted(folder.glob("chain*.csv")) or sorted(folder.glob("*.csv"))
    outs = sorted(folder.glob("chain*.stdout")) or sorted(folder.glob("*-stdout.txt"))
    assert len(csvs) == len(outs) and csvs, "unpaired chain files"
    res = dict(kind="historical summary; not pilot qualification", folder=str(folder), **statistics(csvs, outs, None))
    print(json.dumps(_clean({k: v for k, v in res.items() if k != "chains"}), indent=1))
    return res


REF_TOL = dict(value=1e-6, derivative=1e-5)  # a reference is converged when doubling its resolution moves it less than this


def _steps(q):
    return dict(sigma=min(1e-4, q["sigma"] / 2), rho=min(1e-4, q["rho"] / 2, (1 - q["rho"]) / 2), kappa_b=1e-4)


def _lse(x):
    m = float(np.max(x))
    return m + math.log(float(np.exp(x - m).sum()))


def local_reference(d, q, n=1600, L=16.0):
    """Log cohort normaliser by Simpson integration on a grid centred and scaled at each Newton mode (2-D in 64-row
    chunks). Independent of the Q = 64 nodes; resolves narrow modes the fixed-innovation reference misses."""
    sig, rho, kb = q["sigma"], q["rho"], q["kappa_b"]
    A = P.cohort_A(d, q)
    b0 = math.exp(q["log_b0"])
    s2h = 0.5 * sig * sig
    e = np.linspace(-L, L, n + 1)
    wt = np.ones(n + 1)
    wt[1:-1:2], wt[2:-1:2] = 4, 2
    lw = np.log(wt * 2 * L / (3 * n))
    ls = lambda x, a, b: -a * np.exp(x - s2h) - b * np.exp(kb * (x - s2h))

    def mode(aa, bb, inv):
        a, b, y = np.array(aa), np.array(bb), np.zeros(len(aa))
        for _ in range(200):
            ep, eb = a * np.exp(y - s2h), b * np.exp(kb * (y - s2h))
            Pm = inv + np.diag(ep + kb * kb * eb)
            dlt = np.linalg.solve(Pm, -inv @ y - ep - kb * eb)
            y = y + dlt
            if np.max(np.abs(dlt)) < 1e-14:
                break
        ep, eb = a * np.exp(y - s2h), b * np.exp(kb * (y - s2h))
        return y, np.linalg.cholesky(np.linalg.inv(inv + np.diag(ep + kb * kb * eb)))
    out = 0.0
    for ii in d["c1_lin"]:
        i = ii - 1
        a, b = A[i], b0 * (d["c"] - d["o"][i])
        m, T = mode([a], [b], np.array([[1 / sig ** 2]]))
        x = m[0] + T[0, 0] * e
        out += math.log(T[0, 0]) + _lse(lw + ls(x, a, b) - 0.5 * x * x / sig ** 2 - math.log(sig) - 0.5 * math.log(2 * math.pi))
    for ip, idd in zip(d["c2_par"], d["c2_dau"]):
        ip, idd = ip - 1, idd - 1
        aa, bb = [A[ip], A[idd]], [b0 * (d["c"] - d["o"][k]) for k in (ip, idd)]
        inv = np.linalg.inv(sig ** 2 * np.array([[1, rho], [rho, 1]]))
        m, T = mode(aa, bb, inv)
        logs = []
        for s in range(0, n + 1, 64):
            e1, e2 = e[s:s + 64, None], e[None, :]
            xp = m[0] + T[0, 0] * e1
            xd = m[1] + T[1, 0] * e1 + T[1, 1] * e2
            arr = (lw[s:s + 64, None] + lw[None, :] + ls(xp, aa[0], bb[0]) + ls(xd, aa[1], bb[1])
                   - 0.5 * (inv[0, 0] * xp * xp + 2 * inv[0, 1] * xp * xd + inv[1, 1] * xd * xd)
                   - math.log(2 * math.pi) - 2 * math.log(sig) - 0.5 * math.log(1 - rho * rho))
            logs.append(_lse(arr))
        out += math.log(T[0, 0] * T[1, 1]) + _lse(np.array(logs))
    return out


def _values(d, q, f):
    """Value and central-difference derivatives (domain-safe steps) of a normaliser function f(q)."""
    hs = _steps(q)
    v = dict(value=f(q))
    for name in ("sigma", "kappa_b") + (("rho",) if d["C2"] else ()):
        h = hs[name]
        v[name] = (f(dict(q, **{name: q[name] + h})) - f(dict(q, **{name: q[name] - h}))) / (2 * h)
    return v


def _converged(a, b):
    ch = {k: b[k] - a[k] for k in a}
    return dict(value_change=float(ch["value"]), derivative_changes={k: float(v) for k, v in ch.items() if k != "value"},
                converged=bool(abs(ch["value"]) <= REF_TOL["value"]
                               and all(abs(v) <= REF_TOL["derivative"] for k, v in ch.items() if k != "value")))


def reference_convergence(d, q):
    """Signed change of the fixed-innovation Simpson reference itself (value and derivatives), 1,600 -> 3,200 intervals."""
    ref = lambda n: (lambda p: P.log_norm_ref(d, p, P.cohort_A(d, p), n))
    return _converged(_values(d, q, ref(1600)), _values(d, q, ref(3200)))


def gate_point(d, q):
    """Q = 64 normaliser against a converged reference at one joint state (value and d/dsigma, d/drho, d/dkappa_b, with
    domain-safe steps). The fixed-innovation Simpson reference is used when it converges; otherwise the local-mode
    reference; if neither converges the state is unresolved, never passed."""
    agh = _values(d, q, lambda p: P.log_norm_agh(d, p, P.cohort_A(d, p)))
    coarse = reference_convergence(d, q)
    used, ref = "fixed_innovation_n1600", None
    if coarse["converged"]:
        ref = _values(d, q, lambda p: P.log_norm_ref(d, p, P.cohort_A(d, p), 1600))
    else:
        a = _values(d, q, lambda p: local_reference(d, p, 800, 12.0))
        b = _values(d, q, lambda p: local_reference(d, p, 1600, 12.0))
        c = _values(d, q, lambda p: local_reference(d, p, 1600, 16.0))
        loc = dict(resolution=_converged(a, b), domain=_converged(b, c))
        if loc["resolution"]["converged"] and loc["domain"]["converged"]:
            used, ref = "local_mode_n1600_L16", c
        coarse["local"] = loc
    res = dict(h=_steps(q), reference=used if ref else "unresolved", reference_convergence=coarse)
    if ref is None:
        res["pass"] = None
        return res
    res["log_err"] = abs(agh["value"] - ref["value"])
    for k in agh:
        if k != "value":
            res[f"d_{k}_err"] = abs(agh[k] - ref[k])
    res["pass"] = bool(res["log_err"] <= 1e-4 and all(v <= 1e-3 for k, v in res.items() if k.startswith("d_")))
    return res


def joint_checks(fit_dir, data_file):
    """Direct Q = 64 checks at selected joint states of one fit (Codex 76/1855): six highest sigma, largest |kappa_b|,
    smallest and largest rho, and 40 evenly spaced draws; reference convergence at the largest log error; and the lower
    tail of sigma per chain. An unperformed check is reported as not tested."""
    import pandas as pd
    d = json.loads(pathlib.Path(data_file).read_text())
    dfs = [pd.read_csv(pathlib.Path(fit_dir) / f"chain{k}.csv", comment="#") for k in range(1, 5)]
    df = pd.concat(dfs, ignore_index=True)
    sel = list(dict.fromkeys([int(i) for i in df.nlargest(6, "sigma").index]
                             + [int(df.kappa_b.abs().idxmax()), int(df.rho.idxmin()), int(df.rho.idxmax())]
                             + [int(i) for i in np.linspace(0, len(df) - 1, 40).astype(int)]))
    states = {i: P.draw_to_params(df.iloc[i], d["N"]) for i in sel}
    gates = {str(i): dict(sigma=float(q["sigma"]), rho=float(q["rho"]), kappa_b=float(q["kappa_b"]), **gate_point(d, q))
             for i, q in states.items()}
    tested = {k: g for k, g in gates.items() if g["pass"] is not None}
    worst = max(tested, key=lambda k: tested[k]["log_err"]) if tested else None
    lower = [dict(chain=k, q001=float(x.sigma.quantile(0.001)), q01=float(x.sigma.quantile(0.01)), min=float(x.sigma.min()),
                  mass_below_0_1=float((x.sigma < 0.1).mean()), mass_below_0_01=float((x.sigma < 0.01).mean()))
             for k, x in enumerate(dfs, start=1)]
    unresolved = [k for k, g in gates.items() if g["pass"] is None]
    verdict = (None if not gates or unresolved else all(g["pass"] for g in gates.values()))
    return dict(states_selected=len(gates), states_with_converged_reference=len(tested), unresolved_states=unresolved,
                status="tested" if gates else "not tested", all_pass=verdict,
                max_log_err=max((g["log_err"] for g in tested.values()), default=None),
                max_derivative_err=max((v for g in tested.values() for k, v in g.items() if k.startswith("d_") and k.endswith("_err")),
                                       default=None),
                worst_state=worst, reference_convergence_at_worst=(gates[worst]["reference_convergence"] if worst else "not tested"),
                states=gates, sigma_lower_tail=lower)


def compare(dir_a, dir_b, out_file, data_file=None):
    """Mapped comparison of two qualified fits of the same dataset (Codex 76/1814): core summaries and eta endpoints with
    chain-preserving MCSEs (descriptive z under zero cross-fit covariance), per-chain cost, and direct joint-state Q = 64
    checks on B (Codex 76/1855; marginal ranges do not establish joint-state accuracy)."""
    import arviz as az
    import pandas as pd
    S = PILOT["screening"]
    load = lambda d: [pd.read_csv(pathlib.Path(d) / f"chain{k}.csv", comment="#") for k in range(1, 5)]
    A, B = load(dir_a), load(dir_b)
    arr = lambda dfs, c: np.stack([x[c].to_numpy() for x in dfs])
    rows = {}
    for c in S["core"]:
        r = {}
        for lab, dfs in (("a", A), ("b", B)):
            x = arr(dfs, c)
            r[lab] = dict(mean=float(x.mean()), sd=float(x.std()), mcse_mean=float(az.mcse(x, method="mean")),
                          q05=float(np.quantile(x, 0.05)), q50=float(np.quantile(x, 0.5)), q95=float(np.quantile(x, 0.95)),
                          mcse_q05=float(az.mcse(x, method="quantile", prob=0.05)),
                          mcse_q95=float(az.mcse(x, method="quantile", prob=0.95)))
        z = lambda k, m: (r["b"][k] - r["a"][k]) / math.hypot(r["a"][m], r["b"][m])
        r["z_mean"], r["z_q05"], r["z_q95"] = z("mean", "mcse_mean"), z("q05", "mcse_q05"), z("q95", "mcse_q95")
        rows[c] = r
    cost = {lab: [dict(step_size=float(next(ln.split("=")[1] for ln in (pathlib.Path(d) / f"chain{k}.csv").read_text().splitlines()
                                              if "Step size" in ln)),
                       treedepth_median=float(df["treedepth__"].median()), leapfrog_mean=float(df["n_leapfrog__"].mean()),
                       seconds=[float(ln.split()[-3]) for ln in (pathlib.Path(d) / f"chain{k}.csv").read_text().splitlines()
                                if "seconds (" in ln])
                  for k, df in enumerate(dfs, start=1)] for lab, d, dfs in (("a", dir_a, A), ("b", dir_b, B))}
    data_file = data_file or PAY / "data" / "R00.json"
    res = dict(a=str(dir_a), b=str(dir_b), core=rows,
               max_abs_z=max(max(abs(r["z_mean"]), abs(r["z_q05"]), abs(r["z_q95"])) for r in rows.values()),
               z_convention=("descriptive: (b - a) / sqrt(mcse_a^2 + mcse_b^2) assumes zero cross-fit Monte Carlo covariance; "
                             "the fits share seeds and chain IDs, so this is not a calibrated equality test (Codex 76/1855)"),
               cost=cost, joint_state_checks_b=joint_checks(dir_b, data_file))
    pathlib.Path(out_file).write_text(json.dumps(_clean(res), indent=1) + "\n")
    return res


def tranche_preflight():
    """For each fit of the active candidate other than the R00 build reference (Codex 76/1855): data byte-identical to the
    frozen original; starts exact a = 0.2 mappings of the original starts; finite actual-Stan v5/v6 density and AD
    identities at the mapped starts and at sigma 0.01 and 0.001; Q = 64 against the reference at the same scalar points."""
    from cmdstanpy.utils import write_stan_json
    I = P.CFG[P.CFG["active"]]["identity"]
    orig = HERE / "payload"
    mdl_old, mdl_new = P.model(P.CFG[P.CFG[P.CFG["active"]]["reference_version"]]["stan_file"]), P.model()
    work = CACHE / "tranche_preflight"
    work.mkdir(parents=True, exist_ok=True)
    out = {}
    for sc in [s for s in CAND["scenarios"] if s != "R00"]:
        r = dict(data_identical=(PAY / "data" / f"{sc}.json").read_bytes() == (orig / "data" / f"{sc}.json").read_bytes())
        starts = [json.loads((orig / "inits" / sc / f"chain{k}.json").read_text()) for k in range(1, 5)]
        same = []
        for k, q in enumerate(starts, start=1):
            write_stan_json(str(work / f"{sc}_{k}.json"), P.to_nc(q))
            same.append((work / f"{sc}_{k}.json").read_bytes() == (PAY / "inits" / sc / f"chain{k}.json").read_bytes())
        r["starts_exact_mapping"] = all(same)
        d = json.loads((PAY / "data" / f"{sc}.json").read_text())
        pts = {f"start_chain{k}": q for k, q in enumerate(starts, start=1)}
        pts.update(sigma_001=dict(starts[0], sigma=0.01), sigma_0001=dict(starts[0], sigma=0.001))
        ids = {n: P.identity_point(mdl_old, mdl_new, d, q) for n, q in pts.items()}
        worst = {k: max(x[k] for x in ids.values()) for k in ("log_identity_error", "grad_w_error", "grad_logsigma_error", "grad_other_error")}
        r["identity"] = dict(worst=worst, rows=ids, **{"pass": all(x["finite"] for x in ids.values())
                                                         and worst["log_identity_error"] <= I["log_tol"]
                                                         and max(worst[k] for k in worst if k.startswith("grad")) <= I["grad_tol"]})
        gates = {n: gate_point(d, q) for n, q in pts.items()}
        r["q64"] = dict(rows=gates, **{"pass": all(g["pass"] for g in gates.values())})
        r["pass"] = r["data_identical"] and r["starts_exact_mapping"] and r["identity"]["pass"] and r["q64"]["pass"]
        out[sc] = r
    out["all_pass"] = all(v["pass"] for v in out.values() if isinstance(v, dict))
    (HERE / f"tranche_preflight_{PILOT['active_candidate']}.json").write_text(json.dumps(_clean(out), indent=1, default=float) + "\n")
    print(json.dumps(_clean({sc: {k: v for k, v in r.items() if k in ("data_identical", "starts_exact_mapping", "pass")}
                             | dict(identity_worst=r["identity"]["worst"],
                                    q64_worst=max((g["log_err"] for g in r["q64"]["rows"].values()), default=None))
                             for sc, r in out.items() if isinstance(r, dict)} | dict(all_pass=out["all_pass"])), indent=1, default=float))


def _lp(mdl, q, d):
    """Actual-Stan log density and AD gradient (jacobian = true); None if Stan rejects the state, with the message."""
    try:
        row = mdl.log_prob(q, data=d, jacobian=True, sig_figs=15).iloc[0]
        return {k: float(v) for k, v in row.items()}, None
    except (RuntimeError, ValueError) as e:
        return None, str(e)[-400:]


def amended_preflight():
    """Preparation checks for an amended candidate with data overrides and solver controls (Codex 76/1895)."""
    import pandas as pd
    from cmdstanpy.utils import write_stan_json
    ov = CAND["data_overrides"]
    orig, prev = HERE / "payload", HERE / "payload_v6p"
    out = dict(candidate=PILOT["active_candidate"], overrides=ov)
    # 1. Data: field-level difference from the frozen originals is exactly the declared override.
    diffs = {}
    for sc in CAND["scenarios"]:
        new, old = json.loads((PAY / "data" / f"{sc}.json").read_text()), json.loads((orig / "data" / f"{sc}.json").read_text())
        diffs[sc] = sorted(k for k in set(new) | set(old) if new.get(k) != old.get(k))
    out["data_field_differences"] = diffs
    data_ok = all(v == sorted(ov) for v in diffs.values()) and all(
        json.loads((PAY / "data" / f"{sc}.json").read_text())[k] == ov[k] for sc in CAND["scenarios"] for k in ov)
    # 2. Starts identical to the previous package's exact mappings.
    starts_ok = all((PAY / "inits" / sc / f"chain{k}.json").read_bytes() == (prev / "inits" / sc / f"chain{k}.json").read_bytes()
                    for sc in CAND["scenarios"] for k in range(1, 5))
    out["starts_identical_to_v6p"] = starts_ok
    mdl_old, mdl_new = P.model(P.CFG[P.CFG[P.CFG["active"]]["reference_version"]]["stan_file"]), P.model()
    I = P.CFG[P.CFG["active"]]["identity"]
    dP = json.loads((PAY / "data" / "P11.json").read_text())
    d_old_tol = dict(dP, **{k: json.loads((orig / "data" / "P11.json").read_text())[k] for k in ov})
    starts = [json.loads((orig / "inits" / "P11" / f"chain{k}.json").read_text()) for k in range(1, 5)]
    pts = {f"start_chain{k}": q for k, q in enumerate(starts, start=1)}
    pts.update(sigma_001=dict(starts[0], sigma=0.01), sigma_0001=dict(starts[0], sigma=0.001))
    # 3. v5/v6 identities under the new data.
    ids = {n: P.identity_point(mdl_old, mdl_new, dP, q) for n, q in pts.items()}
    worst = {k: max(x[k] for x in ids.values()) for k in ("log_identity_error", "grad_w_error", "grad_logsigma_error", "grad_other_error")}
    id_ok = all(x["finite"] for x in ids.values()) and worst["log_identity_error"] <= I["log_tol"] and \
        max(worst[k] for k in worst if k.startswith("grad")) <= I["grad_tol"]
    out["identity"] = dict(worst=worst, **{"pass": id_ok})
    # 4. Old and new solver thresholds agree on accepted states: starts, small sigma, and the first P11 fit's states.
    fit = HERE.parents[1] / "scratch/q012-pilot/fetch-20261017-v6p/runs/P11/attempt1"
    df = pd.concat([pd.read_csv(fit / f"chain{k}.csv", comment="#") for k in range(1, 5)], ignore_index=True)
    sel = list(dict.fromkeys([int(i) for i in df.nlargest(6, "sigma").index]
                             + [int(df.kappa_b.abs().idxmax()), int(df.rho.idxmin()), int(df.rho.idxmax())]
                             + [int(i) for i in np.linspace(0, len(df) - 1, 40).astype(int)]
                             + [int(i) for i in np.flatnonzero(df.divergent__.to_numpy())]
                             + [int(df.iloc[k * 4000:(k + 1) * 4000].sigma.idxmin()) for k in range(4)]))
    states = dict(pts, **{f"p11_row{i}": P.draw_to_params(df.iloc[i], dP["N"]) for i in sel})
    eq = {}
    for n, q in states.items():
        a, ea = _lp(mdl_new, P.to_nc(q), d_old_tol)
        b, eb = _lp(mdl_new, P.to_nc(q), dP)
        eq[n] = dict(accepted_old=a is not None, accepted_new=b is not None,
                     max_abs_difference=(max(abs(a[k] - b[k]) for k in a) if a and b else None))
    eq_ok = all(r["accepted_old"] and r["accepted_new"] and r["max_abs_difference"] == 0.0 for r in eq.values())
    out["threshold_equivalence"] = dict(states=len(eq), all_identical=eq_ok,
                                        max_abs_difference=max((r["max_abs_difference"] or 0.0) for r in eq.values()),
                                        not_accepted=[n for n, r in eq.items() if not (r["accepted_old"] and r["accepted_new"])])
    # 5. Deterministic controls: p75 newly admitted, p53 still rejected; AD against actual-LP finite differences at p75.
    C = CAND["controls"]
    pdir = HERE.parents[1] / C["probe_dir"]
    dR = json.loads((PAY / "data" / "R00.json").read_text())
    dR_old = dict(dR, **{k: json.loads((orig / "data" / "R00.json").read_text())[k] for k in ov})
    ctl = {}
    for name in (C["accept"], C["reject"]):
        q = json.loads((pdir / f"{name}.json").read_text())
        qp = dict(q, w=q["w"][:dP["N"]])
        for sc, dn, do, qq in (("R00", dR, dR_old, q), ("P11", dP, d_old_tol, qp)):
            new, en = _lp(mdl_new, qq, dn)
            old, eo = _lp(mdl_new, qq, do)
            ctl[f"{name}_{sc}"] = dict(accepted_f10=new is not None, accepted_f11=old is not None,
                                       finite=(all(math.isfinite(v) for v in new.values()) if new else None),
                                       rejection=(en or "")[-200:] if new is None else None)
    qa = json.loads((pdir / f"{C['accept']}.json").read_text())
    qa = dict(qa, w=qa["w"][:dP["N"]])
    base, _ = _lp(mdl_new, qa, dP)
    fd = {}
    h = 1e-4
    for name, col in (("sigma", "g_sigma"), ("kappa_b", "g_kappa_b")):
        shift = (lambda s: dict(qa, sigma=qa["sigma"] * math.exp(s))) if name == "sigma" else (lambda s: dict(qa, kappa_b=qa["kappa_b"] + s))
        hi, _ = _lp(mdl_new, shift(h), dP)
        lo, _ = _lp(mdl_new, shift(-h), dP)
        g = (hi["lp__"] - lo["lp__"]) / (2 * h)
        fd[name] = dict(ad=base[col], fd=g, scaled_error=abs(base[col] - g) / max(1.0, abs(g)))
    ctl_ok = (ctl[f"{C['accept']}_R00"]["accepted_f10"] and not ctl[f"{C['accept']}_R00"]["accepted_f11"]
              and ctl[f"{C['accept']}_P11"]["accepted_f10"] and ctl[f"{C['accept']}_P11"]["finite"]
              and not ctl[f"{C['reject']}_R00"]["accepted_f10"] and not ctl[f"{C['reject']}_P11"]["accepted_f10"]
              and all(v["scaled_error"] <= 1e-6 for v in fd.values()))
    out["controls"] = dict(rows=ctl, finite_difference_at_accept=fd, **{"pass": bool(ctl_ok)})
    # 6. Q = 64 gates at the starts, small sigma and the admitted control (converged reference required).
    qa_eps = dict({k: v for k, v in qa.items() if k != "w"}, eps=list(np.asarray(qa["w"]) / qa["sigma"] ** 0.2))
    gpts = dict(pts, **{f"control_{C['accept']}_P11": qa_eps})
    gates = {n: gate_point(dP, q) for n, q in gpts.items()}
    out["q64"] = dict(rows=gates, **{"pass": all(g["pass"] is True for g in gates.values())})
    out["binding"] = {str(f.relative_to(HERE.parents[1])): sha(f) for f in
                      [PAY / "data" / "P11.json", PAY / "data" / "R00.json", PAY / "model_v6.stan", HERE / "pilot.py",
                       pdir / f"{C['accept']}.json", pdir / f"{C['reject']}.json"] + sorted((PAY / "inits").rglob("*.json"))}
    out["all_pass"] = bool(data_ok and starts_ok and id_ok and eq_ok and ctl_ok and out["q64"]["pass"])
    out["data_ok"] = bool(data_ok)
    (HERE / f"amended_preflight_{PILOT['active_candidate']}.json").write_text(json.dumps(_clean(out), indent=1, default=float) + "\n")
    print(json.dumps(_clean({k: v for k, v in out.items() if k not in ("binding",)} | dict(q64=dict(
        worst_log=max((g.get("log_err") or 0) for g in gates.values()), refs={n: g["reference"] for n, g in gates.items()},
        **{"pass": out["q64"]["pass"]}))), indent=1, default=float)[:5000])


def dispatch_test():
    """Local fixture for stage.sh and submit_fit.sh (Codex 76/1855): fake transport (local bash and cp), fake qsub/qstat that
    record every call, and a local 'remote' root. Writes dispatch_test.json."""
    import os
    root = CACHE / "dispatch_fixture"
    shutil.rmtree(root, ignore_errors=True)
    lib = root / "nectar" / "scripts" / "lib"
    lib.mkdir(parents=True)
    (lib / "common.sh").write_text('die() { echo "DIE: $*" >&2; exit 1; }\nrequire_cmd() { :; }\n')
    (lib / "tpac-expect.exp").write_text("spawn scp \\\n")
    (lib / "kunanyi.sh").write_text(
        'tpac_transport_setup() { TPAC_EXPECT_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/tpac-expect.exp"; export TPAC_EXPECT_SCRIPT; }\n'
        'tpac_set_expect_timeout() { :; }\n'
        'tpac_quote() { printf "%q" "$1"; }\n'
        'tpac_expect_ssh() { bash -c "$1"; }\n'
        'tpac_expect_scp() { cp "$1" "${2#*:}"; }\n')
    log = root / "qsub.log"
    (root / "fake_qsub").write_text(f'#!/bin/bash\necho "$*" >> {log}\nn=$(wc -l < {log}); echo "9000$n.fake"\n')
    (root / "fake_qstat").write_text("#!/bin/bash\necho Job_Name = fake\n")
    for f in ("fake_qsub", "fake_qstat"):
        (root / f).chmod(0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PBS_")}
    env.update(NECTAR_ROOT=str(root / "nectar"), PAYLOAD_DIR=CAND["payload_dir"], QSUB=str(root / "fake_qsub"),
               QSTAT=str(root / "fake_qstat"), REMOTE_BASE=str(root / "remote"), KUNANYI_SSH_ALIAS="fixture")
    run = lambda cmd, extra: subprocess.run(cmd, capture_output=True, text=True, cwd=HERE.parents[1], env=dict(env, **extra))
    calls = lambda: log.read_text().splitlines() if log.exists() else []
    out = {}
    r = run(["bash", str(HERE / "stage.sh"), "fx"], {})
    out["no_fit_scenario_refused"] = dict(exit=r.returncode, calls=calls(), ok=r.returncode != 0 and not calls())
    r = run(["bash", str(HERE / "stage.sh"), "fx"], dict(FIT_SCEN="R00"))
    out["r00_refused"] = dict(exit=r.returncode, calls=calls(), ok=r.returncode != 0 and not calls())
    fits = CAND["fits"]
    first, later = fits[0], (fits[1] if len(fits) > 1 else None)
    others = [s["id"] for s in scenarios() if s["id"] != first]
    r = run(["bash", str(HERE / "stage.sh"), "fx"], dict(FIT_SCEN=first))
    c = calls()
    out[f"stage_{first.lower()}"] = dict(exit=r.returncode, calls=c,
                                         ok=r.returncode == 0 and len(c) == 2 and c[0] == "pbs/build.pbs"
                                         and c[1] == f"-v SCEN={first} -W depend=afterok:90001.fake pbs/fit.pbs"
                                         and not any(o in x for o in others for x in c) and not any("-J" in x for x in c))
    remote = root / "remote" / "q012-pilot-fx"
    out["remote_payload_verified"] = dict(ok=(remote / "manifest.sha256").exists() and (remote / "submitted.txt").exists(),
                                          submitted=(remote / "submitted.txt").read_text().split() if (remote / "submitted.txt").exists() else None)
    n0 = len(calls())
    r = run(["bash", str(HERE / "submit_fit.sh"), "fx", "P06"], {})
    out["p06_refused_without_build"] = dict(exit=r.returncode, ok=r.returncode != 0 and len(calls()) == n0, said=r.stdout[-120:])
    (remote / "build").mkdir(exist_ok=True)
    (remote / "build" / "receipt.txt").write_text(f"status=ok\nmanifest_sha256={sha(remote / 'manifest.sha256')}\n")
    r = run(["bash", str(HERE / "submit_fit.sh"), "fx", "R00"], {})
    out["submit_fit_r00_refused"] = dict(exit=r.returncode, ok=r.returncode != 0 and len(calls()) == n0)
    r = run(["bash", str(HERE / "submit_fit.sh"), "fx", "P06"], {})
    c = calls()
    if later:
        out[f"submit_fit_{later.lower()}_after_build"] = dict(exit=r.returncode, new_calls=c[n0:],
                                                              ok=r.returncode == 0 and c[n0:] == [f"-v SCEN={later} pbs/fit.pbs"])
    else:
        out["submit_fit_p06_refused_even_after_build"] = dict(exit=r.returncode, new_calls=c[n0:],
                                                               ok=r.returncode != 0 and c[n0:] == [])
    out["all_pass"] = all(v["ok"] for v in out.values())
    (HERE / f"dispatch_test_{PILOT['active_candidate']}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- control fixtures
def _run(cmd, root, env=None, timeout=900):
    import os
    e = {k: v for k, v in os.environ.items() if not k.startswith("PBS_") and k != "LOADEDMODULES"}
    e.update(PILOT_ROOT=str(root), **(env or {}))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=root, env=e, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def _fixture_seal(root, binary=None):
    """Rewrite a fixture's manifest and a successful build receipt bound to it."""
    binary = binary or RUN_ENV["MODEL_BIN"][2:]
    write_manifest(root)
    (root / "build").mkdir(exist_ok=True)
    (root / "build" / "receipt.txt").write_text(
        f"status=ok\nmanifest_sha256={sha(root / 'manifest.sha256')}\nbinary_sha256={sha(root / binary)}\n")


def _write_env(root, env):
    (root / "run.env").write_text("".join(f"{k}={v}\n" for k, v in env.items()))


def selftest():
    """Cheap fixtures for every control the cluster relies on; writes selftest.json. Uses the local CmdStan binary."""
    from cmdstanpy.utils import write_stan_json
    import os
    import signal
    out = {}
    # Generator controls.
    o = generate(20261017, dict(lineage_cap=30), 60)
    out["generator_cap"] = dict(outcome=o[0], ok=o[0] == "capped")
    o = generate(20261017, {}, 0.001)
    out["generator_timeout"] = dict(outcome=o[0], ok=o[0] == "timeout")
    # Runner fixtures: the frozen-seed dataset (62 lineages), the payload's scripts and the local binary.
    root = CACHE / "selftest"
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(PAY / "pbs", root / "pbs")
    exe = P.OUT / P.CFG[P.CFG["active"]]["stan_file"].removesuffix(".stan")
    shutil.copy(exe, root / RUN_ENV["MODEL_BIN"][2:])
    d, _, _ = P.dataset(P.CFG["seed"])
    (root / "data").mkdir()
    for scen in ("FX", "FY", "FB", "FT"):
        write_stan_json(str(root / "data" / f"{scen}.json"), d)
        write_starts(root / "inits" / scen, d["N"])
    bad = json.loads((root / "inits" / "FB" / "chain2.json").read_text())
    bad["sigma"] = -1.0
    (root / "inits" / "FB" / "chain2.json").write_text(json.dumps(bad))
    (root / "scenarios.tsv").write_text("id\trole\n" + "FX\treplay\nFY\tpanel\nFB\treplay\nFT\treplay\n")
    env = dict(RUN_ENV, WARMUP=10, SAMPLING=5, FIT_SECONDS=600, MODULE="")
    _write_env(root, env)
    _fixture_seal(root)
    fit = ["bash", "pbs/fit.sh"]

    code, txt = _run(fit, root, dict(SCEN="FX"))
    rc = _receipt(root / "runs" / "FX" / "receipt.txt")
    out["complete"] = dict(exit=code, status=rc.get("status"), maxrss_kb=[rc.get(f"chain{k}_maxrss_kb") for k in range(1, 5)],
                           ok=code == 0 and rc.get("status") == "complete")
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["resume_skip"] = dict(exit=code, ok=code == 0 and "SKIP" in txt and not (root / "runs" / "FX" / "attempt2").exists())
    code, txt = _run(fit, root, dict(PBS_ARRAY_INDEX="1"))
    out["array_index_maps_to_first_panel_row"] = dict(exit=code, ok=code == 0 and (root / "runs" / "FY" / "receipt.txt").exists())
    code, txt = _run(fit, root, dict(SCEN="FB"))
    rc = _receipt(root / "runs" / "FB" / "receipt.txt")
    out["chain_failure"] = dict(exit=code, status=rc.get("status"), chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, 5)],
                                ok=code == 1 and rc.get("status") == "failed" and rc.get("chain2_exit") != "0")
    # Module: a declared module that is not loaded is refused; when loaded, the runner proceeds (here to the skip).
    _write_env(root, dict(env, MODULE=RUN_ENV["MODULE"]))
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["module_not_loaded_refused"] = dict(exit=code, ok=code == 2 and "module" in txt)
    code, txt = _run(fit, root, dict(SCEN="NODATA", LOADEDMODULES=f"GCCcore/12.3.0:{RUN_ENV['MODULE']}"))
    out["module_loaded_passes_module_check"] = dict(exit=code, ok=code == 2 and "no data or starts" in txt)
    _write_env(root, env)
    _fixture_seal(root)
    # Signal, cooperative model: TERM the runner mid-fit.
    slow = dict(env, WARMUP=2000, SAMPLING=2000)
    _write_env(root, slow)
    _fixture_seal(root)

    def term_test(scen, wait):
        p = subprocess.Popen(fit, cwd=root, env=dict({k: v for k, v in os.environ.items() if not k.startswith("PBS_")},
                                                      PILOT_ROOT=str(root), SCEN=scen),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        time.sleep(wait)
        p.send_signal(signal.SIGTERM)
        p.wait(60)
        rc = _receipt(root / "runs" / scen / "receipt.txt")
        left = subprocess.run(["pgrep", "-f", f"runs/{scen}/attempt"], capture_output=True, text=True).stdout.split()
        left += subprocess.run(["pgrep", "-f", "fake_model"], capture_output=True, text=True).stdout.split()
        return p.returncode, rc, left
    code, rc, left = term_test("FT", 8)
    out["signal_term"] = dict(exit=code, status=rc.get("status"), cleanup=rc.get("cleanup"), left_running=left,
                              ok=code == 3 and rc.get("status") == "terminated_TERM" and not left)
    # Signal, TERM-ignoring model: the runner must escalate to KILL and leave nothing behind before the receipt.
    (root / "fake_model").write_text("#!/bin/bash\ntrap '' TERM\nwhile :; do sleep 1; done\n")
    (root / "fake_model").chmod(0o755)
    _write_env(root, dict(slow, MODEL_BIN="./fake_model"))
    _fixture_seal(root, "fake_model")
    code, rc, left = term_test("FY", 3)
    for pid in left:
        subprocess.run(["kill", "-KILL", pid])
    out["signal_term_ignoring_model"] = dict(exit=code, status=rc.get("status"), cleanup=rc.get("cleanup"), left_running=left,
                                             ok=code == 3 and rc.get("status") == "terminated_TERM" and not left
                                             and "kill_escalated yes" in rc.get("cleanup", "") and "survivors no" in rc.get("cleanup", ""))
    # Timeout: a 3-second fit limit.
    _write_env(root, dict(slow, FIT_SECONDS=3))
    _fixture_seal(root)
    code, txt = _run(fit, root, dict(SCEN="FT"))
    rc = _receipt(root / "runs" / "FT" / "receipt.txt")
    out["timeout"] = dict(exit=code, status=rc.get("status"), attempt=rc.get("attempt"),
                          chain_exits=[rc.get(f"chain{k}_exit") for k in range(1, 5)],
                          ok=code == 4 and rc.get("status") == "timeout" and rc.get("attempt") == "2")
    _write_env(root, env)
    _fixture_seal(root)
    # Refusals: stale data, a binary differing from the build receipt, and a build receipt for another manifest.
    f = root / "data" / "FY.json"
    f.write_text(f.read_text() + " ")
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["stale_data_refused"] = dict(exit=code, ok=code == 2 and "manifest mismatch" in txt)
    _fixture_seal(root)
    br = (root / "build" / "receipt.txt").read_text()
    (root / "build" / "receipt.txt").write_text(br.replace(f"binary_sha256={sha(root / RUN_ENV['MODEL_BIN'][2:])}", "binary_sha256=" + "0" * 64))
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["binary_mismatch_refused"] = dict(exit=code, ok=code == 2 and "binary hash" in txt)
    (root / "build" / "receipt.txt").write_text(br.replace(f"manifest_sha256={sha(root / 'manifest.sha256')}", "manifest_sha256=" + "1" * 64))
    code, txt = _run(fit, root, dict(SCEN="FX"))
    out["build_manifest_mismatch_refused"] = dict(exit=code, ok=code == 2 and "different payload manifest" in txt)
    (root / "build" / "receipt.txt").write_text(br)
    # Screening refuses failed, mismatched or malformed output before any statistics.
    good = root / "runs" / "FX" / "attempt1"
    man, bld = sha(root / "manifest.sha256"), _receipt(root / "build" / "receipt.txt")
    # The FX receipt predates later reseals; requalify it against the manifest and binary it was produced under.
    rcx = _receipt(good / "receipt.txt")
    q = lambda a, s="FX", e=env, m=None, b=None: qualify(a, s, e, m or rcx["manifest_sha256"],
                                                         b or dict(bld, manifest_sha256=rcx["manifest_sha256"]))
    scr = {}
    scr["good_attempt_qualifies"] = (q(good), lambda r: r == [])

    def variant(name, mutate):
        v = root / "runs" / "DX" / name / "attempt1"
        shutil.copytree(good, v)
        mutate(v)
        return v
    scr["no_receipt"] = (q(variant("norec", lambda v: (v / "receipt.txt").unlink())), bool)
    scr["receipt_for_other_scenario_failed_and_stale"] = (q(variant("other", lambda v: (v / "receipt.txt").write_text(
        (v / "receipt.txt").read_text().replace("scenario=FX", "scenario=P12").replace("status=complete", "status=failed")
        .replace(rcx["manifest_sha256"], "2" * 64)))), bool)
    scr["nonzero_chain_exit"] = (q(variant("exit", lambda v: (v / "chain3.exit").write_text("1\n"))), bool)
    def inject(fname, after, text):
        def f(v):
            lines = (v / fname).read_text().split("\n")
            k = next(i for i, ln in enumerate(lines) if ln.startswith(after)) + 1
            (v / fname).write_text("\n".join(lines[:k] + text.split("\n") + lines[k:]))
        return f
    scr["fatal_text_in_log"] = (q(variant("fatal", inject("chain1.log", "Iteration:  3 /", "Exception: fatal"))), bool)
    scr["separate_stderr_file"] = (q(variant("stderr", lambda v: (v / "chain1.stderr").write_text(""))), bool)
    scr["fewer_draws_than_declared"] = (q(good, e=dict(env, SAMPLING=6)), bool)

    def drop_row(v):
        lines = (v / "chain2.csv").read_text().splitlines()
        j = max(i for i, ln in enumerate(lines) if ln and not ln.startswith("#"))
        (v / "chain2.csv").write_text("\n".join(lines[:j] + lines[j + 1:]) + "\n")
    scr["unequal_chain_lengths"] = (q(variant("short", drop_row)), bool)
    scr["fifth_csv"] = (q(variant("fifth", lambda v: shutil.copy(v / "chain1.csv", v / "chain5.csv"))), bool)
    scr["csv_settings_mismatch"] = (q(variant("meta", lambda v: (v / "chain3.csv").write_text(
        (v / "chain3.csv").read_text().replace("delta = 0.995", "delta = 0.9", 1)))), bool)
    scr["build_receipt_other_manifest"] = (q(good, b=dict(bld, manifest_sha256="3" * 64)), bool)

    def no_hash(v):
        (v / "receipt.txt").write_text("\n".join(ln for ln in (v / "receipt.txt").read_text().splitlines()
                                                 if not ln.startswith("binary_sha256=")) + "\n")
    nb = {k: x for k, x in dict(bld, manifest_sha256=rcx["manifest_sha256"]).items() if k != "binary_sha256"}
    scr["binary_hash_absent_from_both_receipts"] = (q(variant("nohash", no_hash), b=nb), bool)
    out["screening_refusals"] = {k: dict(failures=r[:3], ok=pred(r)) for k, (r, pred) in scr.items()}
    out["screening_refusals"]["ok"] = all(v["ok"] for v in out["screening_refusals"].values())
    # The combined-log parser on a real fixture log (WARMUP 10, SAMPLING 5, refresh 1): phase boundaries and failure cases.
    log = (good / "chain1.log").read_text()
    W, S = int(env["WARMUP"]), int(env["SAMPLING"])
    env_text = lambda exc: "\n".join([LOG_FIXED["rej"], exc, LOG_FIXED["rej3"], LOG_FIXED["rej4"], ""])
    known = "Exception: Exception: Q012 input failure: 1-D initial score (in 'model_v6.stan', line 39)"

    def after(text, prefix, ins):
        lines = text.split("\n")
        k = next(i for i, ln in enumerate(lines) if ln.startswith(prefix)) + 1
        return "\n".join(lines[:k] + ins.split("\n") + lines[k:])

    def drop(text, prefix):
        return "\n".join(ln for ln in text.split("\n") if not ln.startswith(prefix))
    last_warm = f"Iteration: {W} / {W + S}"
    first_samp = f"Iteration: {W + 1} / {W + S}"
    cases = dict(
        clean=(log, lambda f, r: not f and not r),
        warmup_rejection=(after(log, "Iteration:  3 /", env_text(known)),
                          lambda f, r: not f and [(x["phase"], x["transition"], x["cause"]) for x in r] == [("warmup", 3, "input")]),
        boundary_last_warmup=(after(log, last_warm, env_text(known)),
                              lambda f, r: not f and [(x["phase"], x["transition"]) for x in r] == [("warmup", W)]),
        boundary_first_sampling=(after(log, first_samp, env_text(known)),
                                 lambda f, r: not f and [(x["phase"], x["transition"]) for x in r] == [("sampling", W + 1)]),
        stepsize_init_rejection=(after(log, "Adjust your expectations", env_text(known)),
                                 lambda f, r: not f and [x["phase"] for x in r] == ["stepsize_init"]),
        init_rejection=(after(log, "num_threads", "\n".join([LOG_FIXED["init"], LOG_FIXED["init_eval"], known])),
                        lambda f, r: not f and [x["phase"] for x in r] == ["init"]),
        unknown_text=(after(log, "Iteration:  5 /", "Something unexpected happened"), lambda f, r: bool(f)),
        unrecognised_cause=(after(log, "Iteration:  5 /", env_text("Exception: Exception: cholesky_decompose: A is not symmetric")),
                            lambda f, r: bool(f)),
        incomplete_envelope=(after(log, "Iteration:  5 /", "\n".join([LOG_FIXED["rej"], known])), lambda f, r: bool(f)),
        orphan_exception=(after(log, "Iteration:  5 /", known), lambda f, r: bool(f)),
        missing_marker=(drop(log, "Iteration:  7 /"), lambda f, r: bool(f)),
        truncated=(log[:log.index(first_samp)], lambda f, r: bool(f)),
        fatal_step_size=(after(log, "Adjust your expectations", "Exception initializing step size.\n" + known), lambda f, r: bool(f)))
    pr = {}
    for name, (text, ok) in cases.items():
        f, r = parse_log(text, W, S)
        pr[name] = dict(failures=f[:2], rejections=[(x["phase"], x["transition"], x["cause"]) for x in r], ok=bool(ok(f, r)))
    pr["ok"] = all(v["ok"] for v in pr.values())
    out["log_parser"] = pr
    # End to end: a sampling-phase rejection leaves the attempt qualified but fails the screen.
    sv = variant("samprej", inject("chain2.log", first_samp, env_text(known)))
    rs = diagnose(sv, "FX", env=env, manifest_sha=rcx["manifest_sha256"], build_receipt=dict(bld, manifest_sha256=rcx["manifest_sha256"]), write=False)
    out["sampling_rejection_fails_screen"] = dict(qualified=rs["qualified"], criterion=rs.get("screening", {}).get("no_fatal_or_sampling_phase_failures"),
                                                  ok=rs["qualified"] and rs.get("screening", {}).get("no_fatal_or_sampling_phase_failures") is False)
    # Finite guards on statistics.
    nan, inf = float("nan"), float("inf")
    eb = eta_block(0.03, 0.40, 0.003, nan, 0.2)
    out["finite_guards"] = dict(
        nan_mcse_leaves_precision_unresolved=eb["mcse_target_met"] is None and eb["X_numerically_uncertain"] is None,
        raw_flags_kept=eb["D"] is False and eb["X"] is False,
        infinite_ess_fails=not ess_pass({"sigma": dict(bulk=inf, tail=500.0)}),
        nan_rhat_fails=not rhat_pass({"sigma": nan}),
        nan_endpoint_unresolved=eta_block(nan, 0.4, 0.003, 0.01, 0.2)["D"] is None,
        nan_endpoint_leaves_precision_unresolved=eta_block(nan, 0.4, 0.003, 0.01, 0.2)["mcse_target_met"] is None)
    out["finite_guards"]["ok"] = all(out["finite_guards"].values())
    # Retrieval after the earliest failure: a failed build and no run directory.
    fx = CACHE / "selftest_fetch"
    shutil.rmtree(fx, ignore_errors=True)
    (fx / "build").mkdir(parents=True)
    shutil.copytree(PAY / "pbs", fx / "pbs")
    (fx / "build" / "receipt.txt").write_text("status=failed\nreason=cmdstan_build\n")
    (fx / "build" / "cmdstan_build.log").write_text("make: *** [error] 2\n")
    (fx / "submitted.txt").write_text("BUILD_JOB=1.kunanyi FIT_JOB=2.kunanyi\n")
    (fx / "q012_build.o1").write_text("BUILD FAILED: cmdstan_build\n")
    code, txt = _run(["bash", "pbs/pack.sh", "R00"], fx)
    listing = subprocess.run(["tar", "tzf", str(fx / "fetch-R00.tar.gz")], capture_output=True, text=True).stdout.split()
    out["fetch_after_failed_build"] = dict(exit=code, archived=listing,
                                           ok=code == 0 and "build/receipt.txt" in listing and "q012_build.o1" in listing)
    # Provenance: mutating a consumed saved-draw bank changes the prototype binding (on a copy of the banks).
    banks = CACHE / "selftest_banks"
    shutil.rmtree(banks, ignore_errors=True)
    for b in P.SAVED_BANKS:
        (banks / b).mkdir(parents=True)
        for f in (P.OUT / b).glob("*.csv"):
            shutil.copy(f, banks / b / f.name)
    d_fit, _, _ = P.dataset(P.CFG["fit_seed"])
    real_out, chk = P.OUT, json.loads((HERE / CAND["checks_file"]).read_text())
    try:
        P.OUT = banks
        before = P.binding(d_fit) == chk["binding"]
        tgt = sorted((banks / "fit_v4").glob("*_3.csv"))[0]
        tgt.write_text(tgt.read_text().replace("2.9932533", "3.0932533", 1))
        after = P.binding(d_fit) == chk["binding"]
    finally:
        P.OUT = real_out
    out["bank_mutation_breaks_binding"] = dict(copy_matches_checks=before, matches_after_mutation=after, ok=before and not after)
    # Preflight on a copy of the real payload with the local binary: must pass, and a perturbed reference must fail.
    pf = CACHE / "selftest_preflight"
    shutil.rmtree(pf, ignore_errors=True)
    shutil.copytree(PAY, pf, ignore=shutil.ignore_patterns("runs", "build"))
    shutil.copy(exe, pf / RUN_ENV["MODEL_BIN"][2:])
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=1200)
    out["preflight_local_binary"] = dict(exit=code, receipt=(pf / "build" / "receipt.tmp").read_text().split(), ok=code == 0)
    refs = sorted((pf / "preflight").glob("ref_point_*.csv"))
    lines = refs[0].read_text().splitlines()
    i = max(j for j, ln in enumerate(lines) if ln and not ln.startswith("#"))
    vals = lines[i].split(",")
    vals[0] = repr(float(vals[0]) * (1 + 1e-5))
    lines[i] = ",".join(vals)
    refs[0].write_text("\n".join(lines) + "\n")
    shutil.rmtree(pf / "build")
    code, txt = _run(["bash", "pbs/preflight.sh", "build/receipt.tmp"], pf, timeout=600)
    reason = (pf / "build" / "preflight_reason.txt").read_text().strip()
    out["preflight_mismatch_detected"] = dict(exit=code, reason=reason, ok=code == 1 and "mismatch" in reason)
    out["all_pass"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    (HERE / "selftest.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "diagnose":
        r = diagnose(sys.argv[2], sys.argv[3])
        print(json.dumps({k: v for k, v in r.items() if k not in ("chains", "rhat_over_threshold")}, indent=1))
    elif cmd == "summarise":
        summarise(sys.argv[2])
    elif cmd == "compare":
        r = compare(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(_clean({k: v for k, v in r.items() if k not in ("core", "cost", "joint_state_checks_b")}), indent=1))
    elif cmd == "joint":
        r = joint_checks(sys.argv[2], sys.argv[3])
        pathlib.Path(sys.argv[4]).write_text(json.dumps(_clean(r), indent=1) + "\n")
        print(json.dumps(_clean({k: v for k, v in r.items() if k != "states"}), indent=1))
    elif cmd == "tranche-preflight":
        tranche_preflight()
    elif cmd == "dispatch-test":
        dispatch_test()
    elif cmd == "amended-preflight":
        amended_preflight()
    else:
        {"build": build, "selftest": selftest}[cmd]()
