# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml==6.0.3", "pyarrow==22.0.0"]
# ///
"""Profile an AusTraits release (austraits-X.zip and the flattened parquet from Zenodo).

Usage: uv run austraits_profile.py AUSTRAITS_ZIP FLATTENED_PARQUET OUT_TSV

Counts rows, traits, datasets and taxa; the dictionary's trait types (numeric
or categorical) crossed with value_type and entity_type; basis_of_record by
token and by combination; the fire-response traits (every trait named with
"fire" or "resprout", plus the core list) and a few vegetation traits, each
with records, taxa, datasets and value types; resprouting_capacity at record
level, by taxon rank, with taxa that carry conflicting values and the
datasets behind them; taxa by rank, status, APC alignment and establishment;
the release metadata (version, licence, taxonomy source) and BibTeX entries; and encoding: invalid UTF-8 lines in each CSV, the rows, datasets, columns
and bytes involved in traits.csv, and whether the flattened parquet
holds the same bytes. Writes long-format
(table, metric, key, value).
"""

import csv
import io
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict

import pyarrow as pa
import pyarrow.parquet as pq
import yaml

csv.field_size_limit(1 << 30)
SURROGATE = re.compile("[\udc80-\udcff]")
FIRE_CORE = ["resprouting_capacity", "post_fire_recruitment", "serotiny", "bud_bank_location", "seedbank_longevity_class",
             "bark_thickness"]
OTHER = ["plant_growth_form", "plant_height", "wood_density", "leaf_mass_per_area", "seed_dry_mass", "photosynthetic_pathway"]
FIRE_NAME = re.compile(r"fire|resprout")
RESPROUT = "resprouting_capacity"
out = []


def add(*row):
    out.append(row)


def pct(n, d):
    return f"{100 * n / d:.1f}"


def tokens(value):
    return tuple(sorted(value.split()))


def bad_lines(raw):
    n = 0
    for line in raw.split(b"\n"):
        try:
            line.decode("utf-8")
        except UnicodeDecodeError:
            n += 1
    return n


def valid_utf8(b):
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


z = zipfile.ZipFile(sys.argv[1])
names = z.namelist()
for n in sorted(names):
    add("zip", "member_bytes", n, z.getinfo(n).file_size)


def member(stem):
    return next(n for n in names if n.endswith("/" + stem) or n == stem)


defs = yaml.load(z.read(member("definitions.yml")), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
ttype = {k: v["type"] for k, v in defs.items()}
add("definitions", "traits_defined", "", len(defs))
for t, n in Counter(ttype.values()).most_common():
    add("definitions", "by:type", t, n)
resprout_vocab = set(defs[RESPROUT]["allowed_values_levels"])
add("definitions", "allowed_values", RESPROUT, " | ".join(sorted(resprout_vocab)))

meta = yaml.load(z.read(member("metadata.yml")), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
for k in ("version", "doi", "publication_date"):
    add("metadata", k, "", meta[k])
add("metadata", "license_rights", "", meta["license"]["rights"])
for r in meta["related_identifiers"]:
    if "APCalign" in r["identifier"] or "traits.build" in r["identifier"]:
        add("metadata", "related_identifier", r["relation_type"], r["identifier"])
apc_licence = re.compile(r"(?i)cc[- ]by[- ]3\.0|licenses/by/3\.0")
for m in ("metadata.yml", "schema.yml", "definitions.yml", "build_info.md"):
    add("metadata", "mentions_of_cc_by_3_0", m, len(apc_licence.findall(z.read(member(m)).decode("utf-8", errors="replace"))))
add("tables", "bibtex_entries", "sources.bib", len(re.findall(r"^@", z.read(member("sources.bib")).decode("utf-8", errors="replace"), re.M)))

raw = z.read(member("traits.csv"))
add("encoding", "lines_with_invalid_utf8", "traits.csv", bad_lines(raw))
reader = csv.reader(io.StringIO(raw.decode("utf-8", errors="surrogateescape")))
del raw
header = next(reader)
col = {c: i for i, c in enumerate(header)}
add("traits", "columns", "", " | ".join(header))

nrows = 0
wrong_width = 0
traits_seen, datasets_seen, taxa_seen = set(), set(), set()
value_type = Counter()
by_type = defaultdict(Counter)
entity_by_type = defaultdict(Counter)
basis_tokens, basis_combos, basis_ntok = Counter(), Counter(), Counter()
selected = {t for t in defs if FIRE_NAME.search(t)} | set(FIRE_CORE) | set(OTHER)
sel = {t: {"records": 0, "taxa": set(), "datasets": set(), "vt": Counter()} for t in selected}
resprouting = []
bad_rows, rows_by_dataset = Counter(), Counter()
bad_bytes, bad_cols, bad_also_valid = Counter(), Counter(), Counter()
nonascii_rows_valid = Counter()
nonascii_cells = []
for row in reader:
    if len(row) != len(header):
        wrong_width += 1
        continue
    nrows += 1
    ds, taxon, trait = row[col["dataset_id"]], row[col["taxon_name"]], row[col["trait_name"]]
    vt, et, basis = row[col["value_type"]], row[col["entity_type"]], row[col["basis_of_record"]]
    traits_seen.add(trait)
    datasets_seen.add(ds)
    taxa_seen.add(taxon)
    rows_by_dataset[ds] += 1
    tt = ttype.get(trait, "undefined")
    value_type[vt] += 1
    by_type[tt][vt] += 1
    entity_by_type[tt][et] += 1
    tok = tokens(basis)
    basis_ntok[len(tok)] += 1
    basis_combos[" ".join(tok)] += 1
    for x in tok:
        basis_tokens[x] += 1
    if trait in sel:
        s = sel[trait]
        s["records"] += 1
        s["taxa"].add(taxon)
        s["datasets"].add(ds)
        s["vt"][vt] += 1
    if trait == RESPROUT:
        resprouting.append((taxon, ds, tokens(row[col["value"]]), et, vt))
    joined = "\x1f".join(row)
    if not joined.isascii():
        has_bad = SURROGATE.search(joined) is not None
        valid_nonascii = any(not c.isascii() and not SURROGATE.match(c) for c in joined)
        if has_bad:
            bad_rows[ds] += 1
            if valid_nonascii:
                bad_also_valid[ds] += 1
        else:
            nonascii_rows_valid[ds] += 1
        for i, cell in enumerate(row):
            if cell.isascii():
                continue
            if SURROGATE.search(cell):
                bad_cols[(ds, header[i])] += 1
                for c in SURROGATE.findall(cell):
                    bad_bytes[(ds, f"0x{ord(c) - 0xDC00:02x}")] += 1
            nonascii_cells.append((ds, header[i], cell))
del reader

add("traits", "rows", "", nrows)
add("traits", "rows_with_wrong_field_count", "", wrong_width)
add("traits", "distinct_traits", "", len(traits_seen))
add("traits", "distinct_datasets", "", len(datasets_seen))
add("traits", "distinct_taxa", "", len(taxa_seen))
add("definitions", "traits_defined_and_present", "", len(set(defs) & traits_seen))
add("definitions", "traits_present_not_defined", "", len(traits_seen - set(defs)))
for t in sorted(set(defs) - traits_seen):
    add("definitions", "defined_not_in_data", t, ttype[t])
for v, n in value_type.most_common():
    add("traits", "by:value_type", v, n)
    add("traits", "pct_of_rows:value_type", v, pct(n, nrows))

rows_of = {tt: sum(c.values()) for tt, c in by_type.items()}
for tt in sorted(rows_of):
    add("traits", "pct_of_rows:trait_type", tt, pct(rows_of[tt], nrows))
for tt in sorted(by_type):
    add("value_type_by_trait_type", f"rows:{tt}", "all", rows_of[tt])
    for v, n in by_type[tt].most_common():
        add("value_type_by_trait_type", f"rows:{tt}", v, n)
        add("value_type_by_trait_type", f"pct_of_{tt}_rows", v, pct(n, rows_of[tt]))
num = by_type["numeric"]
add("value_type_by_trait_type", "pct_of_numeric_rows", "minimum_or_maximum", pct(num["minimum"] + num["maximum"], rows_of["numeric"]))
mode_total = value_type["mode"]
for tt in sorted(by_type):
    add("value_type_by_trait_type", "mode_rows_by_trait_type", tt, by_type[tt]["mode"])
    add("value_type_by_trait_type", "pct_of_mode_rows", tt, pct(by_type[tt]["mode"], mode_total))
for tt in sorted(entity_by_type):
    for v, n in entity_by_type[tt].most_common():
        add("entity_type_by_trait_type", f"rows:{tt}", v, n)
        add("entity_type_by_trait_type", f"pct_of_{tt}_rows", v, pct(n, rows_of[tt]))

for v, n in basis_tokens.most_common():
    add("basis_of_record", "rows_with_token", v, n)
    add("basis_of_record", "pct_of_rows_with_token", v, pct(n, nrows))
for v, n in sorted(basis_ntok.items()):
    add("basis_of_record", "rows_by_token_count", str(v), n)
add("basis_of_record", "rows_with_2_or_3_tokens", "", basis_ntok[2] + basis_ntok[3])
add("basis_of_record", "pct_of_rows_with_2_or_3_tokens", "", pct(basis_ntok[2] + basis_ntok[3], nrows))
for v, n in basis_combos.most_common():
    add("basis_of_record", "rows_by_combination", v, n)
    add("basis_of_record", "pct_of_rows_by_combination", v, pct(n, nrows))

for t in FIRE_CORE + sorted(t for t in sel if FIRE_NAME.search(t) and t not in FIRE_CORE) + OTHER:
    s = sel[t]
    add("selected_traits", "label", t, defs[t]["label"] if t in defs else "")
    add("selected_traits", "type", t, ttype.get(t, "undefined"))
    add("selected_traits", "records", t, s["records"])
    add("selected_traits", "taxa", t, len(s["taxa"]))
    add("selected_traits", "datasets", t, len(s["datasets"]))
    add("selected_traits", "value_types", t, "; ".join(f"{v} {n}" for v, n in s["vt"].most_common()))
    if s["records"] and ttype.get(t) == "numeric":
        add("selected_traits", "pct_minimum_or_maximum", t, pct(s["vt"]["minimum"] + s["vt"]["maximum"], s["records"]))

taxa_rows = []
for k in ("taxa.csv", "locations.csv", "contexts.csv", "methods.csv", "contributors.csv", "excluded_data.csv", "taxonomic_updates.csv"):
    try:
        data = z.read(member(k))
    except StopIteration:
        continue
    add("encoding", "lines_with_invalid_utf8", k, bad_lines(data))
    rows = list(csv.DictReader(io.StringIO(data.decode("utf-8", errors="replace"))))
    add("tables", "rows", k, len(rows))
    if k == "taxa.csv":
        taxa_rows = rows
for col_name in ("taxon_rank", "taxonomic_status", "taxonomic_dataset", "establishment_means"):
    for v, n in Counter(r[col_name] for r in taxa_rows).most_common():
        add("taxa", f"by:{col_name}", v, n)
rank = {r["taxon_name"]: r["taxon_rank"] for r in taxa_rows}
add("taxa", "not_species", "", sum(r["taxon_rank"] != "species" for r in taxa_rows))

add("resprouting", "records", "", len(resprouting))
for (et, vt), n in Counter((et, vt) for _, _, _, et, vt in resprouting).most_common():
    add("resprouting", "records_by_entity_type_value_type", f"{et} {vt}", n)
add("resprouting", "records_single_valued", "", sum(len(v) == 1 for _, _, v, _, _ in resprouting))
add("resprouting", "records_multi_valued", "", sum(len(v) > 1 for _, _, v, _, _ in resprouting))
for v, n in Counter(" ".join(v) for _, _, v, _, _ in resprouting).most_common():
    add("resprouting", "records_by_value", v, n)
tok_counts = Counter(x for _, _, v, _, _ in resprouting for x in v)
for v, n in tok_counts.most_common():
    add("resprouting", "token_count", v, n)
add("resprouting", "token_count_total", "", sum(tok_counts.values()))
add("resprouting", "tokens_outside_dictionary", "", sum(n for v, n in tok_counts.items() if v not in resprout_vocab))

per_taxon = defaultdict(list)
for taxon, ds, v, _, _ in resprouting:
    per_taxon[taxon].append((ds, v))
add("resprouting", "taxa", "", len(per_taxon))
for r, n in Counter(rank.get(t, "not in taxa.csv") or "blank" for t in per_taxon).most_common():
    add("resprouting", "taxa_by_rank", r, n)
add("resprouting", "taxa_not_species", "", sum(rank.get(t) != "species" for t in per_taxon))


def profile(taxa, label):
    c = Counter()
    for t in taxa:
        recs = per_taxon[t]
        dsets = {d for d, _ in recs}
        values = {v for _, v in recs}
        toks = {x for v in values for x in v}
        singles = {v[0] for v in values if len(v) == 1}
        c["taxa"] += 1
        c["datasets_1"] += len(dsets) == 1
        c["datasets_2plus"] += len(dsets) >= 2
        c["one_distinct_value"] += len(values) == 1
        c["two_plus_distinct_values"] += len(values) >= 2
        c["any_mixed_code_record"] += any(len(v) > 1 for v in values)
        c["two_plus_distinct_tokens"] += len(toks) >= 2
        c["tokens_resprouts_and_fire_killed"] += {"resprouts", "fire_killed"} <= toks
        hard = {"resprouts", "fire_killed"} <= singles
        c["both_tokens_without_separate_single_records"] += {"resprouts", "fire_killed"} <= toks and not hard
        c["one_distinct_value_but_multi_valued"] += len(values) == 1 and len(toks) >= 2
        c["records_resprouts_vs_fire_killed"] += hard
        if hard:
            within = any({"resprouts", "fire_killed"} <= {v[0] for d2, v in recs if d2 == d and len(v) == 1} for d in dsets)
            c["hard_conflict_within_a_dataset"] += within
            c["hard_conflict_between_datasets_only"] += not within
        modal = {}
        for d in dsets:
            cnt = Counter(v for d2, v in recs if d2 == d).most_common()
            modal[d] = cnt[0][0] if len(cnt) == 1 or cnt[0][1] > cnt[1][1] else None
        votes = Counter(v for v in modal.values() if v is not None)
        if len(values) == 1:
            c["vote:all_records_agree"] += 1
        elif votes and len(votes) == 1 and None not in modal.values():
            c["vote:datasets_agree_on_modal_value"] += 1
        elif votes and votes.most_common(1)[0][1] > len(dsets) / 2:
            c["vote:strict_majority_of_datasets"] += 1
        else:
            c["vote:no_majority"] += 1
    for k, n in c.items():
        add("resprouting", f"{label}:{k}", "", n)
        if k != "taxa":
            add("resprouting", f"{label}:pct_of_taxa:{k}", "", pct(n, c["taxa"]))


profile(list(per_taxon), "all_ranks")
profile([t for t in per_taxon if rank.get(t) == "species"], "species")

bad_ds = sorted(bad_rows)
for ds in bad_ds:
    add("encoding", "rows_with_invalid_utf8", ds, bad_rows[ds])
    add("encoding", "dataset_rows", ds, rows_by_dataset[ds])
    add("encoding", "invalid_rows_also_holding_valid_nonascii_utf8", ds, bad_also_valid[ds])
add("encoding", "rows_with_invalid_utf8", "all datasets", sum(bad_rows.values()))
add("encoding", "datasets_with_invalid_utf8", "", len(bad_ds))
add("encoding", "rows_with_valid_nonascii_utf8_only", "all datasets", sum(nonascii_rows_valid.values()))
for ds in bad_ds:
    add("encoding", "valid_nonascii_utf8_rows", ds, nonascii_rows_valid[ds])
for (ds, b), n in sorted(bad_bytes.items()):
    try:
        ch = bytes([int(b, 16)]).decode("cp1252")
        label = f"{ch!r} {unicodedata.name(ch)}"
    except UnicodeDecodeError:
        label = "undefined in cp1252"
    add("encoding", "invalid_byte_occurrences", f"{ds} {b}", f"{n} -> cp1252 {label}")
for (ds, c), n in sorted(bad_cols.items()):
    add("encoding", "cells_with_invalid_utf8", f"{ds} {c}", n)
for ds in bad_ds:
    for c, n in Counter(cc for d, cc, x in nonascii_cells if d == ds and not SURROGATE.search(x)).most_common():
        add("encoding", "cells_with_valid_nonascii_utf8", f"{ds} {c}", n)
    contexts = Counter()
    for d, cc, x in nonascii_cells:
        if d == ds and SURROGATE.search(x):
            raw_cell = x.encode("utf-8", "surrogateescape")
            k = next(j for j, v in enumerate(raw_cell) if v >= 0x80)
            contexts[raw_cell[max(0, k - 10) : k + 8].decode("cp1252")] += 1
    for ctx, n in contexts.most_common(3):
        add("encoding", "example_cp1252_context", ds, f"{n} cells: {ctx}")

if bad_cols:
    wanted = {c for _, c in bad_cols}
    pf = pq.read_table(sys.argv[2], columns=["dataset_id"] + sorted(wanted))
    add("encoding", "parquet_rows", "", pf.num_rows)
    p_ds = pf.column("dataset_id").to_pylist()
    for ds, c in sorted(bad_cols):
        try:
            pf.column(c).to_pylist()
            raises = "no"
        except UnicodeDecodeError as e:
            raises = f"UnicodeDecodeError: {e.reason}"
        add("encoding", "parquet_to_pylist_raises", c, raises)
        p_cells = Counter(x for d, x in zip(p_ds, pf.column(c).cast(pa.binary()).to_pylist()) if d == ds and x and not x.isascii())
        csv_cells = Counter(x.encode("utf-8", "surrogateescape") for d, cc, x in nonascii_cells if d == ds and cc == c)
        add("encoding", "parquet_nonascii_cells", f"{ds} {c}", sum(p_cells.values()))
        add("encoding", "csv_nonascii_cells", f"{ds} {c}", sum(csv_cells.values()))
        add("encoding", "parquet_cells_invalid_utf8", f"{ds} {c}", sum(n for x, n in p_cells.items() if not valid_utf8(x)))
        add("encoding", "parquet_bytes_equal_traits_csv_bytes", f"{ds} {c}", p_cells == csv_cells)

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
