#!/usr/bin/env bash
# Mirror the two classic range compendia: Benton's The Fossil Record 2 (families)
# and Sepkoski's genus compendium, each from every independent copy found.
#   fr2/bristol            Bristol's 2019 re-posting (45 chapter workbooks, the
#                          zip, summaries) plus the WordPress page and media listings
#   fr2/wayback            the original 1997-2006 Bristol files, from the Wayback
#                          Machine, one capture per distinct payload (wayback_captures.tsv)
#   sepkoski/peters        Peters' online port, every phylum and class page
#   sepkoski/r-package-*   the palaeoverse R package (GitHub head; CRAN release)
#   sepkoski/bhl-scan      BHL's scan of the printed compendium, via the Internet Archive
# Usage: classic_compendia_snapshot.sh WAYBACK_CAPTURES_TSV [ROUTE ...]
# ROUTE is any of bristol wayback peters github cran bhl (default: all).
set -euo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=classic-compendia
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
ROUTES=" ${*:2} "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

BR="https://palaeoresources.blogs.bristol.ac.uk"
if want bristol; then
{
  echo "wp_pages.json::$BR/wp-json/wp/v2/pages?per_page=100"
  echo "wp_media.json::$BR/wp-json/wp/v2/media?per_page=100"
  for f in 1-Monera 2-Fungi 3-Algae 4-Protozoa 5-Porifera 6-Coelenterata 7-Mollusca-1 8-Mollusca-2 \
    9-Mollusca-3 10-Mollusca-4 11-Mollusca-5 12-Mollusca-6 13-Mollusca-7 14-Mollusca-8 15-Annelida \
    16-Trilobita 17-Aglaspidida 18-Crustacea 19-Ostracoda 20-Myriapoda 21-Hexapoda 22-Brachiopoda \
    23-Phoronida 24-Bryozoa 25-Echinodermata 26-Deuterostomes 27-Graptolithina 28-Problematica \
    29-Miscellania 30-Conodonta 31-Agnatha 32-Placodermi 33-Acanthodii 34-Chondrichthyes \
    35-Osteichthyes 36-Teleostei 37-Sarcopterygii 38-Amphibia 39-Reptilia 40-Aves 41-Mammalia \
    42-Bryophyta 43-Pteridophyta 44-Gymnospermophyta 45-Magnoliophyta \
    All-Life All-data Diversitydata95 Birds; do
    echo "$f.xlsx::$BR/files/2019/08/$f.xlsx"
  done
  echo "FR2.zip::$BR/files/2019/08/FR2.zip"
} > "$T/bristol"
$M url "$D/fr2/bristol" --specs-file "$T/bristol" --pause 1 \
  --license "none stated; University of Bristol pages (palaeoresources.blogs.bristol.ac.uk); cite Benton (ed.) 1993 The Fossil Record 2 and Benton 1995 Science 268:52-58"
fi

if want wayback; then
tail -n +2 "$1" | awk -F'\t' '{print $5 "::https://web.archive.org/web/" $1 "id_/" $6}' > "$T/wayback"
$M url "$D/fr2/wayback" --specs-file "$T/wayback" --pause 2 \
  --license "none stated; Internet Archive Wayback Machine captures of palaeo.gly.bris.ac.uk/frwhole (University of Bristol, 1997-2006)"
fi

SP="https://strata.geology.wisc.edu/jack"
if want peters; then
curl -sSf -m 120 "$SP/start.php" -o "$T/start.html"
{
  echo "index.html::$SP/"
  echo "start.html::$SP/start.php"
  echo "explain.html::$SP/explain.html"
  grep -oE "showgenera\.php\?taxon=[0-9]+&rank=(phylum|class)" "$T/start.html" | sort -u |
    sed -E "s#^showgenera\.php\?taxon=([0-9]+)&rank=([a-z]+)\$#\2_\1.html::$SP/&#"
} > "$T/peters"
$M url "$D/sepkoski/peters" --specs-file "$T/peters" --pause 2 \
  --license "site terms: 'You are welcome to use these data with proper citation of Sepkoski's work. It would also be appropriate to acknowledge this online database and its creator/maintainer.' (S. E. Peters, University of Wisconsin-Madison)"
fi

# url takes its URLs before the options: argparse does not collect positionals given after them.
if want github; then $M github palaeoverse/sepkoski "$D/sepkoski/r-package-github" --latest; fi
if want cran; then
$M url "$D/sepkoski/r-package-cran" "https://cran.r-project.org/src/contrib/sepkoski_0.0.1.tar.gz" \
  --license "GPL (>= 3) (CRAN)"
fi

IA="https://archive.org/download/bulletinsofameri363pale"
if want bhl; then
$M url "$D/sepkoski/bhl-scan" \
  "ia_metadata.json::https://archive.org/metadata/bulletinsofameri363pale" \
  "$IA/bulletinsofameri363pale.pdf" "$IA/bulletinsofameri363pale_djvu.txt" \
  "$IA/bulletinsofameri363pale_meta.xml" "$IA/bulletinsofameri363pale_dc.xml" \
  "$IA/bulletinsofameri363pale_marc.xml" --pause 2 \
  --license "In copyright. Digitized with the permission of the Paleontological Research Institution (BHL; https://www.biodiversitylibrary.org/permissions/)"
fi
echo DONE
