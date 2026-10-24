"""Descriptive tallies of Clapham & Payne 2011, GSA Data Repository 2011310, Table DR1.

Input: text extracted with `pdftotext -layout` from the DR PDF
(Figshare 10.1130/2011310; md5 357d6a3b40b72a95b9b7f5ca88c1d01e).
Counts only; no association or model is computed.
"""
import collections
import sys

STAGES = {4: "Kungurian", 5: "Roadian", 6: "Wordian", 7: "Capitanian", 8: "Wuchiapingian", 9: "Changhsingian"}
SKIP = {"GSA", "2011310", "Table", "Genus", "Aragonite", "Genera"}

by = collections.defaultdict(dict)
unparsed = 0
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    t = line.split()
    if not t or t[0] in SKIP:
        continue
    idx = next((i for i, x in enumerate(t) if x.isdigit()), None)
    if idx is None or idx < 2:
        unparsed += 1
        continue
    nums = t[idx:]
    if not all(x.isdigit() for x in nums) or t[idx] not in "456789" or not 8 <= len(nums) <= 9:
        unparsed += 1
        continue
    by[int(nums[0])][t[0]] = int(nums[-1])

print("rows", sum(len(v) for v in by.values()), "unparsed", unparsed,
      "genera", len(set().union(*by.values())))
for s in sorted(by):
    e = sum(by[s].values())
    print(f"{STAGES[s]:14s} rows {len(by[s]):4d} extinct {e:4d} not {len(by[s]) - e:4d}")

g7, g8, g9 = set(by[7]), set(by[8]), set(by[9])
for label, S in [("Capitanian and Changhsingian", g9 & g7),
                 ("Changhsingian, no Capitanian row", g9 - g7),
                 ("  ... with a Wuchiapingian row", (g9 - g7) & g8),
                 ("  ... no Capitanian or Wuchiapingian row", g9 - g7 - g8),
                 ("Capitanian and Changhsingian, no Wuchiapingian row", (g9 & g7) - g8)]:
    e = sum(by[9][g] for g in S)
    print(f"{label:52s} n {len(S):4d} extinct {e:4d} survive {len(S) - e:4d} ({100 * e / len(S):.1f}%)")
