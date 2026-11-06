#!/usr/bin/env python3
"""Extract unreviewed candidates or write reviewed private agenda units."""

import argparse
import csv
import io
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter

import elsevier as e
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


CELL_THEMES = [
    ("Arendt", "cell-type diversification", "heading_supported"),
    ("King", "origins, complexity and evolvability", "provisional_lexical"),
    ("Carroll", "genetic variation, phenotypic change and adaptation", "provisional_lexical"),
    ("Wittkopp", "developmental bias", "public_institutional_corroboration"),
    ("Koonin", "evolvability, adaptation and prediction", "provisional_lexical"),
    ("Kruglyak", "evolutionary prediction", "heading_supported_scope_provisional"),
]
LOPEZ_THEMES = [
    "ancestral eukaryotic complexity", "mitochondrial ancestry and metabolism",
    "host ancestry", "host cellular capabilities", "metabolic partnerships",
    "mitochondrial acquisition timing", "nuclear origins and selective drivers",
    "membrane transformation",
]
CURATION_NOTE = "literature/2026-11-06-three-agendas-curation.md"
REVIEWED_XML_SHA256 = {
    "10.1016/j.cell.2016.07.021": "83c410f0f8e7cd0479a04d3e629df6edb1476638867b92f0933daaca12fa2fde",
    "10.1016/j.tree.2015.09.005": "fc6f6db1e910f5c787f9362cabe2d10c2b586f2c17cf53600eee78b9513de9bf",
    "10.1016/j.jafrearsci.2023.105155": "4233425b38e15236e4bd2af7dc479fc8de932ac8634eda6a98a7e285a80d6e7c",
}


def require(condition):
    if not condition:
        raise ValueError("unexpected_agenda_structure")


def nodes(root, name):
    return [n for n in root.iter() if e.local_name(n) == name]


def identified(root, name, identifier):
    found = [n for n in nodes(root, name) if n.get("id") == identifier]
    require(len(found) == 1)
    return found[0]


def paragraph_locator(section, paragraph):
    identifier = paragraph.get("id")
    require(bool(identifier))
    require(len([p for p in nodes(section, "para") if p.get("id") == identifier]) == 1)
    return {"section_id": section.get("id"), "paragraph_id": identifier}


def cell_units(body):
    container = identified(body, "section", "sec1")
    children = [n for n in container if e.local_name(n) == "section"]
    require([n.get("id") for n in children] == [f"sec1.{i}" for i in range(1, 7)])
    require(len(nodes(body, "section")) == 7 and not nodes(body, "textbox"))
    require(len(nodes(body, "para")) == 12)
    units = []
    for i, (section, (contributor, theme, confidence), questions) in enumerate(
            zip(children, CELL_THEMES, [3, 1, 3, 2, 2, 4]), 1):
        require([e.local_name(n) for n in section] == ["section-title", "para", "para"])
        byline, paragraph = [n for n in section if e.local_name(n) == "para"]
        byline_text, text = "".join(byline.itertext()), "".join(paragraph.itertext())
        require(bool(re.search(r"\b" + contributor + r"\b", byline_text)))
        require(byline_text.count("?") == 0 and text.count("?") == questions)
        units.append({"id": f"cell-2016-perspective-{i:02d}", "type": "contributor_perspective",
                      "contributor": contributor, "theme": theme, "evidence_confidence": confidence,
                      "source_locator": paragraph_locator(section, paragraph),
                      "byline_locator": paragraph_locator(section, byline),
                      "original_byline": byline_text, "original_paragraph": text,
                      "interrogatives": questions})
    return units, "invited_perspectives", False


def lopez_units(body):
    require(len(nodes(body, "textbox")) == 1)
    box = identified(body, "textbox", "tb0005")
    bodies = [n for n in box if e.local_name(n) == "textbox-body"]
    require(len(bodies) == 1)
    sections = [n for n in bodies[0] if e.local_name(n) == "sections"]
    require(len(sections) == 1)
    paragraphs = list(sections[0])
    require(len(paragraphs) == 8 and all(e.local_name(n) == "para" for n in paragraphs))
    require([n.get("id") for n in paragraphs] == [f"par{i:04d}" for i in range(95, 135, 5)])
    require(["".join(n.itertext()).count("?") for n in paragraphs] == [2, 3, 4, 2, 1, 3, 3, 1])
    require(len(nodes(box, "para")) == 8 and "".join(box.itertext()).count("?") == 19)
    require(len(LOPEZ_THEMES) == 8)
    units = [{"id": f"lopez-moreira-2015-box-item-{i:02d}", "type": "formal_question_group",
              "theme": theme, "evidence_confidence": "public_author_manuscript_inspected",
              "source_locator": {"textbox_id": "tb0005", "paragraph_id": paragraph.get("id")},
              "external_locator": {"url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4640172/",
                                   "version": "public_author_manuscript_available_2015-11-10",
                                   "heading": "Outstanding questions", "item_ordinal": i},
              "xml_item_boundaries": "one_paragraph_per_group_verified",
              "original_paragraph": "".join(paragraph.itertext()),
              "interrogatives": "".join(paragraph.itertext()).count("?")}
             for i, (theme, paragraph) in enumerate(zip(LOPEZ_THEMES, paragraphs), 1)]
    return units, "formal_grouped_question_box", True


def abdelhady_units(body):
    require(not nodes(body, "textbox"))
    blocks = []
    for section in nodes(body, "section"):
        for paragraph in section:
            if e.local_name(paragraph) == "para" and "?" in "".join(paragraph.itertext()):
                blocks.append((section, paragraph))
    require(len(blocks) == 2 and [s.get("id") for s, _ in blocks] == ["sec1", "sec4.5"])
    units = []
    for i, ((section, paragraph), theme) in enumerate(zip(blocks, [
            "illustrative origins and innovation motivations", "technology prospects and limitations"]), 1):
        text = "".join(paragraph.itertext())
        require(text.count("?") == 3)
        units.append({"id": f"abdelhady-2024-prompt-block-{i:02d}", "type": "contextual_prompt_block",
                      "theme": theme, "evidence_confidence": "structural_context_supported",
                      "source_locator": paragraph_locator(section, paragraph),
                      "original_paragraph": text, "interrogatives": 3})
    return units, "technology_review_context", False


def curate(store):
    private = {"format": 1, "curation_note": CURATION_NOTE, "sources": {}}
    summary = {"format": 1, "mode": "curated_units", "sources": {}}
    builders = {"10.1016/j.cell.2016.07.021": cell_units,
                "10.1016/j.tree.2015.09.005": lopez_units,
                "10.1016/j.jafrearsci.2023.105155": abdelhady_units}
    with locked(store) as root:
        manifests = list(latest(root / "manifest.tsv").values())
        for doi, builder in builders.items():
            matches = [r for r in manifests if r["doi"] == doi]
            require(len(matches) == 1)
            row = matches[0]
            held(root, row)
            data = (root / row["xml_path"]).read_bytes()
            require(e.sha(data) == row["xml_sha256"])
            require(row["xml_sha256"] == REVIEWED_XML_SHA256[doi])
            e.parse_article(data, doi)
            document = ET.fromstring(data)
            bodies = nodes(document, "body")
            require(len(bodies) == 1)
            units, kind, formal = builder(bodies[0])
            private["sources"][doi] = {"openalex_id": row["openalex_id"],
                "xml_path": row["xml_path"], "xml_sha256": row["xml_sha256"],
                "text_sha256": row["text_sha256"], "agenda_type": kind,
                "formal_agenda": formal, "units": units}
            summary["sources"][doi] = {"agenda_type": kind, "formal_agenda": formal,
                "units": len(units), "unit_types": dict(Counter(u["type"] for u in units)),
                "confidence_counts": dict(Counter(u["evidence_confidence"] for u in units))}
        require([len(s["units"]) for s in private["sources"].values()] == [6, 8, 2])
        atomic(root / "derived" / "agenda-curated-units.json", (json.dumps(private, indent=2) + "\n").encode())
        atomic(root / "derived" / "agenda-curated-summary.json", (json.dumps(summary, indent=2) + "\n").encode())
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True)
    parser.add_argument("--curate", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(curate(args.store) if args.curate else mine(args.store), sort_keys=True))
    except Exception:
        print(json.dumps({"error": "agenda_mining_failed"}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
