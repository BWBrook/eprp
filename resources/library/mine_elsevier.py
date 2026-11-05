#!/usr/bin/env python3
"""Classify unreviewed agenda-question candidates inside the restricted store."""

import argparse
import csv
import io
import json
import re
from collections import Counter

from elsevier import atomic, held, latest, locked


AGENDAS = {
    "10.1016/j.cell.2016.07.021",
    "10.1016/j.tree.2015.09.005",
    "10.1016/j.jafrearsci.2023.105155",
}
THEMES = {
    "imaging-and-morphology": r"imag|tomograph|morpholog|microscop|scan|anatom",
    "molecular-and-cellular": r"molecul|genom|genetic|dna|rna|protein|eukary|mitochond|cell|symbio",
    "diversification-and-origins": r"evol|origin|speciat|diversif|extinct|radiat|adapt|ancestor",
    "ecology-and-interactions": r"ecolog|interact|predat|ecosystem|food|compet|recover|biodivers",
    "environment-and-preservation": r"climat|environment|geochem|isotop|taphonom|preserv|sedimen|temperat",
    "computing-and-data": r"comput|digital|algorithm|machine learn|artificial intellig|databas|model|simulat",
    "chronology-and-sampling": r"chronolog|dating|resolution|sampl|stratigraph|bias|fossil record",
    "taxonomy-and-phylogeny": r"taxonom|phylogen|systematic|classif|species|clad",
}


def classify(text):
    return [name for name, pattern in THEMES.items() if re.search(pattern, text, re.I)] or ["unclassified"]


def mine(store):
    summary = {"method": "literal question-mark candidates with deterministic keyword themes",
               "review_status": "unreviewed; rhetorical questions and missed headings possible",
               "sources": {}}
    output = io.StringIO()
    fields = ["doi", "candidate", "start_character", "themes", "question_text", "text_sha256", "review_status"]
    writer = csv.DictWriter(output, fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    with locked(store) as root:
        rows = latest(root / "manifest.tsv").values()
        for doi in sorted(AGENDAS):
            row = next((r for r in rows if r["doi"] == doi), None)
            if row is None:
                summary["sources"][doi] = {"status": "not_held"}
                continue
            held(root, row)
            text = (root / row["text_path"]).read_text(encoding="utf-8")
            themes, count = Counter(), 0
            for match in re.finditer(r"[^.!?\n]+\?", text):
                question = " ".join(match.group().split())
                if len(question) < 12:
                    continue
                count += 1
                labels = classify(question)
                themes.update(labels)
                writer.writerow(dict(doi=doi, candidate=count, start_character=match.start(),
                                     themes=";".join(labels), question_text=question,
                                     text_sha256=row["text_sha256"], review_status="unreviewed_machine_candidate"))
            summary["sources"][doi] = {"status": "held", "candidate_count": count,
                                       "theme_memberships": dict(themes), "text_sha256": row["text_sha256"]}
        atomic(root / "derived" / "agenda-question-candidates.tsv", output.getvalue().encode())
        atomic(root / "derived" / "agenda-summary.json", (json.dumps(summary, indent=2) + "\n").encode())
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(mine(args.store), sort_keys=True))
    except Exception:
        print(json.dumps({"error": "agenda_mining_failed"}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
