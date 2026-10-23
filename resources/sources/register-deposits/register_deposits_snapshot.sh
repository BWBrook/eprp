#!/usr/bin/env bash
# Mirror the Dryad deposits cited by the EPRP question registers (latest version each),
# with the Dryad API account on the host (credentials outside the repository).
set -uo pipefail
cd /data/paleodata
while read -r code slug; do
  echo "== $code $slug"
  python3 _tools/data_mirror.py dryad "10.5061/dryad.$code" "register-deposits/$slug" --latest || echo "$code FAILED"
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
echo DONE
