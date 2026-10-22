"""Profile NSB snapshots mirrored by zenodo_mirror.py.

Usage: python3 profile.py MIRROR_ROOT OUT_DIR VERSION_DIR [VERSION_DIR ...]

MIRROR_ROOT holds raw/<version_dir>/ zips. The SQLite database is extracted to
MIRROR_ROOT/derived/<version_dir>/nsb.sqlite if absent. Writes long-format TSVs to
OUT_DIR: per-version counts, detailed coverage for the last version given, the
full-versus-filtered occurrence comparison for that version, and drift between
consecutive versions. Standard library only.
"""

import csv
import io
import os
import sqlite3
import sys
import zipfile
from collections import Counter

EPOCHS = [(0, 2.58, "Pleistocene-Holocene"), (2.58, 5.333, "Pliocene"), (5.333, 23.03, "Miocene"),
          (23.03, 33.9, "Oligocene"), (33.9, 56.0, "Eocene"), (56.0, 66.0, "Paleocene"),
          (66.0, 100.5, "Late Cretaceous"), (100.5, 145.0, "Early Cretaceous"), (145.0, 1e9, "pre-Cretaceous")]


def epoch(age):
    if age is None or age == "":
        return "no age"
    a = float(age)
    if a < 0:
        return "negative age"
    return next(name for lo, hi, name in EPOCHS if lo <= a < hi)


def programme(leg):
    if leg is None:
        return "unknown"
    leg = int(leg)
    return "DSDP" if leg < 100 else "ODP" if leg < 300 else "IODP"


def open_db(root, vdir):
    path = os.path.join(root, "derived", vdir, "nsb.sqlite")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with zipfile.ZipFile(os.path.join(root, "raw", vdir, "nsb_sqlite.zip")) as z:
            member = next(n for n in z.namelist() if n.endswith(".sqlite"))
            with z.open(member) as src, open(path + ".part", "wb") as dst:
                while chunk := src.read(1 << 20):
                    dst.write(chunk)
        os.replace(path + ".part", path)
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def columns(con, table):
    return [r[1] for r in con.execute(f'pragma table_info("{table}")')]


def tables(con):
    return [r[0] for r in con.execute("select name from sqlite_master where type='table' order by name")]


def version_counts(con, vdir, out):
    for t in tables(con):
        out.append((vdir, "table_rows", t, con.execute(f'select count(*) from "{t}"').fetchone()[0]))
        out.append((vdir, "table_columns", t, ",".join(columns(con, t))))
    q = """select s.fossil_group, count(*) from neptune_sample_taxa st
           join neptune_sample s using (sample_id) group by 1"""
    for g, n in con.execute(q):
        out.append((vdir, "occurrences_by_group", g, n))
    for g, n in con.execute("select fossil_group, count(*) from neptune_sample group by 1"):
        out.append((vdir, "samples_by_group", g, n))
    out.append((vdir, "samples_without_age", "", con.execute("select count(*) from neptune_sample where sample_age_ma is null").fetchone()[0]))
    out.append((vdir, "holes_with_samples", "", con.execute("select count(distinct hole_id) from neptune_sample").fetchone()[0]))
    for st, n in con.execute("select taxon_status, count(*) from neptune_taxonomy group by 1"):
        out.append((vdir, "taxa_by_status", st, n))


def detail(con, vdir, out):
    holes = {r[0]: r[1:] for r in con.execute("select hole_id, leg, ocean_code, latitude from neptune_hole_summary")}
    by_epoch, by_ocean, by_prog, by_lat, by_qual, by_status = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    q = """select s.fossil_group, s.sample_age_ma, s.hole_id, t.taxon_status,
                  coalesce(t.genus_qualifier, ''), coalesce(t.species_qualifier, ''), st.taxon_qualifier
           from neptune_sample_taxa st join neptune_sample s using (sample_id)
           left join neptune_taxonomy t on t.taxon_id = st.taxon_id"""
    for g, age, hole, status, gq, sq, tq in con.execute(q):
        by_epoch[(g, epoch(age))] += 1
        leg, ocean, lat = holes.get(hole, (None, None, None))
        by_ocean[(g, ocean or "unknown")] += 1
        by_prog[(g, programme(leg))] += 1
        by_lat[(g, "unknown" if lat is None else f"{int(min(abs(float(lat)), 89.999) // 30) * 30}-{int(min(abs(float(lat)), 89.999) // 30) * 30 + 30} abs lat")] += 1
        by_qual[(g, "open nomenclature" if (gq or sq) else "plain")] += 1
        by_status[(g, status or "taxon not found")] += 1
    for name, c in [("occ_by_group_epoch", by_epoch), ("occ_by_group_ocean", by_ocean), ("occ_by_group_programme", by_prog),
                    ("occ_by_group_abs_latitude", by_lat), ("occ_by_group_nomenclature", by_qual), ("occ_by_group_taxon_status", by_status)]:
        for (g, k), n in sorted(c.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
            out.append((vdir, name, f"{g}|{k}", n))
    q = """select h.age_quality, count(*) from neptune_age_model_history h where h.current_flag = 'Y' group by 1"""
    for aq, n in con.execute(q):
        out.append((vdir, "current_age_models_by_quality", aq, n))
    out.append((vdir, "age_model_revisions", "", con.execute("select count(*) from neptune_age_model_history").fetchone()[0]))
    out.append((vdir, "holes_with_any_age_model", "", con.execute("select count(distinct site_hole) from neptune_age_model_history").fetchone()[0]))
    out.append((vdir, "current_age_models", "", con.execute("select count(*) from neptune_age_model_history where current_flag = 'Y'").fetchone()[0]))
    q = """select h.age_quality, count(*) from neptune_sample s join neptune_hole_summary hs using (hole_id)
           left join neptune_age_model_history h on h.site_hole = hs.site_hole and h.current_flag = 'Y'
           where s.sample_age_ma is not null group by 1"""
    for aq, n in con.execute(q):
        out.append((vdir, "dated_samples_by_current_age_quality", aq, n))
    sample_holes = con.execute("select count(distinct hole_id) from neptune_sample").fetchone()[0]
    with_model = con.execute("""select count(distinct s.hole_id) from neptune_sample s join neptune_hole_summary hs using (hole_id)
                                where hs.site_hole in (select site_hole from neptune_age_model_history where current_flag = 'Y')""").fetchone()[0]
    out.append((vdir, "holes_with_samples_and_current_age_model", "", with_model))
    out.append((vdir, "holes_with_samples", "", sample_holes))
    if "neptune_sod_off" in tables(con):
        out.append((vdir, "datasets", "", con.execute("select count(*) from neptune_sod_off").fetchone()[0]))
        out.append((vdir, "distinct_source_citations", "", con.execute("select count(distinct source_citation) from neptune_sod_off").fetchone()[0]))


def read_occ_csv(z, name):
    with z.open(next(n for n in z.namelist() if os.path.basename(n) == name)) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", newline=""), delimiter="\t")


def portal_default_reasons(status, taxon_qualifier, sample_status, age):
    # Portal defaults (Renaudie et al. 2020, Fig. 3) as implemented in NSBcompanion 2.1 getNeptuneData.
    r = []
    if status is None:
        r.append("taxon not in taxonomy")
    elif status == "G":
        r.append("status G")
    elif status in ("Q", "I", "U", "O", "H"):
        r.append(f"status {status}")
    if taxon_qualifier not in (None, ""):
        r.append("taxon_qualifier")
    if sample_status in ("c", "w"):
        r.append(f"sample_status {sample_status}")
    if age is None:
        r.append("no age")
    return r


def filter_comparison(con, root, vdir, out):
    with zipfile.ZipFile(os.path.join(root, "raw", vdir, "denormalized_tables.zip")) as z:
        full_csv = sum(1 for _ in read_occ_csv(z, "occurrences.csv"))
        kept = Counter((int(r["sample_id"]), int(r["taxon_id"])) for r in read_occ_csv(z, "filtered_occurrences.csv"))
    out.append((vdir, "denorm_full_rows", "", full_csv))
    out.append((vdir, "denorm_filtered_rows", "", sum(kept.values())))
    tq = "st.taxon_qualifier" if "taxon_qualifier" in columns(con, "neptune_sample_taxa") else "null"
    ss = "s.sample_status" if "sample_status" in columns(con, "neptune_sample") else "null"
    q = f"""select st.sample_id, st.taxon_id, s.fossil_group, t.taxon_status, {tq}, {ss}, s.sample_age_ma
            from neptune_sample_taxa st join neptune_sample s using (sample_id)
            left join neptune_taxonomy t on t.taxon_id = st.taxon_id"""
    agree, disagree = Counter(), Counter()
    for sid, tid, g, status, tqual, sstat, age in con.execute(q):
        reasons = portal_default_reasons(status, tqual, sstat, age)
        key = (sid, int(tid) if tid is not None else None)
        in_csv = kept[key] > 0
        if in_csv:
            kept[key] -= 1
        predicted = not reasons
        if predicted == in_csv:
            agree[(g, "kept" if predicted else "removed")] += 1
        else:
            disagree[(g, ("in csv, predicted removed: " if in_csv else "not in csv, predicted kept: ") + (";".join(reasons) or f"status {status}"))] += 1
    for (g, k), n in sorted(agree.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        out.append((vdir, "portal_filter_agrees", f"{g}|{k}", n))
    for (g, k), n in sorted(disagree.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        out.append((vdir, "portal_filter_disagrees", f"{g}|{k}", n))
    out.append((vdir, "filtered_csv_rows_not_in_db", "", sum(v for v in kept.values() if v > 0)))
    if ss != "null":
        for code, n in con.execute("select sample_status, count(*) from neptune_sample group by 1"):
            out.append((vdir, "samples_by_status", code, n))
    if tq != "null":
        for code, n in con.execute("select taxon_qualifier, count(*) from neptune_sample_taxa group by 1"):
            out.append((vdir, "occurrences_by_taxon_qualifier", code, n))


def drift(con_a, va, con_b, vb, out):
    occ = lambda c: Counter(c.execute("select sample_id, taxon_id from neptune_sample_taxa"))
    oa, ob = occ(con_a), occ(con_b)
    pair = f"{va}->{vb}"
    out.append((pair, "occ_added", "", sum((ob - oa).values())))
    out.append((pair, "occ_removed", "", sum((oa - ob).values())))
    ages = lambda c: dict(c.execute("select sample_id, sample_age_ma from neptune_sample"))
    aa, ab = ages(con_a), ages(con_b)
    shared = aa.keys() & ab.keys()
    out.append((pair, "samples_shared", "", len(shared)))
    out.append((pair, "samples_added", "", len(ab.keys() - aa.keys())))
    out.append((pair, "samples_removed", "", len(aa.keys() - ab.keys())))
    deltas = [abs(float(ab[s]) - float(aa[s])) for s in shared if aa[s] is not None and ab[s] is not None]
    for thr in (0.01, 0.1, 0.5, 1.0, 5.0):
        out.append((pair, "shared_sample_age_change_gt", f"{thr} Myr", sum(d > thr for d in deltas)))
    out.append((pair, "shared_sample_age_gained_or_lost", "", sum((aa[s] is None) != (ab[s] is None) for s in shared)))


def write(path, rows, header):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    root, out_dir, vdirs = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(out_dir, exist_ok=True)
    counts, det, filt, dr = [], [], [], []
    cons = [(v, open_db(root, v)) for v in vdirs]
    for v, con in cons:
        version_counts(con, v, counts)
        print("counted", v, flush=True)
    detail(cons[-1][1], vdirs[-1], det)
    filter_comparison(cons[-1][1], root, vdirs[-1], filt)
    for (va, ca), (vb, cb) in zip(cons, cons[1:]):
        drift(ca, va, cb, vb, dr)
        print("drift", va, vb, flush=True)
    write(os.path.join(out_dir, "version_counts.tsv"), counts, ["version", "metric", "key", "value"])
    write(os.path.join(out_dir, "latest_detail.tsv"), det + filt, ["version", "metric", "key", "value"])
    write(os.path.join(out_dir, "drift.tsv"), dr, ["pair", "metric", "key", "value"])


if __name__ == "__main__":
    main()
