#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
base_id=sha256:d0c1c51a6c65e5811654e60a54ab84aa25b65218064a8366c42f009f821db39b
test "$(docker image inspect eprp-sw/bench-r4:t4 --format '{{.Id}}')" = "$base_id"
mkdir -p source
if ! test -f source/sp_2.2-4.tar.gz; then
    curl -fL --max-time 120 https://cran.r-project.org/src/contrib/sp_2.2-4.tar.gz -o source/sp_2.2-4.tar.gz
fi
if ! test -f source/dggridR_3.0.0.tar.gz; then
    curl -fL --max-time 120 https://cran.r-project.org/src/contrib/Archive/dggridR/dggridR_3.0.0.tar.gz -o source/dggridR_3.0.0.tar.gz
fi
sha256sum -c sources.sha256
DOCKER_BUILDKIT=0 docker build --pull=false --network=none --cpu-period=100000 --cpu-quota=200000 --memory=7g -t eprp-q027-eligibility:20261029 .
test "$(docker image inspect eprp-sw/bench-r4:t4 --format '{{.Id}}')" = "$base_id"
docker image inspect eprp-q027-eligibility:20261029 > image-inspect.json
docker run --rm --network=none --read-only --tmpfs /tmp:rw,size=256m --cpus=2 --memory=7g \
    -v "$PWD:/environment" -w /environment --entrypoint Rscript \
    eprp-q027-eligibility:20261029 controls.R > controls.log 2>&1
