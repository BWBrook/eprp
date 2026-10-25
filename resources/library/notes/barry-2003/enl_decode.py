"""Decode legacy EndNote (.enl, EndNote 5-8 era) libraries by walking their tag-length-value fields.
Each field: tag (2 bytes) | field length incl. header (2) | string length (2) | string | padding.
Usage: python3 enl_decode.py FILE... -> prints tag statistics and writes <file>.records.json"""
import collections
import json
import sys

FIELD_MAX = 0x60


def chains(data):
    """Yield (offset, [(tag, text), ...]) for every maximal run of well-formed fields."""
    i, n = 0, len(data)
    while i < n - 6:
        fields, j = [], i
        while j < n - 6:
            tag = int.from_bytes(data[j:j + 2], "big")
            tlen = int.from_bytes(data[j + 2:j + 4], "big")
            slen = int.from_bytes(data[j + 4:j + 6], "big")
            if not (1 <= tag <= FIELD_MAX and slen > 0 and 6 + slen <= tlen <= 6 + slen + 512 and j + tlen <= n):
                break
            raw = data[j + 6:j + 6 + slen]
            if sum(b < 9 or 13 < b < 32 for b in raw) > 0:
                break
            fields.append((tag, raw.decode("mac_roman").replace("\r", "\n")))
            j += tlen
        if len(fields) >= 3:
            yield i, fields
            i = j
        else:
            i += 1


def records(path):
    data = open(path, "rb").read()
    out = []
    for off, fields in chains(data):
        rec = {}
        for tag, text in fields:
            if tag in rec:  # a repeated tag starts the next record
                out.append(rec)
                rec = {}
            rec[tag] = text
        out.append(rec)
    return [r for r in out if 4 in r or 2 in r]


if __name__ == "__main__":
    for path in sys.argv[1:]:
        recs = records(path)
        tags = collections.Counter(t for r in recs for t in r)
        print(f"\n{path}: {len(recs)} records (header count {int.from_bytes(open(path, 'rb').read()[6:8], 'big')})")
        for t, c in sorted(tags.items()):
            ex = next(r[t] for r in recs if t in r)
            print(f"  tag {t:3d} x{c:4d}  e.g. {ex[:70]!r}")
        json.dump([{str(k): v for k, v in r.items()} for r in recs], open(path + ".records.json", "w"), ensure_ascii=False)
