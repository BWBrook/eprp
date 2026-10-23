#!/usr/bin/env bash
# Mirror the deposits cited by the EPRP question registers, ideation notes,
# literature notes and data READMEs (latest version each).
# Usage: register_deposits_snapshot.sh [dryad] [zenodo] [figshare] [pangaea] [index] (default: all)
#   dryad     Dryad deposits, with the Dryad API account on the host (credentials outside the repository)
#   zenodo    Zenodo records up to 5 GB, four at a time (Zenodo serves about 0.3 MB/s per connection)
#   figshare  Figshare articles
#   pangaea   PANGAEA datasets as tab-delimited text (the IODP U1313 series of the Q-050 crosswalk)
#   index     version indexes only, for the Zenodo records over 5 GB (fetch on demand)
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want dryad; then
while read -r code slug; do
  echo "== dryad $code $slug"
  $M dryad "10.5061/dryad.$code" "register-deposits/$slug" --latest || echo "$code FAILED"
done <<'EOF'
931zcrjqw monarrez2023-selectivity
c17p8 walton2018-ammonoid-ontogeny
3v0p84v close2019-tetrapod-local-richness
8jf2k brombacher2017-foram-allometry
m010p hunt2015-trait-stasis
gd8038s cantalapiedra2019-phylogenetic-diversity
sqv9s4ndb slattery2025-nuculid-stasis
6djh9w1bx benson2025-marine-latitudinal-diversity
nk218ht franeck2018-ordovician-radiation
5dv41nsmd stigall2026-ordovician-species
1vhhmgr44 leventhal2025-bryozoan-brooding
zpc866t6s liow2021-cheilostome-cyclostome
tx95x69vr hunt2020-ostracod-dimorphism
vx0k6dk71 crampton2026-extinction-spectrum
1ns1rn91g malanoski2024-climate-extinction-risk
EOF
fi

if want zenodo; then
mkdir -p /data/codex/scratch/eprp-paleodata/register-deposits/logs
cat <<'EOF' | xargs -P 4 -L 1 bash -c 'echo "== zenodo $0 $1"; python3 _tools/data_mirror.py zenodo "$0" "register-deposits/$1" --latest > "/data/codex/scratch/eprp-paleodata/register-deposits/logs/$1.log" 2>&1 && echo "done $1" || echo "$0 $1 FAILED"'
10014585 cooke2023-extinct-birds
10149114 foster2023-siliceous-permian-triassic
10403766 penn2023-mi-traits-obis
13294509 tsuboi2024-paradox-of-predictability
14903138 gavirneni2025-bivalve-metabolic-rate
11400588 beckerman2024-toarcian-secondary-extinction
11522106 alaswad2024-end-permian-homogenization
1211555 kocsis2018-biogeographic-imprint
12187757 rogger2024-lip-climate-sensitivity
12735901 tang2024-proterozoic-eukaryotes
1285673 padfield2016-metabolic-traits
14918283 leventhal2025-bryozoan-brooding-code
15079899 wang2025-trace-fossil-trajectories
15096088 natscher2025-ectotherm-body-size
15269137 close2025-marine-latitudinal-diversity-code
18512912 minsky2026-snowball-limit-cycle
18700674 rui2026-cgenie-kpg
21414007 lamyman2026-pforam-phylogeny
18926572 rogger2026-treed-vegetation-model
19824423 cribb2026-ecosystem-engineers
3701302 ward2020-mcm-model
3770348 carrillo2020-south-american-mammals
5519730 stockey2021-cgenie-metabolic-index
21933976 seebens2026-sinas
5899743 penn2022-metabolic-index-extinction
6535496 garciacomas2022-inditek
7242861 swain2022-palaeoherbivory-review
7816408 monarrez2023-selectivity-code
8154672 smith2023-biodeeptime
8341743 monarrez2023-selectivity-zenodo
8398420 cribb2023-ete-ecospace
EOF
fi

if want index; then
while read -r rec slug; do
  echo "== zenodo index-only $rec $slug"
  $M zenodo "$rec" "register-deposits/$slug" --index-only || echo "$rec FAILED"
done <<'EOF'
11001479 rahman2024-ediacaran-animal-forests
17035672 rahman2025-ediacaran-hydrodynamics
17252973 rogger2025-petm-vegetation
EOF
fi

if want figshare; then
while read -r art slug; do
  echo "== figshare $art $slug"
  $M figshare "article/$art" "register-deposits/$slug" --latest || echo "$art FAILED"
done <<'EOF'
26103031 qvarnstrom2024-supplementary-figures
27201498 balembois2025-marine-biodiversity-drivers
27909116 craffey2024-ediacaran-cooccurrence-figshare
5046964 klompmaker2017-external-database-2
7357193 penn2018-end-permian-climate
EOF
fi

if want pangaea; then
P="https://doi.pangaea.de/10.1594/PANGAEA"
$M url register-deposits/pangaea-u1313 \
  "PANGAEA.736778.tab::$P.736778?format=textfile" "PANGAEA.761442.tab::$P.761442?format=textfile" \
  "PANGAEA.761443.tab::$P.761443?format=textfile" "PANGAEA.892803.tab::$P.892803?format=textfile" \
  "PANGAEA.892804.tab::$P.892804?format=textfile" --pause 2 \
  --license "CC BY 3.0 (PANGAEA dataset metadata, all five)" || echo "pangaea FAILED"
fi
echo DONE
