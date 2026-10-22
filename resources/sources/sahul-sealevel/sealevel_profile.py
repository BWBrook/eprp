"""Profile the Sahul sea-level pack: Pico et al. (2020) shelf areas and the Spratt and Lisiecki (2016) stack.

Usage: python3 sealevel_profile.py PICO_CSV SPRATT_NOAA_TXT OUT_TSV

Reports rows, duplicates, time ranges, the shelf-area peaks under both ice
histories, and sea level at selected ages (short PC1 stack, with 1 sigma).
Writes long-format (table, metric, key, value). Standard library only.
"""

import csv
import sys
from collections import Counter

out = []


def add(*row):
    out.append(row)


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))
head, data = rows[0], [r for r in rows[1:] if r and r[0].strip()]
add("pico", "columns", "", " | ".join(head))
add("pico", "rows", "", len(data))
add("pico", "duplicate_rows", "", len(data) - len({tuple(r) for r in data}))
times = [float(r[0]) for r in data]
add("pico", "time_range_ka", "", f"{min(times)} to {max(times)}")
for i, name in enumerate(head[1:], start=1):
    vals = [(float(r[i]), float(r[0])) for r in data]
    v, t = max(vals)
    add("pico", "peak_km2_at_ka", name.split(" increase")[0], f"{v:.3g} at {t}")
    for ka in (21, 50):
        add("pico", f"value_at_ka_{ka}", name.split(" increase")[0], next(r[i] for r in data if float(r[0]) == ka))

with open(sys.argv[2], encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f if l.strip() and not l.startswith("#")]
cols = lines[0].split("\t")
recs = [dict(zip(cols, l.split("\t"))) for l in lines[1:]]
add("spratt", "columns", "", " | ".join(cols))
add("spratt", "rows", "", len(recs))
ages = [float(r["age_calkaBP"]) for r in recs]
add("spratt", "age_range_ka", "", f"{min(ages)} to {max(ages)}")
add("spratt", "age_steps_ka", "", " ".join(f"{k}:{v}" for k, v in Counter(round(b - a, 3) for a, b in zip(ages, ages[1:])).most_common(3)))
for a in (0, 5, 14, 18, 21, 22, 24, 30, 40, 50, 60, 65, 80, 100, 120):
    r = next(r for r in recs if float(r["age_calkaBP"]) == a)
    add("spratt", "short_pc1_m_at_ka", a, f'{r["SeaLev_shortPC1"]} (1 sigma {r["SeaLev_shortPC1_err_sig"]})')
low = min(recs, key=lambda r: float(r["SeaLev_shortPC1"]))
add("spratt", "lowest_short_pc1", "", f'{low["SeaLev_shortPC1"]} m at {low["age_calkaBP"]} ka')

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
