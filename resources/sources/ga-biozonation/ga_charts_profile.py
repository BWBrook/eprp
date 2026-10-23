"""Profile the mirrored Geoscience Australia biozonation charts from the text printed in each PDF.

Usage: python3 -I ga_charts_profile.py RAW_VERSION_DIR OUT_PROFILE_TSV OUT_SUMMARY_TSV

RAW_VERSION_DIR is /data/paleodata/ga-biozonation/raw/<version_dir> (files plus MANIFEST.json).
Needs pdftotext (poppler). Writes one row per mirrored file, plus one row per PDF inside
64962__Data.zip, with: eCat record, size, sha256 check against MANIFEST.json, pages, chart
number, title and copyright years, printed catalogue number, raster image count, the time scales the chart names
as its own and those named in its "revision of previous charts" statement, the licence or
copyright statement printed in the PDF, whether it says it revises previous charts, whether
it names STRATDAT, and draft or under-revision notes. The summary is long format
(table, metric, key, value). Email addresses are removed from every output cell.
Standard library only.
"""

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter

raw_dir, out_profile, out_summary = sys.argv[1:4]
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")


def pdf_text(path):
    return subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"], check=True, capture_output=True).stdout.decode("utf-8")


def raster_images(path):
    out = subprocess.run(["pdfimages", "-list", path], check=True, capture_output=True).stdout.decode("utf-8").splitlines()
    return max(len(out) - 2, 0)


def squash(s):
    return re.sub(r"\s+", " ", s)


def clip(s, n=220):
    s = EMAIL.sub("[email removed]", squash(s)).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


REVISION = re.compile(r"This chart represents a revision of previous charts[^.]*\.")
OWN_SCALES = [
    ("GTS2004", r"GTS ?2004|Geologic Time ?Scale,? 2004|Gradstein et al\.? ?\(?2004|ICS 2004 Geologic"),
    ("GTS2008", r"GTS ?2008|Concise Geologic Time ?scale"),
    ("GTS2012", r"GTS ?2012|Geologic Time Scale(?: \(GTS\))?(?: \([^)]*\))?,? 2012"),
    ("GTS2016", r"GTS ?2016|Ogg, Ogg and Gradstein, 2016"),
    ("AGSO timescale", r"AGSO time ?scale"),
    ("Young & Laurie 1996", r"Young (?:&|and) Laurie,? 1996|Australian? Phanerozoic Timescale"),
    ("Gradstein et al 1995", r"Gradstein et al\.?,? ?\(?1995"),
]
STATEMENTS = [
    r"Magnetic polarity timescale after .{0,25}?rescaled to AGSO timescale",
    r"(?:The timescale, biozonation and stratigraphic data|The biozonation data) in this product has been compiled to .{1,160}",
    r"Stage and sub-stage terminology from Gradstein et al,? ?1995",
    r"Date of Gradstein et al,? ?1995",
    r"Geologic Time Scale 2004 Gradstein et al\. 2004",
    r"correlation to the ICS 2004 Geologic Time Scale",
    r"Australian Timescale Young (?:&|and) Laurie,? 1996",
]
STOP = re.compile(r" Published with permission| ©| Production| Inquiries| The stratigraphy| Cartography| Feedback")
REVISION_SCALES = [("GTS2004", r"GTS 2004"), ("GTS2008", r"GTS 2008"), ("AGSO 1996", r"AGSO 1996")]
CATALOGUE = re.compile(r"(?:AGSO Catalogue No\.?|Catalogue number:|Geocat|GeoCat #?|GEOCAT:)\s*(\d+)")
TITLE_YEAR = re.compile(r"(?:Biozonation (?:and|&) Stratigraphy|Panorama, Chart \d+[ab]),?\s*((?:19|20)\d\d)")
COPY_YEAR = re.compile(r"(?:©|\(c\))? ?Commonwealth of Australia(?: \(Geoscience Australia\))?,? ((?:19|20)\d\d)")
ALL_RIGHTS = re.compile(r"no part may be reproduced by any process without (?:the )?written permission")
CC4 = re.compile(r"Creative Commons Attribution 4\.0 International")
CC3AU = re.compile(r"Creative Commons Attribution 3\.0 Australia")
CC_ANY = re.compile(r"Creative Commons")
NOTE = re.compile(r".{0,70}(?:currently being revised|are being revised|under revision).{0,50}")


def profile(label_file, member, ecat, size, sha_ok, text, images):
    flat = squash(text)
    row = {"file": label_file, "member": member, "ecat": ecat, "bytes": size, "sha256_ok": sha_ok}
    row["pages"] = text.count("\f")
    own_chart = (re.findall(r"(?m)^Chart (\d+[ab]?)\b", text) + re.findall(r"(?:Stratigraphy|Panorama),? (?:(?:19|20)\d\d, )?Chart (\d+[ab]?)", flat)
                 + re.findall(r"Chart (\d) of 4", flat))
    row["chart_no_printed"] = ",".join(sorted(set(own_chart)))
    row["raster_images"] = images
    m = re.search(r"(?m)^([A-Z][A-Z ,&-]+BIOZONATION AND STRATIGRAPHY)$", text)
    row["title_line"] = m.group(1) if m else ""
    row["title_year"] = ",".join(sorted(set(TITLE_YEAR.findall(flat))))
    row["copyright_year"] = ",".join(sorted(set(COPY_YEAR.findall(flat))))
    row["printed_year"] = row["title_year"] or row["copyright_year"]
    row["printed_catalogue_no"] = ",".join(sorted(set(CATALOGUE.findall(flat))))
    rev = REVISION.search(flat)
    row["revises_previous"] = "yes" if rev else "no"
    row["revision_statement"] = clip(rev.group(0)) if rev else ""
    row["revision_scales_named"] = ",".join(n for n, p in REVISION_SCALES if rev and re.search(p, rev.group(0)))
    body = flat.replace(rev.group(0), " ") if rev else flat
    own = [(n, re.search(p, body)) for n, p in OWN_SCALES]
    row["timescales_named_own"] = ",".join(n for n, mm in own if mm)
    row["timescale_statements"] = " | ".join(STOP.split(mm.group(0))[0].strip() for p in STATEMENTS for mm in [re.search(p, body)] if mm)
    lic = []
    if CC4.search(flat):
        lic.append("CC BY 4.0")
    if CC3AU.search(flat):
        lic.append("CC BY 3.0 AU")
    if CC_ANY.search(flat) and not lic:
        lic.append("other Creative Commons")
    if ALL_RIGHTS.search(flat):
        lic.append("all rights reserved (written permission required)")
    copyright_line = bool(COPY_YEAR.search(flat))
    row["licence_printed"] = " + ".join(lic) if lic else ("copyright line only" if copyright_line else "none printed")
    row["copyright_line"] = ("(c) in text layer" if re.search(r"(?:©|\(c\)) ?Commonwealth of Australia", flat) else "year line, (c) not in text layer") if copyright_line else "none in text layer"
    row["states_preferred_agso_ages"] = "yes" if "preferred AGSO ages" in flat else "no"
    row["published_with_permission_of_ceo"] = "yes" if re.search(r"Published with permission of the CEO", flat) else "no"
    row["names_timescale_creator"] = "yes" if re.search(r"Timescale Creator", flat, re.I) else "no"
    row["names_stratdat"] = "yes" if "STRATDAT" in flat else "no"
    row["stratdat_mentions"] = flat.count("STRATDAT")
    row["says_zonations_from_stratdat"] = "yes" if re.search(r"zonations presented here are from the STRATDAT", flat) else "no"
    flags = [w for w, p in (("DRAFT", r"\bDRAFT\b"), ("Preliminary version", r"Preliminary version")) if re.search(p, flat)]
    row["status_flag"] = ",".join(flags)
    note = NOTE.search(flat)
    row["own_revision_note"] = clip(note.group(0)) if note else ""
    return row


COLUMNS = ["file", "member", "ecat", "bytes", "sha256_ok", "pages", "raster_images", "chart_no_printed", "title_line", "title_year", "copyright_year",
           "printed_year", "printed_catalogue_no", "timescales_named_own", "timescale_statements", "revises_previous", "revision_scales_named",
           "revision_statement", "states_preferred_agso_ages", "licence_printed", "copyright_line", "published_with_permission_of_ceo", "names_timescale_creator", "names_stratdat",
           "stratdat_mentions", "says_zonations_from_stratdat", "status_flag", "own_revision_note"]

with open(os.path.join(raw_dir, "MANIFEST.json"), encoding="utf-8") as f:
    manifest = {x["key"]: x for x in json.load(f)["files"]}

files = sorted(k for k in os.listdir(raw_dir) if k != "MANIFEST.json")
rows = []
unlisted = [k for k in files if k not in manifest]
missing = [k for k in manifest if k not in files]
for k in files:
    path = os.path.join(raw_dir, k)
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    ok = "yes" if size == manifest[k]["size"] and sha == manifest[k]["sha256"] else "no"
    ecat = k.split("__")[0]
    if k.endswith(".pdf"):
        rows.append(profile(k, "", ecat, size, ok, pdf_text(path), raster_images(path)))
    elif k.endswith(".zip"):
        rows.append({"file": k, "member": "", "ecat": ecat, "bytes": size, "sha256_ok": ok})
        with zipfile.ZipFile(path) as z, tempfile.TemporaryDirectory() as tmp:
            for info in z.infolist():
                if info.filename.lower().endswith(".pdf"):
                    out = os.path.join(tmp, "member.pdf")
                    with open(out, "wb") as fh:
                        fh.write(z.read(info))
                    rows.append(profile(k, info.filename, ecat, info.file_size, "", pdf_text(out), raster_images(out)))
    else:
        rows.append({"file": k, "member": "", "ecat": ecat, "bytes": size, "sha256_ok": ok})

with open(out_profile, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(COLUMNS)
    w.writerows([[EMAIL.sub("[email removed]", str(r.get(c, ""))) for c in COLUMNS] for r in rows])


mirror = [r for r in rows if not r["member"]]
pdfs = [r for r in mirror if r["file"].endswith(".pdf")]
members = [r for r in rows if r["member"]]
whole = pdfs + members
summary = []


def add(*row):
    summary.append(row)


def chart_no(r):
    if r["chart_no_printed"]:
        return r["chart_no_printed"]
    m = re.search(r"Chart_(\d+)", r["file"])
    return m.group(1).lstrip("0") if m else ""


def label(r):
    if r["ecat"] in ("61127", "64962"):
        return r["member"] or r["file"].split("__")[1]
    return chart_no(r)


def order(s):
    m = re.match(r"\d+", s)
    return (int(m.group()), s) if m else (10**6, s)


def names(grp):
    return " ".join(sorted((label(r) for r in grp), key=order))


charts = [r for r in pdfs if r["ecat"] not in ("61127", "64962")]
groups = {
    "charts_printed_1996_2001": [r for r in charts if r["printed_year"] and int(r["printed_year"]) <= 2001],
    "charts_printed_2013_2017": [r for r in charts if r["printed_year"] and int(r["printed_year"]) >= 2013],
    "charts_without_printed_year": [r for r in charts if not r["printed_year"]],
    "61127": [r for r in pdfs if r["ecat"] == "61127"],
    "record_2006_23_and_zip_pdfs": [r for r in whole if r["ecat"] == "64962"],
}

add("mirror", "files", "", len(mirror))
add("mirror", "bytes", "", sum(r["bytes"] for r in mirror))
add("mirror", "files_failing_size_or_sha256_check", "", sum(r["sha256_ok"] != "yes" for r in mirror))
add("mirror", "files_not_in_manifest", "", len(unlisted))
add("mirror", "manifest_entries_without_file", "", len(missing))
add("mirror", "pdfs", "", len(pdfs))
add("mirror", "pdfs_inside_64962_Data.zip", "", len(members))
for k, v in sorted(Counter(r["ecat"] for r in mirror).items()):
    add("mirror", "files_by_ecat", k, v)
largest = max(mirror, key=lambda r: r["bytes"])
add("mirror", "largest_file", largest["file"], largest["bytes"])
add("mirror", "pdfs_with_raster_images", "", names([r for r in whole if int(r["raster_images"]) > 0]) or "none")

add("charts", "chart_pdfs", "", len(charts))
add("charts", "chart_pdfs_with_one_page", "", sum(r["pages"] == 1 for r in charts))
add("charts", "chart_pdfs_in_ecat_76687", "", sum(r["ecat"] == "76687" for r in charts))
add("charts", "chart_pdfs_in_other_ecat_records", "", sum(r["ecat"] != "76687" for r in charts))
for g, grp in groups.items():
    add("charts", f"group:{g}", "", len(grp))
    add("charts", f"group:{g}: ecat 76687", "", sum(r["ecat"] == "76687" for r in grp))
    add("charts", f"group:{g}: members", "", names(grp) or "none")
    for k, v in sorted(Counter(r["printed_year"] or "none" for r in grp).items()):
        add("charts", f"group:{g}: printed_year", k, v)
nums = sorted({re.match(r"\d+", chart_no(r)).group() for r in charts}, key=int)
add("charts", "distinct_chart_numbers (8a/8b and 28a/28b count once)", "", len(nums))
add("charts", "chart_numbers_present", "", " ".join(nums))
add("charts", "chart_numbers_missing_below_max", "", " ".join(str(n) for n in range(1, int(nums[-1])) if str(n) not in nums))
add("charts", "chart_pdfs_without_printed_chart_number (number taken from file name)", "", names([r for r in charts if not r["chart_no_printed"]]))
add("charts", "printed_catalogue_numbers (chart: number)", "", " ".join(f"{label(r)}:{r['printed_catalogue_no']}" for r in sorted(whole, key=lambda r: order(label(r))) if r["printed_catalogue_no"]))

for col in ("licence_printed", "copyright_line", "published_with_permission_of_ceo", "names_timescale_creator", "revises_previous", "revision_scales_named", "timescales_named_own", "states_preferred_agso_ages", "names_stratdat", "says_zonations_from_stratdat", "status_flag"):
    for g, grp in groups.items():
        for k, v in sorted(Counter(r[col] or "none" for r in grp).items()):
            add(g, f"by:{col}", k, v)
for col in ("licence_printed", "timescales_named_own"):
    for k in sorted({r[col] for r in whole if r[col]}):
        add("members", f"{col} = {k}", "", names([r for r in whole if r[col] == k]))
add("members", "timescales_named_own = (none)", "", names([r for r in whole if not r["timescales_named_own"]]))
add("members", "revises_previous = yes", "", names([r for r in whole if r["revises_previous"] == "yes"]))
add("members", "revises_previous = no (chart pdfs)", "", names([r for r in charts if r["revises_previous"] == "no"]))
add("members", "names_timescale_creator = yes", "", names([r for r in whole if r["names_timescale_creator"] == "yes"]))
add("members", "names_stratdat = yes", "", names([r for r in whole if r["names_stratdat"] == "yes"]))
add("members", "says_zonations_from_stratdat = yes", "", names([r for r in whole if r["says_zonations_from_stratdat"] == "yes"]))
add("members", "names_stratdat = no", "", names([r for r in whole if r["names_stratdat"] == "no"]))
add("members", "states_preferred_agso_ages = yes", "", names([r for r in whole if r["states_preferred_agso_ages"] == "yes"]))
add("members", "states_preferred_agso_ages = no (1996-2001 charts)", "", names([r for r in groups["charts_printed_1996_2001"] if r["states_preferred_agso_ages"] == "no"]))
add("members", "status_flag set", "", " ".join(f"{label(r)}:{r['status_flag']}" for r in sorted(whole, key=lambda r: order(label(r))) if r["status_flag"]))
add("members", "own_revision_note set", "", names([r for r in whole if r["own_revision_note"]]))
add("members", "copyright_line = none in text layer", "", names([r for r in whole if r["copyright_line"].startswith("none")]))
add("members", "copyright_line = year line, (c) not in text layer", "", names([r for r in whole if r["copyright_line"].startswith("year")]))

with open(out_summary, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows([[EMAIL.sub("[email removed]", str(c)) for c in row] for row in summary])
