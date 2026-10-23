"""Write data_mirror.py url specs that test whether GBIF's PRESERVED_SPECIMEN basis hides Australian fossils.

Usage: python3 gbif_basis_specs.py OUT_SPECS

Counts of Australian PRESERVED_SPECIMEN records carrying each geological
period (with dataset and class facets for the Quaternary), mammals among the
Quaternary ones, and the FOSSIL_SPECIMEN mammal count that confirms the
Mammalia class key (359). Standard library only.
"""

import sys

G = "https://api.gbif.org/v1/occurrence/search?country=AU&limit=0"
PERIODS = ["Quaternary", "Neogene", "Paleogene", "Cretaceous", "Jurassic", "Triassic", "Permian",
           "Carboniferous", "Devonian", "Silurian", "Ordovician", "Cambrian"]
specs = [f"preserved__{p}.json::{G}&basisOfRecord=PRESERVED_SPECIMEN&geologicalTime={p}" for p in PERIODS]
specs[0] += "&facet=datasetKey&facet=classKey&facetLimit=20"
specs += [f"preserved__Quaternary__Mammalia.json::{G}&basisOfRecord=PRESERVED_SPECIMEN&geologicalTime=Quaternary&classKey=359",
          f"fossil__Mammalia.json::{G}&basisOfRecord=FOSSIL_SPECIMEN&classKey=359"]
with open(sys.argv[1], "w") as f:
    f.write("\n".join(specs) + "\n")
