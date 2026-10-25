"""Build one citation table from Barry's 2003-04 materials: the docx list (list.txt), the RTF bibliography
(papers_held.txt) and the five EndNote libraries (*.enl.records.json). Run from the eprp2004 directory."""
import csv
import json
import re
from pathlib import Path

CITE_RE = re.compile(r"^(?P<authors>.+?) (?P<body>[A-Z0-9\"'(].*?) (?P<vol>[\w-]+), (?P<pages>[\w+-]+) \((?P<year>1[89]\d\d|20[0-2]\d)\)\.?$")
GROUPS = {"NATURE": "Nature", "SCIENCE": "Science", "Trends in Ecology & Evolution": "TREE", "OTHER": "Other"}
rows = []


def first_author(authors):
    return authors.split(",")[0].strip()


def nature_style(line):
    """Split 'Authors. Title. Journal Vol, pages (Year).' into fields (title and journal approximately)."""
    m = re.search(r" (?P<vol>[\w-]+), (?P<pages>[\w+-]+) \((?P<year>1[89]\d\d|20[0-2]\d)\)\.?$", line)
    if not m:
        return None
    head = line[:m.start()]
    am = re.match(r"^((?:[^,.&]+, (?:[A-Z][a-z]?\.(?: |-)?)+[ ,]*(?:&| ,)? *)+)", head)
    authors = am.group(1).strip(" ,&") if am else ""
    rest = head[am.end():] if am else head
    title, _, journal = rest.rpartition(". ")
    return {"authors": authors, "title": title.strip() or rest, "journal": journal.strip(), "volume": m["vol"],
            "pages": m["pages"], "year": m["year"]}


# 1. the 2003 list (docx), in its four groups, numbered within each group as in the repo transcription
group, n = None, 0
for line in Path("list.txt").read_text().splitlines():
    line = line.strip()
    if not line:
        continue
    if line in GROUPS:
        group, n = GROUPS[line], 0
        continue
    n += 1
    f = nature_style(line) or {}
    rows.append({"source": "list", "item": f"{group} {n}", "raw": line, **f,
                 "first_author": first_author(f.get("authors") or line)})

# 2. the RTF bibliography of papers held (Jan 2003): citation lines only, abstracts skipped
k = 0
for line in Path("papers_held.txt").read_text().splitlines():
    line = line.strip()
    f = nature_style(line) if line else None
    if f and len(line) < 400:
        k += 1
        rows.append({"source": "papers-held-rtf", "item": f"Papers Held {k}", "raw": line, **f,
                     "first_author": first_author(f["authors"] or line)})

# 3. the EndNote libraries
for path in sorted(Path("src").glob("*.enl.records.json")):
    lib = path.name.replace("EPRP - ", "").replace(".enl.records.json", "")
    for i, r in enumerate(json.load(open(path)), 1):
        authors = (r.get("2") or "").replace("\n", "; ")
        pages = r.get("5") or ""
        rows.append({"source": f"endnote:{lib}", "item": f"{lib} {i}",
                     "raw": f'{authors}. {r.get("4", "")}. {r.get("6", "")} {r.get("7", "")}, {pages} ({r.get("3", "")}).',
                     "authors": authors, "title": (r.get("4") or "").replace("\n", " "), "journal": r.get("6") or "",
                     "volume": r.get("7") or "", "pages": pages, "year": r.get("3") or "",
                     "first_author": first_author(authors), "publisher": r.get("12") or "",
                     "isi": (r.get("30") or "").split("\n")[0] if (r.get("30") or "").startswith("ISI:") else ""})

fields = ["source", "item", "first_author", "year", "title", "journal", "volume", "pages", "authors", "publisher", "isi", "raw"]
with open("citations.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
from collections import Counter
print(Counter(r["source"].split(":")[0] if r["source"] != "list" else r["item"].split()[0] for r in rows))
print("total", len(rows), "| list rows without a parsed title:", sum(1 for r in rows if r["source"] == "list" and not r.get("title")))
for r in rows[:3] + [r for r in rows if r["source"] == "papers-held-rtf"][:2]:
    print({k: r.get(k, "")[:50] for k in ("item", "first_author", "year", "title", "journal", "volume", "pages")})
