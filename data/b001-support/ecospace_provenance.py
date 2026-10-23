"""Provenance of PBDB genus-level ecospace values (B-001, coding-dependence check).

Fetches valid metazoan genera with ecospace and its basis fields into the
git-ignored data/raw/pbdb/b001/, then counts, per field, how many genera carry
a value and how many of those values were entered for the genus itself
(`<field>_basis` equal to the genus name) rather than inherited from a higher
taxon. Counts are given for all genera and for genera whose PBDB range
overlaps each provisional recovery window. Standard library only.
"""

import csv
import hashlib
import io
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/pbdb/b001/genera.csv"
OUT = pathlib.Path(__file__).resolve().parent / "ecospace_provenance.tsv"
URL = ("https://paleobiodb.org/data1.2/taxa/list.csv?base_name=Metazoa&rank=genus"
       "&taxon_status=valid&show=class,ecospace,etbasis,app&rowcount&datainfo&limit=200000")
FIELDS = ["motility", "life_habit", "diet"]
WINDOWS = {"all_genera": None, "end_permian_252_242": (242.0, 252.0),
           "end_triassic_201_191": (191.0, 201.4), "k_pg_66_56": (56.0, 66.0)}


HOLD = ("PBDB data hold (76/2259, 76/2327): this legacy rebuild is disabled; the extracts were deleted at Barry's instruction on 23 October 2026. Rebuild "
        "only from public record-level data (resources/sources/pbdb/).")


def fetch():
    raise SystemExit(HOLD)                # legacy fetch disabled; see HOLD
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL, timeout=300) as r:
            RAW.write_bytes(r.read())
    data = RAW.read_bytes()
    print("extract", RAW.relative_to(ROOT), "sha256", hashlib.sha256(data).hexdigest())
    lines = data.decode("utf-8").splitlines()
    for line in lines:
        if line.startswith(('"Access Time"', '"Records Found"')):
            print(line)
    start = next(i for i, l in enumerate(lines) if l.startswith('"orig_no"'))
    return list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))


def overlaps(r, window):
    try:
        first, last = float(r["firstapp_max_ma"]), float(r["lastapp_min_ma"])
    except ValueError:
        return False
    return first >= window[0] and last <= window[1]


def main():
    rows = fetch()
    out = [["subset", "field", "genera", "with_value", "direct", "inherited",
            "inherited_share_of_valued", "direct_share_of_all"]]
    for name, window in WINDOWS.items():
        sub = rows if window is None else [r for r in rows if overlaps(r, window)]
        for f in FIELDS:
            valued = [r for r in sub if r[f]]
            direct = sum(r[f + "_basis"] == r["taxon_name"] for r in valued)
            out.append([name, f, len(sub), len(valued), direct, len(valued) - direct,
                        f"{(len(valued) - direct) / len(valued):.4f}" if valued else "NA",
                        f"{direct / len(sub):.4f}" if sub else "NA"])
    with OUT.open("w", newline="") as fh:
        csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(out)
    for row in out:
        print("\t".join(map(str, row)))


if __name__ == "__main__":
    main()
