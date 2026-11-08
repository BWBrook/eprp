"""Record public-safe revision and content hashes without filesystem/host details."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

repo, out = map(pathlib.Path, sys.argv[1:])
prefix = pathlib.Path("papers/infrastructure-audit/evidence/replay-20261108/software")
files = [prefix / n for n in ("replay_packages.R", "replay_plate.py", "run.sh", "receipt.py")]
files += [pathlib.Path("resources/software/bench") / p for p in (
    "validate/t2_checks.R", "validate/t2_strat.R", "validate/t2_extinction.R", "validate/t3_checks.py",
    "validate/t3_checks.R", "validate/t3_palaeoverse.R", "validate/t3_rotate.py", "env/Dockerfile.r3", "env/Dockerfile.py3")]
hashes = {str(p): hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in files}
result = dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source_revision=subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"],text=True).strip(),
    source_files_sha256=hashes,
    images=dict(R="sha256:44432c896c3622e92c68f11716d639745b0fa2b4d6c47124538461389f6daab6",
                Python="sha256:8c333ab2e7a7d6f54f42730c047227acd4c70688c702ca288a873c88ad975bac"),
    evidence_type="Fresh direct-package and raw-model runs against independently coded mathematical/control routes",
    notes="New replay scripts were uncommitted at execution; their exact bytes are pinned by the hashes above. No host identity or absolute infrastructure path is required to interpret these results. R fixed synthetic inputs are embedded in the hashed script and repeated in the result files.")
(out/"provenance.json").write_text(json.dumps(result,indent=2)+"\n")
