#!/usr/bin/env bash
# Fetch one pilot run's receipts, logs, chain output and PBS accounting after Barry's wake-up.
# Run only while Barry has the TPAC jumpbox window open.
#   KUNANYI_SSH_ALIAS=kunanyi data/q012-pilot/fetch.sh TAG SCEN
# Files land in scratch/q012-pilot/fetch-TAG/; screen with: pilot.py diagnose <attempt dir> SCEN
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

TAG="${1:?TAG}"
SCEN="${2:?SCEN}"
REMOTE="${REMOTE_BASE:-/u/bwbrook/codex_kunanyi}/q012-pilot-$TAG"
DEST="$HERE/../../scratch/q012-pilot/fetch-$TAG"
mkdir -p "$DEST"
tpac_set_expect_timeout 300
tpac_expect_ssh "cd $(tpac_quote "$REMOTE") && bash pbs/pack.sh $(tpac_quote "$SCEN")"
tpac_set_expect_timeout 1800
tpac_expect_scp "$KUNANYI_SSH_ALIAS:$REMOTE/fetch-$SCEN.tar.gz" "$DEST/"
tar xzf "$DEST/fetch-$SCEN.tar.gz" -C "$DEST"
sha256sum "$DEST/fetch-$SCEN.tar.gz"
echo "Fetched into $DEST"
