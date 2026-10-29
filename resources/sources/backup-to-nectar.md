# Retained private paleodata backup on Nectar

Barry authorised the settled VM `/data` volume for this backup on 28 October
2026: “Yes, the VM's /data volume is settled then. Let's go with your
recommendation: proceed at your discretion (now or later; I assume we can have
a sync script at some point?).” This procedure implements a private second
copy of `deep:/data/paleodata`, retaining independent dated generations.
It does not publish data, change source licences or clear PBDB empirical holds.
The [mirror terms and boundaries](paleodata-README.md) travel with the files.

Implementation: [paleodata_backup.py](../tools/paleodata_backup.py), Python
standard library plus system SSH, SCP and rsync. Tests:
[test_paleodata_backup.py](../tools/test_paleodata_backup.py).

## Location and retention

Source remains `deep:/data/paleodata`. Run the script there; transfer
travels from `deep` over public SSH to `nectar` (`131.217.178.240`),
with no large payload on the laptop. The `nectar` SSH alias selects this route;
`deep` and WSL are off Tailscale. Source-side state and temporary online
database copies go under
`/data/codex/scratch/eprp-paleodata-backup/`. VM storage is:

```text
/data/codex/artifacts/eprp-paleodata-backup/
  paleodata_backup.py
  latest -> snapshots/<UTC-generation>/paleodata
  snapshots/<UTC-generation>/
    paleodata/                 readable research replica, read-only
    manifest.json             SHA256, sizes, source modes, SQLite capture times
    source-before.json        path and filesystem-signature inventory
    source-after.json         inventory after transfer
    verification.json         full destination hash and SQLite check receipt
    restore-test.json         fresh sample recovery receipt
  snapshots/<UTC-generation>.partial/   unpromoted failed/incomplete attempt
  restore-tests/<UTC-generation>/       independent fresh sample restore
```

Each generation contains independent regular files: no hardlinks to earlier
generations and no writable working view sharing their inodes. Successful
snapshots have all write bits removed, including directory write bits;
`latest` points to their read-only payload. These are ordinary filesystem
permissions, not administrative tamper protection or WORM storage. Write
analysis outputs in their owning projects. A full restore to a new target
reinstates original source modes, so mutable library databases are writable
and originally read-only source files remain read-only.

Nothing is pruned automatically, and source or backup files are never deleted
by this tool. New runs create new generations. A failed run leaves its staging
for diagnosis and does not replace `latest`; rerun to create a fresh generation.
Review capacity and failed staging deliberately before subsequent backups.
No periodic job has been installed.

Live preflight on 28 October found 75,878,303,013 source bytes and
450,824,081,408 bytes free on the VM's separate `/dev/vdb` `/data` filesystem.
These are a dated capacity observation, not a reservation. Every run requires
free space for twice its payload plus 20 GiB before transfer, allowing a full
fresh restore as well as its new generation. A source change or another
workload can alter the available capacity; the script checks each run and
refuses the root filesystem. Retained generations eventually fill a finite
volume; expansion or any retention pruning is a separate deliberate action.

## Capture and integrity semantics

[Detail withheld pending disclosure to the data custodian.]

Ordinary files, including every immutable `raw/` file and any raw SQLite
file, are copied byte-for-byte. The script hashes each source file, checks
its filesystem signature after hashing, transfers an explicit path list and
compares a fresh source inventory after transfer. A changed ordinary file,
new or removed path, changed mode, unreadable subtree or checksum mismatch
prevents publication. Three rsync attempts can resume a transport failure
within a run; a final source-drift failure requires a new run. Empty
directories and file names containing spaces are preserved.

The two mutable library databases, `library/search.sqlite` and
`library/tdm/search-tdm.sqlite`, are captured with SQLite's online backup API.
Each has its own start/end UTC times and an `integrity_check`; WAL, SHM and
journal sidecars for those two paths are omitted. Only these generated
SQLite copies are made standalone with DELETE journal mode. Source databases
are opened read-only. Immutable raw database bytes are never re-encoded.
Other files must remain stable while these captures and the transfer proceed.

This establishes individually consistent library databases and a stable
ordinary-file capture. It does not establish one atomic transaction across
the whole tree or between the databases and their text/PDF side files. For
application-level consistency during a library re-index or bulk update,
coordinate a quiet interval with its owner before running. The script does
not stop another owner's processes or declare mutable library content frozen.

Before promotion, every destination payload file must match its captured
source SHA256 and byte size, with exact file/directory inventories. This
checks transfer and recovery integrity; it does not verify the source against
provider manifests or establish scientific validity. Provider-manifest
verification remains the mirror's separate `data_mirror.py verify` operation.

Every successful run also copies a deterministic sample to a new independent
restore directory: up to 20 ordinary files, 20 provider manifests, the root
README, and every captured live library database. It rechecks all copied
hashes and runs SQLite `integrity_check` plus a readable-schema query. This
is a sample restore, not a full restore or a complete application test.
`restore --sample` repeats it in a new target; omitting `--sample` restores
and checks every payload file and empty directory. Existing targets are
refused to prevent overwrite.

## Run and recover

First coordinate with active source writers; in particular the initial run
must wait for the 28 October Fossilworks export to finish. Check the owning
project's current correspondence and machine readiness before use. Deploy
the reviewed script to the source host, then run it there:

```bash
ssh deep 'mkdir -p /data/codex/scratch/eprp-paleodata-backup'
scp resources/tools/paleodata_backup.py deep:/data/codex/scratch/eprp-paleodata-backup/
ssh deep 'python3 /data/codex/scratch/eprp-paleodata-backup/paleodata_backup.py snapshot'
```

For a long transfer run that last command in an owned `tmux` session or with
an explicitly retained log on deep so a laptop disconnect does not
end the job. The script prints inventory, transfer and completion receipts.
Only a completed result with a non-`.partial` generation and matching
verification and restore receipts supports a completed-backup claim.

On the VM, select an actual generation from `snapshots/` and verify it:

```bash
python3 /data/codex/artifacts/eprp-paleodata-backup/paleodata_backup.py verify /data/codex/artifacts/eprp-paleodata-backup/snapshots/<UTC-generation>
```

Restore to a new directory on a data volume with enough free space:

```bash
python3 /data/codex/artifacts/eprp-paleodata-backup/paleodata_backup.py restore /data/codex/artifacts/eprp-paleodata-backup/snapshots/<UTC-generation> /data/codex/scratch/paleodata-restored-<UTC-generation>
```

For recovery to another host, copy the selected generation and its manifest
together, verify it there, then restore to a new directory. Do not overwrite
the primary mirror during a drill. The VM data volume is separate from its
root-disk image: an instance snapshot alone does not back it up. This copy
provides separation from deep storage, not separation from Barry's
administrative credentials or a complete disaster-recovery service.

## Verification record

On 28 October, seven bounded regression tests passed: online SQLite capture
with a committed WAL transaction, raw SQLite byte preservation, empty-directory
recovery, full restore, original writable/read-only modes, retained independent
inodes, read-only generations, corruption/missing/extra-file refusal, source
drift, protected paths/symlinks, traversal I/O failure, and overwrite/path
traversal refusal. A synthetic cross-host smoke transferred four files
(16,436 bytes) from deep-server to a separate VM smoke root, verified every
SHA256, and restored all four independently with a passing SQLite integrity
and schema check. The production mirror transfer is a separate gated action;
no production-backup completion is claimed by these tests.

### First production backup: completed 28 October 2026

The first production generation completed with exit status 0 before the final
state check at **13:19 AEDT on 28 October 2026**. Fossilworks' owner confirmed
all writes finished before launch. The deployed script from commit `995e1a2`
matched SHA256
`17aa126bc3945ac7a36bca83e163edbb24ebe094467e00745fa11815cbe37037`
on the controlling checkout, deep-server and Nectar.

- Completed VM generation:
  `/data/codex/artifacts/eprp-paleodata-backup/snapshots/20261028T015047.271965Z`.
  Its `paleodata/` contains **51,456 files, 2,138 directories and
  75,910,524,400 payload bytes**. All file sizes and SHA256 hashes match the
  captured source manifest. Fossilworks contributes 513 files and 32,221,387
  bytes. This verifies copying against the captured source, not provider
  manifests or scientific validity.
- `verification.json` and `restore-test.json` in that generation are the
  detailed receipts. The two online library database copies passed
  `integrity_check` and a schema query: 7 tables in `library/search.sqlite`,
  6 in `library/tdm/search-tdm.sqlite`. Their separate capture intervals were
  01:57:57.826–01:58:07.826 UTC and 01:58:07.826–01:58:08.572 UTC.
- Fresh sample recovery at
  `/data/codex/artifacts/eprp-paleodata-backup/restore-tests/20261028T015047.271965Z`
  checked **42 files and 505,275,835 bytes**, including both library databases.
  Every copied hash matched and both SQLite checks passed. This was a sample
  restore; a full production restore has not been run.
- A separate final metadata check confirmed identical before/after ordinary
  source signatures, directory paths, live database paths and source modes;
  every retained file and directory has no write bits; every regular file has
  link count 1; all 42 restored files have independent inodes and their
  original modes. `latest` resolves to this completed `paleodata/`, and the
  corresponding `.partial` path is absent. The backup root is private mode
  700. Final available VM data-volume capacity was 374,249,578,496 bytes.
- Deep-server's persistent run was `tmux` session
  `eprp-backup-20261028T015047Z`. Its log and numeric exit receipt remain at
  `/data/codex/scratch/eprp-paleodata-backup/production-20261028T015047Z.log`
  and the same stem with `.exit`. Source-side manifests, inventories and
  `result.json` remain under
  `/data/codex/scratch/eprp-paleodata-backup/20261028T015047.271965Z/`.

The production run reported no source drift or transfer failure. No source,
previous generation or other data was deleted. No periodic schedule was added.
