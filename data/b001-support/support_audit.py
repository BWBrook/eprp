"""B-001 support audit: Knope et al. 2015 coding joined to PBDB occurrences.

Implements the definitions fixed in section 8 of
literature/2026-10-14-b001-reassembly-contract.md (commit e7697d9).
Computes support only: baseline richness, coverage, survivors, join rates,
guild x event x class incidence and the covariance-basis rank. It computes
no post-event richness and no crossing or restoration time.

Run from the repository root:
  uv run -q --no-project --with xlrd==2.0.1 --with numpy==2.1.3 \
      python -I data/b001-support/support_audit.py
"""

import collections
import csv
import hashlib
import io
import itertools
import json
import math
import pathlib
import urllib.request

import numpy as np
import xlrd

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "data/raw"
KNOPE = RAW / "knope2015/41467_2015_BFncomms7455_MOESM1087_ESM.xls"
KNOPE_SHA = "e5c1eef44f51e788c12c80efdceba9e6597472af57d0a7146ae8f015ecf3f181"
TAXA = RAW / "pbdb/b001/genera.csv"
PHYLA = ["Mollusca", "Brachiopoda", "Echinodermata", "Cnidaria", "Arthropoda",
         "Chordata", "Porifera", "Bryozoa", "Hemichordata"]
OCC_URL = ("https://paleobiodb.org/data1.2/occs/list.csv?base_name={phyla}"
           "&max_ma={old}&min_ma={young}&timerule=overlap&envtype=marine&pres=regular"
           "&idqual=genus_certain&idreso=lump_genus&show=class&datainfo&limit=all")

# PBDB timescale 1 stage bounds (base, top), as served on 15 October 2026.
STAGES = {
    "Wuchiapingian": (259.857, 254.14), "Changhsingian": (254.14, 251.902),
    "Induan": (251.902, 250.8), "Olenekian": (250.8, 247.0),
    "Anisian": (247.0, 241.464), "Ladinian": (241.464, 237.0),
    "Norian": (227.3, 205.7), "Rhaetian": (205.7, 201.4),
    "Hettangian": (201.4, 199.5), "Sinemurian": (199.5, 192.9),
    "Pliensbachian": (192.9, 184.2), "Toarcian": (184.2, 174.7),
    "Campanian": (83.6, 72.2), "Maastrichtian": (72.2, 66.0),
    "Danian": (66.0, 61.66), "Selandian": (61.66, 59.24),
    "Thanetian": (59.24, 56.0), "Ypresian": (56.0, 48.07),
}
EVENTS = {
    "end_permian": dict(age=251.902, penultimate="Wuchiapingian", baseline="Changhsingian",
                        follow=["Induan", "Olenekian", "Anisian"], confirm="Ladinian"),
    "end_triassic": dict(age=201.4, penultimate="Norian", baseline="Rhaetian",
                         follow=["Hettangian", "Sinemurian", "Pliensbachian"], confirm="Toarcian"),
    "k_pg": dict(age=66.0, penultimate="Campanian", baseline="Maastrichtian",
                 follow=["Danian", "Selandian", "Thanetian"], confirm="Ypresian"),
}
QUORUM, MIN_BASELINE, MIN_COLLECTIONS = 0.5, 5.0, 50
TIER = {1: "pelagic", 2: "epifaunal", 3: "epifaunal", 4: "infaunal", 5: "infaunal", 6: "infaunal"}
MOT = {1: "fast", 2: "slow", 3: "stationary", 4: "stationary", 5: "stationary", 6: "stationary"}
FEED = {1: "suspension", 2: "deposit", 3: "deposit", 4: "grazing", 5: "predatory", 6: "other"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_pbdb_csv(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    meta = [l for l in lines[:40] if l.startswith(('"Access Time"', '"Records Found"', '"Records Returned"'))]
    start = next(i for i, l in enumerate(lines) if l.startswith('"occurrence_no"') or l.startswith('"orig_no"'))
    return meta, list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))


def fetch_occurrences(event, cfg):
    stages = [cfg["penultimate"], cfg["baseline"], *cfg["follow"], cfg["confirm"]]
    old, young = STAGES[stages[0]][0], STAGES[stages[-1]][1]
    path = RAW / f"pbdb/b001/occs_{event}.csv"
    if not path.exists():
        url = OCC_URL.format(phyla=",".join(PHYLA), old=old, young=young)
        with urllib.request.urlopen(url, timeout=900) as r:
            path.write_bytes(r.read())
    meta, rows = read_pbdb_csv(path)
    return path, meta, rows


def stage_of(row):
    hi, lo = float(row["max_ma"]), float(row["min_ma"])
    for name, (base, top) in STAGES.items():
        if hi <= base + 1e-6 and lo >= top - 1e-6:
            return name
    return None


def load_knope():
    assert sha256(KNOPE) == KNOPE_SHA, "Knope workbook hash differs"
    s = xlrd.open_workbook(str(KNOPE)).sheet_by_index(0)
    hdr = s.row_values(0)
    rows = [dict(zip(hdr, s.row_values(i))) for i in range(1, s.nrows)]
    by_name_phylum, by_name = {}, collections.defaultdict(list)
    for r in rows:
        rec = dict(tier=int(r["tiering"]), mot=int(r["motility"]), feed=int(r["feeding"]),
                   cls=r["class"], phylum=r["phylum"], ref=str(r["eco_ref"]).split(".")[0][:60])
        by_name_phylum[(r["taxon_name"], r["phylum"])] = rec
        by_name[r["taxon_name"]].append(rec)
    return len(rows), by_name_phylum, by_name


def knope_lookup(genus, phylum, by_name_phylum, by_name):
    if (genus, phylum) in by_name_phylum:
        return by_name_phylum[(genus, phylum)], "name+phylum"
    if len(by_name.get(genus, [])) == 1:
        return by_name[genus][0], "name"
    return None, "ambiguous" if genus in by_name else "absent"


def load_lastapp():
    meta, rows = read_pbdb_csv(TAXA)
    out = {}
    for r in rows:
        try:
            out[(r["taxon_name"], r["phylum"])] = float(r["lastapp_max_ma"])
        except ValueError:
            pass
    return out


def log_choose(n, k):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def coverage_rarefied_richness(counts, target):
    """Chao & Jost (2012) abundance-based rarefaction to sample coverage `target`."""
    n = sum(counts)

    def cov(m):
        if m >= n:
            return None
        den = log_choose(n - 1, m)
        return 1 - sum((x / n) * math.exp(log_choose(n - x, m) - den) for x in counts if n - x >= m)

    def rich(m):
        den = log_choose(n, m)
        return sum(1 - (math.exp(log_choose(n - x, m) - den) if n - x >= m else 0) for x in counts)

    prev_m, prev_c = 1, cov(1)
    if prev_c is None or prev_c >= target:
        return rich(1) if prev_c is not None else float(len(counts))
    for m in range(2, n):
        c = cov(m)
        if c >= target:
            w = (target - prev_c) / (c - prev_c) if c > prev_c else 1.0
            return rich(prev_m) + w * (rich(m) - rich(prev_m))
        prev_m, prev_c = m, c
    return float(len(counts))


def cell_stats(genus_counts):
    counts = list(genus_counts.values())
    n = sum(counts)
    f1 = sum(1 for x in counts if x == 1)
    u = 1 - f1 / n if n else 0.0
    return n, len(counts), u


def guild_key(rec, merged):
    tier, mot, feed = TIER[rec["tier"]], MOT[rec["mot"]], FEED[rec["feed"]]
    if mot in ("fast", "slow") and (tier, feed) in merged:
        mot = "mobile"
    return f"{tier}|{mot}|{feed}"


def main():
    n_knope, by_name_phylum, by_name = load_knope()
    lastapp = load_lastapp()
    summary = dict(knope_rows=n_knope, knope_distinct_names=len(by_name),
                   knope_sha256=KNOPE_SHA, taxa_extract_sha256=sha256(TAXA), events={})
    occ = {}
    for event, cfg in EVENTS.items():
        path, meta, rows = fetch_occurrences(event, cfg)
        summary["events"][event] = dict(extract=str(path.relative_to(ROOT)), sha256=sha256(path),
                                        datainfo=meta, rows=len(rows))
        occ[event] = rows
        print(event, len(rows), meta)

    join_rows = [["event", "stage", "role", "collections", "occurrences",
                  "genera", "genera_joined", "genera_join_share", "occ_join_share",
                  "join_name_phylum", "join_name_only", "unjoined_ambiguous", "unjoined_absent"]]
    class_join = collections.defaultdict(lambda: [0, 0])
    cells = {}
    for event, cfg in EVENTS.items():
        roles = {cfg["penultimate"]: "penultimate", cfg["baseline"]: "baseline",
                 **{s: "follow" for s in cfg["follow"]}, cfg["confirm"]: "confirm"}
        by_stage = collections.defaultdict(list)
        unbinned = 0
        for r in occ[event]:
            st = stage_of(r)
            if st in roles:
                by_stage[st].append(r)
            else:
                unbinned += 1
        summary["events"][event]["occurrences_not_in_one_stage"] = unbinned
        for st, role in roles.items():
            rs = by_stage[st]
            colls = {r["collection_no"] for r in rs}
            genera = {}
            how = collections.Counter()
            occ_joined = 0
            for r in rs:
                g, ph = r["genus"], r["phylum"]
                if not g:
                    continue
                rec, mode = knope_lookup(g, ph, by_name_phylum, by_name)
                genera[(g, ph)] = (rec, mode)
                occ_joined += rec is not None
                cell = cells.setdefault((event, st), {})
                if rec is not None:
                    cell.setdefault((g, ph), [rec, 0])[1] += 1
                pre_post = "pre" if role in ("penultimate", "baseline") else "post"
                class_join[(event, pre_post, r["class"] or "(none)")][0] += 1
                class_join[(event, pre_post, r["class"] or "(none)")][1] += rec is not None
            for rec, mode in genera.values():
                how[mode] += 1
            joined = how["name+phylum"] + how["name"]
            join_rows.append([event, st, role, len(colls), len(rs), len(genera), joined,
                              f"{joined / len(genera):.3f}" if genera else "NA",
                              f"{occ_joined / len(rs):.3f}" if rs else "NA",
                              how["name+phylum"], how["name"], how["ambiguous"], how["absent"]])

    def baseline_support(merged):
        sup = collections.defaultdict(dict)
        for event, cfg in EVENTS.items():
            g = collections.defaultdict(collections.Counter)
            for (gen, ph), (rec, k) in cells.get((event, cfg["baseline"]), {}).items():
                g[guild_key(rec, merged)][(gen, ph)] += k
            for guild, cnt in g.items():
                n, s, u = cell_stats(cnt)
                rich = coverage_rarefied_richness(list(cnt.values()), QUORUM) if u >= QUORUM else None
                sup[guild][event] = (u >= QUORUM and rich is not None and rich >= MIN_BASELINE)
        return sup

    sup0 = baseline_support(set())
    all_guilds = {guild_key(rec, set()) for c in cells.values() for rec, _ in c.values()}
    merged = set()
    for guild in all_guilds:
        tier, mot, feed = guild.split("|")
        if mot in ("fast", "slow") and not any(sup0.get(guild, {}).values()):
            merged.add((tier, feed))
    summary["merged_tier_feed"] = sorted("|".join(x) for x in merged)

    stage_support = {}
    for row in join_rows[1:]:
        stage_support[(row[0], row[1])] = row[3] >= MIN_COLLECTIONS

    guild_stage = [["event", "stage", "role", "guild", "occurrences", "genera", "goods_u",
                    "resolved", "stage_supported", "subsampled_richness_at_0.5"]]
    at_risk = [["event", "guild", "baseline_occurrences", "baseline_genera", "baseline_u",
                "baseline_richness_0.5", "penultimate_richness_0.5", "survivors",
                "dominant_class", "dominant_share", "class_composition", "at_risk",
                "follow_stages_resolved", "confirm_resolved"]]
    incidence = []
    excluded = collections.Counter()
    for event, cfg in EVENTS.items():
        roles = {cfg["penultimate"]: "penultimate", cfg["baseline"]: "baseline",
                 **{s: "follow" for s in cfg["follow"]}, cfg["confirm"]: "confirm"}
        per_stage = {}
        for st, role in roles.items():
            g = collections.defaultdict(collections.Counter)
            cls = collections.defaultdict(collections.Counter)
            for (gen, ph), (rec, k) in cells.get((event, st), {}).items():
                key = guild_key(rec, merged)
                g[key][(gen, ph)] += k
                cls[key][rec["cls"]] += k
            per_stage[st] = (g, cls)
            for guild, cnt in sorted(g.items()):
                n, s, u = cell_stats(cnt)
                rich = ""
                if role in ("penultimate", "baseline") and u >= QUORUM:
                    rich = f"{coverage_rarefied_richness(list(cnt.values()), QUORUM):.2f}"
                guild_stage.append([event, st, role, guild, n, s, f"{u:.3f}", u >= QUORUM,
                                    stage_support[(event, st)], rich])
        g_base, cls_base = per_stage[cfg["baseline"]]
        g_pen, _ = per_stage[cfg["penultimate"]]
        for guild, cnt in sorted(g_base.items()):
            n, s, u = cell_stats(cnt)
            rich = coverage_rarefied_richness(list(cnt.values()), QUORUM) if u >= QUORUM else None
            pen = g_pen.get(guild)
            pen_rich = (coverage_rarefied_richness(list(pen.values()), QUORUM)
                        if pen and cell_stats(pen)[2] >= QUORUM else None)
            surv = sum(1 for (gen, ph) in cnt if lastapp.get((gen, ph), 1e9) < cfg["age"])
            comp = cls_base[guild]
            dom, dom_n = comp.most_common(1)[0]
            risk = (stage_support[(event, cfg["baseline"])] and u >= QUORUM
                    and rich is not None and rich >= MIN_BASELINE)
            if not risk:
                excluded[event] += 1
            follow_res = sum(1 for st in cfg["follow"]
                             if stage_support[(event, st)] and guild in per_stage[st][0]
                             and cell_stats(per_stage[st][0][guild])[2] >= QUORUM)
            conf = per_stage[cfg["confirm"]][0].get(guild)
            conf_res = bool(stage_support[(event, cfg["confirm"])] and conf
                            and cell_stats(conf)[2] >= QUORUM)
            at_risk.append([event, guild, n, s, f"{u:.3f}",
                            f"{rich:.2f}" if rich is not None else "",
                            f"{pen_rich:.2f}" if pen_rich is not None else "", surv, dom,
                            f"{dom_n / n:.3f}",
                            ";".join(f"{c}:{k}" for c, k in comp.most_common()), risk,
                            f"{follow_res}/{len(cfg['follow'])}", conf_res])
            if risk:
                incidence.append(dict(event=event, guild=guild, cls=dom, surv=surv,
                                      base=rich, comp=dict(comp)))

    summary["at_risk_per_event"] = dict(collections.Counter(c["event"] for c in incidence))
    summary["baseline_guilds_not_at_risk"] = dict(excluded)
    summary["zero_survivor_cells"] = sum(c["surv"] == 0 for c in incidence)
    guilds_events = collections.defaultdict(dict)
    for c in incidence:
        guilds_events[c["guild"]][c["event"]] = c["cls"]
    summary["guilds_at_risk_in_all_three"] = sum(len(v) == 3 for v in guilds_events.values())
    summary["guilds_at_risk_in_two_or_more"] = sum(len(v) >= 2 for v in guilds_events.values())
    summary["guilds_with_dominant_class_switch"] = sorted(
        g for g, v in guilds_events.items() if len(v) >= 2 and len(set(v.values())) > 1)

    pairs = collections.Counter()
    for a, b in itertools.combinations(incidence, 2):
        sg, sc = a["guild"] == b["guild"], a["cls"] == b["cls"]
        pairs[("same_guild" if sg else "diff_guild") + "|" + ("same_class" if sc else "diff_class")] += 1
    summary["pair_types"] = dict(pairs)

    nc = len(incidence)
    G = np.array([[float(a["guild"] == b["guild"]) for b in incidence] for a in incidence])
    C = np.array([[float(a["cls"] == b["cls"]) for b in incidence] for a in incidence])
    ev = sorted({c["event"] for c in incidence})
    X1 = np.array([[float(c["event"] == e) for e in ev] for c in incidence])
    X2 = np.column_stack([X1, [math.log1p(c["surv"]) for c in incidence],
                          [math.log(c["base"]) for c in incidence]])
    ranks = {}
    for name, X in (("event_only", X1), ("event_plus_covariates", X2)):
        P = np.eye(nc) - X @ np.linalg.pinv(X)
        basis = np.array([(P @ M @ P).ravel() for M in (G, C, np.eye(nc))])
        sv = np.linalg.svd(basis, compute_uv=False)
        ranks[name] = dict(rank=int(np.linalg.matrix_rank(basis)),
                           singular_values=[float(f"{x:.4g}") for x in sv])
    summary["covariance_basis"] = ranks
    summary["cells_at_risk"] = nc

    cj = [["event", "pre_post", "class", "occurrences", "joined", "join_share"]]
    for (event, pp, cl), (tot, j) in sorted(class_join.items()):
        if tot >= 100:
            cj.append([event, pp, cl, tot, j, f"{j / tot:.3f}"])
    refs = collections.Counter(c_rec["ref"] for cell in cells.values() for c_rec, _ in cell.values())
    summary["eco_ref_top"] = refs.most_common(8)

    for name, rows in (("support_join_by_stage.tsv", join_rows),
                       ("support_join_by_class.tsv", cj),
                       ("support_guild_stage.tsv", guild_stage),
                       ("support_at_risk.tsv", at_risk)):
        with (HERE / name).open("w", newline="") as fh:
            csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(rows)
    (HERE / "support_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "events"}, indent=1))


if __name__ == "__main__":
    main()
