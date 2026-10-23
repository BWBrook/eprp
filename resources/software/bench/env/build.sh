#!/usr/bin/env bash
# Build the tranche-1 images on deep-server. Logs and image ids go to ../logs.
set -u
cd "$(dirname "$0")"
mkdir -p ../logs
for name in r pyrate revbayes; do
  echo "== $name $(date -u +%FT%TZ)"
  if docker build -t "eprp-sw/bench-$name:t1" -f "Dockerfile.$name" . > "../logs/build-$name.log" 2>&1; then
    echo "built $name $(docker image inspect --format '{{.Id}}' "eprp-sw/bench-$name:t1")" | tee -a ../logs/image-ids.txt
  else
    echo "FAILED $name"
  fi
done
echo "== done $(date -u +%FT%TZ)"
