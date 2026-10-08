"""Tiny translation of SNCI-v2's connectivity operations; no upstream model run.

Uses column-major component ordering and eight-neighbour connectivity. This is
an explicit Python diagnostic, not a MATLAB numerical reproduction.
Run: python3 data/model-contract-audit/connectivity_probe.py
"""

import csv
from collections import deque
from pathlib import Path


def labels(grid, longitude_periodic=False):
    rows, cols = len(grid), len(grid[0])
    result = [[0] * cols for _ in range(rows)]
    count = 0
    for col in range(cols):
        for row in range(rows):
            if not grid[row][col] or result[row][col]:
                continue
            count += 1
            result[row][col] = count
            queue = deque([(row, col)])
            while queue:
                r, c = queue.popleft()
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        rr, cc = r + dr, c + dc
                        if longitude_periodic:
                            rr %= rows
                        if (0 <= rr < rows and 0 <= cc < cols and grid[rr][cc]
                                and not result[rr][cc]):
                            result[rr][cc] = count
                            queue.append((rr, cc))
    return result, count


def deposited_operations(grid):
    padded = [[row[-1], *row, row[0]] for row in grid]
    labelled, _ = labels(padded)
    cropped = [row[1:-1] for row in labelled]
    for row in range(len(cropped)):
        first, last = cropped[row][0], cropped[row][-1]
        if first and last and first != last:
            cropped = [[first if value == last else value for value in values]
                       for values in cropped]
    positive = {value for row in cropped for value in row if value}
    return max(positive, default=0), len(positive)


def main():
    cases = [
        ("longitude_seam_pair", 5, 7, ((0, 3), (4, 3)), (2, 2, 1)),
        ("latitude_endpoints_plus_island", 7, 7, ((1, 0), (1, 6), (5, 3)), (2, 2, 3)),
        ("one_latitude_edge_plus_island", 7, 7, ((1, 6), (5, 3)), (3, 2, 2)),
    ]
    records = []
    for name, rows, cols, occupied, expected in cases:
        grid = [[False] * cols for _ in range(rows)]
        for row, col in occupied:
            grid[row][col] = True
        reported, surviving = deposited_operations(grid)
        _, reference = labels(grid, longitude_periodic=True)
        assert (reported, surviving, reference) == expected
        records.append({"case": name, "reported_max_label": reported,
                        "surviving_components": surviving,
                        "longitude_periodic_reference": reference})
    with Path(__file__).with_name("connectivity_results.tsv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=records[0], delimiter="\t")
        writer.writeheader()
        writer.writerows(records)
    for record in records:
        print(record)


if __name__ == "__main__":
    main()
