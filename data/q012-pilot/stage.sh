#!/usr/bin/env bash
# Stage the pilot payload to kunanyi and submit the build and the technical replay (R00).
# Run only while Barry has the TPAC jumpbox window open. Uses nectar's password-fed transport.
#   KUNANYI_SSH_ALIAS=kunanyi data/q012-pilot/stage.sh [TAG]      # campus or eduroam; REMOTE_BASE overrides /u/bwbrook/codex_kunanyi
#   KUNANYI_SSH_ALIAS=kunanyi-via-nectar data/q012-pilot/stage.sh  # via a running Nectar bastion
# The 12-fit panel is not submitted here; it waits for Codex's review of the replay.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NECTAR="${NECTAR_ROOT:-$HOME/work/nectar}"
# shellcheck source=/dev/null
. "$NECTAR/scripts/lib/common.sh"
# shellcheck source=/dev/null
. "$NECTAR/scripts/lib/kunanyi.sh"
export KUNANYI_SSH_ALIAS="${KUNANYI_SSH_ALIAS:-kunanyi}"
tpac_transport_setup
# kunanyi's SFTP server fails on close when writing /scratch (16 Oct 2026: 0-byte file, "close remote: Failure"),
# while shell writes succeed; use scp's legacy protocol (-O) through a copy of nectar's expect script.
LEGACY_EXP="$HERE/../../scratch/q012-pilot/tpac-expect-legacy-scp.exp"
sed 's/spawn scp \\$/spawn scp -O \\/' "$TPAC_EXPECT_SCRIPT" > "$LEGACY_EXP"
grep -q "spawn scp -O" "$LEGACY_EXP" || die "could not prepare the legacy-scp expect script"
export TPAC_EXPECT_SCRIPT="$LEGACY_EXP"

TAG="${1:-$(date +%Y%m%dT%H%M%S)}"
REMOTE="${REMOTE_BASE:-/u/bwbrook/codex_kunanyi}/q012-pilot-$TAG"
CACHE="$HERE/../../scratch/q012-pilot"
TARBALL="$CACHE/cmdstan-2.38.0.tar.gz"
PAYLOAD="$CACHE/payload-$TAG.tar.gz"

( cd "$HERE/payload" && sha256sum -c --strict --quiet manifest.sha256 )
( cd "$CACHE" && sha256sum -c --strict --quiet "$HERE/payload/cmdstan.sha256" )
tar czf "$PAYLOAD" -C "$HERE/payload" --exclude=runs --exclude=build .
PAYLOAD_SHA="$(sha256sum "$PAYLOAD" | cut -d' ' -f1)"
echo "payload $PAYLOAD_SHA; remote $REMOTE"

tpac_set_expect_timeout 60
tpac_expect_ssh "mkdir -p $(tpac_quote "$REMOTE") && chmod 700 $(tpac_quote "$REMOTE")"
tpac_set_expect_timeout 1200
tpac_expect_scp "$PAYLOAD" "$KUNANYI_SSH_ALIAS:$REMOTE/payload.tar.gz"
tpac_expect_scp "$TARBALL" "$KUNANYI_SSH_ALIAS:$REMOTE/cmdstan-2.38.0.tar.gz"
tpac_set_expect_timeout 120
tpac_expect_ssh "set -e; cd $(tpac_quote "$REMOTE"); \
  echo '$PAYLOAD_SHA  payload.tar.gz' | sha256sum -c --strict; tar xzf payload.tar.gz; \
  sha256sum -c --strict --quiet manifest.sha256; sha256sum -c --strict cmdstan.sha256; \
  B=\$(/opt/pbs/bin/qsub pbs/build.pbs); F=\$(/opt/pbs/bin/qsub -v SCEN=R00 -W depend=afterok:\$B pbs/fit.pbs); \
  echo BUILD_JOB=\$B FIT_JOB=\$F | tee submitted.txt; \
  /opt/pbs/bin/qstat -f \$F | grep -E 'Job_Name|Mail_Users|Mail_Points|depend|Resource_List|queue|Variable_List' | cut -c1-200"
echo "Staged $REMOTE. Barry receives PBS mail when the replay ends or either job aborts."
