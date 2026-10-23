# /// script
# requires-python = ">=3.10"
# dependencies = ["rdata==0.11.2"]
# ///
"""Profile the mirrored copies of Sepkoski's (2002) genus compendium.

Usage: uv run sepkoski_profile.py PETERS_RAW RPKG_GITHUB_RAW RPKG_CRAN_RAW BHL_RAW OUT_DIR OUT_TSV

PETERS_RAW holds Peters' online port as captured: the start page and one page
per phylum (26) and class (96). Each page's genus rows are checked against the
count in its heading and on the start page. The phylum pages list every genus
once (order, genus, first and last period and stage); class is recovered by
matching each class page's rows to phylum rows on all six fields, as a multiset.
OUT_DIR/sepkoski_genera.csv is the resulting table, bytes decoded as Latin-1
(the site declares ISO-8859-1).

The palaeoverse R package is compared with this capture: its 2022 scrape of
the same pages (inst/extdata), and sepkoski_raw, which joins class rows to
phylum rows (an inner join, so genera without a class page drop out) in both
the GitHub head and the CRAN release. R strings are read as raw bytes, because
some are stored with an ASCII flag but hold Latin-1 bytes.

BHL_RAW holds the Internet Archive copy of BHL's scan: the PDF and OCR text are
checked against the archive's MD5s, and a seeded sample of genus names is looked
up in the OCR text. Exit status 1 if a page count or checksum fails.
"""

import csv
import glob
import gzip
import hashlib
import json
import os
import random
import re
import sys
import tarfile
import tempfile
from collections import Counter, defaultdict

import rdata
from rdata.parser import RObjectType as T

peters, gh_raw, cran_raw, bhl_raw, out_dir, out_tsv = sys.argv[1:7]
out, failures = [], []


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def r_attr(obj, key):
    a = obj.attributes
    while a is not None and a.info.type == T.LIST:
        if a.tag is not None and a.tag.value.value == key.encode():
            return a.value[0]
        a = a.value[1]
    return None


def r_string(charsxp):
    b = charsxp.value
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1")


def r_frame(obj):
    names = [c.value.decode() for c in r_attr(obj, "names").value]
    cols = {}
    for name, col in zip(names, obj.value):
        if col.info.type == T.STR:
            cols[name] = [None if c.value is None else r_string(c) for c in col.value]
        else:
            cols[name] = [float(x) for x in col.value]
    return cols


def r_objects(path):
    o = rdata.parser.parse_file(path, extension=".rds" if path.lower().endswith(".rds") else ".rda").object
    if path.lower().endswith(".rds"):
        return {"rds": r_frame(o)}
    objs = {}
    while o is not None and o.info.type == T.LIST:
        objs[o.tag.value.value.decode()] = r_frame(o.value[0])
        o = o.value[1]
    return objs


def rows_of(frame, cols):
    n = len(frame[cols[0]])
    return [tuple(frame[c][i] for c in cols) for i in range(n)]


def norm(v):
    return "" if v in (None, "&nbsp", "&nbsp;") else v.strip()


# --- Peters' pages -----------------------------------------------------------
start = open(os.path.join(peters, "start.html"), "rb").read().decode("latin-1")
listed = {}
for tid, rank, name, n in re.findall(
        r"showgenera\.php\?taxon=(\d+)&rank=(phylum|class)'[^>]*>([^<]+)</a>\s*<small>\((\d+)\)", start):
    listed[(rank, int(tid))] = (name.strip(), int(n))
put("peters", "start_page", "taxa_listed", f"phyla {sum(r == 'phylum' for r, _ in listed)}; classes {sum(r == 'class' for r, _ in listed)}")

head_re = re.compile(r"<h2>(\d+|One) gen(?:era are|us is) assigned to the (phylum|class) ([^<]+)</h2>")
row_re = re.compile(r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", re.S)
pages = {}
for path in glob.glob(os.path.join(peters, "*_*.html")):
    m = re.fullmatch(r"(phylum|class)_(\d+)\.html", os.path.basename(path))
    if not m:
        continue
    text = open(path, "rb").read().decode("latin-1")
    h = head_re.search(text)
    rows = [tuple(norm(re.sub(r"<[^>]+>", "", c)) for c in r) for r in row_re.findall(text)]
    key = (m.group(1), int(m.group(2)))
    n_head = 1 if h.group(1) == "One" else int(h.group(1))
    pages[key] = (h.group(3).strip(), n_head, rows)
    name, n_start = listed.get(key, ("?", None))
    if not (h.group(2) == key[0] and h.group(3).strip() == name and n_head == len(rows) == n_start):
        failures.append(f"page {key}: heading {h.group(0)!r}, rows {len(rows)}, start page {n_start}")
missing = set(listed) - set(pages)
if missing:
    failures.append(f"pages missing: {sorted(missing)}")
for rank in ("phylum", "class"):
    ks = [k for k in pages if k[0] == rank]
    put("peters", "pages", rank, f"{len(ks)} pages; {sum(len(pages[k][2]) for k in ks)} genus rows; "
        f"headings, rows and start-page counts agree on {sum(1 for k in ks if f'page {k}:' not in ' '.join(failures))}")

phylum_rows = []
for k in sorted(k for k in pages if k[0] == "phylum"):
    phylum_rows += [(pages[k][0],) + r for r in pages[k][2]]
pool = defaultdict(list)
for i, r in enumerate(phylum_rows):
    pool[r[1:]].append(i)
klass = [None] * len(phylum_rows)
class_phylum, unmatched = {}, 0
for k in sorted(k for k in pages if k[0] == "class"):
    cname, _, rows = pages[k]
    phyla = Counter()
    for r in rows:
        free = [i for i in pool[r] if klass[i] is None]
        if not free:
            unmatched += 1
            continue
        klass[free[0]] = cname
        phyla[phylum_rows[free[0]][0]] += 1
    class_phylum[cname] = phyla
put("peters", "class_matching", "class_rows_without_phylum_row", unmatched)
put("peters", "class_matching", "classes_spanning_several_phyla",
    "; ".join(f"{c}: {dict(p)}" for c, p in sorted(class_phylum.items()) if len(p) > 1) or "none")
dups = {key: ix for key, ix in pool.items() if len(ix) > 1}
put("peters", "class_matching", "identical_phylum_rows", f"{sum(len(ix) for ix in dups.values())} rows in {len(dups)} groups")
no_class = [phylum_rows[i] for i in range(len(phylum_rows)) if klass[i] is None]
put("peters", "class_matching", "genera_without_class_page", len(no_class))
put("peters", "class_matching", "genera_without_class_page_by_phylum",
    "; ".join(f"{p} {n}" for p, n in Counter(r[0] for r in no_class).most_common()))

os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "sepkoski_genera.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["phylum", "class", "order", "genus", "FOP", "FOS", "LOP", "LOS"])
    for r, c in zip(phylum_rows, klass):
        w.writerow([r[0], c or ""] + list(r[1:]))

genera = phylum_rows
put("genera", "rows", "total", len(genera))
names = Counter(r[2] for r in genera)
put("genera", "names", "distinct", len(names))
put("genera", "names", "repeated_names", f"{sum(1 for n in names.values() if n > 1)} names on {sum(n for n in names.values() if n > 1)} rows")
odd = sorted({r[2] for r in genera if not re.fullmatch(r"[A-Z][a-z]+", r[2])})
put("genera", "names", "not_a_plain_capitalised_word", f"{len(odd)}: " + ", ".join(odd[:40]))
nonascii = sorted({r[2] for r in genera if any(ord(ch) > 127 for ch in r[2])})


def low7(name):
    return "".join(chr(ord(ch) & 0x7F) for ch in name)


put("genera", "names", "non_ascii (bit 7 set on one letter or more; bit cleared)", ", ".join(f"{n} -> {low7(n)}" for n in nonascii))
put("genera", "orders", "uncertain_or_incertae_sedis", sum(r[1].lower() in ("uncertain", "incertae sedis") for r in genera))
for col, i in (("FOP", 3), ("LOP", 5)):
    put("genera", "periods", col, "; ".join(f"{k or '(blank)'} {v}" for k, v in Counter(r[i] for r in genera).most_common()))
for col, i in (("FOS", 4), ("LOS", 6)):
    c = Counter(r[i] for r in genera)
    put("genera", "stages", col, f"{len(c)} codes; blank {c.get('', 0)}; '?' {c.get('?', 0)}; top: "
        + ", ".join(f"{k} {v}" for k, v in c.most_common(12)))
put("genera", "stages", "codes spelling Maastrichtian 'Maes'", sum(("Maes" in r[4]) + ("Maes" in r[6]) for r in genera))
put("genera", "ranges", "extant (LOP R)", sum(r[5] == "R" for r in genera))
put("genera", "ranges", "single_interval (same FOP/FOS as LOP/LOS)", sum(r[3:5] == r[5:7] for r in genera))
put("genera", "by_phylum", "rows", "; ".join(f"{p} {n}" for p, n in Counter(r[0] for r in genera).most_common()))

# --- R package -------------------------------------------------------------
gh_files = {os.path.relpath(p, gh_raw): p for p in glob.glob(os.path.join(gh_raw, "**", "*"), recursive=True)}
scrape = r_objects(gh_files["inst/extdata/sepkoski_scrape.RDS"])["rds"]
srows = [(a, b) + tuple(norm(x) for x in rest) for a, b, *rest in
         rows_of(scrape, ["name", "rank", "Order", "Genus", "FOP", "FOS", "LOP", "LOS"])]
ours = []
for (rank, _), (name, _, rows) in pages.items():
    ours += [(name, rank) + r for r in rows]
s_c, o_c = Counter((r[1],) + r[2:] for r in srows), Counter((r[1],) + r[2:] for r in ours)
put("rpackage", "scrape_2022_vs_capture", "rows", f"scrape {len(srows)}; capture {len(ours)}")
put("rpackage", "scrape_2022_vs_capture", "rows_only_in_scrape", sum((s_c - o_c).values()))
put("rpackage", "scrape_2022_vs_capture", "rows_only_in_capture", sum((o_c - s_c).values()))
diff_ex = list((s_c - o_c).elements())[:5] + list((o_c - s_c).elements())[:5]
put("rpackage", "scrape_2022_vs_capture", "examples", " | ".join(" ".join(x) for x in diff_ex) or "none")

def maas(code):
    return code.replace("Maes", "Maas")


def pkg_key(r):
    return (r[2].lower(), r[1].lower(), r[3], maas(r[4]), r[5], maas(r[6]) or None)


ours_keys = Counter(pkg_key(r) for r in genera)


def compare_raw(label, objs):
    raw = objs["sepkoski_raw"]
    rr = rows_of(raw, ["genus", "order", "FOP", "FOS", "LOP", "LOS"])
    rk = Counter((g.lower(), o.lower(), a, b, c, d if d not in ("", None) else None) for g, o, a, b, c, d in rr)
    put("rpackage", f"{label}_sepkoski_raw", "rows", len(rr))
    absent = ours_keys - rk
    put("rpackage", f"{label}_sepkoski_raw", "capture_rows_absent", sum(absent.values()))
    if label == "github":
        cls = {pkg_key(r): c for r, c in zip(genera, klass)}
        put("rpackage", "github_sepkoski_raw", "capture_rows_absent_with_no_class_page",
            sum(n for k, n in absent.items() if cls.get(k) is None))
    put("rpackage", f"{label}_sepkoski_raw", "rows_not_in_capture", sum((rk - ours_keys).values()))
    sep = objs["sepkoski"]
    na = sum(1 for x in sep["max_ma"] if x != x) + sum(1 for x in sep["min_ma"] if x != x)
    put("rpackage", f"{label}_sepkoski", "rows; missing ages", f"{len(sep['genus'])}; {na}")
    fauna = Counter(sep.get("fauna", [None] * 0))
    put("rpackage", f"{label}_sepkoski", "fauna", "; ".join(f"{k or 'NA'} {v}" for k, v in fauna.most_common()))
    return sep


gh_objs = {}
for p in ("data/sepkoski_raw.rda", "data/sepkoski.rda", "data/interval_table.rda"):
    gh_objs.update(r_objects(gh_files[p]))
gh_sep = compare_raw("github", gh_objs)
put("rpackage", "github_interval_table", "rows", len(gh_objs["interval_table"][next(iter(gh_objs["interval_table"]))]))

tarball = glob.glob(os.path.join(cran_raw, "sepkoski_*.tar.gz"))[0]
with tempfile.TemporaryDirectory() as tmp, tarfile.open(tarball) as tf:
    cran_objs = {}
    for m in tf.getmembers():
        if re.fullmatch(r"sepkoski/data/\w+\.rda", m.name):
            target = os.path.join(tmp, os.path.basename(m.name))
            with open(target, "wb") as f:
                f.write(tf.extractfile(m).read())
            cran_objs.update(r_objects(target))
    put("rpackage", "cran_release", "data_objects", ", ".join(sorted(cran_objs)))
    cran_sep = compare_raw("cran", cran_objs)
key = lambda s, i: (s["genus"][i], s["interval_max"][i], s["interval_min"][i])
gh_ages = {key(gh_sep, i): (gh_sep["max_ma"][i], gh_sep["min_ma"][i]) for i in range(len(gh_sep["genus"]))}
cran_keys = [key(cran_sep, i) for i in range(len(cran_sep["genus"]))]
changed = sum(1 for i, k in enumerate(cran_keys)
              if k in gh_ages and gh_ages[k] != (cran_sep["max_ma"][i], cran_sep["min_ma"][i]))
put("rpackage", "cran_vs_github_sepkoski", "rows_with_changed_ages",
    f"{changed} of {len(cran_keys)}; keys (genus, intervals) not in GitHub head {sum(k not in gh_ages for k in cran_keys)}")
pkg_names = sorted({g for g in gh_objs["sepkoski_raw"]["genus"] if any(ord(ch) > 127 for ch in g)})
put("rpackage", "github_sepkoski_raw", "non_ascii_genus_names", ", ".join(pkg_names))

# --- BHL scan ---------------------------------------------------------------
meta = json.load(open(os.path.join(bhl_raw, "ia_metadata.json")))
md5 = {f["name"]: f.get("md5") for f in meta["files"]}
for name in ("bulletinsofameri363pale.pdf", "bulletinsofameri363pale_djvu.txt"):
    h = hashlib.md5(open(os.path.join(bhl_raw, name), "rb").read()).hexdigest()
    ok = h == md5.get(name)
    put("bhl", "md5_vs_archive", name, "ok" if ok else f"MISMATCH {h} vs {md5.get(name)}")
    if not ok:
        failures.append(f"md5 {name}")
put("bhl", "metadata", "rights", meta["metadata"].get("possible-copyright-status"))
ocr = open(os.path.join(bhl_raw, "bulletinsofameri363pale_djvu.txt"), encoding="utf-8", errors="replace").read()
words = Counter(w.lower() for w in re.findall(r"[A-Za-zÀ-ɏ]+", ocr))
pool_names = sorted(n for n in names if re.fullmatch(r"[A-Z][a-z]+", n))
sample = random.Random(2002).sample(pool_names, 500)
hits = sum(words[n.lower()] > 0 for n in sample)
put("bhl", "ocr_lookup", "seeded_sample_of_500_plain_names", f"{hits} found as words in the OCR text ({hits / 5:.1f}%)")
put("bhl", "ocr_lookup", "all_plain_names", f"{sum(words[n.lower()] > 0 for n in pool_names)} of {len(pool_names)}")
fixed_found = sum(words[low7(n).lower()] > 0 for n in nonascii)
put("bhl", "ocr_lookup_non_ascii", "names with bit 7 cleared found in the OCR text",
    f"{fixed_found} of {len(nonascii)}; as captured {sum(words[n.lower()] > 0 for n in nonascii)}; missing: "
    + (", ".join(low7(n) for n in nonascii if not words[low7(n).lower()]) or "none"))
missed = [n for n in pool_names if not words[n.lower()]]
put("bhl", "ocr_lookup", "plain names not found", ", ".join(missed[:60]))

for f in failures:
    put("checks", "failure", "", f)
put("checks", "summary", "", "ok" if not failures else f"{len(failures)} failures")
with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
sys.exit(1 if failures else 0)
