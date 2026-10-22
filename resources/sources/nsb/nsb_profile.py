"""Profile NSB snapshots mirrored by zenodo_mirror.py.

Usage: python3 nsb_profile.py MIRROR_ROOT OUT_DIR RECIPE_SQL VERSION_DIR [VERSION_DIR ...]

MIRROR_ROOT holds raw/<version_dir>/ zips. Each SQLite database is extracted to
MIRROR_ROOT/derived/<version_dir>/nsb.sqlite if absent. Writes long-format TSVs to
OUT_DIR: version_counts.tsv (every version), latest_detail.tsv (coverage, the
filtered-file reconstruction and the recipe check for the last version) and
drift.tsv (consecutive versions). Standard library only.
"""

import csv
import io
import os
import sqlite3
import sys
import zipfile
from collections import Counter

# GTS2012 boundaries (Ma), the scale NSB reports ages on.
EPOCHS = [(0, 2.588, "Pleistocene-Holocene"), (2.588, 5.333, "Pliocene"), (5.333, 23.03, "Miocene"),
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


def one(con, q):
    try:
        return con.execute(q).fetchone()[0]
    except sqlite3.OperationalError:
        return "NA"


def rows_or_none(con, q):
    try:
        return con.execute(q).fetchall()
    except sqlite3.OperationalError:
        return []


def version_counts(con, vdir, out):
    add = lambda metric, key, value: out.append((vdir, metric, key, value))
    for t in tables(con):
        add("table_rows", t, one(con, f'select count(*) from "{t}"'))
        add("table_columns", t, ",".join(columns(con, t)))
    occ = "neptune_sample_taxa st join neptune_sample s using (sample_id)"
    for g, n in rows_or_none(con, f"select s.fossil_group, count(*) from {occ} group by 1"):
        add("occurrences_by_group", g, n)
    for g, n in rows_or_none(con, "select fossil_group, count(*) from neptune_sample group by 1"):
        add("samples_by_group", g, n)
    add("samples_without_age", "", one(con, "select count(*) from neptune_sample where sample_age_ma is null"))
    add("occurrences_without_age", "", one(con, f"select count(*) from {occ} where s.sample_age_ma is null"))
    add("samples_without_occurrences", "", one(con, "select count(*) from neptune_sample where sample_id not in (select sample_id from neptune_sample_taxa)"))
    add("holes_with_samples", "", one(con, "select count(distinct hole_id) from neptune_sample"))
    for st, n in rows_or_none(con, "select taxon_status, count(*) from neptune_taxonomy group by 1"):
        add("taxa_by_status", st, n)
    add("age_model_revisions", "", one(con, "select count(*) from neptune_age_model_history"))
    add("current_age_models", "", one(con, "select count(*) from neptune_age_model_history where current_flag = 'Y'"))
    add("age_quality_distinct_values", "all revisions", one(con, "select count(distinct age_quality) from neptune_age_model_history"))
    add("age_quality_distinct_values", "current", one(con, "select count(distinct age_quality) from neptune_age_model_history where current_flag = 'Y'"))
    cited = "dataset_id in (select dataset_id from neptune_sod_off where trim(coalesce(source_citation, '')) <> '')"
    add("samples_with_dataset_id", "", one(con, "select count(*) from neptune_sample where dataset_id is not null"))
    add("samples_with_source_citation", "", one(con, f"select count(*) from neptune_sample where {cited}"))
    add("occurrences_with_dataset_id", "", one(con, f"select count(*) from {occ} where s.dataset_id is not null"))
    add("occurrences_with_source_citation", "", one(con, f"select count(*) from {occ} where s.{cited}"))
    q = f"""select count(*) from {occ} join neptune_hole_summary hs using (hole_id) where hs.latitude < """
    add("occurrences_south_of", "50S", one(con, q + "-50"))
    add("occurrences_south_of", "60S", one(con, q + "-60"))
    add("occurrences_sample_group_ne_taxon_group", "", one(con, f"""select count(*) from {occ}
        join neptune_taxonomy t on t.taxon_id = st.taxon_id where t.fossil_group <> s.fossil_group"""))


def detail(con, vdir, out):
    holes = {r[0]: r[1:] for r in con.execute("select hole_id, leg, ocean_code, latitude from neptune_hole_summary")}
    by_epoch, by_ocean, by_prog, by_lat, by_qual, by_status = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    q = """select s.fossil_group, s.sample_age_ma, s.hole_id, t.taxon_status,
                  coalesce(t.genus_qualifier, ''), coalesce(t.species_qualifier, '')
           from neptune_sample_taxa st join neptune_sample s using (sample_id)
           left join neptune_taxonomy t on t.taxon_id = st.taxon_id"""
    for g, age, hole, status, gq, sq in con.execute(q):
        by_epoch[(g, epoch(age))] += 1
        leg, ocean, lat = holes.get(hole, (None, None, None))
        by_ocean[(g, ocean or "unknown")] += 1
        by_prog[(g, programme(leg))] += 1
        band = "unknown" if lat is None else f"{int(min(abs(float(lat)), 89.999) // 30) * 30}-{int(min(abs(float(lat)), 89.999) // 30) * 30 + 30} abs lat"
        by_lat[(g, band)] += 1
        by_qual[(g, "open nomenclature" if (gq or sq) else "plain")] += 1
        by_status[(g, status or "taxon not found")] += 1
    for name, c in [("occ_by_group_epoch", by_epoch), ("occ_by_group_ocean", by_ocean), ("occ_by_group_programme", by_prog),
                    ("occ_by_group_abs_latitude", by_lat), ("occ_by_group_nomenclature", by_qual), ("occ_by_group_taxon_status", by_status)]:
        for (g, k), n in sorted(c.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
            out.append((vdir, name, f"{g}|{k}", n))
    for aq, n in con.execute("select age_quality, count(*) from neptune_age_model_history where current_flag = 'Y' group by 1"):
        out.append((vdir, "current_age_models_by_quality", aq, n))
    q = """select h.age_quality, count(*) from neptune_sample s join neptune_hole_summary hs using (hole_id)
           left join neptune_age_model_history h on h.site_hole = hs.site_hole and h.current_flag = 'Y'
           where s.sample_age_ma is not null group by 1"""
    for aq, n in con.execute(q):
        out.append((vdir, "dated_samples_by_current_age_quality", aq, n))
    out.append((vdir, "holes_with_any_age_model", "", one(con, "select count(distinct site_hole) from neptune_age_model_history")))
    out.append((vdir, "holes_with_samples_and_current_age_model", "", one(con, """select count(distinct s.hole_id)
        from neptune_sample s join neptune_hole_summary hs using (hole_id)
        where hs.site_hole in (select site_hole from neptune_age_model_history where current_flag = 'Y')""")))
    out.append((vdir, "datasets", "", one(con, "select count(*) from neptune_sod_off")))
    out.append((vdir, "distinct_source_citations", "", one(con, "select count(distinct source_citation) from neptune_sod_off")))
    for code, n in con.execute("select sample_status, count(*) from neptune_sample group by 1"):
        out.append((vdir, "samples_by_status", code, n))
    for code, n in con.execute("select taxon_qualifier, count(*) from neptune_sample_taxa group by 1"):
        out.append((vdir, "occurrences_by_taxon_qualifier", code, n))


def read_occ_csv(z, name):
    with z.open(next(n for n in z.namelist() if os.path.basename(n) == name)) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", newline=""), delimiter="\t")


def default_filter_reasons(status, taxon_qualifier, sample_status, age):
    # Status, qualifier and sample-status rules as in NSBcompanion >= 2.2 getNeptuneData defaults;
    # the age rule is the portal's (Renaudie et al. 2020, p. 9).
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


def filter_and_recipe(con, root, vdir, recipe, out):
    with zipfile.ZipFile(os.path.join(root, "raw", vdir, "denormalized_tables.zip")) as z:
        csv_resolved = {}
        for r in read_occ_csv(z, "occurrences.csv"):
            csv_resolved[(int(r["sample_id"]), int(r["taxon_id"]))] = int(r["resolved_taxon_id"]) if r["resolved_taxon_id"] else None
        kept = Counter((int(r["sample_id"]), int(r["taxon_id"])) for r in read_occ_csv(z, "filtered_occurrences.csv"))
    out.append((vdir, "denorm_full_rows", "", len(csv_resolved)))
    out.append((vdir, "denorm_filtered_rows", "", sum(kept.values())))
    q = """select st.sample_id, st.taxon_id, s.fossil_group, t.taxon_status, st.taxon_qualifier, s.sample_status, s.sample_age_ma
           from neptune_sample_taxa st join neptune_sample s using (sample_id)
           left join neptune_taxonomy t on t.taxon_id = st.taxon_id"""
    agree, disagree, dated_filtered = Counter(), Counter(), set()
    for sid, tid, g, status, tqual, sstat, age in con.execute(q):
        reasons = default_filter_reasons(status, tqual, sstat, age)
        key = (sid, tid)
        in_csv = kept[key] > 0
        if in_csv:
            kept[key] -= 1
            if age is not None:
                dated_filtered.add(key)
        predicted = not reasons
        if predicted == in_csv:
            agree[(g, "kept" if predicted else "removed")] += 1
        else:
            disagree[(g, ("in csv, predicted removed: " if in_csv else "not in csv, predicted kept: ") + (";".join(reasons) or f"status {status}"))] += 1
    for (g, k), n in sorted(agree.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        out.append((vdir, "default_filter_agrees", f"{g}|{k}", n))
    for (g, k), n in sorted(disagree.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        out.append((vdir, "default_filter_disagrees", f"{g}|{k}", n))
    out.append((vdir, "filtered_csv_rows_not_in_db", "", sum(v for v in kept.values() if v > 0)))
    rows = con.execute(open(recipe).read()).fetchall()
    keys = {(r[0], r[2]) for r in rows}
    out.append((vdir, "recipe_rows", "", len(rows)))
    out.append((vdir, "recipe_keys_equal_dated_filtered_csv_keys", "", int(keys == dated_filtered)))
    out.append((vdir, "recipe_keys_not_in_dated_filtered_csv", "", len(keys - dated_filtered)))
    out.append((vdir, "dated_filtered_csv_keys_not_in_recipe", "", len(dated_filtered - keys)))
    out.append((vdir, "recipe_resolved_id_disagrees_with_csv", "", sum(csv_resolved.get((r[0], r[2])) != r[5] for r in rows)))
    out.append((vdir, "recipe_samples", "", len({r[0] for r in rows})))
    out.append((vdir, "recipe_holes", "", len({r[13] for r in rows})))
    out.append((vdir, "recipe_resolved_taxa", "", len({r[5] for r in rows})))
    out.append((vdir, "recipe_duplicate_sample_resolved_taxon_rows", "", len(rows) - len({(r[0], r[5]) for r in rows})))
    out.append((vdir, "recipe_renamed_by_resolution", "", sum(r[2] != r[5] for r in rows)))
    for st, n in Counter(r[9] for r in rows).items():
        out.append((vdir, "recipe_rows_by_resolved_status", st, n))


def sample_state(con):
    q = """select s.sample_id, s.sample_age_ma, s.sample_depth_mbsf, cur.revision_no
           from neptune_sample s join neptune_hole_summary hs using (hole_id)
           left join (select site_hole, max(revision_no) as revision_no from neptune_age_model_history
                      where current_flag = 'Y' group by site_hole) cur on cur.site_hole = hs.site_hole"""
    return {r[0]: r[1:] for r in con.execute(q)}


def drift(con_a, va, con_b, vb, out):
    pair = f"{va}->{vb}"
    add = lambda metric, key, value: out.append((pair, metric, key, value))
    occ = lambda c: Counter(c.execute("select sample_id, taxon_id from neptune_sample_taxa"))
    oa, ob = occ(con_a), occ(con_b)
    add("occ_added", "", sum((ob - oa).values()))
    add("occ_removed", "", sum((oa - ob).values()))
    sa, sb = sample_state(con_a), sample_state(con_b)
    shared = sa.keys() & sb.keys()
    add("samples_shared", "", len(shared))
    add("samples_added", "", len(sb.keys() - sa.keys()))
    add("samples_removed", "", len(sa.keys() - sb.keys()))
    dated = [s for s in shared if sa[s][0] is not None and sb[s][0] is not None]
    add("shared_samples_dated_in_both", "", len(dated))
    add("shared_sample_age_gained", "", sum(sa[s][0] is None and sb[s][0] is not None for s in shared))
    add("shared_sample_age_lost", "", sum(sa[s][0] is not None and sb[s][0] is None for s in shared))
    add("shared_sample_depth_changed_gt_0.005m", "", sum(sa[s][1] is not None and sb[s][1] is not None
                                                         and abs(float(sa[s][1]) - float(sb[s][1])) > 0.005 for s in shared))
    for model in ("revised", "unchanged"):
        subset = [s for s in dated if (sa[s][2] != sb[s][2]) == (model == "revised")]
        add("dated_in_both_by_model", model, len(subset))
        for thr in (0.01, 0.1, 0.5, 1.0, 5.0):
            add(f"age_change_gt_{thr}_myr", f"model {model}", sum(abs(float(sb[s][0]) - float(sa[s][0])) > thr for s in subset))


def write(path, rows, header):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main():
    root, out_dir, recipe, vdirs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    os.makedirs(out_dir, exist_ok=True)
    counts, det, dr = [], [], []
    prev = None
    for v in vdirs:
        con = open_db(root, v)
        version_counts(con, v, counts)
        if prev:
            drift(prev[1], prev[0], con, v, dr)
        print("profiled", v, flush=True)
        prev = (v, con)
    detail(prev[1], prev[0], det)
    filter_and_recipe(prev[1], root, prev[0], recipe, det)
    write(os.path.join(out_dir, "version_counts.tsv"), counts, ["version", "metric", "key", "value"])
    write(os.path.join(out_dir, "latest_detail.tsv"), det, ["version", "metric", "key", "value"])
    write(os.path.join(out_dir, "drift.tsv"), dr, ["pair", "metric", "key", "value"])


if __name__ == "__main__":
    main()
