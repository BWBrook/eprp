"""Test at what depth STRATDAT's *_MIDPOINT, *_BASE and *_BELOW_M fields are evaluated.

Usage: python3 stratdat_midpoint_check.py BIOSTRATIGRAPHY_CSV OUT_TSV

Each pick has one depth (SAMPLE_DEPTH_M). STRAT_UNIT_TOP is the unit at that
depth, and DISTANCE_TO_STRAT_UNIT_ABOVE_M the distance up to the unit above, so
depth minus that distance is the top of the pick's unit. From the picks of one
borehole this gives a partial unit sequence:

- strict: a unit's interval runs from its top to the deepest pick in it; a depth
  inside exactly one such interval has that unit.
- sequence: the unit at a depth is the one with the greatest known top at or
  above it (assumes the known tops are consecutive).

STRAT_UNIT_MIDPOINT is then compared with the sequence's unit at f times the
sample depth for a grid of f, and at depth minus a constant offset. The same is
done for SEQUENCE_MIDPOINT, and the *_BASE and *_BELOW_M fields are tested
against the midpoint and top fields. Writes long-format (table, metric, key,
value). Standard library only.
"""

import bisect
import csv
import sys
from collections import defaultdict

csv.field_size_limit(1 << 30)
out = []
FRACTIONS = (1.0, 0.9, 0.7, 0.55, 0.52, 0.5, 0.48, 0.45)
OFFSETS = (0, 5, 10, 25, 50, 100, 250, 500, 1000)


def add(*row):
    out.append(row)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def filled(r, k):
    return bool(r[k].strip())


def share(m, n):
    return f"{m} of {n} ({100 * m / n:.1f}%)" if n else "0 of 0"


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
by_hole = defaultdict(list)
for r in rows:
    by_hole[r["ENO"]].append(r)


class Sequence:
    """One borehole's partial sequence of units, rebuilt from a TOP field and its ABOVE distance."""

    def __init__(self, hole_rows, top, above):
        reach = {}
        for r in hole_rows:
            d, a, u = num(r["SAMPLE_DEPTH_M"]), num(r[above]), r[top].strip()
            if u and a is not None and d is not None:
                key = (round(d - a, 2), u)
                reach[key] = max(reach.get(key, d), d)
        self.reach = reach
        self.starts = {}
        for s, u in reach:
            self.starts.setdefault(s, set()).add(u)
        self.sorted_starts = sorted(self.starts)

    def strict(self, x):
        units = {u for (s, u), deepest in self.reach.items() if s - 1e-9 <= x <= deepest + 1e-9}
        return next(iter(units)) if len(units) == 1 else None

    def sequence(self, x):
        i = bisect.bisect_right(self.sorted_starts, x + 1e-9) - 1
        if i < 0:
            return None
        units = self.starts[self.sorted_starts[i]]
        return next(iter(units)) if len(units) == 1 else None


def families():
    return {
        "strat_unit": ("STRAT_UNIT_TOP", "DISTANCE_TO_STRAT_UNIT_ABOVE_M", "STRAT_UNIT_MIDPOINT", ";"),
        "sequence": ("SEQUENCE_TOP", "DISTANCE_TO_SEQUENCE_ABOVE_M", "SEQUENCE_MIDPOINT", None),
    }


def midpoint_matches(label, mid, sep):
    return label == mid or (sep is not None and label in mid.split(sep))


def evaluate(seqs, mid_field, sep, kind, x_of, picks):
    n = m = 0
    for r in picks:
        d = num(r["SAMPLE_DEPTH_M"])
        x = x_of(d)
        if x < 0:
            continue
        s = seqs[r["ENO"]]
        label = s.strict(x) if kind == "strict" else s.sequence(x)
        if label is None:
            continue
        n += 1
        m += midpoint_matches(label, r[mid_field].strip(), sep)
    return m, n


for name, (top, above, mid_field, sep) in families().items():
    t = f"{name}_midpoint_vs_top_sequence"
    seqs = {e: Sequence(rs, top, above) for e, rs in by_hole.items()}
    picks = [r for r in rows if filled(r, mid_field) and num(r["SAMPLE_DEPTH_M"]) is not None]
    add(t, "picks_with_midpoint", "", len(picks))
    add(t, "boreholes_with_a_rebuilt_sequence", "", sum(bool(s.reach) for s in seqs.values()))
    for kind in ("strict", "sequence"):
        for f in FRACTIONS:
            m, n = evaluate(seqs, mid_field, sep, kind, lambda d: f * d, picks)
            add(t, f"{kind}:match_at_depth_fraction", f"{f:.2f}", share(m, n))
    fixed = [
        r for r in picks
        if all(seqs[r["ENO"]].strict(f * num(r["SAMPLE_DEPTH_M"])) is not None for f in FRACTIONS)
    ]
    for f in FRACTIONS:
        m, n = evaluate(seqs, mid_field, sep, "strict", lambda d: f * d, fixed)
        add(t, "strict_fixed_set:match_at_depth_fraction", f"{f:.2f}", share(m, n))
    for c in OFFSETS:
        m, n = evaluate(seqs, mid_field, sep, "strict", lambda d: d - c, picks)
        add(t, "strict:match_at_depth_minus_offset_m", c, share(m, n))
    scan = []
    for i in range(30, 101):
        m, n = evaluate(seqs, mid_field, sep, "strict", lambda d: i / 100 * d, picks)
        scan.append((m / n if n else 0, i / 100, m, n))
    best = max(scan)
    add(t, "strict:best_fraction_0.30_to_1.00_step_0.01", f"{best[1]:.2f}", share(best[2], best[3]))
    scan = []
    for c in range(0, 1001, 5):
        m, n = evaluate(seqs, mid_field, sep, "strict", lambda d: d - c, picks)
        scan.append((m / n if n else 0, c, m, n))
    best = max(scan)
    add(t, "strict:best_offset_m_0_to_1000_step_5", best[1], share(best[2], best[3]))
    if name == "strat_unit":
        for lo, hi in ((0, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, 99999)):
            sub = [r for r in picks if lo <= num(r["SAMPLE_DEPTH_M"]) < hi]
            m, n = evaluate(seqs, mid_field, sep, "strict", lambda d: 0.5 * d, sub)
            add(t, "strict:match_at_half_depth_by_sample_depth_m", f"{lo}-{hi}", share(m, n))

t = "strat_unit_below_distance"
seqs = {e: Sequence(rs, "STRAT_UNIT_TOP", "DISTANCE_TO_STRAT_UNIT_ABOVE_M") for e, rs in by_hole.items()}
below_rows = [r for r in rows if num(r["DISTANCE_TO_STRAT_UNIT_BELOW_M"]) is not None and num(r["SAMPLE_DEPTH_M"]) is not None]
for frac in (1.0, 0.5):
    hit = 0
    for r in below_rows:
        s = seqs[r["ENO"]].sorted_starts
        y = frac * num(r["SAMPLE_DEPTH_M"]) + num(r["DISTANCE_TO_STRAT_UNIT_BELOW_M"])
        i = bisect.bisect_left(s, y - 0.06)
        hit += i < len(s) and s[i] <= y + 0.06
    add(t, "depth_fraction_plus_distance_is_a_known_unit_top_within_0.06m", f"{frac:.1f}", share(hit, len(below_rows)))

t = "base_and_state_fields"
mid_rows = [r for r in rows if filled(r, "STRAT_UNIT_MIDPOINT")]
add(t, "strat_unit_base_filled", "", sum(filled(r, "STRAT_UNIT_BASE") for r in rows))
add(t, "strat_unit_base_equals_midpoint", "", share(sum(r["STRAT_UNIT_BASE"] == r["STRAT_UNIT_MIDPOINT"] for r in mid_rows), len(mid_rows)))
add(t, "strat_unit_midpoint_with_several_units_semicolon", "", sum(";" in r["STRAT_UNIT_MIDPOINT"] for r in mid_rows))
add(t, "strat_unit_base_is_a_member_of_midpoint_list", "", share(sum(r["STRAT_UNIT_BASE"] in r["STRAT_UNIT_MIDPOINT"].split(";") for r in mid_rows), len(mid_rows)))
pairs = (
    ("strat_unit", "STRAT_UNIT_TOP", "STRAT_UNIT_MIDPOINT", "differ"),
    ("sequence", "SEQUENCE_TOP", "SEQUENCE_MIDPOINT", "differ"),
    ("state_strat_unit", "STATE_STRAT_UNIT_TOP", "STATE_STRAT_UNIT_MIDPOINT", "differ"),
    ("sequence", "SEQUENCE_BASE", "SEQUENCE_MIDPOINT", "equal"),
    ("state_strat_unit", "STATE_STRAT_UNIT_BASE", "STATE_STRAT_UNIT_TOP", "equal"),
    ("strat_unit", "STRAT_UNIT_BASE", "STRAT_UNIT_MIDPOINT", "equal"),
)
for fam, a, b, how in pairs:
    both = [r for r in rows if filled(r, a) and filled(r, b)]
    k = sum((r[a] != r[b]) if how == "differ" else (r[a] == r[b]) for r in both)
    add(t, f"{a}_{how}s_{b}", fam, share(k, len(both)))
add(t, "state_strat_unit_base_filled_and_top_filled_together", "", sum(filled(r, "STATE_STRAT_UNIT_BASE") == filled(r, "STATE_STRAT_UNIT_TOP") for r in rows))
for k in ("STRAT_UNIT_MIDPOINT", "STRAT_UNIT_BASE", "STRATNO_MIDPOINT", "STRATIGRAPHIC_AGE_MIDPOINT", "DINOCYST_MIDPOINT",
          "SPORE_POLLEN_MIDPOINT", "DISTANCE_TO_STRAT_UNIT_BELOW_M", "SEQUENCE_MIDPOINT", "SEQUENCE_BASE",
          "DISTANCE_TO_SEQUENCE_BELOW_M", "STATE_STRAT_UNIT_MIDPOINT"):
    add(t, "filled", k, sum(filled(r, k) for r in rows))
    add(t, "filled_exactly_when_strat_unit_midpoint_filled", k, sum(filled(r, k) == filled(r, "STRAT_UNIT_MIDPOINT") for r in rows))

t = "yampi_1"
yampi = [r for r in rows if r["BOREHOLE_NAME"] == "Yampi 1"]
ys = Sequence(yampi, "STRAT_UNIT_TOP", "DISTANCE_TO_STRAT_UNIT_ABOVE_M")
first_mid = {}
for r in sorted(yampi, key=lambda r: num(r["SAMPLE_DEPTH_M"])):
    for u in r["STRAT_UNIT_MIDPOINT"].split(";"):
        first_mid.setdefault(u.strip(), num(r["SAMPLE_DEPTH_M"]))
tops = {}
for s, u in sorted(ys.reach):
    tops.setdefault(u, s)
add(t, "picks_with_strat_unit_top", "", sum(filled(r, "STRAT_UNIT_TOP") for r in yampi))
for u, s in sorted(tops.items(), key=lambda kv: kv[1]):
    if u in first_mid:
        add(t, "unit_top_m | first_sample_depth_m_whose_midpoint_unit_is_it | ratio", u, f"{s:g} | {first_mid[u]:g} | {first_mid[u] / s:.2f}" if s else f"{s:g} | {first_mid[u]:g} | n/a")

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
