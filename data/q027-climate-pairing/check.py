import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_table(path, delimiter="\t"):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter=delimiter))


def write_table(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def declare(root, destination):
    source = root / "scratch/q027-independent-audit/source/subscripts/define-time-ints.R"
    times = root / "data/raw/benson2025/pbdb_time_int.csv"
    target = root / "data/q027-regional-support/summary.json"
    assert sha(source) == "57d45a486d945029c21415ca679b94e3ce0d8b9cc91d2e8b74f62c5d9ba95958"
    assert sha(times) == "023c31855b30247b324a2fb2c2edeb493eef84f898c082c359d647da3c3f9765"
    stages = [r for r in read_table(times, ",") if r["scale_no"] == "1" and r["scale_level"] == "5"]
    ordered = sorted(stages, key=lambda r: (float(r["max_ma"]) + float(r["min_ma"])) / 2)
    names = [r["interval_name"] for r in ordered]
    assert len(names) == len(set(names)) == 100
    text = source.read_text()
    mappings = {}
    for field in ("climate_regime_intervals", "icehouse_and_hothouse_intervals"):
        block = text.split(f"mutate({field} = case_when(", 1)[1].split(")) %>%", 1)[0]
        mapping = {}
        for line in block.splitlines():
            match = re.search(r'get_bins\((.*?)\).*?~ "([^"]+)"', line)
            if not match:
                continue
            args = dict(re.findall(r'(earliest_bin|latest_bin)\s*=\s*"([^"]+)"', match[1]))
            start, end = sorted([names.index(args["earliest_bin"]), names.index(args["latest_bin"])])
            for name in names[start:end + 1]:
                assert name not in mapping
                mapping[name] = match[2]
        mappings[field] = mapping
    rows = []
    for name, base, top, period in json.loads(target.read_text())["stages"]:
        label = mappings["climate_regime_intervals"].get(name, "NA")
        literal = next((s for s in ("Hot", "Cold", "Variable") if s in label), "NA")
        extreme = mappings["icehouse_and_hothouse_intervals"].get(name, "Ignore")
        extreme_class = next((s for s in ("Hothouse", "Icehouse") if s in extreme), "Ignore")
        rows.append(dict(stage=name, period=period, base_ma=base, top_ma=top,
                         literal_regime_label=label, literal_hot_cold=literal,
                         label_implied_sensitivity="Hot" if name in ("Thanetian", "Ypresian") else literal,
                         source_extreme_class=extreme_class))
    assert Counter(r["literal_hot_cold"] for r in rows) == {"Hot": 9, "Cold": 10, "NA": 2}
    scenarios = [("literal_hot_cold", "Hot", "Cold"),
                 ("label_implied_sensitivity", "Hot", "Cold"),
                 ("source_extreme_class", "Hothouse", "Icehouse")]
    pairs = [dict(scenario=field, period=hot["period"], hot_stage=hot["stage"], cold_stage=cold["stage"])
             for field, warm, cool in scenarios for hot in rows for cold in rows
             if hot["period"] == cold["period"] and hot[field] == warm and cold[field] == cool]
    assert Counter(p["scenario"] for p in pairs) == {
        "literal_hot_cold": 45, "label_implied_sensitivity": 55, "source_extreme_class": 3}
    destination.mkdir(parents=True, exist_ok=False)
    write_table(destination / "source-classes.tsv", rows)
    write_table(destination / "candidate-pairs.tsv", pairs)
    plan = dict(primary="literal_hot_cold", secondary=[s[0] for s in scenarios[1:]],
                pair_rule="All opposite-class stage pairs within the same geological period; no cross-period pairs",
                support_rule="At least two shared source regions each with >=1 qualifying tropical and midlatitude cell in both stages",
                bands=["0-20", "20-40"], excluded_regions=["EU", "NAm", "UNKNOWN"],
                primary_subset="dated_public_member", sensitivity_subset="original",
                focal_pair=["Albian", "Campanian"],
                focal_pair_basis="Named before joined evaluation from prior known overlap and verified opposite author classes; not a blind selection",
                failure_scope="Failure is confined to this conservative presence screen, not an upper bound on estimator support",
                pass_scope="A pass permits checking estimator-specific eligibility; it does not establish power, independence or novelty",
                source_sha256={str(p.relative_to(root)): sha(p) for p in (source, times, target)},
                declaration_sha256={p.name: sha(p) for p in destination.glob("*.tsv")})
    (destination / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    return dict(classes=len(rows), candidate_pairs=len(pairs), plan_sha256=sha(destination / "plan.json"))


def evaluate(root, declaration, destination):
    plan = json.loads((declaration / "plan.json").read_text())
    for name, expected in plan["declaration_sha256"].items():
        assert sha(declaration / name) == expected
    path = root / "data/q027-regional-support/region-band-overlap.tsv"
    assert sha(path) == "fd4af48211df496480bd03c068d1c8c3c2782a079d68e418cc316e6672f91cec"
    overlaps = read_table(path)
    keys = [(r["subset"], r["stage"], r["region"]) for r in overlaps]
    assert len(keys) == len(set(keys)) == 546
    regions = {}
    for row in overlaps:
        key = (row["subset"], row["stage"])
        regions.setdefault(key, set())
        paired = set(plan["bands"]).issubset(row["bands_with_eligible_cells"].split(","))
        assert paired == bool(int(row["tropical_mid_overlap"]))
        if paired and row["region"] not in plan["excluded_regions"]:
            regions[key].add(row["region"])
    rows = []
    for pair in read_table(declaration / "candidate-pairs.tsv"):
        for subset in ("dated_public_member", "original"):
            hot = regions[subset, pair["hot_stage"]]
            cold = regions[subset, pair["cold_stage"]]
            shared = hot & cold
            rows.append(dict(**pair, subset=subset, hot_regions=",".join(sorted(hot)),
                             cold_regions=",".join(sorted(cold)), shared_regions=",".join(sorted(shared)),
                             n_shared_regions=len(shared), passes=int(len(shared) >= 2)))
    destination.mkdir(parents=True, exist_ok=False)
    write_table(destination / "pair-results.tsv", rows)
    stage_rows = [dict(subset=k[0], stage=k[1], paired_band_regions=",".join(sorted(v)), n_regions=len(v))
                  for k, v in sorted(regions.items())]
    write_table(destination / "stage-regions.tsv", stage_rows)
    summary = dict(plan_sha256=sha(declaration / "plan.json"), script_sha256=sha(Path(__file__)),
                   overlap_sha256=sha(path), rows=len(rows),
                   pass_counts={f"{scenario}:{subset}": sum(r["passes"] for r in rows if r["scenario"] == scenario and r["subset"] == subset)
                                for scenario in [plan["primary"], *plan["secondary"]]
                                for subset in ("dated_public_member", "original")},
                   passing_primary_pairs=[r for r in rows if r["scenario"] == plan["primary"] and r["subset"] == plan["primary_subset"] and r["passes"]],
                   output_sha256={p.name: sha(p) for p in destination.glob("*.tsv")})
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["declare", "evaluate"])
    parser.add_argument("root", type=Path)
    parser.add_argument("declaration", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = declare(args.root, args.declaration) if args.mode == "declare" else evaluate(args.root, args.declaration, args.output)
    print(json.dumps(result, indent=2))
