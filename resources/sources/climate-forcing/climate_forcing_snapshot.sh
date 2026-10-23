#!/usr/bin/env bash
# Mirror the climate-forcing series the EPRP registers cite: Phanerozoic temperature
# (PhanDA, PhanSST, Scotese et al. 2021, Song et al. 2021), Cenozoic benthic
# isotopes (CENOGRID, LR04), and the event tables (Green, Renne & Keller 2022 LIPs;
# Rothman 2017 carbon-isotope events).
# Usage: climate_forcing_snapshot.sh [ROUTE ...]
#   ROUTE: phanda phansst priors song scotese cenogrid lr04 rothman green (default: all)
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=climate-forcing
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want phanda; then $M github EJJudd/PhanDA "$D/phanda" --latest || echo "phanda FAILED"; fi
if want phansst; then $M github EJJudd/PhanSST "$D/phansst" --latest || echo "phansst FAILED"; fi
# The HadCM3L priors are 11.4 GB at about 0.3 MB/s: index only, fetch on demand.
if want priors; then $M zenodo 8237751 "$D/phanda-hadcm3l-priors" --index-only || echo "priors FAILED"; fi
if want song; then $M zenodo 5027293 "$D/song2021-temperature-thresholds" --latest || echo "song FAILED"; fi
if want scotese; then $M zenodo 8238875 "$D/scotese2021-gmst" --latest || echo "scotese FAILED"; fi
if want cenogrid; then  # a PANGAEA collection: zip of its member datasets (no text format)
  $M url "$D/cenogrid" "Westerhold-etal_2020.zip::https://doi.pangaea.de/10.1594/PANGAEA.917503?format=zip" \
    --license "CC BY 4.0 (PANGAEA dataset metadata)" || echo "cenogrid FAILED"
fi
if want lr04; then
  $M url "$D/lr04" "lisiecki2005.txt::https://www.ncei.noaa.gov/pub/data/paleo/contributions_by_author/lisiecki2005/lisiecki2005.txt" \
    "LR04stack.txt::https://lorraine-lisiecki.com/LR04stack.txt" --pause 2 \
    --license "NOAA NCEI World Data Service for Paleoclimatology (US government, no restriction stated); author's site copy: none stated" \
    || echo "lr04 FAILED"
fi
EPMC="https://www.ebi.ac.uk/europepmc/webservices/rest"
if want rothman; then
  $M url "$D/rothman2017-carbon-events" "PMC5606709_fullText.xml::$EPMC/PMC5606709/fullTextXML" \
    --license "CC BY-NC 4.0 (article licence, Science Advances 3: e1700906)" || echo "rothman FAILED"
fi
if want green; then
  $M url "$D/green2022-lips" "PMC9499591_supplementaryFiles.zip::$EPMC/PMC9499591/supplementaryFiles" \
    "PMC9499591_fullText.xml::$EPMC/PMC9499591/fullTextXML" --pause 2 \
    --license "CC BY-NC-ND 4.0 (article licence, PNAS 119: e2120441119)" || echo "green FAILED"
fi
echo DONE
